from city_map import CityMap, Geolocation, compute_distance, get_first_location_with_tag
from map_utils import create_map_with_landmarks
from search import Heuristic, SearchProblem, State, UniformCostSearch


# Please first read the code as well as docstrings in file `search.py`.
# In this assignment, you will write code that interfaces with the classes in
# `search.py` to solve the problems.
#
# A key part of this assignment is figuring out how to model states effectively.
# In `search.py`, we have defined a class `State` to help you think through
# this, with a field called `custom_data`.  As you implement the different types
# of search problems below, think about what `custom_data` you should store with
# each state to enable more efficient search!
#
# Please also read code as well as docstrings in file `city_map.py` -- you will
# also need to use its classes and functions.


################################################################################
# Part 1a: Modeling the shortest path problem


class ShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path
    from `start_location` to any location with the specified `end_tag`.
    """

    def __init__(
            self,
            start_location: str,
            end_tag: str,
            city_map: CityMap,
    ):
        self.start_location = start_location
        self.end_tag = end_tag
        self.city_map = city_map

    def start_state(self) -> State:
        #TODO:
        return State(self.start_location)
        

    def is_end(self, state: State) -> bool:
        #TODO:
        #if the tags of the starting location
        tags = self.city_map.tags[state.location]
        #self end tag is what we need to check
        if(self.end_tag in tags):
            return True
        

    def successors_and_costs(self, state: State) -> list[tuple[State, float]]:
        # Note we want to return a list of *2-tuples* of the form:
        #     (successor_state: State, cost: float)
        #TODO: Our solution has 7 lines of code, but don't worry if yours doesn't 
        successors = []
        for adj,cost in self.city_map.distances[state.location].items():
            successor_state = State(adj)
            successors.append((successor_state, cost))

        return successors  


################################################################################
# Part 1b: Plan a route through RIT


def get_rit_shortest_path_problem() -> tuple[ShortestPathProblem, str]:
    """
    Create your own search problem using the RIT map, specifying your own
    `start_location` and `end_tag`. If you prefer, you may use a different map
    and/or different landmarks.

    Run `python dump_map.py` to dump a file `readable-map.txt` with a list of
    locations and associated tags.  You might find it useful to search in
    `readable-map.txt` for the following tag keys (amongst others):
    - `landmark=`: Landmarks defined in `data/rit-landmarks.json`
    - `amenity=`: Various amenity types (e.g. "food", "loading_dock"),
      defined either by the map or in `data/rit-landmarks.json`
    """

    # If you would use a custom map and/or custom landmarks,
    # feel free to modify the two lines below:
    map_filename = 'data/rit-map.pbf'
    landmark_filename = 'data/rit-landmarks.json'

    city_map = create_map_with_landmarks(map_filename, landmark_filename)

    #TODO: Replace this line with your code
    # Our solution has 2 lines of code, but don't worry if yours doesn't
    start_location = get_first_location_with_tag('landmark=Golisano_Hall', city_map)
    end_tag = 'landmark=Global_Village_Plaza'

    plot_title = map_filename.split("/")[-1].split("_")[0]
    return ShortestPathProblem(start_location, end_tag, city_map), plot_title


################################################################################
# Part 2a: Modeling the waypoints shortest path problem


class WaypointsShortestPathProblem(SearchProblem):
    """
    Defines a search problem that corresponds to finding the shortest path from
    `start_location` to any location with the specified `end_tag` such that the
    path also traverses locations that cover the set of tags in `waypoint_tags`.

    Hint: Naively, your `custom_data` could be a list of all locations visited.
    However, that would be too large of a state space to search over! Think 
    carefully about what `custom_data` should be stored.
    """
    def __init__(
            self,
            start_location: str,
            waypoint_tags: list[str],
            end_tag: str,
            city_map: CityMap,
    ):
        self.start_location = start_location
        self.end_tag = end_tag
        self.city_map = city_map

        # We want waypoint_tags to be consistent/canonical (sorted)
        # and hashable (tuple)
        self.waypoint_tags = tuple(sorted(waypoint_tags))

    def start_state(self) -> State:
        #TODO: 3 lines
        return State(self.start_location, custom_data=frozenset())
        

    def is_end(self, state: State) -> bool:
        # TODO: 4 lines
        #if waypoint has been used
        #if self.end tag == current tags
        if state.custom_data is not None:
            visited_waypoints = state.custom_data
        else:
            visited_waypoints = frozenset()
        tags = self.city_map.tags[state.location]
        #self end tag is what we need to check
        return(
            frozenset(self.waypoint_tags) == visited_waypoints
            and self.end_tag in tags
        )



    def successors_and_costs(self, state: State) -> list[tuple[State, float]]:
        # TODO: Replace this line with your code
        # Our solution has 10 lines of code, but don't worry if yours doesn't
        #go to each waypoint tag listed before
        successors = []
        visited_waypoints = state.custom_data  # frozenset of visited waypoints

        for adj, cost in self.city_map.distances[state.location].items():
            # Update visited waypoints if this location is one of the waypoint tags
            new_visited_waypoints = set(visited_waypoints)
            tags = self.city_map.tags[adj]
            for tag in self.waypoint_tags:
                if tag in tags:
                    new_visited_waypoints.add(tag)

            # Create a new state with the updated frozenset of visited waypoints
            successor_state = State(adj, custom_data=frozenset(new_visited_waypoints))
            successors.append((successor_state, cost))

        return successors 


################################################################################
# Part 2b: Plan a route with unordered waypoints through RIT


def get_rit_waypoints_shortest_path_problem() \
        -> tuple[WaypointsShortestPathProblem, str]:
    """
    Create your own search problem using the map of Stanford, specifying your
    own `start_location`, `end_tag`, and `waypoint_tags`.

    Similar to part 1b, use `readable-map.txt` to identify potential locations
    and tags.
    """
    map_filename = 'data/rit-map.pbf'
    landmark_filename = 'data/rit-landmarks.json'

    city_map = create_map_with_landmarks(map_filename, landmark_filename)

    #TODO: Replace this line with your code
    start_location = get_first_location_with_tag('landmark=Golisano_Hall', city_map)
    waypoint_tags = ['landmark=Sustainability_Institute', 'landmark=Slaughter_Hall']
    end_tag = 'landmark=Global_Village_Plaza'

    plot_title = map_filename.split("/")[-1].split("_")[0]
    return WaypointsShortestPathProblem(
        start_location, waypoint_tags, end_tag, city_map), plot_title


################################################################################
# Part 3a: "Straight-line" heuristic for A*


class StraightLineHeuristic(Heuristic):
    """
    Estimate the cost between locations as the straight-line distance.
    Hint: you might consider using `compute_distance()` in `city_map.py`
    """
    def __init__(self, end_tag: str, city_map: CityMap):
        self.end_tag = end_tag
        self.city_map = city_map

        # Precompute
        #TODO: 5 lines
        start_lat = self.city_map.geolocations[self.end_tag].latitude
        start_lon = self.city_map.geolocations[self.end_tag].longitude

        #compute distance
        distance = compute_distance(start_lat, start_lon)
     

    def evaluate(self, state: State) -> float:
       # TODO: 6 lines
        start_lat = self.city_map.geolocations[self.end_tag].latitude
        start_long = self.city_map.geolocations[self.end_tag].latitude
        start = Geolocation(start_lat, start_long)

        end_lat = state.location[0]
        end_long = state.location[1]
        end = Geolocation(end_lat, end_long)

        return(compute_distance(start, end))

################################################################################
# Part 3b: "No waypoints" heuristic for A*


class NoWaypointsHeuristic(Heuristic):
    """
    Returns the minimum distance from `start_location` to any location with
    `end_tag`, ignoring all waypoints.
    """
    def __init__(self, end_tag: str, city_map: CityMap):
        """
        Precompute cost of shortest path from each location to a location with
        the desired `end_tag`.
        """
        # Define a reversed shortest path problem from a special END state
        # (which connects via 0 cost to all end locations) to `start_location`.
        class ReverseShortestPathProblem(SearchProblem):
            def start_state(self) -> State:
                """
                Return special "END" state
                """
                # TODO: 1 line
                return(self.is_end)


            def is_end(self, state: State) -> bool:
                """
                Return False for each state.
                Because there is *not* a valid end state (`is_end` always
                returns False),  UCS will exhaustively compute costs to *all*
                other states.
                """
                #TODO: 1 line
                return False

            def successors_and_costs(
                    self, state: State) -> list[tuple[State, float]]:
                # If current location is the special "END" state,
                # return all the locations with the desired end_tag and cost 0
                # (i.e we connect the special location "END" with cost 0 to
                # all locations with `end_tag`)
                # Else, return all the successors of current location and their
                # corresponding distances according to the `city_map`
                raise NotImplementedError  # TODO: Replace this line with your code
                # Our solution has 14 lines of code, but don't worry if yours doesn't

        # Call UCS.solve on our `ReverseShortestPathProblem` instance.  Because
        # there is *not* a valid end state (`is_end` always returns False),
        # will exhaustively compute costs to *all* other states.
        # TODO: 2 lines
        UniformCostSearch.solve(ReverseShortestPathProblem)


        # Now that we've exhaustively computed costs from any valid
        # "end" location (any location with `end_tag`), we can retrieve
        # `ucs.past_costs`; this stores the minimum cost path to each
        # state in our state space.
        #
        # Note that we are making a critical assumption here:
        # costs are symmetric!
        # TODO: 1 line
        costs = UniformCostSearch.past_costs
        

    def evaluate(self, state: State) -> float:
        self.evaluate(self, state)
