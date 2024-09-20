from collections.abc import Hashable
from dataclasses import dataclass
import heapq
from typing import Optional

################################################################################
# Abstract Interfaces for State, Search Problems, and Search Algorithms


@dataclass(frozen=True, order=True)
class State:
    """
    A State consists of a string `location` and (possibly `None`) `custom_data`.
    Note that `custom_data` must be _hashable_
    <https://docs.python.org/3/glossary.html#term-hashable>
    because we implement our search algorithm using a dict and use instances of
    `State` class as keys for the values.

    Examples of hashable objects:
    - Any immutable primitives (such as str, int, float)
    - Immutable containers (such as tuples, frozensets)
    - Nested combinations of the above

    As you implement different types of search problems throughout the
    assignment, think of what data could be stored in `custom_data`
    to enable efficient search!

    Example usage:
        state = State(location="A", custom_data=("some_hashable_object", 123))
    """
    location: str
    custom_data: Optional[Hashable] = None


class SearchProblem:
    def start_state(self) -> State:
        """Return the start state."""
        raise NotImplementedError("Override me")

    def is_end(self, state: State) -> bool:
        """Return whether `state` is an end state or not."""
        raise NotImplementedError("Override me")

    def successors_and_costs(self, state: State) \
            -> list[tuple[State, float]]:
        """Return a list of `(successor_state: State, cost: float)` tuples
        corresponding to the various edges coming out of `state`."""
        raise NotImplementedError("Override me")


class SearchAlgorithm:
    def __init__(self):
        """
        A SearchAlgorithm is defined by the function
        `solve(problem: SearchProblem)`

        A call to `solve` sets the following instance variables:
        - self.actions: List of "actions" that takes one from the start state
          to a valid end state, or `None` if no such action sequence exists.
          - Note: For this assignment, an "action" is just the string
            "nextLocation" for a state, but in general, an action
            could be something like "up/down/left/right".

        - self.path_cost: Sum of the costs along the path,
          or `None` if no valid path.

        - self.num_states_explored: Number of States explored by the given
          search algorithm as it attempts to find a satisfying path.  You can
          use this to gauge the efficiency of search heuristics, for example.

        - self.past_costs: Dictionary mapping each string location visited
          by the SearchAlgorithm to the corresponding cost to get there
          from the starting location.
        """
        self.actions: list[str] = list()
        self.path_cost: float = 0.0
        self.num_states_explored: int = 0
        self.past_costs: dict[str, float] = dict()

    def solve(self, problem: SearchProblem) -> None:
        raise NotImplementedError("Override me")


class Heuristic:
    """
    A Heuristic object is defined by a single function `evaluate(state)` that
    returns an estimate of the cost of going from the specified `state` to an
    end state. Used by A* search.
    """
    def evaluate(self, state: State) -> float:
        raise NotImplementedError("Override me")


class ZeroHeuristic(Heuristic):
    """A heuristic function that always returns 0."""
    def evaluate(self, state: State) -> float:
        return 0.0


################################################################################
# A* Search and Uniform-Cost Search (Dijkstra's algorithm)


class AStarSearch(SearchAlgorithm):
    def __init__(self, heuristic: Heuristic, verbose: int = 0):
        super().__init__()
        self.heuristic = heuristic
        self.verbose = verbose

    def solve(self, problem: SearchProblem) -> None:
        """
        Run A* Search on the specified `problem` instance.

        Sets the following instance variables (see `SearchAlgorithm` docstring).
        - self.actions: list[str]
        - self.path_cost: float
        - self.num_states_explored: int
        - self.past_costs: dict[str, float]

        *Hint*: Some of these variables might be really helpful for part 3!
        """
        self.actions: list[str] = list()
        self.path_cost: float = 0.0
        self.num_states_explored: int = 0
        self.past_costs: dict[str, float] = dict()

        # Cache the heuristic function's return values
        h = dict()

        # Initialize data structures
        frontier = PriorityQueue()  # Explored states maintained by the frontier
        backpointers = dict()       # Map state -> previous state

        # Add the start state
        start_state = problem.start_state()
        h[start_state] = self.heuristic.evaluate(start_state)
        frontier.update(start_state, h[start_state])

        while True:
            # Remove the state with the lowest past cost (priority)
            state, f_state = frontier.remove_min()
            if state is None and f_state is None:
                if self.verbose >= 1:
                    print("Searched the entire search space!")
                return

            g_state = f_state - h[state]
            # Update tracking variables
            self.past_costs[state.location] = g_state
            self.num_states_explored += 1
            if self.verbose >= 2:
                print(f"Exploring {state} with past cost {g_state}")

            # Check if we've reached an end state; if so, extract solution
            if problem.is_end(state):
                self.actions = list()
                while state != start_state:
                    action, prev_state = backpointers[state]
                    self.actions.append(action)
                    state = prev_state
                self.actions.reverse()
                self.path_cost = g_state
                if self.verbose >= 1:
                    print(f"{self.num_states_explored = }")
                    print(f"{self.path_cost = }")
                    print(f"{self.actions = }")
                return

            # Expand from `state`, updating the frontier with each `new_state`
            for new_state, cost in problem.successors_and_costs(state):
                g_new_state = g_state + cost
                if new_state not in h:
                    h[new_state] = self.heuristic.evaluate(new_state)
                f_new_state = g_new_state + h[new_state]
                if self.verbose >= 3:
                    print(f"\t{state} => {new_state} "
                          f"(Priority: {f_new_state})")

                if frontier.update(new_state, f_new_state):
                    # We found better way to go to `new_state`
                    # -- update backpointer!
                    action = new_state.location
                    backpointers[new_state] = (action, state)


class UniformCostSearch(AStarSearch):
    def __init__(self, verbose: int = 0):
        super().__init__(heuristic=ZeroHeuristic(), verbose=verbose)


class PriorityQueue:
    """Data structure to support uniform cost search."""

    def __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    def update(self, state: State, new_priority: float) -> bool:
        """
        If `state` is not already in the heap, or `new_priority` is smaller
        than the existing priority, then insert `state` into the heap with
        priority `new_priority.

        Return whether the priority queue was updated.
        """
        old_priority = self.priorities.get(state)
        if old_priority is None or new_priority < old_priority:
            self.priorities[state] = new_priority
            heapq.heappush(self.heap, (new_priority, state))
            return True
        return False

    def remove_min(self):
        """Returns a (state with minimum priority, priority) tuple, or
        (None, None) if the priority queue is empty."""
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE:
                # Outdated priority, skip
                continue
            self.priorities[state] = self.DONE
            return state, priority

        # Nothing left...
        return None, None
