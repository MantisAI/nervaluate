# pylint: disable=C0302
from nervaluate import Evaluator


def test_evaluator_simple_case():
    true = [
        [{"label": "PER", "start": 2, "end": 4}],
        [
            {"label": "LOC", "start": 1, "end": 2},
            {"label": "LOC", "start": 3, "end": 4},
        ],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
        [
            {"label": "LOC", "start": 1, "end": 2},
            {"label": "LOC", "start": 3, "end": 4},
        ],
    ]
    evaluator = Evaluator(true, pred, tags=["LOC", "PER"])
    results, _, _, _ = evaluator.evaluate()
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


def test_evaluator_simple_case_filtered_tags():
    """Check that tags can be excluded by passing the tags argument"""
    true = [
        [{"label": "PER", "start": 2, "end": 4}],
        [
            {"label": "LOC", "start": 1, "end": 2},
            {"label": "LOC", "start": 3, "end": 4},
        ],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
        [
            {"label": "LOC", "start": 1, "end": 2},
            {"label": "LOC", "start": 3, "end": 4},
        ],
    ]
    evaluator = Evaluator(true, pred, tags=["PER", "LOC"])
    results, _, _, _ = evaluator.evaluate()
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


def test_evaluator_extra_classes():
    """Case when model predicts a class that is not in the gold (true) data"""
    true = [
        [{"label": "ORG", "start": 1, "end": 3}],
    ]
    pred = [
        [{"label": "FOO", "start": 1, "end": 3}],
    ]
    evaluator = Evaluator(true, pred, tags=["ORG", "FOO"])
    results, _, _, _ = evaluator.evaluate()
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
            "f1": 0,
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
            "f1": 0,
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


def test_evaluator_no_entities_in_prediction():
    """Case when model predicts a class that is not in the gold (true) data"""
    true = [
        [{"label": "PER", "start": 2, "end": 4}],
    ]
    pred = [
        [],
    ]
    evaluator = Evaluator(true, pred, tags=["PER"])
    results, _, _, _ = evaluator.evaluate()
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
            "f1": 0,
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
            "f1": 0,
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
            "f1": 0,
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
            "f1": 0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_evaluator_compare_results_and_results_agg():
    """Check that the label level results match the total results."""
    true = [
        [{"label": "PER", "start": 2, "end": 4}],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
    ]
    evaluator = Evaluator(true, pred, tags=["PER"])
    results, results_agg, _, _ = evaluator.evaluate()
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
            "f1": 1,
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
            "f1": 1,
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
            "f1": 1,
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
            "f1": 1,
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
                "f1": 1,
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
                "f1": 1,
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
                "f1": 1,
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
                "f1": 1,
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
    """Test case when model predicts a label not in the test data."""
    true = [
        [],
        [{"label": "ORG", "start": 2, "end": 4}],
        [{"label": "MISC", "start": 2, "end": 4}],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
        [{"label": "ORG", "start": 2, "end": 4}],
        [{"label": "MISC", "start": 2, "end": 4}],
    ]
    evaluator = Evaluator(true, pred, tags=["PER", "ORG", "MISC"])
    results, results_agg, _, _ = evaluator.evaluate()
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
            "f1": 0.8,
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
            "f1": 0.8,
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
            "f1": 0.8,
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
            "f1": 0.8,
        },
    }
    expected_agg = {
        "ORG": {
            "strict": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "possible": 1,
                "actual": 1,
                "precision": 1.0,
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
                "precision": 1.0,
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
                "f1": 1,
            },
        },
        "MISC": {
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
                "f1": 1,
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
                "f1": 1,
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
                "f1": 1,
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
                "f1": 1,
            },
        },
    }

    assert results_agg["ORG"]["strict"] == expected_agg["ORG"]["strict"]
    assert results_agg["ORG"]["ent_type"] == expected_agg["ORG"]["ent_type"]
    assert results_agg["ORG"]["partial"] == expected_agg["ORG"]["partial"]
    assert results_agg["ORG"]["exact"] == expected_agg["ORG"]["exact"]

    assert results_agg["MISC"]["strict"] == expected_agg["MISC"]["strict"]
    assert results_agg["MISC"]["ent_type"] == expected_agg["MISC"]["ent_type"]
    assert results_agg["MISC"]["partial"] == expected_agg["MISC"]["partial"]
    assert results_agg["MISC"]["exact"] == expected_agg["MISC"]["exact"]

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_evaluator_with_extra_keys_in_pred():
    true = [
        [{"label": "PER", "start": 2, "end": 4}],
        [
            {"label": "LOC", "start": 1, "end": 2},
            {"label": "LOC", "start": 3, "end": 4},
        ],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4, "token_start": 0, "token_end": 5}],
        [
            {"label": "LOC", "start": 1, "end": 2, "token_start": 0, "token_end": 6},
            {"label": "LOC", "start": 3, "end": 4, "token_start": 0, "token_end": 3},
        ],
    ]
    evaluator = Evaluator(true, pred, tags=["LOC", "PER"])
    results, _, _, _ = evaluator.evaluate()
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


def test_evaluator_with_extra_keys_in_true():
    true = [
        [{"label": "PER", "start": 2, "end": 4, "token_start": 0, "token_end": 4}],
        [
            {"label": "LOC", "start": 1, "end": 2, "token_start": 0, "token_end": 5},
            {"label": "LOC", "start": 3, "end": 4, "token_start": 7, "token_end": 9},
        ],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
        [
            {"label": "LOC", "start": 1, "end": 2},
            {"label": "LOC", "start": 3, "end": 4},
        ],
    ]
    evaluator = Evaluator(true, pred, tags=["LOC", "PER"])
    results, _, _, _ = evaluator.evaluate()
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


def test_issue_29():
    true = [
        [
            {"label": "PER", "start": 1, "end": 2},
            {"label": "PER", "start": 3, "end": 10},
        ]
    ]
    pred = [
        [
            {"label": "PER", "start": 1, "end": 2},
            {"label": "PER", "start": 3, "end": 5},
            {"label": "PER", "start": 6, "end": 10},
        ]
    ]
    evaluator = Evaluator(true, pred, tags=["PER"])
    results, _, _, _ = evaluator.evaluate()
    expected = {
        "strict": {
            "correct": 1,
            "incorrect": 1,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "possible": 2,
            "actual": 3,
            "precision": 0.3333333333333333,
            "recall": 0.5,
            "f1": 0.4,
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
            "f1": 0.8,
        },
        "partial": {
            "correct": 1,
            "incorrect": 0,
            "partial": 1,
            "missed": 0,
            "spurious": 1,
            "possible": 2,
            "actual": 3,
            "precision": 0.5,
            "recall": 0.75,
            "f1": 0.6,
        },
        "exact": {
            "correct": 1,
            "incorrect": 1,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "possible": 2,
            "actual": 3,
            "precision": 0.3333333333333333,
            "recall": 0.5,
            "f1": 0.4,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_evaluator_compare_results_indices_and_results_agg_indices():
    """Check that the label level results match the total results."""
    true = [
        [{"label": "PER", "start": 2, "end": 4}],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
    ]
    evaluator = Evaluator(true, pred, tags=["PER"])
    _, _, evaluation_indices, evaluation_agg_indices = evaluator.evaluate()
    expected_evaluation_indices = {
        "strict": {
            "correct_indices": [(0, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [],
        },
        "ent_type": {
            "correct_indices": [(0, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [],
        },
        "partial": {
            "correct_indices": [(0, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [],
        },
        "exact": {
            "correct_indices": [(0, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [],
        },
    }
    expected_evaluation_agg_indices = {
        "PER": {
            "strict": {
                "correct_indices": [(0, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "ent_type": {
                "correct_indices": [(0, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "partial": {
                "correct_indices": [(0, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "exact": {
                "correct_indices": [(0, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
        }
    }
    assert evaluation_agg_indices["PER"]["strict"] == expected_evaluation_agg_indices["PER"]["strict"]
    assert evaluation_agg_indices["PER"]["ent_type"] == expected_evaluation_agg_indices["PER"]["ent_type"]
    assert evaluation_agg_indices["PER"]["partial"] == expected_evaluation_agg_indices["PER"]["partial"]
    assert evaluation_agg_indices["PER"]["exact"] == expected_evaluation_agg_indices["PER"]["exact"]

    assert evaluation_indices["strict"] == expected_evaluation_indices["strict"]
    assert evaluation_indices["ent_type"] == expected_evaluation_indices["ent_type"]
    assert evaluation_indices["partial"] == expected_evaluation_indices["partial"]
    assert evaluation_indices["exact"] == expected_evaluation_indices["exact"]

    assert evaluation_indices["strict"] == expected_evaluation_agg_indices["PER"]["strict"]
    assert evaluation_indices["ent_type"] == expected_evaluation_agg_indices["PER"]["ent_type"]
    assert evaluation_indices["partial"] == expected_evaluation_agg_indices["PER"]["partial"]
    assert evaluation_indices["exact"] == expected_evaluation_agg_indices["PER"]["exact"]


def test_evaluator_compare_results_indices_and_results_agg_indices_1():
    """Test case when model predicts a label not in the test data."""
    true = [
        [],
        [{"label": "ORG", "start": 2, "end": 4}],
        [{"label": "MISC", "start": 2, "end": 4}],
    ]
    pred = [
        [{"label": "PER", "start": 2, "end": 4}],
        [{"label": "ORG", "start": 2, "end": 4}],
        [{"label": "MISC", "start": 2, "end": 4}],
    ]
    evaluator = Evaluator(true, pred, tags=["PER", "ORG", "MISC"])
    _, _, evaluation_indices, evaluation_agg_indices = evaluator.evaluate()

    expected_evaluation_indices = {
        "strict": {
            "correct_indices": [(1, 0), (2, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [(0, 0)],
        },
        "ent_type": {
            "correct_indices": [(1, 0), (2, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [(0, 0)],
        },
        "partial": {
            "correct_indices": [(1, 0), (2, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [(0, 0)],
        },
        "exact": {
            "correct_indices": [(1, 0), (2, 0)],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [(0, 0)],
        },
    }
    expected_evaluation_agg_indices = {
        "PER": {
            "strict": {
                "correct_indices": [],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [(0, 0)],
            },
            "ent_type": {
                "correct_indices": [],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [(0, 0)],
            },
            "partial": {
                "correct_indices": [],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [(0, 0)],
            },
            "exact": {
                "correct_indices": [],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [(0, 0)],
            },
        },
        "ORG": {
            "strict": {
                "correct_indices": [(1, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "ent_type": {
                "correct_indices": [(1, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "partial": {
                "correct_indices": [(1, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "exact": {
                "correct_indices": [(1, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
        },
        "MISC": {
            "strict": {
                "correct_indices": [(2, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "ent_type": {
                "correct_indices": [(2, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "partial": {
                "correct_indices": [(2, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
            "exact": {
                "correct_indices": [(2, 0)],
                "incorrect_indices": [],
                "partial_indices": [],
                "missed_indices": [],
                "spurious_indices": [],
            },
        },
    }
    assert evaluation_agg_indices["ORG"]["strict"] == expected_evaluation_agg_indices["ORG"]["strict"]
    assert evaluation_agg_indices["ORG"]["ent_type"] == expected_evaluation_agg_indices["ORG"]["ent_type"]
    assert evaluation_agg_indices["ORG"]["partial"] == expected_evaluation_agg_indices["ORG"]["partial"]
    assert evaluation_agg_indices["ORG"]["exact"] == expected_evaluation_agg_indices["ORG"]["exact"]

    assert evaluation_agg_indices["MISC"]["strict"] == expected_evaluation_agg_indices["MISC"]["strict"]
    assert evaluation_agg_indices["MISC"]["ent_type"] == expected_evaluation_agg_indices["MISC"]["ent_type"]
    assert evaluation_agg_indices["MISC"]["partial"] == expected_evaluation_agg_indices["MISC"]["partial"]
    assert evaluation_agg_indices["MISC"]["exact"] == expected_evaluation_agg_indices["MISC"]["exact"]

    assert evaluation_indices["strict"] == expected_evaluation_indices["strict"]
    assert evaluation_indices["ent_type"] == expected_evaluation_indices["ent_type"]
    assert evaluation_indices["partial"] == expected_evaluation_indices["partial"]
    assert evaluation_indices["exact"] == expected_evaluation_indices["exact"]
