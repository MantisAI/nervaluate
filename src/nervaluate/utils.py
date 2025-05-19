def split_list(token: list[str], split_chars: list[str] | None = None) -> list[list[str]]:
    """
    Split a list into sublists based on a list of split characters.

    If split_chars is None, the list is split on empty strings.

    :param token: The list to split.
    :param split_chars: The characters to split on.

    :returns:
        A list of lists.
    """
    if split_chars is None:
        split_chars = [""]
    out = []
    chunk = []
    for i, item in enumerate(token):
        if item not in split_chars:
            chunk.append(item)
            if i + 1 == len(token):
                out.append(chunk)
        else:
            out.append(chunk)
            chunk = []
    return out


def conll_to_spans(doc: str) -> list[list[dict]]:
    """
    Convert a CoNLL-formatted string to a list of spans.

    :param doc: The CoNLL-formatted string.

    :returns:
        A list of spans.
    """
    out = []
    doc_parts = split_list(doc.split("\n"), split_chars=None)

    for example in doc_parts:
        labels = []
        for token in example:
            token_parts = token.split("\t")
            label = token_parts[1]
            labels.append(label)
        out.append(labels)

    spans = list_to_spans(out)

    return spans


def list_to_spans(doc: list[list[str]]) -> list[list[dict]]:
    """
    Convert a list of tags to a list of spans.

    :param doc: The list of tags.

    :returns:
        A list of spans.
    """
    spans = [collect_named_entities(tokens) for tokens in doc]
    return spans


def collect_named_entities(tokens: list[str]) -> list[dict]:
    """
    Creates a list of Entity named-tuples, storing the entity type and the start and end offsets of the entity.

    :param tokens: a list of tags

    :returns:
        A list of Entity named-tuples.
    """

    named_entities = []
    start_offset = None
    end_offset = None
    ent_type = None

    for offset, token_tag in enumerate(tokens):
        if token_tag == "O":
            if ent_type is not None and start_offset is not None:
                end_offset = offset - 1
                named_entities.append({"label": ent_type, "start": start_offset, "end": end_offset})
                start_offset = None
                end_offset = None
                ent_type = None

        elif ent_type is None:
            ent_type = token_tag[2:]
            start_offset = offset

        elif ent_type != token_tag[2:] or (ent_type == token_tag[2:] and token_tag[:1] == "B"):
            end_offset = offset - 1
            named_entities.append({"label": ent_type, "start": start_offset, "end": end_offset})

            # start of a new entity
            ent_type = token_tag[2:]
            start_offset = offset
            end_offset = None

    # Catches an entity that goes up until the last token
    if ent_type is not None and start_offset is not None and end_offset is None:
        named_entities.append({"label": ent_type, "start": start_offset, "end": len(tokens) - 1})

    return named_entities


def find_overlap(true_range: range, pred_range: range) -> set:
    """
    Find the overlap between two ranges.

    :param true_range: The true range.
    :param pred_range: The predicted range.

    :returns:
        A set of overlapping values.

    Examples:
        >>> find_overlap(range(1, 3), range(2, 4))
        {2}
        >>> find_overlap(range(1, 3), range(3, 5))
        set()
    """

    true_set = set(true_range)
    pred_set = set(pred_range)
    overlaps = true_set.intersection(pred_set)

    return overlaps


def clean_entities(ent: dict) -> dict:
    """
    Returns just the useful keys if additional keys are present in the entity
    dict.

    This may happen if passing a list of spans directly from prodigy, which
    typically may include 'token_start' and 'token_end'.
    """
    return {"start": ent["start"], "end": ent["end"], "label": ent["label"]}
