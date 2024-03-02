from nervaluate import Evaluator


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
