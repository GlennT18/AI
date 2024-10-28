#!/usr/bin/env python3

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""
        Solve a cryptarithmetic PUZZLE whose format is like CP+IS+FUN=TRUE.
        """,
    )
    parser.add_argument(
        'puzzle',
        metavar="PUZZLE",
        help="The cryptarithmetic puzzle",
    )
    args = parser.parse_args()

    from submission import Solver
    solutions = Solver().solve(args.puzzle)
    for solution in solutions:
        print(solution)


if __name__ == '__main__':
    main()