from nervaluate import compute_metrics
from nervaluate import collect_named_entities
from nervaluate import find_overlap
from nervaluate import compute_actual_possible
from nervaluate import compute_precision_recall
from nervaluate import compute_precision_recall_wrapper


def test_collect_named_entities_same_type_in_sequence():
    tags = ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O']
    result = collect_named_entities(tags)
    expected = [{"label": "LOC", "start": 1, "end": 2},
                {"label": "LOC", "start": 3, "end": 4}]
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


def test_compute_metrics_case_1():
    true_named_entities = [
        {"label":"PER", "start": 59, "end": 69},
        {"label":"LOC", "start": 127, "end": 134},
        {"label":"LOC", "start": 164, "end": 174},
        {"label":"LOC", "start": 197, "end": 205},
        {"label":"LOC", "start": 208, "end": 219},
        {"label":"MISC", "start": 230, "end": 240},
    ]

    pred_named_entities = [
        {"label":"PER", "start": 24, "end": 30},
        {"label":"LOC", "start": 124, "end": 134},
        {"label":"PER", "start": 164, "end": 174},
        {"label":"LOC", "start": 197, "end": 205},
        {"label":"LOC", "start": 208, "end": 219},
        {"label":"LOC", "start": 225, "end": 243},
    ]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER', 'LOC', 'MISC']
    )

    results = compute_precision_recall_wrapper(results)

    expected = {'strict': {'correct': 2,
                           'incorrect': 3,
                           'partial': 0,
                           'missed': 1,
                           'spurious': 1,
                           'possible': 6,
                           'actual': 6,
                           'precision': 0.3333333333333333,
                           'recall': 0.3333333333333333},
                'ent_type': {'correct': 3,
                             'incorrect': 2,
                             'partial': 0,
                             'missed': 1,
                             'spurious': 1,
                             'possible': 6,
                             'actual': 6,
                             'precision': 0.5,
                             'recall': 0.5},
                'partial': {'correct': 3,
                            'incorrect': 0,
                            'partial': 2,
                            'missed': 1,
                            'spurious': 1,
                            'possible': 6,
                            'actual': 6,
                            'precision': 0.6666666666666666,
                            'recall': 0.6666666666666666},
                'exact': {'correct': 3,
                          'incorrect': 2,
                          'partial': 0,
                          'missed': 1,
                          'spurious': 1,
                          'possible': 6,
                          'actual': 6,
                          'precision': 0.5,
                          'recall': 0.5}
                }

    assert results == expected


def test_compute_metrics_agg_scenario_3():

    true_named_entities = [{"label": "PER", "start":59, "end":69}]

    pred_named_entities = []

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER']
    )

    expected_agg = {
        'PER': {
            'strict': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 1,
                'spurious': 0,
                'actual': 0,
                'possible': 1,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 1,
                'spurious': 0,
                'actual': 0,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 1,
                'spurious': 0,
                'actual': 0,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 1,
                'spurious': 0,
                'actual': 0,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            }
        }
    }

    assert results_agg['PER']['strict'] == expected_agg['PER']['strict']
    assert results_agg['PER']['ent_type'] == expected_agg['PER']['ent_type']
    assert results_agg['PER']['partial'] == expected_agg['PER']['partial']
    assert results_agg['PER']['exact'] == expected_agg['PER']['exact']


def test_compute_metrics_agg_scenario_2():

    true_named_entities = []

    pred_named_entities = [{"label":"PER", "start":59, "end":69}]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER']
    )

    expected_agg = {
        'PER': {
            'strict': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 1,
                'actual': 1,
                'possible': 0,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 1,
                'actual': 1,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 1,
                'actual': 1,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 1,
                'actual': 1,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            }
        }
    }

    assert results_agg['PER']['strict'] == expected_agg['PER']['strict']
    assert results_agg['PER']['ent_type'] == expected_agg['PER']['ent_type']
    assert results_agg['PER']['partial'] == expected_agg['PER']['partial']
    assert results_agg['PER']['exact'] == expected_agg['PER']['exact']


def test_compute_metrics_agg_scenario_5():

    true_named_entities = [{"label":"PER", "start":59, "end":69}]

    pred_named_entities = [{"label":"PER", "start":57, "end":69}]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER']
    )

    expected_agg = {
        'PER': {
            'strict': {
                'correct': 0,
                'incorrect': 1,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 1,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 0,
                'incorrect': 0,
                'partial': 1,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 0,
                'incorrect': 1,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            }
        }
    }

    assert results_agg['PER']['strict'] == expected_agg['PER']['strict']
    assert results_agg['PER']['ent_type'] == expected_agg['PER']['ent_type']
    assert results_agg['PER']['partial'] == expected_agg['PER']['partial']
    assert results_agg['PER']['exact'] == expected_agg['PER']['exact']


def test_compute_metrics_agg_scenario_4():

    true_named_entities = [{"label":"PER", "start":59, "end":69}]

    pred_named_entities = [{"label":"LOC", "start":59, "end":69}]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER', 'LOC']
    )

    expected_agg = {
        'PER': {
            'strict': {
                'correct': 0,
                'incorrect': 1,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 0,
                'incorrect': 1,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 1,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 1,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            }
        },
        'LOC': {
            'strict': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            }
        }
    }

    assert results_agg['PER']['strict'] == expected_agg['PER']['strict']
    assert results_agg['PER']['ent_type'] == expected_agg['PER']['ent_type']
    assert results_agg['PER']['partial'] == expected_agg['PER']['partial']
    assert results_agg['PER']['exact'] == expected_agg['PER']['exact']

    assert results_agg['LOC'] == expected_agg['LOC']


def test_compute_metrics_agg_scenario_1():

    true_named_entities = [{"label":"PER", "start": 59, "end": 69}]

    pred_named_entities = [{"label":"PER", "start": 59, "end": 69}]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER']
    )

    expected_agg = {
        'PER': {
            'strict': {
                'correct': 1,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 1,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 1,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 1,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            }
        }
    }

    assert results_agg['PER']['strict'] == expected_agg['PER']['strict']
    assert results_agg['PER']['ent_type'] == expected_agg['PER']['ent_type']
    assert results_agg['PER']['partial'] == expected_agg['PER']['partial']
    assert results_agg['PER']['exact'] == expected_agg['PER']['exact']


def test_compute_metrics_agg_scenario_6():

    true_named_entities = [{"label":"PER", "start": 59, "end": 69}]

    pred_named_entities = [{"label":"LOC", "start": 54, "end": 69}]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER', 'LOC']
    )

    expected_agg = {
        'PER': {
            'strict': {
                'correct': 0,
                'incorrect': 1,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 0,
                'incorrect': 1,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 0,
                'incorrect': 0,
                'partial': 1,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 0,
                'incorrect': 1,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 1,
                'possible': 1,
                'precision': 0,
                'recall': 0,
            }
        },
        'LOC': {
            'strict': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
                },
            'ent_type': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            },
            'partial': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            },
            'exact': {
                'correct': 0,
                'incorrect': 0,
                'partial': 0,
                'missed': 0,
                'spurious': 0,
                'actual': 0,
                'possible': 0,
                'precision': 0,
                'recall': 0,
            }
        }
    }

    assert results_agg['PER']['strict'] == expected_agg['PER']['strict']
    assert results_agg['PER']['ent_type'] == expected_agg['PER']['ent_type']
    assert results_agg['PER']['partial'] == expected_agg['PER']['partial']
    assert results_agg['PER']['exact'] == expected_agg['PER']['exact']

    assert results_agg["LOC"] == expected_agg["LOC"]


def test_compute_metrics_extra_tags_in_prediction():

    true_named_entities = [
        {"label":"PER", "start": 50, "end": 52},
        {"label":"ORG", "start": 59, "end": 69},
        {"label":"ORG", "start": 71, "end": 72},
    ]

    pred_named_entities = [
        {"label":"LOC",  "start": 50,  "end": 52},  # Wrong type
        {"label":"ORG",  "start": 59,  "end": 69},  # Correct
        {"label":"MISC", "start": 71, "end": 72}, # Wrong type
    ]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER', 'LOC', 'ORG']
    )

    expected = {
        'strict': {
            'correct': 1,
            'incorrect': 1,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'actual': 2,
            'possible': 3,
            'precision': 0,
            'recall': 0,
        },
        'ent_type': {
            'correct': 1,
            'incorrect': 1,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'actual': 2,
            'possible': 3,
            'precision': 0,
            'recall': 0,
        },
        'partial': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'actual': 2,
            'possible': 3,
            'precision': 0,
            'recall': 0,
        },
        'exact': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 1,
            'spurious': 0,
            'actual': 2,
            'possible': 3,
            'precision': 0,
            'recall': 0,
        }
    }

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']


def test_compute_metrics_extra_tags_in_true():

    true_named_entities = [
        {"label": "PER", "start": 50, "end": 52},
        {"label": "ORG", "start": 59, "end": 69},
        {"label":"MISC", "start": 71, "end": 72},
    ]

    pred_named_entities = [
        {"label":"LOC", "start": 50, "end": 52},  # Wrong type
        {"label":"ORG", "start": 59, "end": 69},  # Correct
        {"label":"ORG", "start": 71, "end": 72},  # Spurious
    ]

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER', 'LOC', 'ORG']
    )

    expected = {
        'strict': {
            'correct': 1,
            'incorrect': 1,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'actual': 3,
            'possible': 2,
            'precision': 0,
            'recall': 0,
            },
        'ent_type': {
            'correct': 1,
            'incorrect': 1,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'actual': 3,
            'possible': 2,
            'precision': 0,
            'recall': 0,
        },
        'partial': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'actual': 3,
            'possible': 2,
            'precision': 0,
            'recall': 0,
        },
        'exact': {
            'correct': 2,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 1,
            'actual': 3,
            'possible': 2,
            'precision': 0,
            'recall': 0,
        }
    }

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']


def test_compute_metrics_no_predictions():

    true_named_entities = [
        {"label": "PER", "start": 50, "end": 52},
        {"label": "ORG", "start": 59, "end": 69},
        {"label":"MISC", "start": 71, "end": 72},
    ]

    pred_named_entities = []

    results, results_agg = compute_metrics(
        true_named_entities, pred_named_entities, ['PER', 'ORG', 'MISC']
    )

    expected = {
        'strict': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 3,
            'spurious': 0,
            'actual': 0,
            'possible': 3,
            'precision': 0,
            'recall': 0,
            },
        'ent_type': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 3,
            'spurious': 0,
            'actual': 0,
            'possible': 3,
            'precision': 0,
            'recall': 0,
        },
        'partial': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 3,
            'spurious': 0,
            'actual': 0,
            'possible': 3,
            'precision': 0,
            'recall': 0,
        },
        'exact': {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 3,
            'spurious': 0,
            'actual': 0,
            'possible': 3,
            'precision': 0,
            'recall': 0,
        }
    }

    assert results['strict'] == expected['strict']
    assert results['ent_type'] == expected['ent_type']
    assert results['partial'] == expected['partial']
    assert results['exact'] == expected['exact']

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

    pred_entity = {"label":"LOC", "start": 5,  "end": 12}
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


def test_compute_actual_possible():

    results = {
        'correct': 6,
        'incorrect': 3,
        'partial': 2,
        'missed': 4,
        'spurious': 2,
        }

    expected = {
        'correct': 6,
        'incorrect': 3,
        'partial': 2,
        'missed': 4,
        'spurious': 2,
        'possible': 15,
        'actual': 13,
    }

    out = compute_actual_possible(results)

    assert out == expected


def test_compute_precision_recall():

    results = {
        'correct': 6,
        'incorrect': 3,
        'partial': 2,
        'missed': 4,
        'spurious': 2,
        'possible': 15,
        'actual': 13,
        }

    expected = {
        'correct': 6,
        'incorrect': 3,
        'partial': 2,
        'missed': 4,
        'spurious': 2,
        'possible': 15,
        'actual': 13,
        'precision': 0.46153846153846156, 
        'recall': 0.4
    }

    out = compute_precision_recall(results)

    assert out == expected

