import pytest

from nervaluate.reporting import summary_report_ent, summary_report_overall


def test_summary_report_ent():
    # Sample input data
    results_agg_entities_type = {
        "PER": {
            "strict": {
                "correct": 10,
                "incorrect": 2,
                "partial": 1,
                "missed": 3,
                "spurious": 2,
                "precision": 0.769,
                "recall": 0.714,
                "f1": 0.741,
            }
        },
        "ORG": {
            "strict": {
                "correct": 15,
                "incorrect": 1,
                "partial": 0,
                "missed": 2,
                "spurious": 1,
                "precision": 0.882,
                "recall": 0.833,
                "f1": 0.857,
            }
        },
    }

    # Call the function
    report = summary_report_ent(results_agg_entities_type, scenario="strict", digits=3)

    # Verify the report contains expected content
    assert "PER" in report
    assert "ORG" in report
    assert "correct" in report
    assert "incorrect" in report
    assert "partial" in report
    assert "missed" in report
    assert "spurious" in report
    assert "precision" in report
    assert "recall" in report
    assert "f1-score" in report

    # Verify specific values are present
    assert "10" in report  # PER correct
    assert "15" in report  # ORG correct
    assert "0.769" in report  # PER precision
    assert "0.857" in report  # ORG f1

    # Test invalid scenario
    with pytest.raises(Exception) as exc_info:
        summary_report_ent(results_agg_entities_type, scenario="invalid")
    assert "Invalid scenario" in str(exc_info.value)


def test_summary_report_overall():
    # Sample input data
    results = {
        "strict": {
            "correct": 25,
            "incorrect": 3,
            "partial": 1,
            "missed": 5,
            "spurious": 3,
            "precision": 0.862,
            "recall": 0.806,
            "f1": 0.833,
        },
        "ent_type": {
            "correct": 26,
            "incorrect": 2,
            "partial": 1,
            "missed": 4,
            "spurious": 3,
            "precision": 0.897,
            "recall": 0.839,
            "f1": 0.867,
        },
    }

    # Call the function
    report = summary_report_overall(results, digits=3)

    # Verify the report contains expected content
    assert "strict" in report
    assert "ent_type" in report
    assert "correct" in report
    assert "incorrect" in report
    assert "partial" in report
    assert "missed" in report
    assert "spurious" in report
    assert "precision" in report
    assert "recall" in report
    assert "f1-score" in report

    # Verify specific values are present
    assert "25" in report  # strict correct
    assert "26" in report  # ent_type correct
    assert "0.862" in report  # strict precision
    assert "0.867" in report  # ent_type f1

    # Test with different number of digits
    report_2digits = summary_report_overall(results, digits=2)
    assert "0.86" in report_2digits  # strict precision with 2 digits
    assert "0.87" in report_2digits  # ent_type f1 with 2 digits
