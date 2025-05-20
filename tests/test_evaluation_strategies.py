import pytest
from nervaluate.entities import Entity
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


# pylint: disable=redefined-outer-name
def test_strict_evaluation(sample_entities, sample_predictions):
    """Test strict evaluation strategy."""
    strategy = StrictEvaluation()
    result, indices = strategy.evaluate(sample_entities, sample_predictions, ["PER", "ORG", "LOC"])

    assert result.correct == 1
    assert result.incorrect == 0
    assert result.partial == 0
    assert result.missed == 2
    assert result.spurious == 2

    assert len(indices.correct_indices) == 1
    assert len(indices.missed_indices) == 2
    assert len(indices.spurious_indices) == 2


# pylint: disable=redefined-outer-name
def test_partial_evaluation(sample_entities, sample_predictions):
    """Test partial evaluation strategy."""
    strategy = PartialEvaluation()
    result, indices = strategy.evaluate(sample_entities, sample_predictions, ["PER", "ORG", "LOC"])

    assert result.correct == 1
    assert result.partial == 1
    assert result.incorrect == 1
    assert result.missed == 1
    assert result.spurious == 0

    assert len(indices.correct_indices) == 1
    assert len(indices.partial_indices) == 1
    assert len(indices.incorrect_indices) == 1
    assert len(indices.missed_indices) == 1


# pylint: disable=redefined-outer-name
def test_entity_type_evaluation(sample_entities, sample_predictions):
    """Test entity type evaluation strategy."""
    strategy = EntityTypeEvaluation()
    result, indices = strategy.evaluate(sample_entities, sample_predictions, ["PER", "ORG", "LOC"])

    assert result.correct == 2
    assert result.incorrect == 0
    assert result.partial == 0
    assert result.missed == 1
    assert result.spurious == 1

    assert len(indices.correct_indices) == 2
    assert len(indices.missed_indices) == 1
    assert len(indices.spurious_indices) == 1


def test_evaluation_with_empty_inputs():
    """Test evaluation with empty inputs."""
    strategy = StrictEvaluation()
    result, indices = strategy.evaluate([], [], ["PER", "ORG", "LOC"])

    assert result.correct == 0
    assert result.incorrect == 0
    assert result.partial == 0
    assert result.missed == 0
    assert result.spurious == 0

    assert len(indices.correct_indices) == 0
    assert len(indices.missed_indices) == 0
    assert len(indices.spurious_indices) == 0
