from logic import *

from typing import List, Tuple


############################################################
# Question 1: Propositional Logic

# Sentence: "If it is a weekend and it is not raining, then I will go out."
def question_1a() -> Formula:
    # Symbols to use:
    #
    # It is a weekend
    Weekend = Atom('Weekend')
    # It is raining
    Raining = Atom('Raining')
    # I will go out
    GoOut = Atom('GoOut')

    # Don't forget to return the constructed formula!
    # BEGIN_YOUR_CODE
    raise NotImplementedError  # TODO: Replace this line with your code
    # END_YOUR_CODE


# Sentence: "We shut down servers only if it is Sunday."
def question_1b() -> Formula:
    # Symbols to use:
    #
    # We shut down servers
    ShutDownServers = Atom('ShutDownServers')
    # It is Sunday
    Sunday = Atom('Sunday')

    # Don't forget to return the constructed formula!
    # BEGIN_YOUR_CODE
    raise NotImplementedError  # TODO: Replace this line with your code
    # END_YOUR_CODE


# Sentence: "A new ticket is opened if and only if a new issue has been
# discovered or a new feature has been proposed."
def question_1c() -> Formula:
    # Symbols to use:
    #
    # A new ticket is opened
    NewTicket = Atom('NewTicket')
    # A new issue has been discovered
    NewIssue = Atom('NewIssue')
    # A new feature has been proposed
    NewFeature = Atom('NewFeature')

    # Don't forget to return the constructed formula!
    # BEGIN_YOUR_CODE
    raise NotImplementedError  # TODO: Replace this line with your code
    # END_YOUR_CODE


############################################################
# Question 2: First-Order Logic

# Sentence: "Bob is either a programmer or a writer."
def question_2a() -> Formula:
    # Symbols to use:
    #
    # Bob
    bob = Constant('bob')
    # x is a programmer
    def Programmer(x): return Atom('Programmer', x)
    # x is a writer
    def Writer(x): return Atom('Writer', x)

    # Don't forget to return the constructed formula!
    # BEGIN_YOUR_CODE
    raise NotImplementedError  # TODO: Replace this line with your code
    # END_YOUR_CODE


# Sentence: "At least one student knows logic."
def question_2b() -> Formula:
    # Symbols to use:
    #
    # x is a student
    def Student(x): return Atom('Student', x)
    # x knows logic
    def KnowsLogic(x): return Atom('KnowsLogic', x)

    # Don't forget to return the constructed formula!
    # BEGIN_YOUR_CODE
    raise NotImplementedError  # TODO: Replace this line with your code
    # END_YOUR_CODE


# Sentence: "Every vehicle is owned by a person."
def question_2c() -> Formula:
    # Symbols to use:
    #
    # x is a vehicle
    def Vehicle(x): return Atom('Vehicle', x)
    # x is a person
    def Person(x): return Atom('Person', x)
    # x owns y
    def Owns(x, y): return Atom('Owns', x, y)

    # Don't forget to return the constructed formula!
    # BEGIN_YOUR_CODE
    raise NotImplementedError  # TODO: Replace this line with your code
    # END_YOUR_CODE


############################################################
# Question 3: Friendships and Criticisms

# Domain of discourse: All people in RIT GCCIS
# Facts:
# 0. Matt is the dean.
# 1. John is not the dean.
# 2. John criticized Matt.
# 3. If a person is a dean, then everyone either befriends that person or
#    doesn't know that person.
# 4. Nobody criticizes someone whom they befriend.
# Query: Does John know Matt?
#
# This function returns a list of 5 formulas corresponding to each of the
# above facts, along with a formula for the query.
def question_3a() -> Tuple[List[Formula], Formula]:
    def Dean(x): return Atom('Dean', x)
    def Befriends(x, y): return Atom('Befriends', x, y)
    def Knows(x, y): return Atom('Knows', x, y)
    def Criticizes(x, y): return Atom('Criticizes', x, y)
    matt = Constant('matt')
    john = Constant('john')

    formulas = []
    # We provide the formula for fact 0 here:
    formulas.append(Dean(matt))
    # BEGIN_YOUR_CODE
    raise NotImplementedError  # TODO: Replace this line with your code
    # END_YOUR_CODE

    query = Knows(john, matt)
    return formulas, query
