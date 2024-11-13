#!/usr/bin/env python3
# python -m pytest test_submission.py    
from submission import *
from logic import *

import gzip
import os
import pickle
import sys

import pytest


def test_1a():
    _test_translation_question('q1a', question_1a())


def test_1b():
    _test_translation_question('q1b', question_1b())


def test_1c():
    _test_translation_question('q1c', question_1c())


def test_2a():
    _test_translation_question('q2a', question_2a())


def test_2b():
    _test_translation_question('q2b', question_2b())


def test_2c():
    _test_translation_question(
        'q2c', And(AntiReflexive('Owns'), question_2c()))


def test_3a_fact_0():
    _test_3a_fact(0)


def test_3a_fact_1():
    _test_3a_fact(1)


def test_3a_fact_2():
    _test_3a_fact(2)


def test_3a_fact_3():
    _test_3a_fact(3)


def test_3a_fact_4():
    _test_3a_fact(4)


def test_3a_all_facts():
    objects, target_models = load_model('q3a-all')
    formulas, _ = question_3a()
    check_models(objects, target_models, AndList(formulas))


def _test_translation_question(question: str, formula):
    objects, target_models = load_model(question)
    check_models(objects, target_models, formula)


def _test_3a_fact(index: int):
    objects, target_models = load_model(f'q3a-{index}')
    formulas, _ = question_3a()
    check_models(objects, target_models, formulas[index])


def hashkey(model):
    return tuple(sorted(str(atom) for atom in model))


def load_model(model_name):
    filename = os.path.join('models', f'{model_name}.pklz')
    return pickle.load(gzip.open(filename, 'rb'))


def check_models(objects, target_models, formula: Formula):
    pred_models = performModelChecking(
        [formula],
        findAll=True,
        objects=objects,
    )
    target_model_set = set(hashkey(model) for model in target_models)
    pred_model_set = set(hashkey(model) for model in pred_models)
    assert pred_model_set == target_model_set, "Incorrect formula"


if __name__ == '__main__':
    sys.exit(pytest.main())
