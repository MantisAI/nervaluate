import os
import pytest

from nervaluate.nervaluate_cli import nervaluate


@pytest.fixture
def data_path(tmp_path):
    return os.path.join(tmp_path, "data.json")


def test_nervaluate(data_path):
    show_results_by_tag = True

    output = nervaluate(data_path=data_path, show_results_by_tag=show_results_by_tag)

    results = output["results"]

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
