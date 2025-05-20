import pandas as pd
import pytest
from nervaluate.entities import Entity
from nervaluate.evaluator import Evaluator
from nervaluate.evaluation_strategies import StrictEvaluation, PartialEvaluation, EntityTypeEvaluation


@pytest.fixture
def sample_entities():
    return [
        Entity(label="PER", start=0, end=0),
        Entity(label="ORG", start=2, end=3),
        Entity(label="LOC", start=5, end=5),
    ]


@pytest.fixture
def sample_predictions():
    return [
        Entity(label="PER", start=0, end=0),  # Correct
        Entity(label="ORG", start=2, end=2),  # Partial
        Entity(label="PER", start=5, end=5),  # Wrong type
    ]


def test_strict_evaluation(sample_entities, sample_predictions):
    strategy = StrictEvaluation()
    result, indices = strategy.evaluate(sample_entities, sample_predictions, ["PER", "ORG", "LOC"])

    assert result.correct == 1
    assert result.incorrect == 0
    assert result.partial == 0
    assert result.missed == 2
    assert result.spurious == 2


def test_partial_evaluation(sample_entities, sample_predictions):
    strategy = PartialEvaluation()
    result, indices = strategy.evaluate(sample_entities, sample_predictions, ["PER", "ORG", "LOC"])

    assert result.correct == 1
    assert result.partial == 1
    assert result.incorrect == 1
    assert result.missed == 1
    assert result.spurious == 0


def test_entity_type_evaluation(sample_entities, sample_predictions):
    strategy = EntityTypeEvaluation()
    result, indices = strategy.evaluate(sample_entities, sample_predictions, ["PER", "ORG", "LOC"])

    assert result.correct == 2
    assert result.incorrect == 0
    assert result.partial == 0
    assert result.missed == 1
    assert result.spurious == 1


def test_evaluator_integration():
    # Test with list format
    true = [["O", "PER", "O", "ORG", "ORG", "LOC"]]
    pred = [["O", "PER", "O", "ORG", "O", "PER"]]

    evaluator = OldEvaluator(true, pred, ["PER", "ORG", "LOC"], loader="list")
    results = evaluator.evaluate()

    assert "overall" in results
    assert "entities" in results
    assert "strict" in results["overall"]
    assert "partial" in results["overall"]
    assert "ent_type" in results["overall"]

    # Test with CoNLL format
    true_conll = "word\tO\nword\tPER\nword\tO\nword\tORG\nword\tORG\nword\tLOC\n\n"
    pred_conll = "word\tO\nword\tPER\nword\tO\nword\tORG\nword\tO\nword\tPER\n\n"

    evaluator = OldEvaluator(true_conll, pred_conll, ["PER", "ORG", "LOC"], loader="conll")
    results = evaluator.evaluate()

    assert "overall" in results
    assert "entities" in results
    assert "strict" in results["overall"]
    assert "partial" in results["overall"]
    assert "ent_type" in results["overall"]


@pytest.fixture
def sample_data():
    true = [
        [Entity(label="PER", start=0, end=0), Entity(label="ORG", start=2, end=3), Entity(label="LOC", start=5, end=5)],
        [Entity(label="PER", start=0, end=0), Entity(label="ORG", start=2, end=2)],
    ]

    pred = [
        [
            Entity(label="PER", start=0, end=0),  # Correct
            Entity(label="ORG", start=2, end=2),  # Partial
            Entity(label="PER", start=5, end=5),  # Wrong type
        ],
        [Entity(label="PER", start=0, end=0), Entity(label="LOC", start=2, end=2)],  # Correct  # Wrong type
    ]

    return true, pred


def test_evaluator_initialization(sample_data):
    """Test evaluator initialization."""
    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["PER", "ORG", "LOC"])

    assert len(evaluator.true) == 2
    assert len(evaluator.pred) == 2
    assert evaluator.tags == ["PER", "ORG", "LOC"]


def test_evaluator_evaluation(sample_data):
    """Test evaluation process."""
    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["PER", "ORG", "LOC"])
    results = evaluator.evaluate()

    # Check that we have results for all strategies
    assert "strict" in results
    assert "partial" in results
    assert "ent_type" in results

    # Check that we have results for overall and each entity type
    for strategy in results:
        assert "overall" in results[strategy]
        assert "PER" in results[strategy]
        assert "ORG" in results[strategy]
        assert "LOC" in results[strategy]


def test_evaluator_dataframe_conversion(sample_data):
    """Test conversion of results to DataFrame."""
    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["PER", "ORG", "LOC"])
    results = evaluator.evaluate()
    df = evaluator.results_to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "strategy" in df.columns
    assert "entity_type" in df.columns
    assert "precision" in df.columns
    assert "recall" in df.columns
    assert "f1" in df.columns


def test_evaluator_with_empty_inputs():
    """Test evaluator with empty inputs."""
    evaluator = Evaluator([], [], ["PER", "ORG", "LOC"])
    results = evaluator.evaluate()

    for strategy in results:
        assert results[strategy]["overall"].correct == 0
        assert results[strategy]["overall"].incorrect == 0
        assert results[strategy]["overall"].partial == 0
        assert results[strategy]["overall"].missed == 0
        assert results[strategy]["overall"].spurious == 0


def test_evaluator_with_invalid_tags(sample_data):
    """Test evaluator with invalid tags."""
    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["INVALID"])
    results = evaluator.evaluate()

    for strategy in results:
        assert results[strategy]["overall"].correct == 0
        assert results[strategy]["overall"].incorrect == 0
        assert results[strategy]["overall"].partial == 0
        assert results[strategy]["overall"].missed == 0
        assert results[strategy]["overall"].spurious == 0
