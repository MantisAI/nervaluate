#!/usr/bin/env python3
# coding: utf-8

import pytest

from nervaluate import Evaluator


def test_evaluator_list_simple_case():

    true = [
        ['O', 'O', 'B-PER', 'I-PER', 'O'],
        ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O'],
    ]

    pred = [
        ['O', 'O', 'B-PER', 'I-PER', 'O'],
        ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O'],
    ]

    evaluator = Evaluator(true, pred, tags=['LOC', 'PER'], loader="list")

    results, results_agg = evaluator.evaluate()

    expected = {
        'strict': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        },
        'ent_type': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        },
        'partial': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        },
        'exact': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        }
    }
    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']

def test_evaluator_list_simple_case_filtered_tags():
    """
    Check that tags can be exluded by passing the tags argument

    """

    true = [
        ['O', 'O', 'B-PER', 'I-PER', 'O'],
        ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O'],
        ['O', 'B-MISC', 'I-MISC', 'O', 'O', 'O'],
    ]

    pred = [
        ['O', 'O', 'B-PER', 'I-PER', 'O'],
        ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O'],
        ['O', 'B-MISC', 'I-MISC', 'O', 'O', 'O'],
    ]

    evaluator = Evaluator(true, pred, tags=['PER', 'LOC'], loader="list")

    results, results_agg = evaluator.evaluate()

    expected = {
        'strict': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        },
        'ent_type': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        },
        'partial': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        },
        'exact': {
            'correct': 3,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 3,
            'actual': 3,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        }
    }

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']


def test_evaluator_list_extra_classes():
    """
    Case when model predicts a class that is not in the gold (true) data
    """

    true = [
        ['O', 'B-ORG', 'I-ORG', 'I-ORG', 'O', 'O'],
    ]

    pred = [
        ['O', 'B-FOO', 'I-FOO', 'I-FOO', 'O', 'O'],
    ]

    evaluator = Evaluator(true, pred, tags=['ORG', 'FOO'], loader="list")

    results, results_agg = evaluator.evaluate()

    expected = {
        'strict': {
            'correct': 0,
            'incorrect': 1,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 0,
            'recall': 0.0,
            'f1': 0
        },
        'ent_type': {
            'correct': 0,
            'incorrect': 1,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 0,
            'recall': 0.0,
            'f1': 0
        },
        'partial': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        },
        'exact': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0
        }
    }

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']

def test_evaluator_list_no_entities_in_prediction():
    """
    Case when model predicts a class that is not in the gold (true) data
    """

    true = [
        ['O', 'O', 'B-PER', 'I-PER', 'O', 'O'],
    ]

    pred = [
        ['O', 'O', 'O', 'O', 'O', 'O'],
    ]

    evaluator = Evaluator(true, pred, tags=['PER'], loader="list")

    results, results_agg = evaluator.evaluate()

    expected = {
        'strict': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'possible': 1,
            'actual': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        },
        'ent_type': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'possible': 1,
            'actual': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        },
        'partial': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'possible': 1,
            'actual': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        },
        'exact': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'possible': 1,
            'actual': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0
        }
    }

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']

def test_evaluator_list_compare_results_and_results_agg():
    """
    Check that the label level results match the total results.
    """

    true = [
        ['O', 'O', 'B-PER', 'I-PER', 'O', 'O'],
    ]

    pred = [
        ['O', 'O', 'B-PER', 'I-PER', 'O', 'O'],
    ]

    evaluator = Evaluator(true, pred, tags=['PER'], loader="list")

    results, results_agg = evaluator.evaluate()

    expected = {
        'strict': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        },
        'ent_type': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        },
        'partial': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        },
        'exact': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        }
    }

    expected_agg = {
        'PER': {
        'strict': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        },
        'ent_type': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        },
        'partial': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        },
        'exact': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1,
            'recall': 1,
            'f1': 1
        }
    }
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']

    assert results['strict'] == expected_agg['PER']['strict']
    assert results['ent_type'] == expected_agg['PER']['ent_type']
    assert results['partial'] == expected_agg['PER']['partial']
    assert results['exact'] == expected_agg['PER']['exact']

def test_evaluator_list_compare_results_and_results_agg_1():
    """
    Test case when model predicts a label not in the test data.
    """

    true = [
        ['O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'B-ORG', 'I-ORG', 'O', 'O'],
        ['O', 'O', 'B-MISC', 'I-MISC', 'O', 'O'],
    ]

    pred = [
        ['O', 'O', 'B-PER', 'I-PER', 'O', 'O'],
        ['O', 'O', 'B-ORG', 'I-ORG', 'O', 'O'],
        ['O', 'O', 'B-MISC', 'I-MISC', 'O', 'O'],
    ]

    evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'MISC'], loader="list")

    results, results_agg = evaluator.evaluate()

    expected = {
        'strict': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 2,
            'actual': 3,
            'precision': 0.6666666666666666,
            'recall': 1.0,
            'f1': 0.8
        },
        'ent_type': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 2,
            'actual': 3,
            'precision': 0.6666666666666666,
            'recall': 1.0,
            'f1': 0.8
        },
        'partial': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 2,
            'actual': 3,
            'precision': 0.6666666666666666,
            'recall': 1.0,
            'f1': 0.8
        },
        'exact': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 2,
            'actual': 3,
            'precision': 0.6666666666666666,
            'recall': 1.0,
            'f1': 0.8
        }
    }

    expected_agg = {
        'ORG': {
        'strict': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        },
        'ent_type': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        },
        'partial': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        },
        'exact': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        }
    },
        'MISC': {
        'strict': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        },
        'ent_type': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        },
        'partial': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        },
        'exact': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'possible': 1,
            'actual': 2,
            'precision': 0.5,
            'recall': 1,
            'f1': 0.6666666666666666
        }
    }
    }

    assert results_agg["ORG"]["strict"] == expected_agg["ORG"]["strict"]
    assert results_agg["ORG"]["ent_type"] == expected_agg["ORG"]["ent_type"]
    assert results_agg["ORG"]["partial"] == expected_agg["ORG"]["partial"]
    assert results_agg["ORG"]["exact"] == expected_agg["ORG"]["exact"]

    assert results_agg["MISC"]["strict"] == expected_agg["MISC"]["strict"]
    assert results_agg["MISC"]["ent_type"] == expected_agg["MISC"]["ent_type"]
    assert results_agg["MISC"]["partial"] == expected_agg["MISC"]["partial"]
    assert results_agg["MISC"]["exact"] == expected_agg["MISC"]["exact"]

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']

@pytest.mark.xfail(strict=True)
def test_evaluator_list_wrong_prediction_length():

    true = [
        ['O', 'B-ORG', 'I-ORG', 'O', 'O'],
    ]

    pred = [
        ['O', 'B-MISC', 'I-MISC', 'O'],
    ]

    evaluator = Evaluator(true, pred, tags=['PER', 'MISC'], loader="list")

    with pytest.raises(ValueError):
        evaluator.evaluate()

def test_evaluator_list_non_matching_corpus_length():

    true = [
        ['O', 'B-ORG', 'I-ORG', 'O', 'O'],
        ['O', 'O', 'O', 'O']
    ]

    pred = [
        ['O', 'B-MISC', 'I-MISC', 'O'],
    ]

    with pytest.raises(ValueError):
        evaluator = Evaluator(true, pred, tags=['PER', 'MISC'], loader="list")
        evaluator.evaluate()

def test_evaluator_on_single_token():

    true = [
        ['PER'],
    ]

    pred = [
        ['PER'],
    ]

    evaluator = Evaluator(true, pred, tags=['PER'], loader="list")

    results, results_agg = evaluator.evaluate()

    expected = {
        'strict': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0,
        },
        'ent_type': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0,
        },
        'partial': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0,
        },
        'exact': {
            'correct': 1,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 1,
            'actual': 1,
            'precision': 1.0,
            'recall': 1.0,
            'f1': 1.0,
        }
    }

    assert expected["strict"] == results["strict"]
    assert expected["ent_type"] == results["ent_type"]
    assert expected["partial"] == results["partial"]
    assert expected["exact"] == results["exact"]
