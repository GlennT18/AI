from logic import *

# Sentence: "If it is raining, then it is wet."
def rain_wet():
    # It is raining
    Rain = Atom('Rain')
    # It is wet
    Wet = Atom('Wet')

    return Implies(Rain, Wet)


# Sentence: "There is a light that shines."
def light_shines():
    # x is lit
    def Light(x): return Atom('Light', x)
    # x is shining
    def Shines(x): return Atom('Shines', x)

    return Exists('$x', And(Light('$x'), Shines('$x')))


# Defining Parent in terms of Child.
def parent_child():
    # x has a parent y
    def Parent(x, y): return Atom('Parent', x, y)
    # x has a child y
    def Child(x, y): return Atom('Child', x, y)

    return Forall('$x', Forall('$y', Equiv(Parent('$x', '$y'), Child('$y', '$x'))))
