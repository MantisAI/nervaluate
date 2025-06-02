import pytest

from nervaluate.loaders import ConllLoader, ListLoader, DictLoader


def test_conll_loader():
    """Test CoNLL format loader."""
    true_conll = (
        "word\tO\nword\tO\nword\tO\nword\tO\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-ORG\nword\tI-ORG\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-MISC\nword\tI-MISC\nword\tO\nword\tO\n\n"
        "word\tB-MISC\nword\tI-MISC\nword\tI-MISC\nword\tI-MISC\nword\tI-MISC\nword\tI-MISC\n"
    )

    pred_conll = (
        "word\tO\nword\tO\nword\tB-PER\nword\tI-PER\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-ORG\nword\tI-ORG\nword\tO\nword\tO\n\n"
        "word\tO\nword\tO\nword\tB-MISC\nword\tI-MISC\nword\tO\nword\tO\n\n"
        "word\tB-MISC\nword\tI-MISC\nword\tI-MISC\nword\tI-MISC\nword\tI-MISC\nword\tI-MISC\n"
    )

    loader = ConllLoader()
    true_entities = loader.load(true_conll)
    pred_entities = loader.load(pred_conll)

    # Test true entities
    assert len(true_entities) == 4  # Four documents
    assert len(true_entities[0]) == 0  # First document has no entities (all O tags)
    assert len(true_entities[1]) == 1  # Second document has 1 entity (ORG)
    assert len(true_entities[2]) == 1  # Third document has 1 entity (MISC)
    assert len(true_entities[3]) == 1  # Fourth document has 1 entity (MISC)

    # Check first entity in second document
    assert true_entities[1][0].label == "ORG"
    assert true_entities[1][0].start == 2
    assert true_entities[1][0].end == 3

    # Test pred entities
    assert len(pred_entities) == 4  # Four documents
    assert len(pred_entities[0]) == 1  # First document has 1 entity (PER)
    assert len(pred_entities[1]) == 1  # Second document has 1 entity (ORG)
    assert len(pred_entities[2]) == 1  # Third document has 1 entity (MISC)
    assert len(pred_entities[3]) == 1  # Fourth document has 1 entity (MISC)

    # Check first entity in first document
    assert pred_entities[0][0].label == "PER"
    assert pred_entities[0][0].start == 2
    assert pred_entities[0][0].end == 3

    # Test empty document handling
    empty_doc = "word\tO\nword\tO\nword\tO\n\n"
    empty_entities = loader.load(empty_doc)
    assert len(empty_entities) == 1  # One document
    assert len(empty_entities[0]) == 0  # Empty list for document with only O tags


def test_list_loader():
    """Test list format loader."""
    true_list = [
        ["O", "O", "O", "O", "O", "O"],
        ["O", "O", "B-ORG", "I-ORG", "O", "O"],
        ["O", "O", "B-MISC", "I-MISC", "O", "O"],
        ["B-MISC", "I-MISC", "I-MISC", "I-MISC", "I-MISC", "I-MISC"],
    ]

    pred_list = [
        ["O", "O", "B-PER", "I-PER", "O", "O"],
        ["O", "O", "B-ORG", "I-ORG", "O", "O"],
        ["O", "O", "B-MISC", "I-MISC", "O", "O"],
        ["B-MISC", "I-MISC", "I-MISC", "I-MISC", "I-MISC", "I-MISC"],
    ]

    loader = ListLoader()
    true_entities = loader.load(true_list)
    pred_entities = loader.load(pred_list)

    # Test true entities
    assert len(true_entities) == 4  # Four documents
    assert len(true_entities[0]) == 0  # First document has no entities (all O tags)
    assert len(true_entities[1]) == 1  # Second document has 1 entity (ORG)
    assert len(true_entities[2]) == 1  # Third document has 1 entity (MISC)
    assert len(true_entities[3]) == 1  # Fourth document has 1 entity (MISC)

    # Check no entities in the first document
    assert len(true_entities[0]) == 0

    # Check first entity in second document
    assert true_entities[1][0].label == "ORG"
    assert true_entities[1][0].start == 2
    assert true_entities[1][0].end == 3

    # Check only entity in the last document
    assert true_entities[3][0].label == "MISC"
    assert true_entities[3][0].start == 0
    assert true_entities[3][0].end == 5

    # Test pred entities
    assert len(pred_entities) == 4  # Four documents
    assert len(pred_entities[0]) == 1  # First document has 1 entity (PER)
    assert len(pred_entities[1]) == 1  # Second document has 1 entity (ORG)
    assert len(pred_entities[2]) == 1  # Third document has 1 entity (MISC)
    assert len(pred_entities[3]) == 1  # Fourth document has 1 entity (MISC)

    # Check first entity in first document
    assert pred_entities[0][0].label == "PER"
    assert pred_entities[0][0].start == 2
    assert pred_entities[0][0].end == 3

    # Test empty document handling
    empty_doc = [["O", "O", "O"]]
    empty_entities = loader.load(empty_doc)
    assert len(empty_entities) == 1  # One document
    assert len(empty_entities[0]) == 0  # Empty list for document with only O tags


def test_dict_loader():
    """Test dictionary format loader."""
    true_prod = [
        [],
        [{"label": "ORG", "start": 2, "end": 3}],
        [{"label": "MISC", "start": 2, "end": 3}],
        [{"label": "MISC", "start": 0, "end": 5}],
    ]

    pred_prod = [
        [{"label": "PER", "start": 2, "end": 3}],
        [{"label": "ORG", "start": 2, "end": 3}],
        [{"label": "MISC", "start": 2, "end": 3}],
        [{"label": "MISC", "start": 0, "end": 5}],
    ]

    loader = DictLoader()
    true_entities = loader.load(true_prod)
    pred_entities = loader.load(pred_prod)

    # Test true entities
    assert len(true_entities) == 4  # Four documents
    assert len(true_entities[0]) == 0  # First document has no entities
    assert len(true_entities[1]) == 1  # Second document has 1 entity (ORG)
    assert len(true_entities[2]) == 1  # Third document has 1 entity (MISC)
    assert len(true_entities[3]) == 1  # Fourth document has 1 entity (MISC)

    # Check first entity in second document
    assert true_entities[1][0].label == "ORG"
    assert true_entities[1][0].start == 2
    assert true_entities[1][0].end == 3

    # Check only entity in the last document
    assert true_entities[3][0].label == "MISC"
    assert true_entities[3][0].start == 0
    assert true_entities[3][0].end == 5

    # Test pred entities
    assert len(pred_entities) == 4  # Four documents
    assert len(pred_entities[0]) == 1  # First document has 1 entity (PER)
    assert len(pred_entities[1]) == 1  # Second document has 1 entity (ORG)
    assert len(pred_entities[2]) == 1  # Third document has 1 entity (MISC)
    assert len(pred_entities[3]) == 1  # Fourth document has 1 entity (MISC)

    # Check first entity in first document
    assert pred_entities[0][0].label == "PER"
    assert pred_entities[0][0].start == 2
    assert pred_entities[0][0].end == 3

    # Test empty document handling
    empty_doc = [[]]
    empty_entities = loader.load(empty_doc)
    assert len(empty_entities) == 1  # One document
    assert len(empty_entities[0]) == 0  # Empty list for empty document


def test_loader_with_empty_input():
    """Test loaders with empty input."""
    # Test ConllLoader with empty string
    conll_loader = ConllLoader()
    entities = conll_loader.load("")
    assert len(entities) == 0

    # Test ListLoader with empty list
    list_loader = ListLoader()
    entities = list_loader.load([])
    assert len(entities) == 0

    # Test DictLoader with empty list
    dict_loader = DictLoader()
    entities = dict_loader.load([])
    assert len(entities) == 0


def test_loader_with_invalid_data():
    """Test loaders with invalid data."""
    with pytest.raises(Exception):
        ConllLoader().load("invalid\tdata")

    with pytest.raises(Exception):
        ListLoader().load([["invalid"]])

    with pytest.raises(Exception):
        DictLoader().load([[{"invalid": "data"}]])
