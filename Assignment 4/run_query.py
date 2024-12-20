#!/usr/bin/env python3

from submission import question_1a
from logic import *


def main():
    kb = createResolutionKB()
    formulas, query = question_1a()
    for formula in formulas:
        showKBResponse(kb.tell(formula))
    showKBResponse(kb.ask(query))


if __name__ == '__main__':
    main()
