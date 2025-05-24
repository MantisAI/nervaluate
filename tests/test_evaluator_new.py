import pytest
from nervaluate.evaluator import Evaluator


@pytest.fixture
def sample_entities():
    return [
        ["O", "B-PER", "O", "B-ORG", "I-ORG", "B-LOC"],
    ]


@pytest.fixture
def sample_predictions():
    return [
        ["O", "B-PER", "O", "B-ORG", "O", "B-PER"],
    ]


def test_strict_evaluation(sample_entities, sample_predictions):
    evaluator = Evaluator(sample_entities, sample_predictions, ["PER", "ORG", "LOC"], loader="list")
    results = evaluator.evaluate()

    # Test overall results
    assert results["overall"]["strict"].correct == 1
    assert results["overall"]["strict"].incorrect == 0
    assert results["overall"]["strict"].partial == 0
    assert results["overall"]["strict"].missed == 2
    assert results["overall"]["strict"].spurious == 2
    assert results["overall"]["strict"].precision == 0.3333333333333333
    assert results["overall"]["strict"].recall == 0.3333333333333333
    assert results["overall"]["strict"].f1 == 0.3333333333333333
    assert results["overall"]["strict"].actual == 3
    assert results["overall"]["strict"].possible == 3

    # Test entity-specific results
    for entity in ["PER", "ORG", "LOC"]:
        assert results["entities"][entity]["strict"].correct == 1
        assert results["entities"][entity]["strict"].incorrect == 0
        assert results["entities"][entity]["strict"].partial == 0
        assert results["entities"][entity]["strict"].missed == 2
        assert results["entities"][entity]["strict"].spurious == 2
        assert results["entities"][entity]["strict"].precision == 0.3333333333333333
        assert results["entities"][entity]["strict"].recall == 0.3333333333333333
        assert results["entities"][entity]["strict"].f1 == 0.3333333333333333
        assert results["entities"][entity]["strict"].actual == 3
        assert results["entities"][entity]["strict"].possible == 3


def test_partial_evaluation(sample_entities, sample_predictions):
    evaluator = Evaluator(sample_entities, sample_predictions, ["PER", "ORG", "LOC"], loader="list")
    results = evaluator.evaluate()

    # Test overall results
    assert results["overall"]["partial"].correct == 1
    assert results["overall"]["partial"].partial == 1
    assert results["overall"]["partial"].incorrect == 1
    assert results["overall"]["partial"].missed == 1
    assert results["overall"]["partial"].spurious == 0
    assert results["overall"]["partial"].precision == 0.5
    assert results["overall"]["partial"].recall == 0.375
    assert results["overall"]["partial"].f1 == 0.42857142857142855
    assert results["overall"]["partial"].actual == 3
    assert results["overall"]["partial"].possible == 4

    # Test entity-specific results
    for entity in ["PER", "ORG", "LOC"]:
        assert results["entities"][entity]["partial"].correct == 1
        assert results["entities"][entity]["partial"].partial == 1
        assert results["entities"][entity]["partial"].incorrect == 1
        assert results["entities"][entity]["partial"].missed == 1
        assert results["entities"][entity]["partial"].spurious == 0
        assert results["entities"][entity]["partial"].precision == 0.5
        assert results["entities"][entity]["partial"].recall == 0.375
        assert results["entities"][entity]["partial"].f1 == 0.42857142857142855
        assert results["entities"][entity]["partial"].actual == 3
        assert results["entities"][entity]["partial"].possible == 4


def test_entity_type_evaluation(sample_entities, sample_predictions):
    evaluator = Evaluator(sample_entities, sample_predictions, ["PER", "ORG", "LOC"], loader="list")
    results = evaluator.evaluate()

    # Test overall results
    assert results["overall"]["ent_type"].correct == 2
    assert results["overall"]["ent_type"].incorrect == 0
    assert results["overall"]["ent_type"].partial == 0
    assert results["overall"]["ent_type"].missed == 1
    assert results["overall"]["ent_type"].spurious == 1
    assert results["overall"]["ent_type"].precision == 0.6666666666666666
    assert results["overall"]["ent_type"].recall == 0.6666666666666666
    assert results["overall"]["ent_type"].f1 == 0.6666666666666666
    assert results["overall"]["ent_type"].actual == 3
    assert results["overall"]["ent_type"].possible == 3

    # Test entity-specific results
    for entity in ["PER", "ORG", "LOC"]:
        assert results["entities"][entity]["ent_type"].correct == 2
        assert results["entities"][entity]["ent_type"].incorrect == 0
        assert results["entities"][entity]["ent_type"].partial == 0
        assert results["entities"][entity]["ent_type"].missed == 1
        assert results["entities"][entity]["ent_type"].spurious == 1
        assert results["entities"][entity]["ent_type"].precision == 0.6666666666666666
        assert results["entities"][entity]["ent_type"].recall == 0.6666666666666666
        assert results["entities"][entity]["ent_type"].f1 == 0.6666666666666666
        assert results["entities"][entity]["ent_type"].actual == 3
        assert results["entities"][entity]["ent_type"].possible == 3


@pytest.fixture
def sample_data():
    true = [
        ["O", "B-PER", "O", "B-ORG", "I-ORG", "B-LOC"],
        ["O", "B-PER", "O", "B-ORG"],
    ]

    pred = [
        ["O", "B-PER", "O", "B-ORG", "O", "B-PER"],
        ["O", "B-PER", "O", "B-LOC"],
    ]

    return true, pred


def test_evaluator_initialization(sample_data):
    """Test evaluator initialization."""
    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["PER", "ORG", "LOC"], loader="list")

    assert len(evaluator.true) == 2
    assert len(evaluator.pred) == 2
    assert evaluator.tags == ["PER", "ORG", "LOC"]


def test_evaluator_evaluation(sample_data):
    """Test evaluation process."""
    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["PER", "ORG", "LOC"], loader="list")
    results = evaluator.evaluate()

    # Check that we have results for all strategies
    assert "overall" in results
    assert "entities" in results
    assert "strict" in results["overall"]
    assert "partial" in results["overall"]
    assert "ent_type" in results["overall"]

    # Check that we have results for each entity type
    for entity in ["PER", "ORG", "LOC"]:
        assert entity in results["entities"]
        assert "strict" in results["entities"][entity]
        assert "partial" in results["entities"][entity]
        assert "ent_type" in results["entities"][entity]


def test_evaluator_with_invalid_tags(sample_data):
    """Test evaluator with invalid tags."""
    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["INVALID"], loader="list")
    results = evaluator.evaluate()

    for strategy in ["strict", "partial", "ent_type"]:
        assert results["overall"][strategy].correct == 0
        assert results["overall"][strategy].incorrect == 0
        assert results["overall"][strategy].partial == 0
        assert results["overall"][strategy].missed == 0
        assert results["overall"][strategy].spurious == 0


def test_evaluator_different_document_lengths():
    """Test that Evaluator raises ValueError when documents have different lengths."""
    true = [
        ["O", "B-PER", "I-PER", "O", "O", "O", "B-ORG", "I-ORG"],  # 8 tokens
        ["O", "B-LOC", "B-PER", "I-PER", "O", "O", "B-DATE"],  # 7 tokens
    ]
    pred = [
        ["O", "B-PER", "I-PER", "O", "O", "O", "B-ORG", "I-ORG"],  # 8 tokens
        ["O", "B-LOC", "I-LOC", "O", "B-PER", "I-PER", "O", "B-DATE", "I-DATE", "O"],  # 10 tokens
    ]
    tags = ["PER", "ORG", "LOC", "DATE"]

    # Test that ValueError is raised
    with pytest.raises(ValueError, match="Document 1 has different lengths: true=7, pred=10"):
        evaluator = Evaluator(true=true, pred=pred, tags=tags, loader="list")
        evaluator.evaluate()
