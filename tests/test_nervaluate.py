import pytest

from nervaluate import (
    Evaluator,
    compute_actual_possible,
    compute_metrics,
    compute_precision_recall,
    compute_precision_recall_wrapper,
)


def test_compute_metrics_case_1():
    true_named_entities = [
        {"label": "PER", "start": 59, "end": 69},
        {"label": "LOC", "start": 127, "end": 134},
        {"label": "LOC", "start": 164, "end": 174},
        {"label": "LOC", "start": 197, "end": 205},
        {"label": "LOC", "start": 208, "end": 219},
        {"label": "MISC", "start": 230, "end": 240},
    ]
    pred_named_entities = [
        {"label": "PER", "start": 24, "end": 30},
        {"label": "LOC", "start": 124, "end": 134},
        {"label": "PER", "start": 164, "end": 174},
        {"label": "LOC", "start": 197, "end": 205},
        {"label": "LOC", "start": 208, "end": 219},
        {"label": "LOC", "start": 225, "end": 243},
    ]
    results, _, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER", "LOC", "MISC"])
    results = compute_precision_recall_wrapper(results)
    expected = {
        "strict": {
            "correct": 2,
            "incorrect": 3,
            "partial": 0,
            "missed": 1,
            "spurious": 1,
            "possible": 6,
            "actual": 6,
            "precision": 0.3333333333333333,
            "recall": 0.3333333333333333,
            "f1": 0.3333333333333333,
        },
        "ent_type": {
            "correct": 3,
            "incorrect": 2,
            "partial": 0,
            "missed": 1,
            "spurious": 1,
            "possible": 6,
            "actual": 6,
            "precision": 0.5,
            "recall": 0.5,
            "f1": 0.5,
        },
        "partial": {
            "correct": 3,
            "incorrect": 0,
            "partial": 2,
            "missed": 1,
            "spurious": 1,
            "possible": 6,
            "actual": 6,
            "precision": 0.6666666666666666,
            "recall": 0.6666666666666666,
            "f1": 0.6666666666666666,
        },
        "exact": {
            "correct": 3,
            "incorrect": 2,
            "partial": 0,
            "missed": 1,
            "spurious": 1,
            "possible": 6,
            "actual": 6,
            "precision": 0.5,
            "recall": 0.5,
            "f1": 0.5,
        },
    }
    assert results == expected


def test_compute_metrics_agg_scenario_3():
    true_named_entities = [{"label": "PER", "start": 59, "end": 69}]
    pred_named_entities = []
    _, results_agg, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER"])
    expected_agg = {
        "PER": {
            "strict": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 1,
                "spurious": 0,
                "actual": 0,
                "possible": 1,
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
                "actual": 0,
                "possible": 1,
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
                "actual": 0,
                "possible": 1,
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
                "actual": 0,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        }
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]


def test_compute_metrics_agg_scenario_2():
    true_named_entities = []
    pred_named_entities = [{"label": "PER", "start": 59, "end": 69}]
    _, results_agg, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER"])
    expected_agg = {
        "PER": {
            "strict": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "actual": 1,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "ent_type": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "actual": 1,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "partial": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "actual": 1,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "exact": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 1,
                "actual": 1,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        }
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]


def test_compute_metrics_agg_scenario_5():
    true_named_entities = [{"label": "PER", "start": 59, "end": 69}]
    pred_named_entities = [{"label": "PER", "start": 57, "end": 69}]
    _, results_agg, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER"])
    expected_agg = {
        "PER": {
            "strict": {
                "correct": 0,
                "incorrect": 1,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "ent_type": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "partial": {
                "correct": 0,
                "incorrect": 0,
                "partial": 1,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "exact": {
                "correct": 0,
                "incorrect": 1,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        }
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]


def test_compute_metrics_agg_scenario_4():
    true_named_entities = [{"label": "PER", "start": 59, "end": 69}]
    pred_named_entities = [{"label": "LOC", "start": 59, "end": 69}]
    _, results_agg, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER", "LOC"])
    expected_agg = {
        "PER": {
            "strict": {
                "correct": 0,
                "incorrect": 1,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "ent_type": {
                "correct": 0,
                "incorrect": 1,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "partial": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "exact": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        },
        "LOC": {
            "strict": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "ent_type": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "partial": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "exact": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        },
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]
    assert results_agg["LOC"] == expected_agg["LOC"]


def test_compute_metrics_agg_scenario_1():
    true_named_entities = [{"label": "PER", "start": 59, "end": 69}]
    pred_named_entities = [{"label": "PER", "start": 59, "end": 69}]
    _, results_agg, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER"])
    expected_agg = {
        "PER": {
            "strict": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "ent_type": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "partial": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "exact": {
                "correct": 1,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        }
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]


def test_compute_metrics_agg_scenario_6():
    true_named_entities = [{"label": "PER", "start": 59, "end": 69}]
    pred_named_entities = [{"label": "LOC", "start": 54, "end": 69}]
    _, results_agg, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER", "LOC"])
    expected_agg = {
        "PER": {
            "strict": {
                "correct": 0,
                "incorrect": 1,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "ent_type": {
                "correct": 0,
                "incorrect": 1,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "partial": {
                "correct": 0,
                "incorrect": 0,
                "partial": 1,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "exact": {
                "correct": 0,
                "incorrect": 1,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 1,
                "possible": 1,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        },
        "LOC": {
            "strict": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "ent_type": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "partial": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
            "exact": {
                "correct": 0,
                "incorrect": 0,
                "partial": 0,
                "missed": 0,
                "spurious": 0,
                "actual": 0,
                "possible": 0,
                "precision": 0,
                "recall": 0,
                "f1": 0,
            },
        },
    }

    assert results_agg["PER"]["strict"] == expected_agg["PER"]["strict"]
    assert results_agg["PER"]["ent_type"] == expected_agg["PER"]["ent_type"]
    assert results_agg["PER"]["partial"] == expected_agg["PER"]["partial"]
    assert results_agg["PER"]["exact"] == expected_agg["PER"]["exact"]
    assert results_agg["LOC"] == expected_agg["LOC"]


def test_compute_metrics_extra_tags_in_prediction():
    true_named_entities = [
        {"label": "PER", "start": 50, "end": 52},
        {"label": "ORG", "start": 59, "end": 69},
        {"label": "ORG", "start": 71, "end": 72},
    ]

    pred_named_entities = [
        {"label": "LOC", "start": 50, "end": 52},  # Wrong type
        {"label": "ORG", "start": 59, "end": 69},  # Correct
        {"label": "MISC", "start": 71, "end": 72},  # Wrong type
    ]
    results, _, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER", "LOC", "ORG"])
    expected = {
        "strict": {
            "correct": 1,
            "incorrect": 1,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "actual": 2,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "ent_type": {
            "correct": 1,
            "incorrect": 1,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "actual": 2,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "partial": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "actual": 2,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "exact": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 1,
            "spurious": 0,
            "actual": 2,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_compute_metrics_extra_tags_in_true():
    true_named_entities = [
        {"label": "PER", "start": 50, "end": 52},
        {"label": "ORG", "start": 59, "end": 69},
        {"label": "MISC", "start": 71, "end": 72},
    ]

    pred_named_entities = [
        {"label": "LOC", "start": 50, "end": 52},  # Wrong type
        {"label": "ORG", "start": 59, "end": 69},  # Correct
        {"label": "ORG", "start": 71, "end": 72},  # Spurious
    ]

    results, _, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER", "LOC", "ORG"])

    expected = {
        "strict": {
            "correct": 1,
            "incorrect": 1,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "actual": 3,
            "possible": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "ent_type": {
            "correct": 1,
            "incorrect": 1,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "actual": 3,
            "possible": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "partial": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "actual": 3,
            "possible": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "exact": {
            "correct": 2,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 1,
            "actual": 3,
            "possible": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_compute_metrics_no_predictions():
    true_named_entities = [
        {"label": "PER", "start": 50, "end": 52},
        {"label": "ORG", "start": 59, "end": 69},
        {"label": "MISC", "start": 71, "end": 72},
    ]
    pred_named_entities = []
    results, _, _, _ = compute_metrics(true_named_entities, pred_named_entities, ["PER", "ORG", "MISC"])
    expected = {
        "strict": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 3,
            "spurious": 0,
            "actual": 0,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "ent_type": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 3,
            "spurious": 0,
            "actual": 0,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "partial": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 3,
            "spurious": 0,
            "actual": 0,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "exact": {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 3,
            "spurious": 0,
            "actual": 0,
            "possible": 3,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
    }

    assert results["strict"] == expected["strict"]
    assert results["ent_type"] == expected["ent_type"]
    assert results["partial"] == expected["partial"]
    assert results["exact"] == expected["exact"]


def test_compute_actual_possible():
    results = {
        "correct": 6,
        "incorrect": 3,
        "partial": 2,
        "missed": 4,
        "spurious": 2,
    }

    expected = {
        "correct": 6,
        "incorrect": 3,
        "partial": 2,
        "missed": 4,
        "spurious": 2,
        "possible": 15,
        "actual": 13,
    }

    out = compute_actual_possible(results)

    assert out == expected


def test_compute_precision_recall():
    results = {
        "correct": 6,
        "incorrect": 3,
        "partial": 2,
        "missed": 4,
        "spurious": 2,
        "possible": 15,
        "actual": 13,
    }

    expected = {
        "correct": 6,
        "incorrect": 3,
        "partial": 2,
        "missed": 4,
        "spurious": 2,
        "possible": 15,
        "actual": 13,
        "precision": 0.46153846153846156,
        "recall": 0.4,
        "f1": 0.42857142857142855,
    }

    out = compute_precision_recall(results)

    assert out == expected


def test_compute_metrics_one_pred_two_true():
    true_named_entities_1 = [
        {"start": 0, "end": 12, "label": "A"},
        {"start": 14, "end": 17, "label": "B"},
    ]
    true_named_entities_2 = [
        {"start": 14, "end": 17, "label": "B"},
        {"start": 0, "end": 12, "label": "A"},
    ]
    pred_named_entities = [
        {"start": 0, "end": 17, "label": "A"},
    ]

    results1, _, _, _ = compute_metrics(true_named_entities_1, pred_named_entities, ["A", "B"])
    results2, _, _, _ = compute_metrics(true_named_entities_2, pred_named_entities, ["A", "B"])

    expected = {
        "ent_type": {
            "correct": 1,
            "incorrect": 1,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 2,
            "actual": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "partial": {
            "correct": 0,
            "incorrect": 0,
            "partial": 2,
            "missed": 0,
            "spurious": 0,
            "possible": 2,
            "actual": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "strict": {
            "correct": 0,
            "incorrect": 2,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 2,
            "actual": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
        "exact": {
            "correct": 0,
            "incorrect": 2,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 2,
            "actual": 2,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        },
    }

    assert results1 == expected
    assert results2 == expected


def test_evaluator_different_number_of_documents():
    """Test that Evaluator raises ValueError when number of predicted documents doesn't match true documents."""

    # Create test data with different number of documents
    true = [
        [{"label": "PER", "start": 0, "end": 5}],  # First document
        [{"label": "LOC", "start": 10, "end": 15}],  # Second document
    ]
    pred = [[{"label": "PER", "start": 0, "end": 5}]]  # Only one document
    tags = ["PER", "LOC"]

    # Test that ValueError is raised
    with pytest.raises(ValueError, match="Number of predicted documents does not equal true"):
        evaluator = Evaluator(true=true, pred=pred, tags=tags)
        evaluator.evaluate()
