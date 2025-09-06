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


def test_evaluator_with_min_overlap_percentage():
    """Test Evaluator class with minimum overlap percentage parameter."""

    # Test data: true entity spans positions 0-9 (10 tokens)
    true_entities = [[{"label": "PER", "start": 0, "end": 9}]]  # 10-token entity

    # Predicted entities with different overlap percentages
    pred_entities = [[{"label": "PER", "start": 0, "end": 2}]]  # 30% overlap

    # Test with default 1% threshold - should be partial match
    evaluator_default = Evaluator(true=true_entities, pred=pred_entities, tags=["PER"], loader="dict")
    results_default = evaluator_default.evaluate()
    partial_default = results_default["overall"]["partial"]
    assert partial_default.partial == 1
    assert partial_default.spurious == 0

    # Test with 50% threshold - should be spurious
    evaluator_50 = Evaluator(
        true=true_entities, pred=pred_entities, tags=["PER"], loader="dict", min_overlap_percentage=50.0
    )
    results_50 = evaluator_50.evaluate()
    partial_50 = results_50["overall"]["partial"]
    assert partial_50.partial == 0
    assert partial_50.spurious == 1


def test_evaluator_min_overlap_validation():
    """Test that Evaluator validates minimum overlap percentage."""
    true_entities = [[{"label": "PER", "start": 0, "end": 5}]]
    pred_entities = [[{"label": "PER", "start": 0, "end": 5}]]

    # Valid values should work
    Evaluator(true_entities, pred_entities, ["PER"], "dict", min_overlap_percentage=1.0)
    Evaluator(true_entities, pred_entities, ["PER"], "dict", min_overlap_percentage=50.0)
    Evaluator(true_entities, pred_entities, ["PER"], "dict", min_overlap_percentage=100.0)

    # Invalid values should raise ValueError during strategy initialization
    with pytest.raises(ValueError, match="min_overlap_percentage must be between 1.0 and 100.0"):
        Evaluator(true_entities, pred_entities, ["PER"], "dict", min_overlap_percentage=0.5)

    with pytest.raises(ValueError, match="min_overlap_percentage must be between 1.0 and 100.0"):
        Evaluator(true_entities, pred_entities, ["PER"], "dict", min_overlap_percentage=101.0)


def test_evaluator_min_overlap_affects_all_strategies():
    """Test that minimum overlap percentage affects all evaluation strategies."""
    true_entities = [[{"label": "PER", "start": 0, "end": 9}]]  # 10 tokens

    pred_entities = [[{"label": "PER", "start": 0, "end": 2}]]  # 30% overlap

    evaluator = Evaluator(
        true=true_entities, pred=pred_entities, tags=["PER"], loader="dict", min_overlap_percentage=50.0
    )

    results = evaluator.evaluate()

    # All strategies should respect the 50% threshold
    # 30% overlap < 50% threshold, so should be spurious for all strategies

    # Partial strategy
    partial_result = results["overall"]["partial"]
    assert partial_result.spurious == 1
    assert partial_result.correct == 0
    assert partial_result.partial == 0

    # Strict strategy
    strict_result = results["overall"]["strict"]
    assert strict_result.spurious == 1
    assert strict_result.correct == 0
    assert strict_result.incorrect == 0

    # Entity type strategy
    ent_type_result = results["overall"]["ent_type"]
    assert ent_type_result.spurious == 1
    assert ent_type_result.correct == 0
    assert ent_type_result.incorrect == 0

    # Exact strategy
    exact_result = results["overall"]["exact"]
    assert exact_result.spurious == 1
    assert exact_result.correct == 0
    assert exact_result.incorrect == 0


def test_evaluator_min_overlap_with_different_thresholds():
    """Test Evaluator with different overlap thresholds."""
    true_entities = [[{"label": "PER", "start": 0, "end": 9}]]  # 10 tokens

    # Test cases with different predicted entities
    test_cases = [
        # (pred_entities, threshold, expected_result_type)
        ([{"label": "PER", "start": 0, "end": 4}], 50.0, "partial"),  # 50% overlap = 50%
        ([{"label": "PER", "start": 0, "end": 4}], 51.0, "spurious"),  # 50% overlap < 51%
        ([{"label": "PER", "start": 0, "end": 6}], 75.0, "spurious"),  # 70% overlap < 75%
        ([{"label": "PER", "start": 0, "end": 7}], 75.0, "partial"),  # 80% overlap > 75%
        ([{"label": "PER", "start": 0, "end": 9}], 100.0, "correct"),  # 100% overlap = exact match
    ]

    for pred_data, threshold, expected_type in test_cases:
        pred_entities = [pred_data]

        evaluator = Evaluator(
            true=true_entities, pred=pred_entities, tags=["PER"], loader="dict", min_overlap_percentage=threshold
        )

        results = evaluator.evaluate()
        partial_results = results["overall"]["partial"]

        if expected_type == "correct":
            assert partial_results.correct == 1, f"Failed for {pred_data} with threshold {threshold}%"
            assert partial_results.partial == 0
            assert partial_results.spurious == 0
        elif expected_type == "partial":
            assert partial_results.partial == 1, f"Failed for {pred_data} with threshold {threshold}%"
            assert partial_results.correct == 0
            assert partial_results.spurious == 0
        elif expected_type == "spurious":
            assert partial_results.spurious == 1, f"Failed for {pred_data} with threshold {threshold}%"
            assert partial_results.correct == 0
            assert partial_results.partial == 0


def test_evaluator_min_overlap_with_multiple_entities():
    """Test Evaluator with multiple entities and minimum overlap threshold."""
    true_entities = [
        [
            {"label": "PER", "start": 0, "end": 4},  # 5 tokens
            {"label": "ORG", "start": 10, "end": 14},  # 5 tokens
            {"label": "LOC", "start": 20, "end": 24},  # 5 tokens
        ]
    ]

    pred_entities = [
        [
            {"label": "PER", "start": 0, "end": 1},  # 40% overlap (2/5 tokens)
            {"label": "ORG", "start": 10, "end": 12},  # 60% overlap (3/5 tokens)
            {"label": "LOC", "start": 20, "end": 24},  # 100% overlap (exact match)
            {"label": "MISC", "start": 30, "end": 32},  # No overlap (spurious)
        ]
    ]

    # Test with 50% threshold
    evaluator = Evaluator(
        true=true_entities,
        pred=pred_entities,
        tags=["PER", "ORG", "LOC", "MISC"],
        loader="dict",
        min_overlap_percentage=50.0,
    )

    results = evaluator.evaluate()
    partial_results = results["overall"]["partial"]

    assert partial_results.correct == 1  # LOC exact match
    assert partial_results.partial == 1  # ORG 60% overlap > 50%
    assert partial_results.spurious == 2  # PER 40% < 50% and MISC no overlap
    assert partial_results.missed == 1  # PER entity not sufficiently matched


def test_evaluator_min_overlap_backward_compatibility():
    """Test that the new feature maintains backward compatibility."""
    true_entities = [[{"label": "PER", "start": 0, "end": 9}]]

    pred_entities = [[{"label": "PER", "start": 9, "end": 9}]]  # 10% overlap (1 token out of 10)

    # Without specifying min_overlap_percentage (should default to 1.0)
    evaluator_default = Evaluator(true=true_entities, pred=pred_entities, tags=["PER"], loader="dict")

    # With explicitly setting to 1.0
    evaluator_explicit = Evaluator(
        true=true_entities, pred=pred_entities, tags=["PER"], loader="dict", min_overlap_percentage=1.0
    )

    results_default = evaluator_default.evaluate()
    results_explicit = evaluator_explicit.evaluate()

    # Results should be identical
    for strategy in ["strict", "partial", "ent_type", "exact"]:
        default_result = results_default["overall"][strategy]
        explicit_result = results_explicit["overall"][strategy]

        assert default_result.correct == explicit_result.correct
        assert default_result.partial == explicit_result.partial
        assert default_result.spurious == explicit_result.spurious
        assert default_result.missed == explicit_result.missed
