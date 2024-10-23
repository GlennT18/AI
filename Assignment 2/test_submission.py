#!/usr/bin/env python3

import pytest
import sys

from city_map import make_tag
from search import AStarSearch
from submission import *
from test_utils import assert_cost_equals, create_grid_map, make_grid_label

rit_map = create_map_with_landmarks(
    'data/rit-map.pbf', 'data/rit-landmarks.json')


@pytest.mark.timeout(1)
class Test1a:
    @pytest.mark.it("Shortest path with 1 end location")
    def test_small_grid(self):
        city_map = create_grid_map(3, 5)
        start_location = make_grid_label(0, 0)
        end_tag = make_tag('label', make_grid_label(2, 2))
        problem = ShortestPathProblem(start_location, end_tag, city_map)
        assert_cost_equals(4, problem, start_location, end_tag, city_map)

    @pytest.mark.it("Shortest path with multiple end locations")
    def test_multiple_ends(self):
        city_map = create_grid_map(30, 30)
        start_location = make_grid_label(20, 10)
        end_tag = make_tag('x', str(5))
        problem = ShortestPathProblem(start_location, end_tag, city_map)
        assert_cost_equals(15, problem, start_location, end_tag, city_map)

    @pytest.mark.it("Shortest path with larger grid")
    def test_large_grid(self):
        city_map = create_grid_map(50, 50)
        start_location = make_grid_label(0, 0)
        end_tag = make_tag('label', make_grid_label(49, 49))
        problem = ShortestPathProblem(start_location, end_tag, city_map)
        assert_cost_equals(98, problem, start_location, end_tag, city_map)

    @pytest.mark.it("Golisano Hall -> Global Village Plaza")
    def test_rit_gccis2gv(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        end_tag = make_tag('landmark', 'Global_Village_Plaza')
        problem = ShortestPathProblem(start_location, end_tag, rit_map)
        assert_cost_equals(285.6319911643564,
                           problem, start_location, end_tag, rit_map)


@pytest.mark.timeout(3)
class Test2a:
    @pytest.mark.it("Shortest path with 1 waypoint")
    def test_small_grid(self):
        city_map = create_grid_map(3, 5)
        start_location = make_grid_label(0, 0)
        waypoint_tags = [make_tag('y', str(4))]
        end_tag = make_tag('label', make_grid_label(2, 2))
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, city_map)
        assert_cost_equals(
            8, problem, start_location, end_tag, city_map,
            waypoint_tags=waypoint_tags)

    @pytest.mark.it("Shortest path with 2 waypoints")
    def test_medium_grid(self):
        city_map = create_grid_map(30, 30)
        start_location = make_grid_label(20, 10)
        waypoint_tags = [make_tag('x', str(5)), make_tag('x', str(7))]
        end_tag = make_tag('label', make_grid_label(3, 3))
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, city_map)
        assert_cost_equals(
            24, problem, start_location, end_tag, city_map,
            waypoint_tags=waypoint_tags)

    @pytest.mark.it(
        "Shortest path with some locations covering multiple waypoints")
    def test_one_location_multi_waypoints(self):
        city_map = create_grid_map(2, 2, {
            (0, 1): ['food', 'fuel', 'books'],
            (1, 0): ['food'],
            (1, 1): ['fuel'],
        })
        start_location = make_grid_label(0, 0)
        waypoint_tags = ['food', 'fuel', 'books']
        end_tag = make_tag('label', make_grid_label(0, 1))
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, city_map)
        assert_cost_equals(
            1, problem, start_location, end_tag, city_map,
            waypoint_tags=waypoint_tags)

    @pytest.mark.it("Shortest path with start location covering some waypoints")
    def test_start_location_waypoints(self):
        city_map = create_grid_map(2, 2, {
            (0, 0): ['food'],
            (0, 1): ['fuel'],
            (1, 0): ['food'],
            (1, 1): ['food', 'fuel'],
        })
        start_location = make_grid_label(0, 0)
        waypoint_tags = ['food', 'fuel']
        end_tag = make_tag('label', make_grid_label(0, 1))
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, city_map)
        assert_cost_equals(
            1, problem, start_location, end_tag, city_map,
            waypoint_tags=waypoint_tags)

    @pytest.mark.it("Golisano Hall -> Crossroads -> Global Village Plaza")
    def test_rit_gccis2cr2gv(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        waypoint_tags = [make_tag('landmark', 'Crossroads')]
        end_tag = make_tag('landmark', 'Global_Village_Plaza')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        assert_cost_equals(320.23400770775726,
                           problem, start_location, end_tag, rit_map,
                           waypoint_tags=waypoint_tags)

    @pytest.mark.it("Golisano Hall -> any loading dock -> Global Village Plaza")
    def test_rit_gccis2dock2gv(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        waypoint_tags = [make_tag('amenity', 'loading_dock')]
        end_tag = make_tag('landmark', 'Global_Village_Plaza')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        assert_cost_equals(1076.424623626272,
                           problem, start_location, end_tag, rit_map,
                           waypoint_tags=waypoint_tags)

    @pytest.mark.it("RIT one-way multiple waypoints")
    def test_rit_multi_waypoints(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'NTID'), rit_map)
        waypoint_tags = [
            make_tag('landmark', 'Wallace_Library'),
            make_tag('landmark', 'SHED'),
            make_tag('landmark', 'Gordon_Field_House'),
        ]
        end_tag = make_tag('landmark', 'Golisano_Hall')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        assert_cost_equals(1775.3599351499195,
                           problem, start_location, end_tag, rit_map,
                           waypoint_tags=waypoint_tags)

    @pytest.mark.it("RIT loop")
    def test_rit_loop(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Wallace_Library'), rit_map)
        waypoint_tags = [
            make_tag('landmark', 'MAGIC_Spell_Studios'),
            make_tag('landmark', 'SHED'),
            make_tag('landmark', 'Eastman_Kodak_Quad'),
        ]
        end_tag = make_tag('landmark', 'Wallace_Library')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        assert_cost_equals(890.6035662549449,
                           problem, start_location, end_tag, rit_map,
                           waypoint_tags=waypoint_tags)


@pytest.mark.timeout(2)
class Test3a:
    @pytest.mark.timeout(1)
    @pytest.mark.it("Straight-line heuristic with small grid")
    def test_heuristic_small_grid(self):
        city_map = create_grid_map(3, 5)
        start_location = make_grid_label(0, 0)
        end_tag = make_tag('label', make_grid_label(2, 2))
        heuristic = StraightLineHeuristic(end_tag, city_map)
        expected = 3.145067466556296
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.timeout(1)
    @pytest.mark.it("Straight-line heuristic with larger grid")
    def test_heuristic_large_grid(self):
        city_map = create_grid_map(50, 50)
        start_location = make_grid_label(0, 0)
        end_tag = make_tag('label', make_grid_label(49, 49))
        heuristic = StraightLineHeuristic(end_tag, city_map)
        expected = 77.05415293016041
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.timeout(1)
    @pytest.mark.it("Straight-line heuristic Golisano Hall -> NTID")
    def test_heuristic_gccis2ntid(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        end_tag = make_tag('landmark', 'NTID')
        heuristic = StraightLineHeuristic(end_tag, rit_map)
        expected = 1005.7121625829818
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.it("A* straight-line heuristic "
                    "Golisano Hall -> Global Village Plaza")
    def test_a_star_gccis2gv(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        end_tag = make_tag('landmark', 'Global_Village_Plaza')
        problem = ShortestPathProblem(start_location, end_tag, rit_map)
        heuristic = StraightLineHeuristic(end_tag, rit_map)
        assert_cost_equals(285.6319911643564,
                           problem, start_location, end_tag, rit_map,
                           search=AStarSearch(heuristic))

    @pytest.mark.it("A* straight-line heuristic Golisano Hall -> NTID")
    def test_a_star_gccis2ntid(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        end_tag = make_tag('landmark', 'NTID')
        problem = ShortestPathProblem(start_location, end_tag, rit_map)
        heuristic = StraightLineHeuristic(end_tag, rit_map)
        assert_cost_equals(1257.1256810560835,
                           problem, start_location, end_tag, rit_map,
                           search=AStarSearch(heuristic))


@pytest.mark.timeout(2)
class Test3b:
    @pytest.mark.it("No-waypoint heuristic with small grid")
    def test_heuristic_small_grid(self):
        city_map = create_grid_map(3, 5)
        start_location = make_grid_label(0, 0)
        end_tag = make_tag('label', make_grid_label(2, 2))
        heuristic = NoWaypointsHeuristic(end_tag, city_map)
        expected = 4
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.it("No-waypoint heuristic with larger grid")
    def test_heuristic_large_grid(self):
        city_map = create_grid_map(50, 50)
        start_location = make_grid_label(0, 0)
        end_tag = make_tag('label', make_grid_label(49, 49))
        heuristic = NoWaypointsHeuristic(end_tag, city_map)
        expected = 98
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.it("No-waypoint heuristic "
                    "Golisano Hall -> Global Village Plaza")
    def test_heuristic_gccis2gv(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        end_tag = make_tag('landmark', 'Global_Village_Plaza')
        heuristic = NoWaypointsHeuristic(end_tag, rit_map)
        expected = 285.6319911643564
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.it("No-waypoint heuristic Golisano Hall -> any loading dock")
    def test_heuristic_gccis2dock(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        end_tag = make_tag('amenity', 'loading_dock')
        heuristic = NoWaypointsHeuristic(end_tag, rit_map)
        expected = 504.0608720975911
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.it("No-waypoint heuristic SHED -> any food")
    def test_heuristic_shed2food(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'SHED'), rit_map)
        end_tag = make_tag('amenity', 'food')
        heuristic = NoWaypointsHeuristic(end_tag, rit_map)
        expected = 162.57680055268384
        actual = heuristic.evaluate(State(start_location))
        assert expected == actual, f"{expected=} != {actual=}"

    @pytest.mark.it("A* no-waypoint heuristic "
                    "Golisano Hall -> Crossroads -> Global Village Plaza")
    def test_a_star_gccis2cr2gv(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Golisano_Hall'), rit_map)
        waypoint_tags = [make_tag('landmark', 'Crossroads')]
        end_tag = make_tag('landmark', 'Global_Village_Plaza')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        heuristic = NoWaypointsHeuristic(end_tag, rit_map)
        assert_cost_equals(320.23400770775726,
                           problem, start_location, end_tag, rit_map,
                           search=AStarSearch(heuristic))

    @pytest.mark.it("A* no-waypoint heuristic "
                    "SHED -> any food -> Eastman Kodak Quad")
    def test_a_star_shed2food2kodak(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'SHED'), rit_map)
        waypoint_tags = [make_tag('amenity', 'food')]
        end_tag = make_tag('landmark', 'Eastman_Kodak_Quad')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        heuristic = NoWaypointsHeuristic(end_tag, rit_map)
        assert_cost_equals(366.1366300656278,
                           problem, start_location, end_tag, rit_map,
                           search=AStarSearch(heuristic))

    @pytest.mark.it("A* no-waypoint heuristic RIT one-way multiple waypoints")
    def test_a_star_rit_multi_waypoints(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'NTID'), rit_map)
        waypoint_tags = [
            make_tag('landmark', 'Wallace_Library'),
            make_tag('landmark', 'SHED'),
            make_tag('landmark', 'Gordon_Field_House'),
        ]
        end_tag = make_tag('landmark', 'Golisano_Hall')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        heuristic = NoWaypointsHeuristic(end_tag, rit_map)
        assert_cost_equals(1775.3599351499195,
                           problem, start_location, end_tag, rit_map,
                           search=AStarSearch(heuristic))

    @pytest.mark.it("A* no-waypoint heuristic RIT loop")
    def test_a_star_rit_loop(self):
        start_location = get_first_location_with_tag(
            make_tag('landmark', 'Wallace_Library'), rit_map)
        waypoint_tags = [
            make_tag('landmark', 'MAGIC_Spell_Studios'),
            make_tag('landmark', 'SHED'),
            make_tag('landmark', 'Eastman_Kodak_Quad'),
        ]
        end_tag = make_tag('landmark', 'Wallace_Library')
        problem = WaypointsShortestPathProblem(
            start_location, waypoint_tags, end_tag, rit_map)
        heuristic = NoWaypointsHeuristic(end_tag, rit_map)
        assert_cost_equals(890.6035662549449,
                           problem, start_location, end_tag, rit_map,
                           search=AStarSearch(heuristic))


if __name__ == '__main__':
    sys.exit(pytest.main())
