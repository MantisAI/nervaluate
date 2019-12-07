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
    Creates a list of dicts containing, storing the entity type and the
    start and end offsets of the entity.

    :param tokens: a list of tags
    :return: a list of Entity named-tuples

    Examples:
    >>> collect_named_entities(['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'I-PER'])
    [
        {'type': 'LOC', 'start': 1, 'end': 3},
        {'type': 'PER', 'start': 4, 'end': 6}
    ]
    """

    named_entities = []
    start_offset = None
    end_offset = None
    ent_type = None

    # Case 1: Entity ends, space begins
    # Case 2: Entity begins from space
    # Case 3: One entity ends, and another immediately begins

    for offset, token_tag in enumerate(tokens):
        # Walk through the tokens

        if token_tag == "O":
            # Case 1: Entity ends, space begins
            # When an 'O' (outside) is hit, check to see whether an entity
            # immediately preceded it. If so, append a new entity, subtracting
            # one from the current token number to give the end of the previous
            # token.

            if ent_type is not None and start_offset is not None:
                end_offset = offset - 1
                named_entities.append(
                    {"label": ent_type, "start": start_offset, "end": end_offset}
                )
                # Reset the offsets and the entity type
                start_offset = None
                end_offset = None
                ent_type = None

        elif ent_type is None:
            # If just the entity type is missing, then cut off the B, I, E from
            # the entity type and set this as the entity type.
            ent_type = token_tag[2:]
            start_offset = offset

        elif ent_type != token_tag[2:] or (
            ent_type == token_tag[2:] and token_tag[:1] == "B"
        ):
            # If the current entity type does not match the previous one, or it
            # is the start of a new entity (i.e. B-...), then append the
            # previous entity to the list of spans...

            end_offset = offset - 1
            named_entities.append(
                {"label": ent_type, "start": start_offset, "end": end_offset}
            )

            # ... and start a new entity
            ent_type = token_tag[2:]
            start_offset = offset
            end_offset = None

    # Catches an entity that goes up until the last token

    if ent_type is not None and start_offset is not None and end_offset is None:
        named_entities.append(
            {"label": ent_type, "start": start_offset, "end": len(tokens) - 1}
        )

    return named_entities


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
