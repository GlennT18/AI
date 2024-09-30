from collections.abc import Mapping, Sequence
from numbers import Number
from types import MappingProxyType

from city_map import UNIT_DELTA, CityMap, Geolocation, make_tag
from map_utils import find_route_from, get_route_cost
from search import SearchAlgorithm, SearchProblem, UniformCostSearch


def make_grid_label(x: int, y: int) -> str:
    """Return a label for the specified coordinate in a grid map."""
    return f'{x},{y}'


def create_grid_map(
        width: int,
        height: int,
        tags: Mapping[tuple[int, int], Sequence[str]] = MappingProxyType({}),
) -> CityMap:
    """Create a simple map with a grid of `width` by `height` locations,
    optionally with a mapping of coordinates to tags they should bear."""

    city_map = CityMap()
    # Create a grid with distance ~1m between adjacent locations
    for x, lat in enumerate([x * UNIT_DELTA for x in range(width)]):
        for y, lon in enumerate([y * UNIT_DELTA for y in range(height)]):
            location_tags = ([make_tag("x", str(x)), make_tag("y", str(y))] +
                             tags.get((x, y), []))
            # We label each location as just the grid index (x, y)
            city_map.add_location(
                make_grid_label(x, y),
                Geolocation(lat, lon),
                tags=location_tags,
            )
            if x > 0:
                city_map.add_connection(
                    make_grid_label(x - 1, y), make_grid_label(x, y), 1)
            if y > 0:
                city_map.add_connection(
                    make_grid_label(x, y - 1), make_grid_label(x, y), 1)
    return city_map


def assert_route_is_valid(
        route: Sequence[str],
        city_map: CityMap,
        start_location: str,
        end_tag: str,
        waypoint_tags: Sequence[str] = tuple(),
):
    # The route's start location must be the start position
    assert route[0] == start_location, f"{route[0]=} != {start_location=}"
    # The route's end location must contain `end_tag`
    route_end_tags = city_map.tags[route[-1]]
    assert end_tag in route_end_tags, f"{end_tag=} not in {route_end_tags=}"
    # Adjacent locations in the route must be connected in `city_map`
    for i in range(1, len(route)):
        adjacent_locations = city_map.distances[route[i - 1]]
        assert route[i] in adjacent_locations, (
            f"{route[i]=} not in route[{i - 1}]'s "
            f"adjacent locations: {adjacent_locations}")
    # The route must cover every waypoint tag
    covered_tags = set()
    for location in route:
        location_tags = set(city_map.tags[location])
        covered_tags.update(location_tags)
    expected_tags = set(waypoint_tags)
    uncovered_tags = expected_tags.difference(covered_tags)
    assert len(uncovered_tags) == 0, \
        f"Uncovered waypoint_tags: {uncovered_tags}"


def assert_cost_equals(
        expected_cost: Number,
        problem: SearchProblem,
        start_location: str,
        end_tag: str,
        city_map: CityMap,
        waypoint_tags: Sequence[str] = tuple(),
        search: SearchAlgorithm = UniformCostSearch(),
):
    route = find_route_from(start_location, problem, search)
    assert_route_is_valid(
        route, city_map, start_location, end_tag, waypoint_tags)
    actual_cost = get_route_cost(route, city_map)
    assert expected_cost == actual_cost, f"{expected_cost=} != {actual_cost=}"
