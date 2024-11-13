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

def findSum(input, base, letterDict):
        baseCount = len(input)-1
        #iterate over every letter
        total = 0
        for letter in input:
            #multiple letter by base
            #TRUE
            #sum(T * base * base * base, R * base * base, U * base, E)
            value = letterDict[letter]
            multiplier = base**baseCount

            #print(value, multiplier)
            total += value * multiplier
            baseCount -= 1

        return total

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions. Pulled from CPSolver"""

    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count

class Solver:
    def __init__(self):
        # If you want to add any fields to this class, define them here
        pass

    def solve(self, puzzle: str) -> List[Dict[str, int]]:
        #create constraints
        model = cp_model.CpModel()
        base = 10

        #iterate over the input
        letterSet = set()
        symbolSet = ('+', '=')
        letterDict = {}
        sentance = ""
        for letter in puzzle:
            #if the letter is a symbol add it to the sentance but don't assign value
            if(letter in symbolSet):
                 sentance = sentance + letter

            #makes sure each letter is only counted 1 time
            if(letter not in letterSet and letter not in symbolSet):
                letterSet.add(letter)
                #map each letter to 1 or 0. 1 if it is leading, 0 if not
                if(sentance == ""):
                     letterDict[str(letter)] = 1
                elif(sentance[-1] == "=" or sentance[-1] == "+"):
                     letterDict[str(letter)] = 1
                else:
                     letterDict[str(letter)] = 0
                
                # letterDict[str(letter)] = counter
                # counter += 1
                sentance = sentance + letter

        #create constraints on the model for each letter and their precomputed value
        modelLetters = []
        for kp in letterDict:
            #model.new_int_var(first_variable, base - 1, letter)
            print("letter:",letterDict.get(kp), "base:", base - 1, "KeyPair:", kp)
            x = model.new_int_var(letterDict.get(kp), base - 1, kp)
            modelLetters.append(x)

        model.add_all_different(modelLetters)

        #once you have created a variable for each letter
        sentanceList = sentance.split("=")
        rhs = sentanceList[1]
        lhsList = sentanceList[0].split("+")

        #sum both sides of the equation
        rhsSum = findSum(rhs, base, letterDict) 
        
        lhsSum = 0
        for listy in lhsList:
             lhsSum += findSum(listy, base, letterDict)
        
        #print(lhsSum, rhsSum)
        #add to model(model.add(lhs == rhs))
        """
        I think this is the issue. Documentation has this:
        model.add(
            c * base + p + i * base + s + f * base * base + u * base + n
            == t * base * base * base + r * base * base + u * base + e
        )

        I am calculating the right hand side and left hand side to total values and adding them
        to the model like this:
        """
        model.add(lhsSum == rhsSum)

        #check doc to make the model find solutions in a dictionary
        #dict = model.solve()
        solver = cp_model.CpSolver()
        solution_printer = VarArraySolutionPrinter(modelLetters)

        solver.parameters.enumerate_all_solutions = True
        status = solver.solve(model, solution_printer)

        #return dictionary of solutions
        

    
