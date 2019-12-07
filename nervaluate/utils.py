#!/usr/bin/env python3
# coding: utf-8


def split_list(x, split_chars=[""]):

    out = []
    chunk = []

    for i, item in enumerate(x):
        if item not in split_chars:
            chunk.append(item)

            if i + 1 == len(x):
                out.append(chunk)
        else:
            out.append(chunk)
            chunk = []

    return out

def conll_to_spans(doc):

    out = []

    doc = split_list(doc.split("\n"))

    for example in doc:
        labels = []

        for token in example:
            token = token.split("\t")
            label = token[1]
            labels.append(label)
        out.append(labels)

    spans = list_to_spans(out)

    return spans

def list_to_spans(doc):

    spans = [collect_named_entities(tokens) for tokens in doc]

    return spans

def collect_named_entities(tokens):
    """
    Creates a list of Entity named-tuples, storing the entity type and the
    start and end offsets of the entity.

    :param tokens: a list of tags
    :return: a list of Entity named-tuples
    """

    named_entities = []
    start_offset = None
    end_offset = None
    ent_type = None

    for offset, token_tag in enumerate(tokens):

        if token_tag == 'O':
            if ent_type is not None and start_offset is not None:
                end_offset = offset - 1
                named_entities.append({"label": ent_type, "start": start_offset, "end":end_offset})
                start_offset = None
                end_offset = None
                ent_type = None

        elif ent_type is None:
            ent_type = token_tag[2:]
            start_offset = offset

        elif ent_type != token_tag[2:] or (ent_type == token_tag[2:] and token_tag[:1] == 'B'):

            end_offset = offset - 1
            named_entities.append({"label": ent_type, "start": start_offset, "end":end_offset})

            # start of a new entity
            ent_type = token_tag[2:]
            start_offset = offset
            end_offset = None

    # catches an entity that goes up until the last token

    if ent_type and start_offset and end_offset is None:
        named_entities.append({"label": ent_type, "start": start_offset, "end":len(tokens)-1})

    return named_entities


def test_list_to_spans():

    before = [
        ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O'],
        ['O', 'B-GPE', 'I-GPE', 'B-GPE', 'I-GPE', 'O'],
    ]

    expected = [
        [
            {"label": "LOC", "start": 1, "end": 2},
            {"label": "LOC", "start": 3, "end": 4},
        ],
        [
            {"label": "GPE", "start": 1, "end": 2},
            {"label": "GPE", "start": 3, "end": 4},
        ]
    ]

    result = list_to_spans(before)

    assert result == expected

test_list_to_spans()

def find_overlap(true_range, pred_range):
    """Find the overlap between two ranges

    Find the overlap between two ranges. Return the overlapping values if
    present, else return an empty set().

    Examples:

    >>> find_overlap((1, 2), (2, 3))
    2
    >>> find_overlap((1, 2), (3, 4))
    set()
    """

    true_set = set(true_range)
    pred_set = set(pred_range)

    overlaps = true_set.intersection(pred_set)

    return overlaps
