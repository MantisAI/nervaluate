from nervaluate import Evaluator
import pytest
from nervaluate.entities import Entity
from nervaluate.loaders import ConllLoader, ListLoader, DictLoader


def test_loaders_produce_the_same_results():
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

    evaluator_list = Evaluator(true_list, pred_list, tags=["PER", "ORG", "MISC"], loader="list")

    evaluator_conll = Evaluator(true_conll, pred_conll, tags=["PER", "ORG", "MISC"], loader="conll")

    evaluator_prod = Evaluator(true_prod, pred_prod, tags=["PER", "ORG", "MISC"])

    _, _, _, _ = evaluator_list.evaluate()
    _, _, _, _ = evaluator_prod.evaluate()
    _, _, _, _ = evaluator_conll.evaluate()

    assert evaluator_prod.pred == evaluator_list.pred == evaluator_conll.pred
    assert evaluator_prod.true == evaluator_list.true == evaluator_conll.true


@pytest.fixture
def conll_data():
    return """PER\t0\t0
ORG\t2\t3
LOC\t5\t5

PER\t0\t0
ORG\t2\t2"""


@pytest.fixture
def list_data():
    return [["PER", "O", "ORG", "O", "LOC"], ["PER", "O", "ORG"]]


@pytest.fixture
def dict_data():
    return [
        [
            {"label": "PER", "start": 0, "end": 0},
            {"label": "ORG", "start": 2, "end": 3},
            {"label": "LOC", "start": 5, "end": 5},
        ],
        [{"label": "PER", "start": 0, "end": 0}, {"label": "ORG", "start": 2, "end": 2}],
    ]


def test_conll_loader(conll_data):
    """Test CoNLL format loader."""
    loader = ConllLoader()
    entities = loader.load(conll_data)

    assert len(entities) == 2  # Two documents
    assert len(entities[0]) == 3  # First document has 3 entities
    assert len(entities[1]) == 2  # Second document has 2 entities

    # Check first entity
    assert entities[0][0].label == "PER"
    assert entities[0][0].start == 0
    assert entities[0][0].end == 0


def test_list_loader(list_data):
    """Test list format loader."""
    loader = ListLoader()
    entities = loader.load(list_data)

    assert len(entities) == 2  # Two documents
    assert len(entities[0]) == 3  # First document has 3 entities
    assert len(entities[1]) == 2  # Second document has 2 entities

    # Check first entity
    assert entities[0][0].label == "PER"
    assert entities[0][0].start == 0
    assert entities[0][0].end == 0


def test_dict_loader(dict_data):
    """Test dictionary format loader."""
    loader = DictLoader()
    entities = loader.load(dict_data)

    assert len(entities) == 2  # Two documents
    assert len(entities[0]) == 3  # First document has 3 entities
    assert len(entities[1]) == 2  # Second document has 2 entities

    # Check first entity
    assert entities[0][0].label == "PER"
    assert entities[0][0].start == 0
    assert entities[0][0].end == 0


def test_loader_with_empty_input():
    """Test loaders with empty input."""
    loaders = [ConllLoader(), ListLoader(), DictLoader()]

    for loader in loaders:
        entities = loader.load([])
        assert len(entities) == 0


def test_loader_with_invalid_data():
    """Test loaders with invalid data."""
    with pytest.raises(Exception):
        ConllLoader().load("invalid\tdata")

    with pytest.raises(Exception):
        ListLoader().load([["invalid"]])

    with pytest.raises(Exception):
        DictLoader().load([[{"invalid": "data"}]])
