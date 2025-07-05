import csv
import io
import pytest
from nervaluate.evaluator import Evaluator


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


def test_results_to_csv(sample_data, tmp_path):

    true, pred = sample_data
    evaluator = Evaluator(true, pred, ["PER", "ORG", "LOC"], loader="list")

    overall_csv_str = evaluator.results_to_csv(mode="overall")
    assert isinstance(overall_csv_str, str)

    csv_reader = csv.reader(io.StringIO(overall_csv_str))
    overall_csv = list(csv_reader)

    assert len(overall_csv) > 1  # should have header + at least one row
    assert overall_csv[0] == [
        "Strategy",
        "Correct",
        "Incorrect",
        "Partial",
        "Missed",
        "Spurious",
        "Precision",
        "Recall",
        "F1-Score",
    ]

    # check that all strategies are present
    strategies = {row[0] for row in overall_csv[1:]}
    assert strategies == {"strict", "partial", "ent_type", "exact"}

    # test entities mode - return as string
    entities_csv_str = evaluator.results_to_csv(mode="entities", scenario="strict")
    assert isinstance(entities_csv_str, str)

    # parse CSV string to check content
    csv_reader = csv.reader(io.StringIO(entities_csv_str))
    entities_csv = list(csv_reader)

    assert len(entities_csv) > 1  # should have header + at least one row
    assert entities_csv[0] == [
        "Entity",
        "Correct",
        "Incorrect",
        "Partial",
        "Missed",
        "Spurious",
        "Precision",
        "Recall",
        "F1-Score",
    ]

    # check that all entity types are present
    entity_types = {row[0] for row in entities_csv[1:]}
    assert entity_types == {"PER", "ORG", "LOC"}

    # test file saving - overall mode
    overall_file = tmp_path / "overall_results.csv"
    result = evaluator.results_to_csv(mode="overall", file_path=str(overall_file))
    assert result is None  # Should return None when saving to file
    assert overall_file.exists()

    # verify file content
    with open(overall_file, "r", encoding="utf-8") as f:
        saved_csv = list(csv.reader(f))
    assert len(saved_csv) > 1
    assert saved_csv[0][0] == "Strategy"

    # test file saving - entities mode
    entities_file = tmp_path / "entities_results.csv"
    result = evaluator.results_to_csv(mode="entities", scenario="partial", file_path=str(entities_file))
    assert result is None  # Should return None when saving to file
    assert entities_file.exists()

    # verify file content
    with open(entities_file, "r", encoding="utf-8") as f:
        saved_csv = list(csv.reader(f))
    assert len(saved_csv) > 1
    assert saved_csv[0][0] == "Entity"

    # test invalid mode
    with pytest.raises(ValueError, match="Invalid mode: must be one of"):
        evaluator.results_to_csv(mode="invalid")

    # test invalid scenario for entities mode
    with pytest.raises(ValueError, match="Invalid scenario: must be one of"):
        evaluator.results_to_csv(mode="entities", scenario="invalid")
