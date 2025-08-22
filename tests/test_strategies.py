import pytest
from nervaluate.entities import Entity
from nervaluate.strategies import EntityTypeEvaluation, ExactEvaluation, PartialEvaluation, StrictEvaluation


def create_entities_from_bio(bio_tags):
    """Helper function to create entities from BIO tags."""
    entities = []
    current_entity = None

    for i, tag in enumerate(bio_tags):
        if tag == "O":
            continue

        if tag.startswith("B-"):
            if current_entity:
                entities.append(current_entity)
            current_entity = Entity(tag[2:], i, i + 1)
        elif tag.startswith("I-"):
            if current_entity:
                current_entity.end = i + 1
            else:
                # Handle case where I- tag appears without B-
                current_entity = Entity(tag[2:], i, i + 1)

    if current_entity:
        entities.append(current_entity)

    return entities


@pytest.fixture
def base_sequence():
    """Base sequence: 'The John Smith who works at Google Inc'"""
    return ["O", "B-PER", "I-PER", "O", "O", "O", "B-ORG", "I-ORG"]


class TestStrictEvaluation:
    """Test cases for strict evaluation strategy."""

    def test_perfect_match(self, base_sequence):
        """Test case: Perfect match of all entities."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(base_sequence)

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_missed_entity(self, base_sequence):
        """Test case: One entity is missed in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "O"])

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 1
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 1)]
        assert result_indices.spurious_indices == []

    def test_wrong_label(self, base_sequence):
        """Test case: Entity with wrong label."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "I-LOC"])

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_wrong_boundary(self, base_sequence):
        """Test case: Entity with wrong boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "O"])

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_shifted_boundary(self, base_sequence):
        """Test case: Entity with shifted boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "B-LOC"])

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity(self, base_sequence):
        """Test case: Extra entity in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "B-PER", "O", "B-LOC", "I-LOC"])

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 2)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == [(0, 1)]


class TestEntityTypeEvaluation:
    """Test cases for entity type evaluation strategy."""

    def test_perfect_match(self, base_sequence):
        """Test case: Perfect match of all entities."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(base_sequence)

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_missed_entity(self, base_sequence):
        """Test case: One entity is missed in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "O"])

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 1
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 1)]
        assert result_indices.spurious_indices == []

    def test_wrong_label(self, base_sequence):
        """Test case: Entity with wrong label."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "I-LOC"])

        evaluator = EntityTypeEvaluation()
        result, _ = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0

    def test_wrong_boundary(self, base_sequence):
        """Test case: Entity with wrong boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "O"])

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_shifted_boundary(self, base_sequence):
        """Test case: Entity with shifted boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "B-LOC"])

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity(self, base_sequence):
        """Test case: Extra entity in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "B-PER", "O", "B-LOC", "I-LOC"])

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 2)]
        assert result_indices.spurious_indices == [(0, 1)]
        assert result_indices.missed_indices == []
        assert result_indices.partial_indices == []


class TestExactEvaluation:
    """Test cases for exact evaluation strategy."""

    def test_perfect_match(self, base_sequence):
        """Test case: Perfect match of all entities."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(base_sequence)

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_missed_entity(self, base_sequence):
        """Test case: One entity is missed in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "O"])

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 1
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 1)]
        assert result_indices.spurious_indices == []

    def test_wrong_label(self, base_sequence):
        """Test case: Entity with wrong label."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "I-LOC"])

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_wrong_boundary(self, base_sequence):
        """Test case: Entity with wrong boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "O"])

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_shifted_boundary(self, base_sequence):
        """Test case: Entity with shifted boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "B-LOC"])

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity(self, base_sequence):
        """Test case: Extra entity in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "B-PER", "O", "B-LOC", "I-LOC"])

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0), (0, 2)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == [(0, 1)]


class TestPartialEvaluation:
    """Test cases for partial evaluation strategy."""

    def test_perfect_match(self, base_sequence):
        """Test case: Perfect match of all entities."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(base_sequence)

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_missed_entity(self, base_sequence):
        """Test case: One entity is missed in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "O"])

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 1
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 1)]
        assert result_indices.spurious_indices == []

    def test_wrong_label(self, base_sequence):
        """Test case: Entity with wrong label."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "I-LOC"])

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_wrong_boundary(self, base_sequence):
        """Test case: Entity with wrong boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "B-LOC", "O"])

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 0
        assert result.partial == 1
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == [(0, 1)]
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_shifted_boundary(self, base_sequence):
        """Test case: Entity with shifted boundary."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "O", "O", "O", "B-LOC"])

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 1
        assert result.incorrect == 0
        assert result.partial == 1
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == [(0, 1)]
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity(self, base_sequence):
        """Test case: Extra entity in prediction."""
        true = create_entities_from_bio(base_sequence)
        pred = create_entities_from_bio(["O", "B-PER", "I-PER", "O", "B-PER", "O", "B-LOC", "I-LOC"])

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG", "LOC"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0), (0, 2)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == [(0, 1)]


class TestSingleCharacterEntities:
    """Test cases for single-character entities to ensure proper range handling."""

    def test_single_token_entities_strict(self):
        """Test case: Single token entities using strict evaluation."""
        # Create entities representing single characters/tokens
        # Entity at position 1 with start=1, end=2 (standard representation)
        true = [Entity("PER", 1, 2), Entity("ORG", 4, 5)]
        pred = [Entity("PER", 1, 2), Entity("ORG", 4, 5)]

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]

    def test_single_token_entities_same_start_end(self):
        """Test case: Single token entities where start==end (edge case)."""
        # Edge case: entities where start and end are the same
        # This tests the scenario mentioned in the user's question
        true = [Entity("PER", 1, 1), Entity("ORG", 4, 4)]
        pred = [Entity("PER", 1, 1), Entity("ORG", 4, 4)]

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]

    def test_single_token_entities_partial_evaluation(self):
        """Test case: Single token entities with partial evaluation."""
        true = [Entity("PER", 1, 1), Entity("ORG", 4, 4)]
        pred = [Entity("PER", 1, 1), Entity("ORG", 4, 4)]

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]

    def test_single_token_entities_overlap_detection(self):
        """Test case: Single token entities with overlapping positions."""
        # Test overlap detection for single character entities
        true = [Entity("PER", 1, 1)]  # Single token at position 1
        pred = [Entity("ORG", 1, 1)]  # Different label, same position

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        # Should be marked as incorrect due to label mismatch but position overlap
        assert result.correct == 0
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.incorrect_indices == [(0, 0)]

    def test_single_token_adjacent_entities(self):
        """Test case: Adjacent single token entities."""
        # Test entities at adjacent positions
        true = [Entity("PER", 1, 1), Entity("ORG", 2, 2)]
        pred = [Entity("PER", 1, 1), Entity("ORG", 2, 2)]

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 2
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1)]

    def test_single_token_missed_entity(self):
        """Test case: Single token entity that is missed."""
        true = [Entity("PER", 1, 1), Entity("ORG", 4, 4)]
        pred = [Entity("PER", 1, 1)]  # Missing the ORG entity

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["PER", "ORG"])

        assert result.correct == 1
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0)]
        assert result_indices.missed_indices == [(0, 1)]
