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
    Creates a list of dicts containing,the entity type and the start and end
    offsets of the entity.

    :param tokens: a list of tags
    :return: a list of Entity named-tuples

    Cases this function needs to handle:

    Case 1: Entity ends, space begins.
    Case 2: Entity begins after space.
    Case 3: Entity ends and another immediately begins.
    Case 4: Entity ends at end of list.
    Case 5: Entity begins at start of list.

    When the start_offset is None, it means that we have not yet found an
    entity. When the start_offset is not None, it means that we are in the
    middle of an entity.

    Examples:

    For the sequence ['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'I-PER']:

    * We start with 'O, but the start_offset is None and the entity_type is
        None, meaning we have not yet found an entity, we do nothing.
    * We start with start_offset = None, and we encounter a 'B-LOC' tag. We
        set start_offset to 1, and we set the entity type to 'LOC'.
    * We encounter an 'I-LOC' tag and we continue to the next token, without
        doing anything.
    * We encounter an 'O' tag, so we know that the first entity ended at the
        previous token, so we set end_offset to the current offset minus one,
        and we append the entity to the list of entities.
    * We encounter a 'B-PER' tag, and we set start_offset to the current offset
        and the entity type to 'PER', and continue.
    * We encounter an 'I-PER' tag which is the end of the list, so we set the
        end_offset to be 1 - the length of the list, and we append the entity
        to the list of entities.

    | token | offset | start_offset | end_offset | entity_type |
    |-------|--------|--------------|------------|-------------|
    | O     | 0      | None         | None       | None        |
    | B-LOC | 1      | 0            | None       | LOC         |
    | I-LOC | 2      | 0            | 2          | LOC         |
    | O     | 3      | None         | None       | None        |
    | B-PER | 4      | 4            | None       | PER         |
    | I-PER | 5      | 4            | 5          | PER         |

    >>> collect_named_entities(['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'I-PER'])
    [
        {'type': 'LOC', 'start': 1, 'end': 2},
        {'type': 'PER', 'start': 4, 'end': 5}
    ]

    """

    named_entities = []
    start_offset = None
    end_offset = None
    ent_type = None

    for offset, token_tag in enumerate(tokens):

        # Walk through the tokens

        if token_tag == "O":

            """
            When an 'O' (outside) is hit, check to see whether an entity
            immediately preceded it. If so, append a new entity, subtracting
            one from the current token number to give the end of the previous
            token.

            >>> collect_named_entities(['B-LOC', 'I-LOC', 'O'])
            [
                {'type': 'LOC', 'start': 0, 'end': 1}
            ]
            """

            if ent_type is not None and start_offset is not None:
                end_offset = offset - 1
                named_entities.append(
                    {"label": ent_type, "start": start_offset, "end": end_offset}
                )

                # Reset the offsets and the entity type

                start_offset = None
                end_offset = None
                ent_type = None

        elif len(tokens) == 1 and token_tag != "O":

            """
            Deals with the case when there is only one token in the sequence,
            and it is an entity.

            If we are looking at a token from an entity, and we have not yet
            found the start of the entity, then we have found the start of the
            entity.

            >>> collect_named_entities(['B-LOC'])
            [{'type': 'LOC', 'start': 0, 'end': 0}]

            """

            ent_type = token_tag[2:]
            start_offset = 0
            end_offset = 0
            named_entities.append(
                {"label": ent_type, "start": start_offset, "end": end_offset}
            )

        elif ent_type is None:

            """
            If we are starting an entity, or in the the middle of an entity,
            and so just the entity type is missing, so we cut off the B, I, E
            from the token tag and set this as the entity type.
            """

            ent_type = token_tag[2:]
            start_offset = offset

        elif ent_type != token_tag[2:] or (
            ent_type == token_tag[2:] and token_tag[:1] == "B"
        ):
            """
            If the current entity type does not match the previous one, or it
            is the start of a new entity (i.e. B-...), then append the
            previous entity to the list of entities, then start a new entity.

            >>> collect_named_entities(['B-LOC', 'I-LOC', 'B-PER', 'O'])
            [
                {'type': 'LOC', 'start': 0, 'end': 1},
                {'type': 'PER', 'start': 2, 'end': 2}
            ]
            """

            end_offset = offset - 1
            named_entities.append(
                {"label": ent_type, "start": start_offset, "end": end_offset}
            )

            # Start a new entity

            ent_type = token_tag[2:]
            start_offset = offset
            end_offset = None

    """
    If an entity goes up until the last token, then the end offset will not
    have been set. This catches that case by subtracting one from the length
    of the tokens list, and settings the end offset to that value.

    >>> collect_named_entities(['O', 'B-LOC', 'I-LOC', 'I-LOC'])
    [
        {'type': 'LOC', 'start': 1, 'end': 3}
    ]
    """

    if (
        ent_type is not None
        and start_offset is not None
        and end_offset is None
        and offset == len(tokens) - 1
    ):
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
