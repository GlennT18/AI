from ortools.sat.python import cp_model
from typing import Dict, List

# Please do not rename this variable!
STEP2_RESPONSE = """
TODO: Set your answer to step 2's question to this variable's value

Multi-line string is supported, in case your response is long.
"""

def findSum(input, base, letterDict):
        baseCount = len(input)-1
        #iterate over every letter
        #print(letterDict)
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
        counter = 0
        letterDict = {}
        sentance = ""
        for letter in puzzle:
            #makes sure each letter is only counted 1 time
            if(letter not in letterSet and letter not in symbolSet):
                letterSet.add(letter)
                #map each letter to a number
                letterDict[str(letter)] = counter
                counter += 1
            sentance = sentance + letter

        #create constraints on the model for each letter and their precomputed value
        for kp in letterDict:
            #model.new_int_var(first_variable, base - 1, letter)
            model.new_int_var(letterDict.get(kp), base - 1, kp)

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
        model.add(lhsSum == rhsSum)

        #return dictionary of solutions

    
