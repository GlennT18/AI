#!/usr/bin/env python3

import argparse
from search import UniformCostSearch


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot the map with locations and any route "
                    "in the web browser.",
    )
    parser.add_argument(
        'part',
        choices=['1b', '2b'],
        help="The assignment part for which the map is plotted",
    )
    args = parser.parse_args()

    # Do slow imports after argument parsing to speed up '--help',
    # invalid argument messages, etc.
    from map_utils import find_route_from, get_route_cost, plot_map
    from submission import (
        get_rit_shortest_path_problem,
        get_rit_waypoints_shortest_path_problem,
    )

    if args.part == '1b':
        problem, plot_title = get_rit_shortest_path_problem()
    elif args.part == '2b':
        problem, plot_title = get_rit_waypoints_shortest_path_problem()
    else:
        raise Exception(f"Unknown part: {args.part}")

    route = find_route_from(
        problem.start_location, problem, UniformCostSearch(verbose=0))
    waypoint_tags = list()
    if args.part == '2b':
        waypoint_tags = problem.waypoint_tags

    city_map = problem.city_map
    cost_meters = get_route_cost(route, city_map)
    cost_miles = cost_meters / 1609.344
    print(f"Route distance: {cost_miles:.2f} miles")
    plot_map(city_map, route, waypoint_tags, plot_title)


if __name__ == '__main__':
    main()
