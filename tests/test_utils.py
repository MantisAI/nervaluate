#!/usr/bin/env python3
# coding: utf-8

import pytest
from nervaluate import (collect_named_entities, conll_to_spans, find_overlap,
                        split_list)


def test_split_list():

    before = ["aa", "bb", "cc", "", "dd", "ee", "ff"]

    expected = [
        ["aa", "bb", "cc"],
        ["dd", "ee", "ff"]
    ]

    out = split_list(before)

    assert expected == out

def test_conll_to_spans():

    before = (
        ",\tO\n"
        "Davos\tB-PER\n"
        "2018\tO\n"
        ":\tO\n"
        "Soros\tB-PER\n"
        "accuses\tO\n"
        "Trump\tB-PER\n"
        "of\tO\n"
        "wanting\tO\n"
        "\n"
        "foo\tO\n"
    )

    after = [
        [
            {'label': 'PER', 'start': 1, 'end': 1},
            {'label': 'PER', 'start': 4, 'end': 4},
            {'label': 'PER', 'start': 6, 'end': 6},
        ],
        []
    ]

    out = conll_to_spans(before)

    assert after == out

def test_collect_named_entities_same_type_in_sequence():
    tags = ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O']
    result = collect_named_entities(tags)
    expected = [{"label": "LOC", "start": 1, "end": 2},
                {"label": "LOC", "start": 3, "end": 4}]
    assert result == expected

def test_collect_named_entities_sequence_has_only_one_entity():
    tags = ['B-LOC', 'I-LOC']
    result = collect_named_entities(tags)
    expected = [{"label": "LOC", "start": 0, "end": 1}]
    assert result == expected


def test_collect_named_entities_entity_goes_until_last_token():
    tags = ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC']
    result = collect_named_entities(tags)
    expected = [{"label": "LOC", "start": 1, "end": 2},
                {"label": "LOC", "start": 3, "end": 4}]
    assert result == expected


def test_collect_named_entities_no_entity():
    tags = ['O', 'O', 'O', 'O', 'O']
    result = collect_named_entities(tags)
    expected = []
    assert result == expected

def test_find_overlap_no_overlap():

    pred_entity = {"label":"LOC", "start": 1,  "end": 10}
    true_entity = {"label":"LOC", "start": 11, "end": 20}

    pred_range = range(pred_entity["start"], pred_entity["end"])
    true_range = range(true_entity["start"], true_entity["end"])

    pred_set = set(pred_range)
    true_set = set(true_range)

    intersect = find_overlap(pred_set, true_set)

    assert not intersect


def test_find_overlap_total_overlap():

    pred_entity = {"label":"LOC", "start": 10, "end": 22}
    true_entity = {"label":"LOC", "start": 11, "end": 20}

    pred_range = range(pred_entity["start"], pred_entity["end"])
    true_range = range(true_entity["start"], true_entity["end"])

    pred_set = set(pred_range)
    true_set = set(true_range)

    intersect = find_overlap(pred_set, true_set)

    assert intersect


def test_find_overlap_start_overlap():

    pred_entity = {"label":"LOC", "start": 5, "end": 12}
    true_entity = {"label":"LOC", "start": 11, "end": 20}

    pred_range = range(pred_entity["start"], pred_entity["end"])
    true_range = range(true_entity["start"], true_entity["end"])

    pred_set = set(pred_range)
    true_set = set(true_range)

    intersect = find_overlap(pred_set, true_set)

    assert intersect


def test_find_overlap_end_overlap():

    pred_entity = {"label":"LOC", "start": 15, "end":25}
    true_entity = {"label":"LOC", "start": 11, "end":20}

    pred_range = range(pred_entity["start"], pred_entity["end"])
    true_range = range(true_entity["start"], true_entity["end"])

    pred_set = set(pred_range)
    true_set = set(true_range)

    intersect = find_overlap(pred_set, true_set)

    assert intersect
