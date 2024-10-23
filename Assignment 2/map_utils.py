from collections import defaultdict
from collections.abc import MutableMapping, MutableSet, Sequence
import json
import osmium
from osmium import osm
import plotly.express as px
import plotly.graph_objects as go

from city_map import CityMap, Geolocation, compute_distance, make_tag
from search import SearchAlgorithm, SearchProblem


def read_map(pbf_filename: str) -> CityMap:
    """Create a CityMap given a path to an OSM `.pbf` file."""

    # Note: `osmium` defines a nice class called `SimpleHandler`
    # to facilitate reading `.pbf` files.
    # You can read more about this class/functionality at
    # <https://docs.osmcode.org/pyosmium/latest/intro.html>.
    class MapCreationHandler(osmium.SimpleHandler):
        def __init__(self) -> None:
            super().__init__()
            self.nodes: MutableMapping[str, Geolocation] = {}
            self.tags: MutableMapping[str, list[str]] = defaultdict(list)
            self.edges: MutableSet[tuple[str, str]] = set()

        def node(self, n: osm.Node) -> None:
            """An `osm.Node` has the actual tag attributes for a given node."""
            self.tags[str(n.id)] = [make_tag(tag.k, tag.v) for tag in n.tags]

        def way(self, w: osm.Way) -> None:
            """An `osm.Way` contains an ordered list of connected nodes."""

            # We only include "ways" that are accessible on foot
            #   =>> Reference: https://github.com/Tristramg/osm4routing2
            #                  See -> `src/osm4routing/categorize.rs#L96`
            path_type = w.tags.get("highway", None)
            if path_type is None or path_type in {
                "motorway",
                "motorway_link",
                "trunk",
                "trunk_link",
            }:
                return
            elif (
                    w.tags.get("pedestrian", "n/a") == "no"
                    or w.tags.get("foot", "n/a") == "no"
            ):
                return

            # Otherwise, iterate through all nodes along the "way"...
            way_nodes = w.nodes
            for source_index in range(len(way_nodes) - 1):
                s, t = way_nodes[source_index], way_nodes[source_index + 1]
                s_label, t_label = str(s.ref), str(t.ref)
                s_loc = Geolocation(s.location.lat, s.location.lon)
                t_loc = Geolocation(t.location.lat, t.location.lon)

                # Assert that the locations aren't the same!
                assert s_loc != t_loc, "Source and Target are the same location"

                # Add to trackers...
                self.nodes[s_label], self.nodes[t_label] = s_loc, t_loc
                self.edges.add((s_label, t_label))

    # Build nodes & edges via MapCreationHandler
    #   > Pass `location=True` to enforce embedded lat/lon geometries!
    map_creator = MapCreationHandler()
    map_creator.apply_file(pbf_filename, locations=True)

    # Build CityMap by iterating through the parsed nodes and connections
    city_map = CityMap()
    for node_label in map_creator.nodes:
        city_map.add_location(node_label,
                              map_creator.nodes[node_label],
                              map_creator.tags[node_label])

    # When adding connections, don't pass distance flag (automatically compute!)
    for src, tgt in map_creator.edges:
        city_map.add_connection(src, tgt)

    return city_map


def add_landmarks_to_city_map(
        city_map: CityMap,
        landmark_filename: str,
        tolerance_meters: float = 250.0
) -> None:
    """
    Add landmarks from the given file to `city_map`.  Each landmark
    in the file will be associated with a `Geolocation`.

    Landmarks are defined in the landmark file using latitude and longitude,
    which may not *exactly* line up with the existing locations in the CityMap,
    so instead we map a given landmark onto the closest existing location
    (subject to a max tolerance).
    """
    with open(landmark_filename) as f:
        landmarks = json.load(f)

    # Iterate through landmarks and map onto the closest location in the map
    for item in landmarks:
        lat_str, lon_str = item["geo"].split(",")
        geo = Geolocation(float(lat_str), float(lon_str))

        # Find the closest location by searching over all locations in the map
        best_distance, best_label = min(
            (compute_distance(geo, existingGeo), existingLabel)
            for existingLabel, existingGeo in city_map.geolocations.items()
        )

        if best_distance < tolerance_meters:
            for key in ["landmark", "amenity"]:
                if key in item:
                    city_map.tags[best_label].append(make_tag(key, item[key]))


def create_map_with_landmarks(
        pbf_filename: str, landmark_filename: str) -> CityMap:
    city_map = read_map(pbf_filename)
    add_landmarks_to_city_map(city_map, landmark_filename)
    return city_map


def find_route_from(
        start_location: str,
        problem: SearchProblem,
        search: SearchAlgorithm,
) -> Sequence[str]:
    """Find the route originating from `start_location` for the given `problem`
    using the specified search algorithm."""
    search.solve(problem)
    return [start_location] + search.actions


def get_route_cost(route: Sequence[str], city_map: CityMap) -> float:
    """Return the specified route's total cost."""
    cost = 0.0
    for i in range(1, len(route)):
        cost += city_map.distances[route[i - 1]][route[i]]
    return cost


def plot_map(
        city_map: CityMap,
        route: Sequence[str],
        waypoint_tags: Sequence[str],
        title: str,
) -> None:
    """
    Plot the full map, highlighting the provided route.

    :param city_map: CityMap to plot
    :param route: List of location labels of the route
    :param waypoint_tags: List of tags that we care about hitting along the way
    :param title: Display title for map visualization
    """
    lat, lon = [], []

    # Convert `city_map.distances` to a list of (source, target) tuples...
    connections = [
        (source, target)
        for source in city_map.distances
        for target in city_map.distances[source]
    ]
    for source, target in connections:
        lat.append(city_map.geolocations[source].latitude)
        lat.append(city_map.geolocations[target].latitude)
        lat.append(None)
        lon.append(city_map.geolocations[source].longitude)
        lon.append(city_map.geolocations[target].longitude)
        lon.append(None)

    # Plot all states & connections
    fig = px.line_geo(lat=lat, lon=lon)

    # Plot path (represented by connections in `path`)
    solution_lat, solution_lon = [], []
    if len(route) > 0:
        # Get and convert `path` to (source, target) tuples
        # to append to lat, lon lists
        connections = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
        for connection in connections:
            source, target = connection
            solution_lat.append(city_map.geolocations[source].latitude)
            solution_lat.append(city_map.geolocations[target].latitude)
            solution_lat.append(None)
            solution_lon.append(city_map.geolocations[source].longitude)
            solution_lon.append(city_map.geolocations[target].longitude)
            solution_lon.append(None)

        # Visualize path by adding a trace
        fig.add_trace(
            go.Scattergeo(
                lat=solution_lat,
                lon=solution_lon,
                mode="lines",
                line=dict(width=5, color="blue"),
                name="solution",
            )
        )

        # Plot the points
        for i, location in enumerate(route):
            tags = set(city_map.tags[location]).intersection(set(waypoint_tags))
            if i == 0 or i == len(route) - 1 or len(tags) > 0:
                for tag in city_map.tags[location]:
                    if tag.startswith("landmark="):
                        tags.add(tag)
            if len(tags) == 0:
                continue

            # Add descriptions as annotations for each point
            description = " ".join(sorted(tags))

            # Color the start node green, the end node red, intermediate gray
            if i == 0:
                color = "red"
            elif i == len(route) - 1:
                color = "green"
            else:
                color = "gray"

            waypoint_lat = [city_map.geolocations[location].latitude]
            waypoint_lon = [city_map.geolocations[location].longitude]

            fig.add_trace(
                go.Scattergeo(
                    lat=waypoint_lat,
                    lon=waypoint_lon,
                    mode="markers",
                    marker=dict(size=20, color=color),
                    name=description,
                )
            )

    # Plot city_map locations with special tags (e.g. amenities, landmarks)
    for location_id, latLon in city_map.geolocations.items():
        tags = city_map.tags[location_id]
        amenity_tags = filter(lambda t: t.startswith('amenity='), tags)
        landmark_tags = filter(lambda t: t.startswith('landmark='), tags)
        # Plot amenities below landmarks to show the landmark's name
        # when the user hovers over a landmark that has amenity
        for tag in amenity_tags:
            fig.add_trace(
                go.Scattergeo(
                    locationmode="USA-states",
                    lon=[latLon.longitude],
                    lat=[latLon.latitude],
                    text=tag.split("amenity=")[1],
                    name=tag.split("amenity=")[1],
                    marker=dict(size=10, color="blue", line_width=3),
                )
            )
        for tag in landmark_tags:
            fig.add_trace(
                go.Scattergeo(
                    locationmode="USA-states",
                    lon=[latLon.longitude],
                    lat=[latLon.latitude],
                    text=tag.split("landmark=")[1],
                    name=tag.split("landmark=")[1],
                    marker=dict(size=10, color="purple", line_width=3),
                )
            )

    # Final scaling, centering, and figure title
    if len(solution_lat) > 0:
        mid_index = len(solution_lat) // 2
        mid_lat = solution_lat[mid_index]
        mid_lon = solution_lon[mid_index]
    else:
        mid_index = len(lat) // 2
        mid_lat = lat[mid_index]
        mid_lon = lon[mid_index]
    fig.update_layout(title=title, title_x=0.5)
    fig.update_layout(
        geo=dict(
            projection_scale=20000,
            center=dict(lat=mid_lat, lon=mid_lon),
        ),
    )
    fig.show()
