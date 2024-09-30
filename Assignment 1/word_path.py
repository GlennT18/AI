#!/usr/bin/env python3

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""
        Print a shortest sequence of words in DICTIONARY from START to TARGET.
        If no sequence is found, print the string \"No solution\".
        """,
    )
    parser.add_argument(
        'dict_file_path',
        metavar="DICTIONARY",
        help="The dictionary file",
    )
    parser.add_argument(
        'start_word',
        metavar="START",
        help="The start word",
    )
    parser.add_argument(
        'target_word',
        metavar="TARGET",
        help="The target word",
    )
    args = parser.parse_args()

    import submission
    words = submission.word_path(
        args.dict_file_path, args.start_word, args.target_word)
    if words:
        for word in words:
            print(word)
    else:
        print("No solution")


if __name__ == '__main__':
    main()
