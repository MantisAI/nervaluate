#!/usr/bin/env python3
# coding: utf-8

import logging
from copy import deepcopy

from .utils import conll_to_spans, find_overlap, list_to_spans

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
)

class Evaluator():

    def __init__(self, true, pred, tags, loader=None):
        """
        """

        self.true = true
        self.pred = pred
        self.tags = tags
        self.list = list

        # Setup dict into which metrics will be stored.

        self.metrics_results = {
            'correct': 0,
            'incorrect': 0,
            'partial': 0,
            'missed': 0,
            'spurious': 0,
            'possible': 0,
            'actual': 0,
            'precision': 0,
            'recall': 0,
            'f1': 0,
        }

        # Copy results dict to cover the four schemes.

        self.results = {
            'strict': deepcopy(self.metrics_results),
            'ent_type': deepcopy(self.metrics_results),
            'partial':deepcopy(self.metrics_results),
            'exact':deepcopy(self.metrics_results),
            }

        # Create an accumulator to store results

        self.evaluation_agg_entities_type = {e: deepcopy(self.results) for e in tags}

        self.loaders = {
            "list": list_to_spans,
            "conll": conll_to_spans,
        }

        self.loader = loader


    def evaluate(self):

        logging.debug(
            "Imported %s predictions for %s true examples",
            len(self.pred), len(self.true)
        )

        if self.loader:
            loader = self.loaders[self.loader]

            self.pred = loader(self.pred)
            self.true = loader(self.true)

            # Check that something got loaded

            len_pred = len([pred for pred in self.pred if pred])
            len_true = len([true for true in self.true if true])

        if len(self.true) != len(self.pred):
            raise ValueError("Number of predicted documents does not equal true")

        for true_ents, pred_ents in zip(self.true, self.pred):


            # Compute results for one message

            tmp_results, tmp_agg_results = compute_metrics(
                true_ents, pred_ents, self.tags
            )

            # Cycle through each result and accumulate

            # TODO: Combine these loops below:

            for eval_schema in self.results:

                for metric in self.results[eval_schema]:

                    self.results[eval_schema][metric] += tmp_results[eval_schema][metric]

            # Calculate global precision and recall

            self.results = compute_precision_recall_wrapper(self.results)

            # Aggregate results by entity type

            for label in self.tags:

                for eval_schema in tmp_agg_results[label]:

                    for metric in tmp_agg_results[label][eval_schema]:

                        self.evaluation_agg_entities_type[label][eval_schema][metric] += tmp_agg_results[label][eval_schema][metric]

                # Calculate precision recall at the individual entity level

                self.evaluation_agg_entities_type[label] = compute_precision_recall_wrapper(self.evaluation_agg_entities_type[label])

        return self.results, self.evaluation_agg_entities_type


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


def compute_metrics(true_named_entities, pred_named_entities, tags):
    """
    Compute metrics on the collected true and predicted named entities

    :true_name_entitites: Collected true named entities output by collect_named_entities
    :pred_name_entitites:  Collected predicted named entities output by collect_named_entities
    :tags: List of tags to be used
    """


    eval_metrics = {
        'correct': 0,
        'incorrect': 0,
        'partial': 0,
        'missed': 0,
        'spurious': 0,
        'precision': 0,
        'recall': 0,
        'f1': 0
    }

    # overall results

    evaluation = {
        'strict': deepcopy(eval_metrics),
        'ent_type': deepcopy(eval_metrics),
        'partial': deepcopy(eval_metrics),
        'exact': deepcopy(eval_metrics)
    }

    # results by entity type

    evaluation_agg_entities_type = {e: deepcopy(evaluation) for e in tags}

    # keep track of entities that overlapped

    true_which_overlapped_with_pred = []

    # Subset into only the tags that we are interested in.
    # NOTE: we remove the tags we don't want from both the predicted and the
    # true entities. This covers the two cases where mismatches can occur:
    #
    # 1) Where the model predicts a tag that is not present in the true data
    # 2) Where there is a tag in the true data that the model is not capable of
    # predicting.

    # Strip the spans down to just start, end, label. Note that failing
    # to do this results in a bug. The exact cause is not clear.

    true_named_entities = [clean_entities(ent) for ent in true_named_entities if ent["label"] in tags]
    pred_named_entities = [clean_entities(ent) for ent in pred_named_entities if ent["label"] in tags]

    # go through each predicted named-entity

    for pred in pred_named_entities:
        found_overlap = False

        # Check each of the potential scenarios in turn. See
        # http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/
        # for scenario explanation.

        # Scenario I: Exact match between true and pred

        if pred in true_named_entities:
            true_which_overlapped_with_pred.append(pred)
            evaluation['strict']['correct'] += 1
            evaluation['ent_type']['correct'] += 1
            evaluation['exact']['correct'] += 1
            evaluation['partial']['correct'] += 1

            # for the agg. by label results
            evaluation_agg_entities_type[pred["label"]]['strict']['correct'] += 1
            evaluation_agg_entities_type[pred["label"]]['ent_type']['correct'] += 1
            evaluation_agg_entities_type[pred["label"]]['exact']['correct'] += 1
            evaluation_agg_entities_type[pred["label"]]['partial']['correct'] += 1

        else:

            # check for overlaps with any of the true entities

            for true in true_named_entities:

                pred_range = range(pred["start"], pred["end"])
                true_range = range(true["start"], true["end"])

                # Scenario IV: Offsets match, but entity type is wrong

                if true["start"] == pred["start"] and pred["end"] == true["end"] \
                        and true["label"] != pred["label"]:

                    # overall results
                    evaluation['strict']['incorrect'] += 1
                    evaluation['ent_type']['incorrect'] += 1
                    evaluation['partial']['correct'] += 1
                    evaluation['exact']['correct'] += 1

                    # aggregated by entity type results
                    evaluation_agg_entities_type[true["label"]]['strict']['incorrect'] += 1
                    evaluation_agg_entities_type[true["label"]]['ent_type']['incorrect'] += 1
                    evaluation_agg_entities_type[true["label"]]['partial']['correct'] += 1
                    evaluation_agg_entities_type[true["label"]]['exact']['correct'] += 1

                    true_which_overlapped_with_pred.append(true)
                    found_overlap = True

                    break

                # check for an overlap i.e. not exact boundary match, with true entities

                elif find_overlap(true_range, pred_range):

                    true_which_overlapped_with_pred.append(true)

                    # Scenario V: There is an overlap (but offsets do not match
                    # exactly), and the entity type is the same.
                    # 2.1 overlaps with the same entity type

                    if pred["label"] == true["label"]:

                        # overall results
                        evaluation['strict']['incorrect'] += 1
                        evaluation['ent_type']['correct'] += 1
                        evaluation['partial']['partial'] += 1
                        evaluation['exact']['incorrect'] += 1

                        # aggregated by entity type results
                        evaluation_agg_entities_type[true["label"]]['strict']['incorrect'] += 1
                        evaluation_agg_entities_type[true["label"]]['ent_type']['correct'] += 1
                        evaluation_agg_entities_type[true["label"]]['partial']['partial'] += 1
                        evaluation_agg_entities_type[true["label"]]['exact']['incorrect'] += 1

                        found_overlap = True

                        break

                    # Scenario VI: Entities overlap, but the entity type is
                    # different.

                    else:
                        # overall results
                        evaluation['strict']['incorrect'] += 1
                        evaluation['ent_type']['incorrect'] += 1
                        evaluation['partial']['partial'] += 1
                        evaluation['exact']['incorrect'] += 1

                        # aggregated by entity type results
                        # Results against the true entity

                        evaluation_agg_entities_type[true["label"]]['strict']['incorrect'] += 1
                        evaluation_agg_entities_type[true["label"]]['partial']['partial'] += 1
                        evaluation_agg_entities_type[true["label"]]['ent_type']['incorrect'] += 1
                        evaluation_agg_entities_type[true["label"]]['exact']['incorrect'] += 1

                        # Results against the predicted entity

                        # evaluation_agg_entities_type[pred["label"]]['strict']['spurious'] += 1

                        found_overlap = True

                        break

            # Scenario II: Entities are spurious (i.e., over-generated).

            if not found_overlap:

                # Overall results

                evaluation['strict']['spurious'] += 1
                evaluation['ent_type']['spurious'] += 1
                evaluation['partial']['spurious'] += 1
                evaluation['exact']['spurious'] += 1

                # Aggregated by entity type results

                # NOTE: when pred["label"] is not found in tags
                # or when it simply does not appear in the test set, then it is
                # spurious, but it is not clear where to assign it at the tag
                # level. In this case, it is applied to all target_tags
                # found in this example. This will mean that the sum of the
                # evaluation_agg_entities will not equal evaluation.

                for true in tags:

                    evaluation_agg_entities_type[true]['strict']['spurious'] += 1
                    evaluation_agg_entities_type[true]['ent_type']['spurious'] += 1
                    evaluation_agg_entities_type[true]['partial']['spurious'] += 1
                    evaluation_agg_entities_type[true]['exact']['spurious'] += 1

    # Scenario III: Entity was missed entirely.

    for true in true_named_entities:
        if true in true_which_overlapped_with_pred:
            continue
        else:
            # overall results
            evaluation['strict']['missed'] += 1
            evaluation['ent_type']['missed'] += 1
            evaluation['partial']['missed'] += 1
            evaluation['exact']['missed'] += 1

            # for the agg. by label
            evaluation_agg_entities_type[true["label"]]['strict']['missed'] += 1
            evaluation_agg_entities_type[true["label"]]['ent_type']['missed'] += 1
            evaluation_agg_entities_type[true["label"]]['partial']['missed'] += 1
            evaluation_agg_entities_type[true["label"]]['exact']['missed'] += 1

    # Compute 'possible', 'actual' according to SemEval-2013 Task 9.1 on the
    # overall results, and use these to calculate precision and recall.

    for eval_type in evaluation:
        evaluation[eval_type] = compute_actual_possible(evaluation[eval_type])

    # Compute 'possible', 'actual', and precision and recall on entity level
    # results. Start by cycling through the accumulated results.

    for entity_type, entity_level in evaluation_agg_entities_type.items():

        # Cycle through the evaluation types for each dict containing entity
        # level results.

        for eval_type in entity_level:

            evaluation_agg_entities_type[entity_type][eval_type] = compute_actual_possible(
                entity_level[eval_type]
            )

    return evaluation, evaluation_agg_entities_type

def compute_actual_possible(results):
    """
    Takes a result dict that has been output by compute metrics.
    Returns the results dict with actual, possible populated.

    When the results dicts is from partial or ent_type metrics, then
    partial_or_type=True to ensure the right calculation is used for
    calculating precision and recall.
    """

    correct = results['correct']
    incorrect = results['incorrect']
    partial = results['partial']
    missed = results['missed']
    spurious = results['spurious']

    # Possible: number annotations in the gold-standard which contribute to the
    # final score

    possible = correct + incorrect + partial + missed

    # Actual: number of annotations produced by the NER system

    actual = correct + incorrect + partial + spurious

    results["actual"] = actual
    results["possible"] = possible

    return results


def compute_precision_recall(results, partial_or_type=False):
    """
    Takes a result dict that has been output by compute metrics.
    Returns the results dict with precison and recall populated.

    When the results dicts is from partial or ent_type metrics, then
    partial_or_type=True to ensure the right calculation is used for
    calculating precision and recall.
    """

    actual = results["actual"]
    possible = results["possible"]
    partial = results['partial']
    correct = results['correct']

    if partial_or_type:
        precision = (correct + 0.5 * partial) / actual if actual > 0 else 0
        recall = (correct + 0.5 * partial) / possible if possible > 0 else 0

    else:
        precision = correct / actual if actual > 0 else 0
        recall = correct / possible if possible > 0 else 0

    results["precision"] = precision
    results["recall"] = recall
    results["f1"] = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return results


def compute_precision_recall_wrapper(results):
    """
    Wraps the compute_precision_recall function and runs on a dict of results
    """

    results_a = {key: compute_precision_recall(value, True) for key, value in results.items() if
                 key in ['partial', 'ent_type']}
    results_b = {key: compute_precision_recall(value) for key, value in results.items() if
                 key in ['strict', 'exact']}

    results = {**results_a, **results_b}

    return results


def clean_entities(ent):
    """
    Returns just the useufl keys if additional keys are present in the entity
    dict.

    This may happen if passing a list of spans directly from prodigy, which
    typically may include "token_start" and "token_end".
    """
    return {"start": ent["start"], "end": ent["end"], "label": ent["label"]}
