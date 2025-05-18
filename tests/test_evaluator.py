# pylint: disable=too-many-lines
import pandas as pd

from nervaluate import Evaluator


def test_results_to_dataframe():
    """
    Test the results_to_dataframe method.
    """
    # Setup
    evaluator = Evaluator(
        true=[["B-LOC", "I-LOC", "O"], ["B-PER", "O", "O"]],
        pred=[["B-LOC", "I-LOC", "O"], ["B-PER", "I-PER", "O"]],
        tags=["LOC", "PER"],
    )

    # Mock results data for the purpose of this test
    evaluator.results = {
        "strict": {
            "correct": 10,
            "incorrect": 5,
            "partial": 3,
            "missed": 2,
            "spurious": 4,
            "precision": 0.625,
            "recall": 0.6667,
            "f1": 0.6452,
            "entities": {
                "LOC": {"correct": 4, "incorrect": 1, "partial": 0, "missed": 1, "spurious": 2},
                "PER": {"correct": 3, "incorrect": 2, "partial": 1, "missed": 0, "spurious": 1},
                "ORG": {"correct": 3, "incorrect": 2, "partial": 2, "missed": 1, "spurious": 1},
            },
        },
        "ent_type": {
            "correct": 8,
            "incorrect": 4,
            "partial": 1,
            "missed": 3,
            "spurious": 3,
            "precision": 0.5714,
            "recall": 0.6154,
            "f1": 0.5926,
            "entities": {
                "LOC": {"correct": 3, "incorrect": 2, "partial": 1, "missed": 1, "spurious": 1},
                "PER": {"correct": 2, "incorrect": 1, "partial": 0, "missed": 2, "spurious": 0},
                "ORG": {"correct": 3, "incorrect": 1, "partial": 0, "missed": 0, "spurious": 2},
            },
        },
        "partial": {
            "correct": 7,
            "incorrect": 3,
            "partial": 4,
            "missed": 1,
            "spurious": 5,
            "precision": 0.5385,
            "recall": 0.6364,
            "f1": 0.5833,
            "entities": {
                "LOC": {"correct": 2, "incorrect": 1, "partial": 1, "missed": 1, "spurious": 2},
                "PER": {"correct": 3, "incorrect": 1, "partial": 1, "missed": 0, "spurious": 1},
                "ORG": {"correct": 2, "incorrect": 1, "partial": 2, "missed": 0, "spurious": 2},
            },
        },
        "exact": {
            "correct": 9,
            "incorrect": 6,
            "partial": 2,
            "missed": 2,
            "spurious": 2,
            "precision": 0.6,
            "recall": 0.6429,
            "f1": 0.6207,
            "entities": {
                "LOC": {"correct": 4, "incorrect": 1, "partial": 0, "missed": 1, "spurious": 1},
                "PER": {"correct": 3, "incorrect": 3, "partial": 0, "missed": 0, "spurious": 0},
                "ORG": {"correct": 2, "incorrect": 2, "partial": 2, "missed": 1, "spurious": 1},
            },
        },
    }

    # Expected DataFrame
    expected_data = {
        "correct": {"strict": 10, "ent_type": 8, "partial": 7, "exact": 9},
        "incorrect": {"strict": 5, "ent_type": 4, "partial": 3, "exact": 6},
        "partial": {"strict": 3, "ent_type": 1, "partial": 4, "exact": 2},
        "missed": {"strict": 2, "ent_type": 3, "partial": 1, "exact": 2},
        "spurious": {"strict": 4, "ent_type": 3, "partial": 5, "exact": 2},
        "precision": {"strict": 0.625, "ent_type": 0.5714, "partial": 0.5385, "exact": 0.6},
        "recall": {"strict": 0.6667, "ent_type": 0.6154, "partial": 0.6364, "exact": 0.6429},
        "f1": {"strict": 0.6452, "ent_type": 0.5926, "partial": 0.5833, "exact": 0.6207},
        "entities.LOC.correct": {"strict": 4, "ent_type": 3, "partial": 2, "exact": 4},
        "entities.LOC.incorrect": {"strict": 1, "ent_type": 2, "partial": 1, "exact": 1},
        "entities.LOC.partial": {"strict": 0, "ent_type": 1, "partial": 1, "exact": 0},
        "entities.LOC.missed": {"strict": 1, "ent_type": 1, "partial": 1, "exact": 1},
        "entities.LOC.spurious": {"strict": 2, "ent_type": 1, "partial": 2, "exact": 1},
        "entities.PER.correct": {"strict": 3, "ent_type": 2, "partial": 3, "exact": 3},
        "entities.PER.incorrect": {"strict": 2, "ent_type": 1, "partial": 1, "exact": 3},
        "entities.PER.partial": {"strict": 1, "ent_type": 0, "partial": 1, "exact": 0},
        "entities.PER.missed": {"strict": 0, "ent_type": 2, "partial": 0, "exact": 0},
        "entities.PER.spurious": {"strict": 1, "ent_type": 0, "partial": 1, "exact": 0},
        "entities.ORG.correct": {"strict": 3, "ent_type": 3, "partial": 2, "exact": 2},
        "entities.ORG.incorrect": {"strict": 2, "ent_type": 1, "partial": 1, "exact": 2},
        "entities.ORG.partial": {"strict": 2, "ent_type": 0, "partial": 2, "exact": 2},
        "entities.ORG.missed": {"strict": 1, "ent_type": 0, "partial": 0, "exact": 1},
        "entities.ORG.spurious": {"strict": 1, "ent_type": 2, "partial": 2, "exact": 1},
    }

    expected_df = pd.DataFrame(expected_data)

    # Execute
    result_df = evaluator.results_to_dataframe()

    # Assert
    pd.testing.assert_frame_equal(result_df, expected_df)


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
