from collections import defaultdict
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt
from typing import Optional

# Constants

# Radius of earth in meters (about 3956 miles)
RADIUS_EARTH = 6371000
# The change in latitude/longitude (in degrees) that equates to distance of ~1m
UNIT_DELTA = 0.00001


################################################################################
# Map Abstraction Overview & Useful Data Structures
# - `Geolocation`: The atomic unit of our abstraction; each `Geolocation`
#   object is uniquely specified as a pair of coordinates denoting
#   latitude/longitude (in degrees).
#
# - `CityMap`: The core structure representing a map defining the following:
#   - `locations` [str -> Geolocation]: A dictionary mapping a unique label to
#     a specific geolocation.
#
#   - `tags` [str -> list[str]]: A dictionary mapping a location label (same
#     keys as above) to a list of meaningful "tags" (e.g. amenity=food or
#     landmark=Golisano_Hall).  These tags are parsed from OpenStreetMaps or
#     defined manually as _landmarks_ in `data/rit-landmarks.json`.
#
#   - `distances` [str -> [str -> float]]: A nested dictionary mapping pairs of
#     locations to distances (e.g. `distances[label1][label2] = 21.3`).


@dataclass(frozen=True)
class Geolocation:
    """A latitude/longitude of a physical location on Earth."""
    latitude: float
    longitude: float

    def __repr__(self):
        return f"{self.latitude},{self.longitude}"


class CityMap:
    """
    A city map consists of a set of *labeled* locations with associated tags,
    and connections between them.
    """
    def __init__(self) -> None:
        # Location label -> actual geolocation (latitude/longitude),
        # e.g. self.geolocations['1165959987'] = Geolocation(43.0840, -77.6797)
        self.geolocations: dict[str, Geolocation] = {}

        # Location label -> list of tags
        # e.g. self.tags['1165959987'] =
        # ['entrance=yes', 'landmark=Golisano_Hall', 'amenity=food', ...])
        self.tags: dict[str, list[str]] = defaultdict(list)

        # Location label -> every adjacent location label-> distance between
        # the two locations
        # e.g. self.distances['A']['B'] = 21.3
        #
        # For a pair of locations, connections in both directions exist
        # with the same distance. e.g. if self.distances['A']['B'] == 21.3,
        # then self.distances['B']['A'] exists and equals 21.3 as well.
        self.distances: dict[str, dict[str, float]] = defaultdict(dict)

    def add_location(
            self, label: str, location: Geolocation, tags: list[str]
    ) -> None:
        """Add a location (denoted by `label`) to map
        with the provided set of tags."""
        assert label not in self.geolocations, \
            f"Location {label} already processed!"
        self.geolocations[label] = location
        self.tags[label] = [make_tag("label", label)] + tags

    def add_connection(
            self, source: str, target: str, distance: Optional[float] = None
    ) -> None:
        """Add a connection between source <--> target to `self.distances`.
        The connection will be established in both directions."""
        if distance is None:
            distance = compute_distance(
                self.geolocations[source], self.geolocations[target]
            )
        self.distances[source][target] = distance
        self.distances[target][source] = distance


################################################################################
# Utility Functions


def make_tag(key: str, value: str) -> str:
    """Locations have string-valued tags,
    which are created from (key, value) pairs."""
    return f"{key}={value}"


def get_first_location_with_tag(tag: str, city_map: CityMap) -> Optional[str]:
    """Return the first location with the specified tag in `city_map`, or None
    if no such location could be found."""
    candidates = sorted([location for location, tags in city_map.tags.items()
                         if tag in tags])
    return candidates[0] if len(candidates) > 0 else None


def compute_distance(geo1: Geolocation, geo2: Geolocation) -> float:
    """
    Compute the straight-line distance in meters between two geolocations,
    specified as latitude/longitude. This function is analogous to
    finding the Euclidean distance between points on a plane; however,
    because the Earth is spherical, we are using the _Haversine formula_
    <https://en.wikipedia.org/wiki/Haversine_formula>
    to compute distance subject to the curved surface.

    Note: For small distances (e.g. RIT -> ROC airport),
    factoring in the curvature of the earth might be a bit overkill!

    However, you could think about using this function to generalize to larger
    maps spanning much greater distances (possibly for fun future projects)!
    """
    lon1, lat1 = radians(geo1.longitude), radians(geo1.latitude)
    lon2, lat2 = radians(geo2.longitude), radians(geo2.latitude)

    # Haversine formula
    delta_lon, delta_lat = lon2 - lon1, lat2 - lat1
    haversine = ((sin(delta_lat / 2) ** 2) +
                 (cos(lat1) * cos(lat2)) * (sin(delta_lon / 2) ** 2))

    # Return distance d (factor in radius of earth in meters)
    return 2 * RADIUS_EARTH * asin(sqrt(haversine))
