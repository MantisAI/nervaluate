#!/usr/bin/env python3
# coding: utf-8

import pytest

from nervaluate import Evaluator


def test_evaluator_simple_case():

    true = "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\n\nword\tO\nword\tB-LOC\nword\tI-LOC\nword\tB-LOC\nword\tI-LOC\nword\tO\n"

    pred = "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\n\nword\tO\nword\tB-LOC\nword\tI-LOC\nword\tB-LOC\nword\tI-LOC\nword\tO\n"

    evaluator = Evaluator(true, pred, tags=["LOC", "PER"], loader="conll")

    results, results_agg = evaluator.evaluate()

    expected = {
        "strict": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        "ent_type": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        "partial": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        "exact": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_evaluator_conll_simple_case_filtered_tags():
    """
    Check that tags can be exluded by passing the tags argument

    """

    true = "word\tO\nword\tO\B-PER\nword\tI-PER\nword\tO\n\nword\tO\nword\tB-LOC\nword\tI-LOC\nword\tB-LOC\nword\tI-LOC\nword\tO\n"

    pred = "word\tO\nword\tO\B-PER\nword\tI-PER\nword\tO\n\nword\tO\nword\tB-LOC\nword\tI-LOC\nword\tB-LOC\nword\tI-LOC\nword\tO\n"

    evaluator = Evaluator(true, pred, tags=["PER", "LOC"], loader="conll")

    results, results_agg = evaluator.evaluate()

    expected = {
        "strict": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        "ent_type": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        "partial": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        "exact": {
            "correct": 3,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 3,
            "actual": 3,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_evaluator_conll_extra_classes():
    """
    Case when model predicts a class that is not in the gold (true) data
    """

    true = "word\tO\nword\tB-ORG\nword\tI-ORG\nword\tI-ORG\nword\tO\nword\tO"
    pred = "word\tO\nword\tB-FOO\nword\tI-FOO\nword\tI-FOO\nword\tO\nword\tO"

    evaluator = Evaluator(true, pred, tags=["ORG", "FOO"], loader="conll")

    results, results_agg = evaluator.evaluate()

    expected = {
        "strict": {
            "correct": 0,
            "incorrect": 1,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 0,
            "recall": 0.0,
            "f1": 0.0,
        },
        "ent_type": {
            "correct": 0,
            "incorrect": 1,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 0,
            "recall": 0.0,
            "f1": 0.0,
        },
        "partial": {
            "correct": 1,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        "exact": {
            "correct": 1,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_evaluator_conll_no_entities_in_prediction():
    """
    Case when model predicts a class that is not in the gold (true) data
    """

    true = "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\nword\tO"
    pred = "word\tO\nword\tO\nword\tO\nword\tO\nword\tO\nword\tO"

    evaluator = Evaluator(true, pred, tags=["PER"], loader="conll")

    results, results_agg = evaluator.evaluate()

    expected = {
        "strict": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "possible": 1,
            "actual": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0.0,
        },
        "ent_type": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "possible": 1,
            "actual": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0.0,
        },
        "partial": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "possible": 1,
            "actual": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0.0,
        },
        "exact": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "possible": 1,
            "actual": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0.0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_evaluator_compare_results_and_results_agg():
    """
    Check that the label level results match the total results.
    """

    true = "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\nword\tO"
    pred = "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\nword\tO"

    evaluator = Evaluator(true, pred, tags=["PER"], loader="conll")

    results, results_agg = evaluator.evaluate()

    expected = {
        "strict": {
            "correct": 1,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 1,
            "recall": 1,
            "f1": 1.0,
        },
        "ent_type": {
            "correct": 1,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 1,
            "recall": 1,
            "f1": 1.0,
        },
        "partial": {
            "correct": 1,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 1,
            "recall": 1,
            "f1": 1.0,
        },
        "exact": {
            "correct": 1,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 1,
            "actual": 1,
            "precision": 1,
            "recall": 1,
            "f1": 1.0,
        },
    }

    expected_agg = {
        "PER": {
            "strict": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "possible": 1,
                "actual": 1,
                "precision": 1,
                "recall": 1,
                "f1": 1.0,
            },
            "ent_type": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "possible": 1,
                "actual": 1,
                "precision": 1,
                "recall": 1,
                "f1": 1.0,
            },
            "partial": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "possible": 1,
                "actual": 1,
                "precision": 1,
                "recall": 1,
                "f1": 1.0,
            },
            "exact": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "possible": 1,
                "actual": 1,
                "precision": 1,
                "recall": 1,
                "f1": 1.0,
            },
        }
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]

    assert results["strict"] == expected_agg["PER"]["strict"]
    assert results["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results["partial"] == expected_agg["PER"]["partial"]
    assert results["exact"] == expected_agg["PER"]["exact"]


def test_evaluator_compare_results_and_results_agg_1():
    """
    Test case when model predicts a label not in the test data.
    """

    true = (
        "word\tO\nword\tO\nword\tO\nword\tO\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-ORG \nword\tI-ORG \nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-MISC\nword\tI-MISC\nword\tO\nword\tO\n\n"
    )

    pred = (
        "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-ORG \nword\tI-ORG \nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-MISC\nword\tI-MISC\nword\tO\nword\tO\n\n"
    )

    evaluator = Evaluator(true, pred, tags=["PER", "ORG", "MISC"], loader="conll")
    results, results_agg = evaluator.evaluate()

    expected = {
        "strict": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "possible": 2,
            "actual": 3,
            "precision": 0.6666666666666666,
            "recall": 1.0,
            "f1": 1.0,
        },
        "ent_type": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "possible": 2,
            "actual": 3,
            "precision": 0.6666666666666666,
            "recall": 1.0,
            "f1": 1.0,
        },
        "partial": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "possible": 2,
            "actual": 3,
            "precision": 0.6666666666666666,
            "recall": 1.0,
            "f1": 1.0,
        },
        "exact": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "possible": 2,
            "actual": 3,
            "precision": 0.6666666666666666,
            "recall": 1.0,
            "f1": 1.0,
        },
    }

    expected_agg = {
        "ORG": {
            "strict": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
            "ent_type": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
            "partial": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
            "exact": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
        },
        "MISC": {
            "strict": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
            "ent_type": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
            "partial": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
            "exact": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "possible": 1,
                "actual": 2,
                "precision": 0.5,
                "recall": 1,
                "f1": 1.0,
            },
        },
    }

    # print(results["strict"])
    # print(expected["strict"])

    # assert results_agg["ORG"]["strict"] == expected_agg["ORG"]["strict"]
    # assert results_agg["ORG"]["ent_type"] == expected_agg["ORG"]["ent_type"]
    # assert results_agg["ORG"]["partial"] == expected_agg["ORG"]["partial"]
    # assert results_agg["ORG"]["exact"] == expected_agg["ORG"]["exact"]

    # assert results_agg["MISC"]["strict"] == expected_agg["MISC"]["strict"]
    # assert results_agg["MISC"]["ent_type"] == expected_agg["MISC"]["ent_type"]
    # assert results_agg["MISC"]["partial"] == expected_agg["MISC"]["partial"]
    # assert results_agg["MISC"]["exact"] == expected_agg["MISC"]["exact"]

    # assert results['strict'] == expected['strict']
    # assert results['ent_type'] == expected['ent_type']
    # assert results['partial'] == expected['partial']
    # assert results['exact'] == expected['exact']


# @pytest.mark.xfail(strict=True)
# def test_evaluator_wrong_prediction_length():
#
#    true = [
#        ['O', 'B-ORG', 'I-ORG', 'O', 'O'],
#    ]
#
#    pred = [
#        ['O', 'B-MISC', 'I-MISC', 'O'],
#    ]
#
#    evaluator = Evaluator(true, pred, tags=['PER', 'MISC'], loader="list")
#
#    with pytest.raises(ValueError):
#        evaluator.evaluate()
#
# def test_evaluator_non_matching_corpus_length():
#
#    true = [
#        ['O', 'B-ORG', 'I-ORG', 'O', 'O'],
#        ['O', 'O', 'O', 'O']
#    ]
#
#    pred = [
#        ['O', 'B-MISC', 'I-MISC', 'O'],
#    ]
#
#    with pytest.raises(ValueError):
#        evaluator = Evaluator(true, pred, tags=['PER', 'MISC'], loader="list")
