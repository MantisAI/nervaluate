#!/usr/bin/env python3
# coding: utf-8

def CONLL_to_spans(doc, ignored_labels=["O"]):

    out = []

    # Split the CONLL doc on newlines

    doc = doc.splitlines()

    for i, token in enumerate(doc):

        # Convert current token to prodigy format

        span = list_to_prodigy(token, i)

        # If out exists (i.e. this is not the first token) and the current
        # token is not labelled O, and it matches the same label as the 
        # previous token, then merge it with the previous token...

        if out and span["label"] not in ignored_labels and out[-1]["label"] == span["label"]:
            span = merge_spans([span, out[-1]])

        # overwrite the last span in the list out.

            out[-1] = span

        # Otherwise just append the span to the list.

        else:
            out.append(span)

    return out


def list_to_prodigy(tokens_str, i):

    tokens = tokens_str.split("\t")

    return {"label": tokens[1], "start": i, "end": i}

def test_list_to_prodigy():

    before = (
        "Davos\tPERSON"
    )

    after = {"label": "PERSON", "start": 7, "end": 7}

    out = list_to_prodigy(before, 7)

    assert out == after


def merge_spans(spans):

    # Sort spans by token_start to ensure merging in order

    spans = sorted(spans, key=lambda k: k['start'])

    out = spans[0]
    out["end"] = spans[-1]["end"]

    return(out)

def test_merge_spans():

    before = [
        {'label': 'PERSON', 'start': 1, 'end': 1},
        {'label': 'PERSON', 'start': 2, 'end': 2},
    ]

    after = {'label': 'PERSON', 'start': 1, 'end': 2}

    out = merge_spans(before)

    assert out == after


def test_CONLL_to_spans_single_tokens():

    before = (
        ",\tO\n"
        "Davos\tPERSON\n"
        "2018\tO\n"
        ":\tO\n"
        "Soros\tPERSON\n"
        "accuses\tO\n"
        "Trump\tPERSON\n"
        "of\tO\n"
        "wanting\tO\n"
        "a\tO\n"
        "`\tO\n"
        "mafia\tO\n"
        "state\tO\n"
        "'\tO\n"
        "and\tO\n"
        "blasts\tO\n"
        "social\tO\n"
        "media\tO\n"
        ".\tO\n"
    )

    after = [
        {'label': 'O', 'start': 0, 'end': 0},
        {'label': 'PERSON', 'start': 1, 'end': 1},
        {'label': 'O', 'start': 2, 'end': 2},
        {'label': 'O', 'start': 3, 'end': 3},
        {'label': 'PERSON', 'start': 4, 'end': 4},
        {'label': 'O', 'start': 5, 'end': 5},
        {'label': 'PERSON', 'start': 6, 'end': 6},
        {'label': 'O', 'start': 7, 'end': 7},
        {'label': 'O', 'start': 8, 'end': 8},
        {'label': 'O', 'start': 9, 'end': 9},
        {'label': 'O', 'start': 10, 'end': 10},
        {'label': 'O', 'start': 11, 'end': 11},
        {'label': 'O', 'start': 12, 'end': 12},
        {'label': 'O', 'start': 13, 'end': 13},
        {'label': 'O', 'start': 14, 'end': 14},
        {'label': 'O', 'start': 15, 'end': 15},
        {'label': 'O', 'start': 16, 'end': 16},
        {'label': 'O', 'start': 17, 'end': 17},
        {'label': 'O', 'start': 18, 'end': 18},
    ]

    out = list(CONLL_to_spans(before))

    assert out == after


def test_CONLL_to_spans_multiple_tokens():

    before = (
        "Mr\tPERSON\n"
        "Johnson\tPERSON\n"
        "’\tO\n"
        "s\tO\n"
        "acolytes\tO\n"
        "compare\tO\n"
        "their\tO\n"
        "leader\tO\n"
        "to\tO\n"
        "Winston\tPERSON\n"
        "Churchill\tPERSON\n"
        ",\tO\n"
        "who\tO\n"
        "also\tO\n"
        "once\tO\n"
        "helped\tO\n"
        "Britain\tGPE\n"
        "out\tO\n"
        "of\tO\n"
        "a\tO\n"
        "pickle\tO\n"
        "in\tO\n"
        "its\tO\n"
        "relations\tO\n"
        "with\tO\n"
        "Europe\tGPE\n"
        ".\tO\n"
    )


    after = [
        {'label': 'PERSON', 'start': 0, 'end': 1},
        {'label': 'O', 'start': 2, 'end': 2},
        {'label': 'O', 'start': 3, 'end': 3},
        {'label': 'O', 'start': 4, 'end': 4},
        {'label': 'O', 'start': 5, 'end': 5},
        {'label': 'O', 'start': 6, 'end': 6},
        {'label': 'O', 'start': 7, 'end': 7},
        {'label': 'O', 'start': 8, 'end': 8},
        {'label': 'PERSON', 'start': 9, 'end': 10},
        {'label': 'O', 'start': 11, 'end': 11},
        {'label': 'O', 'start': 12, 'end': 12},
        {'label': 'O', 'start': 13, 'end': 13},
        {'label': 'O', 'start': 14, 'end': 14},
        {'label': 'O', 'start': 15, 'end': 15},
        {'label': 'GPE', 'start': 16, 'end': 16},
        {'label': 'O', 'start': 17, 'end': 17},
        {'label': 'O', 'start': 18, 'end': 18},
        {'label': 'O', 'start': 19, 'end': 19},
        {'label': 'O', 'start': 20, 'end': 20},
        {'label': 'O', 'start': 21, 'end': 21},
        {'label': 'O', 'start': 22, 'end': 22},
        {'label': 'O', 'start': 23, 'end': 23},
        {'label': 'O', 'start': 24, 'end': 24},
        {'label': 'GPE', 'start': 25, 'end': 25},
        {'label': 'O', 'start': 26, 'end': 26},
    ]


    out = list(CONLL_to_spans(before))

    assert out == after

test_list_to_prodigy()
test_merge_spans()
test_CONLL_to_spans_single_tokens()
test_CONLL_to_spans_multiple_tokens()
