#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple

from naive_bayes import NaiveBayes


def check_data_dir(data_dir: str) -> None:
    dirs_to_check = [
        f'{data_dir}/training/ham',
        f'{data_dir}/training/spam',
        f'{data_dir}/test/ham',
        f'{data_dir}/test/spam',
    ]
    for path_str in dirs_to_check:
        path_obj = Path(path_str)
        if not path_obj.is_dir():
            raise NotADirectoryError(f"'{path_obj}' is not a valid directory")


def email_to_unique_words(file: os.PathLike) -> List[str]:
    words = set()
    with open(file) as f:
        first_line = True
        for line in f:
            if first_line:
                # Skip the 'Subject:' line
                first_line = False
            else:
                words.update(line.strip().split(' '))
    return list(words)


def train(model: NaiveBayes, data_dir: str) -> None:
    training_set_path = Path(f'{data_dir}/training')
    spams = list()
    hams = list()
    for label, emails in (('spam', spams), ('ham', hams)):
        for email in (training_set_path / label).iterdir():
            emails.append(email_to_unique_words(email))
    model.train(spams, hams)


def predict(model: NaiveBayes, data_dir: str) \
        -> Tuple[List[str], List[str], List[str], List[str]]:
    test_set_path = Path(f'{data_dir}/test')
    true_spam, false_spam, true_ham, false_ham = (list() for _ in range(4))
    for label in ('spam', 'ham'):
        if label == 'spam':
            correct = true_spam
            incorrect = false_spam
        else:
            correct = true_ham
            incorrect = false_ham
        expected = label == 'spam'
        for email in (test_set_path / label).iterdir():
            filename = email.name
            actual = model.predict_is_spam(email_to_unique_words(email))
            if expected == actual:
                correct.append(filename)
            else:
                incorrect.append(filename)
    return true_spam, false_spam, true_ham, false_ham


def main() -> None:
    parser = argparse.ArgumentParser(
        description="""
        Run naive Bayes spam classification on the specified dataset.
        """,
    )
    parser.add_argument(
        '-d', '--data-dir',
        metavar="DIR",
        default='./data/',
        help="use DIR as the dataset directory (default: %(default)s)",
    )
    args = parser.parse_args()
    data_dir = args.data_dir

    try:
        check_data_dir(data_dir)
    except NotADirectoryError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("Please make sure your dataset directory is valid.",
              file=sys.stderr)
        print(f"Try '{sys.argv[0]} --help' for more information.")
        sys.exit(1)

    model = NaiveBayes()
    print("Training...")
    train(model, data_dir)

    print("Running predictions...")
    true_spam, false_spam, true_ham, false_ham = predict(model, data_dir)
    num_correct = len(true_spam) + len(true_ham)
    num_total = num_correct + len(false_spam) + len(false_ham)
    print()
    print(f"Correctly-classified Spams: {len(true_spam)}")
    print(f"Correctly-classified Hams: {len(true_ham)}")
    print(f"Misclassified Spams: {len(false_spam)}")
    print(f"Misclassified Hams: {len(false_ham)}")
    print(f"Accuracy: {num_correct / num_total}")


if __name__ == '__main__':
    main()
