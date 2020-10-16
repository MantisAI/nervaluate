#!/usr/bin/env python3
# coding: utf-8

import pytest

from nervaluate import Evaluator


def test_loaders_produce_the_same_results():
    true_list = [
        ["O", "O", "O", "O", "O", "O"],
        ["O", "O", "B-ORG", "I-ORG", "O", "O"],
        ["O", "O", "B-MISC", "I-MISC", "O", "O"],
    ]

    pred_list = [
        ["O", "O", "B-PER", "I-PER", "O", "O"],
        ["O", "O", "B-ORG", "I-ORG", "O", "O"],
        ["O", "O", "B-MISC", "I-MISC", "O", "O"],
    ]

    true_conll = (
        "word\tO\nword\tO\nword\tO\nword\tO\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-ORG\nword\tI-ORG\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-MISC\nword\tI-MISC\nword\tO\nword\tO\n"
    )

    pred_conll = (
        "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-ORG\nword\tI-ORG\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-MISC\nword\tI-MISC\nword\tO\nword\tO\n"
    )

    true_prod = [
        [],
        [{"label": "ORG", "start": 2, "end": 3}],
        [{"label": "MISC", "start": 2, "end": 3}],
    ]

    pred_prod = [
        [{"label": "PER", "start": 2, "end": 3}],
        [{"label": "ORG", "start": 2, "end": 3}],
        [{"label": "MISC", "start": 2, "end": 3}],
    ]

    evaluator_list = Evaluator(
        true_list, pred_list, tags=["PER", "ORG", "MISC"], loader="list"
    )

    evaluator_conll = Evaluator(
        true_conll, pred_conll, tags=["PER", "ORG", "MISC"], loader="conll"
    )

    evaluator_prod = Evaluator(true_prod, pred_prod, tags=["PER", "ORG", "MISC"])

    results_list, results_agg_list = evaluator_list.evaluate()
    results_prod, results_agg_prod = evaluator_prod.evaluate()
    results_conll, results_agg_conll = evaluator_conll.evaluate()

    assert evaluator_prod.pred == evaluator_list.pred == evaluator_conll.pred
    assert evaluator_prod.true == evaluator_list.true == evaluator_conll.true

