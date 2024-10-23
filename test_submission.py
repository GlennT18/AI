#!/usr/bin/env python3

import pytest
import sys

from submission import Solver


@pytest.mark.it("CP+IS+FUN=TRUE")
def test_google_example():
    solution = Solver().solve('CP+IS+FUN=TRUE')
    assert len(solution) == 72, "Incorrect total number of solutions"
    assert {'C': 2, 'P': 3, 'I': 7, 'S': 4, 'F': 9,
            'U': 6, 'N': 8, 'T': 1, 'R': 0, 'E': 5} in solution


@pytest.mark.it("TWO+TWO=FOUR")
def test_textbook_example():
    solution = Solver().solve('TWO+TWO=FOUR')
    assert len(solution) == 7, "Incorrect total number of solutions"
    assert {'T': 7, 'W': 3, 'O': 4, 'F': 1, 'U': 6, 'R': 8} in solution
    assert {'T': 7, 'W': 6, 'O': 5, 'F': 1, 'U': 3, 'R': 0} in solution
    assert {'T': 8, 'W': 3, 'O': 6, 'F': 1, 'U': 7, 'R': 2} in solution
    assert {'T': 8, 'W': 4, 'O': 6, 'F': 1, 'U': 9, 'R': 2} in solution
    assert {'T': 8, 'W': 6, 'O': 7, 'F': 1, 'U': 3, 'R': 4} in solution
    assert {'T': 9, 'W': 2, 'O': 8, 'F': 1, 'U': 5, 'R': 6} in solution
    assert {'T': 9, 'W': 3, 'O': 8, 'F': 1, 'U': 7, 'R': 6} in solution


@pytest.mark.it("CRASH+HACKER=REBOOT")
def test_unique_solution_2():
    solution = Solver().solve('CRASH+HACKER=REBOOT')
    assert solution == [{
        'C': 3, 'R': 6, 'A': 8, 'S': 4, 'H': 5,
        'K': 9, 'E': 2, 'B': 0, 'O': 7, 'T': 1,
    }]


@pytest.mark.it("SEVEN+SEVEN+SIX=TWENTY")
def test_unique_solution_3():
    solution = Solver().solve('SEVEN+SEVEN+SIX=TWENTY')
    assert solution == [{
        'S': 6, 'E': 8, 'V': 7, 'N': 2, 'I': 5,
        'X': 0, 'T': 1, 'W': 3, 'Y': 4,
    }]


@pytest.mark.it("HAWAII+IDAHO+IOWA+OHIO=STATES")
def test_unique_solution_4():
    solution = Solver().solve('HAWAII+IDAHO+IOWA+OHIO=STATES')
    assert solution == [{
        'H': 5, 'A': 1, 'W': 0, 'I': 9, 'D': 8,
        'O': 3, 'S': 6, 'T': 2, 'E': 4,
    }]


@pytest.mark.it(
    "ACCURACIES+ACCURACIES+ACCURACIES+ACCURACIES+ACCURACIES=MATHEMATICS")
def test_unique_solution_5():
    solution = Solver().solve(
        'ACCURACIES+ACCURACIES+ACCURACIES+ACCURACIES+ACCURACIES'
        '=MATHEMATICS')  # Don't worry, the string does not have a newline
    assert solution == [{
        'A': 2, 'C': 5, 'U': 3, 'R': 8, 'I': 4,
        'E': 9, 'S': 0, 'M': 1, 'T': 7, 'H': 6,
    }]


@pytest.mark.it("TWELVE+TWELVE+TWELVE+TWELVE+TWELVE+THIRTY=NINETY")
def test_unique_solution_6():
    solution = Solver().solve(
        'TWELVE+TWELVE+TWELVE+TWELVE+TWELVE+THIRTY=NINETY')
    assert solution == [{
        'T': 1, 'W': 3, 'E': 0, 'L': 7, 'V': 6,
        'H': 9, 'I': 4, 'R': 2, 'Y': 5, 'N': 8,
    }]


if __name__ == '__main__':
    sys.exit(pytest.main())
