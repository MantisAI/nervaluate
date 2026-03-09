from copy import deepcopy
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


@pytest.fixture
def base_sequence_nested():
    """
    Base sequence: 'The Treaty of Westphalia negotiations concluded in 1648.'

    first_level_entity: Treaty of Westphalia negotiations
    second_level_entity: Treaty of Westphalia
    third_level_entity: Westphalia
    other_entity: 1648
    """
    first_level_entity = Entity("EVENT", 4, 37)
    second_level_entity = Entity("EVENT", 4, 24)
    third_level_entity = Entity("LOCATION", 14, 24)
    other_entity = Entity("DATE", 51, 55)

    return [first_level_entity, second_level_entity, third_level_entity, other_entity]


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

    def test_perfect_match_nested(self, base_sequence_nested):
        """Test case: Perfect match of all entities with nested entities."""
        evaluator = StrictEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_perfect_match_nested_reverse_order(self, base_sequence_nested):
        """Test case: Perfect match of all entities in reverse order, with nested entities."""
        evaluator = StrictEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[::-1]
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
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

    def test_missed_entity_nested(self, base_sequence_nested):
        """Test case: First level entity is missed in prediction."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[1:]

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 0)]
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

    def test_wrong_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong label."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].label = "DATE"

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
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

    def test_wrong_boundary_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].end = 30

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity_nested(self, base_sequence_nested):
        """Test case: Extra (spurious) entity in prediction with nested entities (Scenario II)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested) + [Entity("MISC", 60, 65)]

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE", "MISC"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == [(0, 4)]

    def test_wrong_boundary_and_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary and wrong label (Scenario VI)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1] = Entity("DATE", 4, 30)

        evaluator = StrictEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
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

    def test_perfect_match_nested(self, base_sequence_nested):
        """Test case: Perfect match of all entities with nested entities."""
        evaluator = EntityTypeEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_perfect_match_nested_reverse_order(self, base_sequence_nested):
        """Test case: Perfect match of all entities in reverse order, with nested entities."""
        evaluator = EntityTypeEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[::-1]
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
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

    def test_missed_entity_nested(self, base_sequence_nested):
        """Test case: First level entity is missed in prediction."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[1:]

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 0)]
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

    def test_wrong_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong label."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].label = "DATE"

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

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

    def test_wrong_boundary_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].end = 30

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity_nested(self, base_sequence_nested):
        """Test case: Extra (spurious) entity in prediction with nested entities (Scenario II)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested) + [Entity("MISC", 60, 65)]

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE", "MISC"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == [(0, 4)]

    def test_wrong_boundary_and_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary and wrong label (Scenario VI)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1] = Entity("DATE", 4, 30)

        evaluator = EntityTypeEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
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

    def test_perfect_match_nested(self, base_sequence_nested):
        """Test case: Perfect match of all entities with nested entities."""
        evaluator = ExactEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_perfect_match_nested_reverse_order(self, base_sequence_nested):
        """Test case: Perfect match of all entities in reverse order, with nested entities."""
        evaluator = ExactEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[::-1]
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
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

    def test_missed_entity_nested(self, base_sequence_nested):
        """Test case: First level entity is missed in prediction."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[1:]

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 0)]
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

    def test_wrong_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong label."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].label = "DATE"

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
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

    def test_wrong_boundary_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].end = 30

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == [(0, 1)]
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity_nested(self, base_sequence_nested):
        """Test case: Extra (spurious) entity in prediction with nested entities (Scenario II)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested) + [Entity("MISC", 60, 65)]

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE", "MISC"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == [(0, 4)]

    def test_wrong_boundary_and_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary and wrong label (Scenario VI)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1] = Entity("DATE", 4, 30)

        evaluator = ExactEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 1
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
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

    def test_perfect_match_nested(self, base_sequence_nested):
        """Test case: Perfect match of all entities with nested entities."""
        evaluator = PartialEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_perfect_match_nested_reverse_order(self, base_sequence_nested):
        """Test case: Perfect match of all entities in reverse order, with nested entities."""
        evaluator = PartialEvaluation()
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[::-1]
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
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

    def test_missed_entity_nested(self, base_sequence_nested):
        """Test case: First level entity is missed in prediction."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)[1:]

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 1
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == [(0, 0)]
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

    def test_wrong_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong label."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].label = "DATE"

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
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

    def test_wrong_boundary_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1].end = 30

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 0
        assert result.partial == 1
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == [(0, 1)]
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == []

    def test_extra_entity_nested(self, base_sequence_nested):
        """Test case: Extra (spurious) entity in prediction with nested entities (Scenario II)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested) + [Entity("MISC", 60, 65)]

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE", "MISC"])

        assert result.correct == 4
        assert result.incorrect == 0
        assert result.partial == 0
        assert result.missed == 0
        assert result.spurious == 1
        assert result_indices.correct_indices == [(0, 0), (0, 1), (0, 2), (0, 3)]
        assert result_indices.incorrect_indices == []
        assert result_indices.partial_indices == []
        assert result_indices.missed_indices == []
        assert result_indices.spurious_indices == [(0, 4)]

    def test_wrong_boundary_and_label_nested(self, base_sequence_nested):
        """Test case: Nested entity with wrong boundary and wrong label (Scenario VI)."""
        true = base_sequence_nested
        pred = deepcopy(base_sequence_nested)
        pred[1] = Entity("DATE", 4, 30)

        evaluator = PartialEvaluation()
        result, result_indices = evaluator.evaluate(true, pred, ["EVENT", "LOCATION", "DATE"])

        assert result.correct == 3
        assert result.incorrect == 0
        assert result.partial == 1
        assert result.missed == 0
        assert result.spurious == 0
        assert result_indices.correct_indices == [(0, 0), (0, 2), (0, 3)]
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


def test_minimum_overlap_percentage_validation():
    """Test that minimum overlap percentage validation works correctly."""

    # Valid values should work
    PartialEvaluation(min_overlap_percentage=1.0)
    PartialEvaluation(min_overlap_percentage=50.0)
    PartialEvaluation(min_overlap_percentage=100.0)

    # Invalid values should raise ValueError
    with pytest.raises(ValueError, match="min_overlap_percentage must be between 1.0 and 100.0"):
        PartialEvaluation(min_overlap_percentage=0.5)

    with pytest.raises(ValueError, match="min_overlap_percentage must be between 1.0 and 100.0"):
        PartialEvaluation(min_overlap_percentage=101.0)

    with pytest.raises(ValueError, match="min_overlap_percentage must be between 1.0 and 100.0"):
        PartialEvaluation(min_overlap_percentage=-5.0)


def test_overlap_percentage_calculation():
    """Test the overlap percentage calculation method."""
    strategy = PartialEvaluation(min_overlap_percentage=50.0)

    true_entity = Entity(label="PER", start=0, end=9)  # 10 tokens (0-9 inclusive)

    test_cases = [
        # (pred_entity, expected_percentage)
        (Entity(label="PER", start=0, end=9), 100.0),  # Complete overlap
        (Entity(label="PER", start=0, end=4), 50.0),  # Half overlap from start
        (Entity(label="PER", start=5, end=9), 50.0),  # Half overlap from end
        (Entity(label="PER", start=0, end=0), 10.0),  # Single token overlap at start
        (Entity(label="PER", start=9, end=9), 10.0),  # Single token overlap at end
        (Entity(label="PER", start=10, end=15), 0.0),  # No overlap (adjacent)
        (Entity(label="PER", start=-5, end=2), 30.0),  # Partial overlap from left (3 tokens: 0,1,2)
        (Entity(label="PER", start=7, end=12), 30.0),  # Partial overlap from right (3 tokens: 7,8,9)
        (Entity(label="PER", start=2, end=7), 60.0),  # Middle overlap (6 tokens: 2,3,4,5,6,7)
    ]

    for pred_entity, expected_percentage in test_cases:
        calculated = strategy._calculate_overlap_percentage(pred_entity, true_entity)
        assert (
            abs(calculated - expected_percentage) < 0.1
        ), f"Expected {expected_percentage}%, got {calculated}% for pred={pred_entity} vs true={true_entity}"


def test_has_sufficient_overlap():
    """Test the has_sufficient_overlap method with different thresholds."""

    true_entity = Entity(label="PER", start=0, end=9)  # 10 tokens

    # Test with 50% threshold
    strategy_50 = PartialEvaluation(min_overlap_percentage=50.0)

    # Should pass: 50% or more overlap
    assert strategy_50._has_sufficient_overlap(Entity(label="PER", start=0, end=4), true_entity)  # 50%
    assert strategy_50._has_sufficient_overlap(Entity(label="PER", start=0, end=6), true_entity)  # 70%
    assert strategy_50._has_sufficient_overlap(Entity(label="PER", start=0, end=9), true_entity)  # 100%

    # Should fail: less than 50% overlap
    assert not strategy_50._has_sufficient_overlap(Entity(label="PER", start=0, end=2), true_entity)  # 30%
    assert not strategy_50._has_sufficient_overlap(Entity(label="PER", start=0, end=0), true_entity)  # 10%
    assert not strategy_50._has_sufficient_overlap(Entity(label="PER", start=10, end=15), true_entity)  # 0%

    # Test with 75% threshold
    strategy_75 = PartialEvaluation(min_overlap_percentage=75.0)

    # Should pass: 75% or more overlap
    assert strategy_75._has_sufficient_overlap(Entity(label="PER", start=0, end=7), true_entity)  # 80%
    assert strategy_75._has_sufficient_overlap(Entity(label="PER", start=0, end=9), true_entity)  # 100%

    # Should fail: less than 75% overlap
    assert not strategy_75._has_sufficient_overlap(Entity(label="PER", start=0, end=6), true_entity)  # 70%
    assert not strategy_75._has_sufficient_overlap(Entity(label="PER", start=0, end=4), true_entity)  # 50%


def test_partial_evaluation_with_min_overlap():
    """Test PartialEvaluation strategy with different minimum overlap thresholds."""

    true_entities = [Entity(label="PER", start=0, end=9)]  # 10 tokens

    test_cases = [
        # (pred_entity, min_overlap_threshold, expected_correct, expected_partial, expected_spurious)
        (Entity(label="PER", start=0, end=4), 50.0, 0, 1, 0),  # 50% overlap -> partial
        (Entity(label="PER", start=0, end=2), 50.0, 0, 0, 1),  # 30% overlap < 50% -> spurious
        (Entity(label="PER", start=0, end=9), 50.0, 1, 0, 0),  # 100% overlap exact match -> correct
        (Entity(label="PER", start=0, end=6), 75.0, 0, 0, 1),  # 70% overlap < 75% -> spurious
        (Entity(label="PER", start=0, end=7), 75.0, 0, 1, 0),  # 80% overlap > 75% -> partial
    ]

    for pred_entity, threshold, expected_correct, expected_partial, expected_spurious in test_cases:
        pred_entities = [pred_entity]
        strategy = PartialEvaluation(min_overlap_percentage=threshold)
        result, _ = strategy.evaluate(true_entities, pred_entities, ["PER"], 0)

        assert (
            result.correct == expected_correct
        ), f"Expected {expected_correct} correct, got {result.correct} for {pred_entity} with threshold {threshold}%"
        assert (
            result.partial == expected_partial
        ), f"Expected {expected_partial} partial, got {result.partial} for {pred_entity} with threshold {threshold}%"
        assert (
            result.spurious == expected_spurious
        ), f"Expected {expected_spurious} spurious, got {result.spurious} for {pred_entity} with threshold {threshold}%"


def test_strict_evaluation_with_min_overlap():
    """Test StrictEvaluation strategy with minimum overlap threshold."""

    true_entities = [Entity(label="PER", start=0, end=9)]

    # Test case where pred has insufficient overlap -> should be spurious
    pred_entities = [Entity(label="PER", start=0, end=2)]  # 30% overlap
    strategy = StrictEvaluation(min_overlap_percentage=50.0)
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER"], 0)

    assert result.correct == 0
    assert result.incorrect == 0
    assert result.spurious == 1  # Insufficient overlap -> spurious
    assert result.missed == 1  # True entity not matched

    # Test case where pred has sufficient overlap but wrong label -> should be incorrect
    pred_entities = [Entity(label="ORG", start=0, end=6)]  # 70% overlap, wrong label
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER", "ORG"], 0)

    assert result.correct == 0
    assert result.incorrect == 1  # Sufficient overlap but wrong label
    assert result.spurious == 0
    assert result.missed == 0


def test_entity_type_evaluation_with_min_overlap():
    """Test EntityTypeEvaluation strategy with minimum overlap threshold."""

    true_entities = [Entity(label="PER", start=0, end=9)]

    # Test case: sufficient overlap with correct label -> correct
    pred_entities = [Entity(label="PER", start=0, end=6)]  # 70% overlap, correct label
    strategy = EntityTypeEvaluation(min_overlap_percentage=50.0)
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER"], 0)

    assert result.correct == 1
    assert result.incorrect == 0
    assert result.spurious == 0
    assert result.missed == 0

    # Test case: sufficient overlap with wrong label -> incorrect
    pred_entities = [Entity(label="ORG", start=0, end=6)]  # 70% overlap, wrong label
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER", "ORG"], 0)

    assert result.correct == 0
    assert result.incorrect == 1
    assert result.spurious == 0
    assert result.missed == 0

    # Test case: insufficient overlap -> spurious
    pred_entities = [Entity(label="PER", start=0, end=2)]  # 30% overlap < 50%
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER"], 0)

    assert result.correct == 0
    assert result.incorrect == 0
    assert result.spurious == 1
    assert result.missed == 1


def test_exact_evaluation_with_min_overlap():
    """Test ExactEvaluation strategy with minimum overlap threshold."""

    true_entities = [Entity(label="PER", start=0, end=9)]

    # Test case: exact boundaries (different label) -> correct
    pred_entities = [Entity(label="ORG", start=0, end=9)]  # Exact match, different label
    strategy = ExactEvaluation(min_overlap_percentage=50.0)
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER", "ORG"], 0)

    assert result.correct == 1
    assert result.incorrect == 0
    assert result.spurious == 0
    assert result.missed == 0

    # Test case: sufficient overlap but not exact -> incorrect
    pred_entities = [Entity(label="ORG", start=0, end=6)]  # 70% overlap, not exact
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER", "ORG"], 0)

    assert result.correct == 0
    assert result.incorrect == 1
    assert result.spurious == 0
    assert result.missed == 0

    # Test case: insufficient overlap -> spurious
    pred_entities = [Entity(label="ORG", start=0, end=2)]  # 30% overlap < 50%
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER", "ORG"], 0)

    assert result.correct == 0
    assert result.incorrect == 0
    assert result.spurious == 1
    assert result.missed == 1


def test_edge_cases_overlap_calculation():
    """Test edge cases for overlap calculation."""

    strategy = PartialEvaluation(min_overlap_percentage=100.0)

    # Test single-token entities
    true_single = Entity(label="ORG", start=5, end=5)  # Single token
    pred_single = Entity(label="ORG", start=5, end=5)  # Exact match

    overlap = strategy._calculate_overlap_percentage(pred_single, true_single)
    assert overlap == 100.0, "Single token exact match should be 100%"

    # Test adjacent but non-overlapping entities
    pred_adjacent = Entity(label="ORG", start=6, end=6)  # Adjacent token
    overlap = strategy._calculate_overlap_percentage(pred_adjacent, true_single)
    assert overlap == 0.0, "Adjacent non-overlapping should be 0%"

    # Test overlapping single-token entities
    pred_overlap = Entity(label="ORG", start=4, end=6)  # Overlaps with true_single at position 5
    overlap = strategy._calculate_overlap_percentage(pred_overlap, true_single)
    assert overlap == 100.0, "Single token overlap should be 100% of true entity"


def test_multiple_entities_with_min_overlap():
    """Test evaluation with multiple entities and minimum overlap."""

    true_entities = [Entity(label="PER", start=0, end=4), Entity(label="ORG", start=10, end=14)]  # 5 tokens  # 5 tokens

    pred_entities = [
        Entity(label="PER", start=0, end=1),  # 40% overlap with first entity
        Entity(label="ORG", start=10, end=12),  # 60% overlap with second entity
        Entity(label="LOC", start=20, end=22),  # No overlap (spurious)
    ]

    # With 50% threshold
    strategy = PartialEvaluation(min_overlap_percentage=50.0)
    result, _ = strategy.evaluate(true_entities, pred_entities, ["PER", "ORG", "LOC"], 0)

    assert result.correct == 0
    assert result.partial == 1  # Only the ORG entity has sufficient overlap (60% > 50%)
    assert result.spurious == 2  # PER entity (40% < 50%) and LOC entity (no overlap)
    assert result.missed == 1  # First true entity (PER) not sufficiently matched
