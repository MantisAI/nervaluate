from nervaluate.entities import Entity, EvaluationResult


def test_entity_equality():
    """Test Entity equality comparison."""
    entity1 = Entity(label="PER", start=0, end=1)
    entity2 = Entity(label="PER", start=0, end=1)
    entity3 = Entity(label="ORG", start=0, end=1)

    assert entity1 == entity2
    assert entity1 != entity3
    assert entity1 != "not an entity"


def test_entity_hash():
    """Test Entity hashing."""
    entity1 = Entity(label="PER", start=0, end=1)
    entity2 = Entity(label="PER", start=0, end=1)
    entity3 = Entity(label="ORG", start=0, end=1)

    assert hash(entity1) == hash(entity2)
    assert hash(entity1) != hash(entity3)


def test_evaluation_result_compute_metrics():
    """Test computation of evaluation metrics."""
    result = EvaluationResult(correct=5, incorrect=2, partial=1, missed=1, spurious=1)

    # Test strict metrics
    result.compute_metrics(partial_or_type=False)
    assert result.precision == 5 / 9  # 5/(5+2+1+1)
    assert result.recall == 5 / (5 + 2 + 1 + 1)

    # Test partial metrics
    result.compute_metrics(partial_or_type=True)
    assert result.precision == 5.5 / 9  # (5+0.5*1)/(5+2+1+1)
    assert result.recall == (5 + 0.5 * 1) / (5 + 2 + 1 + 1)


def test_evaluation_result_zero_cases():
    """Test evaluation metrics with zero values."""
    result = EvaluationResult()
    result.compute_metrics()
    assert result.precision == 0
    assert result.recall == 0
    assert result.f1 == 0
