from ortools.sat.python import cp_model
from typing import Dict, List

# Please do not rename this variable!
STEP2_RESPONSE = """
The second arguement in new_int_var(x, y, letter) represents the upper bound
the value tied to the letter can be. This model finds solutions that makes
the left side equal the right side, and no letters can have the same value
assigned to them. 

The values that are assigned to each letter are in a range of 1-9 or 0-9.
9 is our upper bound(second variable). 

So if our letter was C, the value assigned to that letter can be
C:1
C:2
C:3
C:4
C:5
C:6
C:7
C:8
C:9
"""

from ortools.sat.python import cp_model
from typing import Dict, List

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    #this is code pulled from CP-SAT solver. Justs handles printing
    def __init__(self, variables: List[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.solutions = []

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v.Name()}={self.Value(v)}", end=" ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count

def findSum(input_str: str, base: int, letter_vars: Dict[str, cp_model.IntVar]) -> cp_model.LinearExpr:
    #finds total for the word
    total = 0
    for i, letter in enumerate(input_str):
        multiplier = base ** (len(input_str) - i - 1)
        total += letter_vars[letter] * multiplier
    return total

class Solver:
    def solve(self, puzzle: str) -> List[Dict[str, int]]:
        model = cp_model.CpModel()
        base = 10

        # Extract unique letters
        letter_vars = {}
        leading_letters = set(word[0] for word in puzzle.replace('=', '+').split('+'))

        # Create `IntVar` for each letter and enforce constraints for leading letters
        for letter in set(c for c in puzzle if c.isalpha()):
            lower_bound = 1 if letter in leading_letters else 0
            letter_vars[letter] = model.NewIntVar(lower_bound, base - 1, letter)

        # Ensure all letters have unique values
        model.AddAllDifferent(letter_vars.values())

        # Parse puzzle into left-hand and right-hand expressions
        lhs_expr = sum(findSum(word, base, letter_vars) for word in puzzle.split('=')[0].split('+'))
        rhs_expr = findSum(puzzle.split('=')[1], base, letter_vars)

        # Add equation constraint
        model.Add(lhs_expr == rhs_expr)

        # Solve and print solutions
        solver = cp_model.CpSolver()
        solution_printer = VarArraySolutionPrinter(list(letter_vars.values()))
        solver.parameters.enumerate_all_solutions = True
        status = solver.Solve(model, solution_printer)

        #print(f"Status = {solver.StatusName(status)}")
        #print(f"Number of solutions found: {solution_printer.solution_count}")

        return(solution_printer.solutions)
