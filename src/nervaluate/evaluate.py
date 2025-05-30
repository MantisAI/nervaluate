import logging
import warnings
from copy import deepcopy
from typing import Any

import pandas as pd

from .utils import conll_to_spans, find_overlap, list_to_spans, clean_entities

logger = logging.getLogger(__name__)


class Evaluator:  # pylint: disable=too-many-instance-attributes, too-few-public-methods
    """
    Evaluator class for evaluating named entity recognition (NER) models.
    """

    def __init__(
        self,
        true: list[list[str]] | list[str] | list[dict] | str | list[list[dict[str, int | str]]],
        pred: list[list[str]] | list[str] | list[dict] | str | list[list[dict[str, int | str]]],
        tags: list[str],
        loader: str = "default",
    ) -> None:
        """
        Initialize the Evaluator class.

        Args:
            true: List of true named entities.
            pred: List of predicted named entities.
            tags: List of tags to be used.
            loader: Loader to be used.

        Raises:
            ValueError: If the number of predicted documents does not equal the number of true documents.
        """
        self.true = true
        self.pred = pred
        self.tags = tags

        # Setup dict into which metrics will be stored.
        self.metrics_results = {
            "correct": 0,
            "incorrect": 0,
            "partial": 0,
            "missed": 0,
            "spurious": 0,
            "possible": 0,
            "actual": 0,
            "precision": 0,
            "recall": 0,
            "f1": 0,
        }

        # Copy results dict to cover the four schemes.
        self.results = {
            "strict": deepcopy(self.metrics_results),
            "ent_type": deepcopy(self.metrics_results),
            "partial": deepcopy(self.metrics_results),
            "exact": deepcopy(self.metrics_results),
        }

        # Create an accumulator to store results
        self.evaluation_agg_entities_type = {e: deepcopy(self.results) for e in tags}
        self.loaders = {
            "list": list_to_spans,
            "conll": conll_to_spans,
        }

        self.loader = loader

        self.eval_indices: dict[str, list[int]] = {
            "correct_indices": [],
            "incorrect_indices": [],
            "partial_indices": [],
            "missed_indices": [],
            "spurious_indices": [],
        }

        # Create dicts to hold indices for correct/spurious/missing/etc examples
        self.evaluation_indices = {
            "strict": deepcopy(self.eval_indices),
            "ent_type": deepcopy(self.eval_indices),
            "partial": deepcopy(self.eval_indices),
            "exact": deepcopy(self.eval_indices),
        }
        self.evaluation_agg_indices = {e: deepcopy(self.evaluation_indices) for e in tags}

    def evaluate(self) -> tuple[dict, dict, dict, dict]:  # noqa: C901
        warnings.warn(
            "The current evaluation method is deprecated and it will the output change in the next release."
            "The output will change to a dictionary with the following keys: overall, entities, entity_results, "
            "overall_indices, entity_indices.",
            DeprecationWarning,
            stacklevel=2
        )
        logging.debug("Imported %s predictions for %s true examples", len(self.pred), len(self.true))

        if self.loader != "default":
            loader = self.loaders[self.loader]
            self.pred = loader(self.pred)  # type: ignore
            self.true = loader(self.true)  # type: ignore

        if len(self.true) != len(self.pred):
            raise ValueError("Number of predicted documents does not equal true")

        for index, (true_ents, pred_ents) in enumerate(zip(self.true, self.pred, strict=False)):
            # Compute results for one message
            tmp_results, tmp_agg_results, tmp_results_indices, tmp_agg_results_indices = compute_metrics(
                true_ents, pred_ents, self.tags, index
            )

            # Cycle through each result and accumulate
            # TODO: Combine these loops below:
            for eval_schema in self.results:
                for metric in self.results[eval_schema]:
                    self.results[eval_schema][metric] += tmp_results[eval_schema][metric]

                # Accumulate indices for each error type
                for error_type in self.evaluation_indices[eval_schema]:
                    self.evaluation_indices[eval_schema][error_type] += tmp_results_indices[eval_schema][error_type]

            # Calculate global precision and recall
            self.results = compute_precision_recall_wrapper(self.results)

            # Aggregate results by entity type
            for label in self.tags:
                for eval_schema in tmp_agg_results[label]:
                    for metric in tmp_agg_results[label][eval_schema]:
                        self.evaluation_agg_entities_type[label][eval_schema][metric] += tmp_agg_results[label][
                            eval_schema
                        ][metric]

                    # Accumulate indices for each error type per entity type
                    for error_type in self.evaluation_agg_indices[label][eval_schema]:
                        self.evaluation_agg_indices[label][eval_schema][error_type] += tmp_agg_results_indices[label][
                            eval_schema
                        ][error_type]

                # Calculate precision recall at the individual entity level
                self.evaluation_agg_entities_type[label] = compute_precision_recall_wrapper(
                    self.evaluation_agg_entities_type[label]
                )

        return self.results, self.evaluation_agg_entities_type, self.evaluation_indices, self.evaluation_agg_indices

    #  Helper method to flatten a nested dictionary
    def _flatten_dict(self, d: dict[str, Any], parent_key: str = "", sep: str = ".") -> dict[str, Any]:
        """
        Flattens a nested dictionary.

        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): The base key string to prepend to each dictionary key.
            sep (str): The separator to use when combining keys.

        Returns:
            dict: A flattened dictionary.
        """
        items: list[tuple[str, Any]] = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # Modified results_to_dataframe method using the helper method
    def results_to_dataframe(self) -> Any:
        if not self.results:
            raise ValueError("self.results should be defined.")

        if not isinstance(self.results, dict) or not all(isinstance(v, dict) for v in self.results.values()):
            raise ValueError("self.results must be a dictionary of dictionaries.")

        # Flatten the nested results dictionary, including the 'entities' sub-dictionaries
        flattened_results: dict[str, dict[str, Any]] = {}
        for outer_key, inner_dict in self.results.items():
            flattened_inner_dict = self._flatten_dict(inner_dict)
            for inner_key, value in flattened_inner_dict.items():
                if inner_key not in flattened_results:
                    flattened_results[inner_key] = {}
                flattened_results[inner_key][outer_key] = value

        # Convert the flattened results to a pandas DataFrame
        try:
            return pd.DataFrame(flattened_results)
        except Exception as e:
            raise RuntimeError("Error converting flattened results to DataFrame") from e


def compute_metrics(  # type: ignore # noqa: C901
    # pylint: disable=too-many-locals,too-many-branches,too-many-statements,missing-type-doc
    true_named_entities,
    pred_named_entities,
    tags: list[str],
    instance_index: int = 0,
) -> tuple[dict, dict, dict, dict]:
    """
    Compute metrics on the collected true and predicted named entities

    :param true_named_entities:
        collected true named entities output by collect_named_entities

    :param pred_named_entities:
        collected predicted named entities output by collect_named_entities

    :param tags:
        list of tags to be used

    :param instance_index:
        index of the example being evaluated. Used to record indices of correct/missing/spurious/exact/partial
        predictions.
    """

    eval_metrics = {
        "correct": 0,
        "incorrect": 0,
        "partial": 0,
        "missed": 0,
        "spurious": 0,
        "precision": 0,
        "recall": 0,
        "f1": 0,
    }

    # overall results
    evaluation = {
        "strict": deepcopy(eval_metrics),
        "ent_type": deepcopy(eval_metrics),
        "partial": deepcopy(eval_metrics),
        "exact": deepcopy(eval_metrics),
    }

    # results by entity type
    evaluation_agg_entities_type = {e: deepcopy(evaluation) for e in tags}

    eval_ent_indices: dict[str, list[tuple[int, int]]] = {
        "correct_indices": [],
        "incorrect_indices": [],
        "partial_indices": [],
        "missed_indices": [],
        "spurious_indices": [],
    }

    # Create dicts to hold indices for correct/spurious/missing/etc examples
    evaluation_ent_indices = {
        "strict": deepcopy(eval_ent_indices),
        "ent_type": deepcopy(eval_ent_indices),
        "partial": deepcopy(eval_ent_indices),
        "exact": deepcopy(eval_ent_indices),
    }
    evaluation_agg_ent_indices = {e: deepcopy(evaluation_ent_indices) for e in tags}

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

    # Sort the lists to improve the speed of the overlap comparison
    true_named_entities.sort(key=lambda x: x["start"])
    pred_named_entities.sort(key=lambda x: x["end"])

    # go through each predicted named-entity
    for within_instance_index, pred in enumerate(pred_named_entities):
        found_overlap = False

        # Check each of the potential scenarios in turn. See
        # http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/
        # for scenario explanation.

        # Scenario I: Exact match between true and pred
        if pred in true_named_entities:
            true_which_overlapped_with_pred.append(pred)
            evaluation["strict"]["correct"] += 1
            evaluation["ent_type"]["correct"] += 1
            evaluation["exact"]["correct"] += 1
            evaluation["partial"]["correct"] += 1
            evaluation_ent_indices["strict"]["correct_indices"].append((instance_index, within_instance_index))
            evaluation_ent_indices["ent_type"]["correct_indices"].append((instance_index, within_instance_index))
            evaluation_ent_indices["exact"]["correct_indices"].append((instance_index, within_instance_index))
            evaluation_ent_indices["partial"]["correct_indices"].append((instance_index, within_instance_index))

            # for the agg. by label results
            evaluation_agg_entities_type[pred["label"]]["strict"]["correct"] += 1
            evaluation_agg_entities_type[pred["label"]]["ent_type"]["correct"] += 1
            evaluation_agg_entities_type[pred["label"]]["exact"]["correct"] += 1
            evaluation_agg_entities_type[pred["label"]]["partial"]["correct"] += 1
            evaluation_agg_ent_indices[pred["label"]]["strict"]["correct_indices"].append(
                (instance_index, within_instance_index)
            )
            evaluation_agg_ent_indices[pred["label"]]["ent_type"]["correct_indices"].append(
                (instance_index, within_instance_index)
            )
            evaluation_agg_ent_indices[pred["label"]]["exact"]["correct_indices"].append(
                (instance_index, within_instance_index)
            )
            evaluation_agg_ent_indices[pred["label"]]["partial"]["correct_indices"].append(
                (instance_index, within_instance_index)
            )

        else:
            # check for overlaps with any of the true entities
            for true in true_named_entities:
                # Only enter this block if an overlap is possible
                if pred["end"] < true["start"]:
                    break

                # overlapping needs to take into account last token as well
                pred_range = range(pred["start"], pred["end"] + 1)
                true_range = range(true["start"], true["end"] + 1)

                # Scenario IV: Offsets match, but entity type is wrong
                if true["start"] == pred["start"] and pred["end"] == true["end"] and true["label"] != pred["label"]:
                    # overall results
                    evaluation["strict"]["incorrect"] += 1
                    evaluation_ent_indices["strict"]["incorrect_indices"].append(
                        (instance_index, within_instance_index)
                    )
                    evaluation["ent_type"]["incorrect"] += 1
                    evaluation_ent_indices["ent_type"]["incorrect_indices"].append(
                        (instance_index, within_instance_index)
                    )
                    evaluation["partial"]["correct"] += 1
                    evaluation["exact"]["correct"] += 1

                    # aggregated by entity type results
                    evaluation_agg_entities_type[true["label"]]["strict"]["incorrect"] += 1
                    evaluation_agg_ent_indices[true["label"]]["strict"]["incorrect_indices"].append(
                        (instance_index, within_instance_index)
                    )
                    evaluation_agg_entities_type[true["label"]]["ent_type"]["incorrect"] += 1
                    evaluation_agg_ent_indices[true["label"]]["ent_type"]["incorrect_indices"].append(
                        (instance_index, within_instance_index)
                    )
                    evaluation_agg_entities_type[true["label"]]["partial"]["correct"] += 1
                    evaluation_agg_entities_type[true["label"]]["exact"]["correct"] += 1

                    true_which_overlapped_with_pred.append(true)
                    found_overlap = True
                    break

                # check for an overlap i.e. not exact boundary match, with true entities
                # overlaps with true entities must only count once
                if find_overlap(true_range, pred_range) and true not in true_which_overlapped_with_pred:
                    true_which_overlapped_with_pred.append(true)

                    # Scenario V: There is an overlap (but offsets do not match
                    # exactly), and the entity type is the same.
                    # 2.1 overlaps with the same entity type
                    if pred["label"] == true["label"]:
                        # overall results
                        evaluation["strict"]["incorrect"] += 1
                        evaluation_ent_indices["strict"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation["ent_type"]["correct"] += 1
                        evaluation["partial"]["partial"] += 1
                        evaluation_ent_indices["partial"]["partial_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation["exact"]["incorrect"] += 1
                        evaluation_ent_indices["exact"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )

                        # aggregated by entity type results
                        evaluation_agg_entities_type[true["label"]]["strict"]["incorrect"] += 1
                        evaluation_agg_ent_indices[true["label"]]["strict"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation_agg_entities_type[true["label"]]["ent_type"]["correct"] += 1
                        evaluation_agg_entities_type[true["label"]]["partial"]["partial"] += 1
                        evaluation_agg_ent_indices[true["label"]]["partial"]["partial_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation_agg_entities_type[true["label"]]["exact"]["incorrect"] += 1
                        evaluation_agg_ent_indices[true["label"]]["exact"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )

                        found_overlap = True

                    else:
                        # Scenario VI: Entities overlap, but the entity type is
                        # different.

                        # overall results
                        evaluation["strict"]["incorrect"] += 1
                        evaluation_ent_indices["strict"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation["ent_type"]["incorrect"] += 1
                        evaluation_ent_indices["ent_type"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation["partial"]["partial"] += 1
                        evaluation_ent_indices["partial"]["partial_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation["exact"]["incorrect"] += 1
                        evaluation_ent_indices["exact"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )

                        # aggregated by entity type results
                        # Results against the true entity

                        evaluation_agg_entities_type[true["label"]]["strict"]["incorrect"] += 1
                        evaluation_agg_ent_indices[true["label"]]["strict"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation_agg_entities_type[true["label"]]["partial"]["partial"] += 1
                        evaluation_agg_ent_indices[true["label"]]["partial"]["partial_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation_agg_entities_type[true["label"]]["ent_type"]["incorrect"] += 1
                        evaluation_agg_ent_indices[true["label"]]["ent_type"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )
                        evaluation_agg_entities_type[true["label"]]["exact"]["incorrect"] += 1
                        evaluation_agg_ent_indices[true["label"]]["exact"]["incorrect_indices"].append(
                            (instance_index, within_instance_index)
                        )

                        # Results against the predicted entity
                        # evaluation_agg_entities_type[pred['label']]['strict']['spurious'] += 1
                        found_overlap = True

            # Scenario II: Entities are spurious (i.e., over-generated).
            if not found_overlap:
                # Overall results
                evaluation["strict"]["spurious"] += 1
                evaluation_ent_indices["strict"]["spurious_indices"].append((instance_index, within_instance_index))
                evaluation["ent_type"]["spurious"] += 1
                evaluation_ent_indices["ent_type"]["spurious_indices"].append((instance_index, within_instance_index))
                evaluation["partial"]["spurious"] += 1
                evaluation_ent_indices["partial"]["spurious_indices"].append((instance_index, within_instance_index))
                evaluation["exact"]["spurious"] += 1
                evaluation_ent_indices["exact"]["spurious_indices"].append((instance_index, within_instance_index))

                # Aggregated by entity type results

                # a over-generated entity with a valid tag should be
                # attributed to the respective tag only
                if pred["label"] in tags:
                    spurious_tags = [pred["label"]]
                else:
                    # NOTE: when pred.e_type is not found in valid tags
                    # or when it simply does not appear in the test set, then it is
                    # spurious, but it is not clear where to assign it at the tag
                    # level. In this case, it is applied to all target_tags
                    # found in this example. This will mean that the sum of the
                    # evaluation_agg_entities will not equal evaluation.

                    spurious_tags = tags

                for true in spurious_tags:
                    evaluation_agg_entities_type[true]["strict"]["spurious"] += 1
                    evaluation_agg_ent_indices[true]["strict"]["spurious_indices"].append(
                        (instance_index, within_instance_index)
                    )
                    evaluation_agg_entities_type[true]["ent_type"]["spurious"] += 1
                    evaluation_agg_ent_indices[true]["ent_type"]["spurious_indices"].append(
                        (instance_index, within_instance_index)
                    )
                    evaluation_agg_entities_type[true]["partial"]["spurious"] += 1
                    evaluation_agg_ent_indices[true]["partial"]["spurious_indices"].append(
                        (instance_index, within_instance_index)
                    )
                    evaluation_agg_entities_type[true]["exact"]["spurious"] += 1
                    evaluation_agg_ent_indices[true]["exact"]["spurious_indices"].append(
                        (instance_index, within_instance_index)
                    )

    # Scenario III: Entity was missed entirely.
    for within_instance_index, true in enumerate(true_named_entities):
        if true in true_which_overlapped_with_pred:
            continue

        # overall results
        evaluation["strict"]["missed"] += 1
        evaluation_ent_indices["strict"]["missed_indices"].append((instance_index, within_instance_index))
        evaluation["ent_type"]["missed"] += 1
        evaluation_ent_indices["ent_type"]["missed_indices"].append((instance_index, within_instance_index))
        evaluation["partial"]["missed"] += 1
        evaluation_ent_indices["partial"]["missed_indices"].append((instance_index, within_instance_index))
        evaluation["exact"]["missed"] += 1
        evaluation_ent_indices["exact"]["missed_indices"].append((instance_index, within_instance_index))

        # for the agg. by label
        evaluation_agg_entities_type[true["label"]]["strict"]["missed"] += 1
        evaluation_agg_ent_indices[true["label"]]["strict"]["missed_indices"].append(
            (instance_index, within_instance_index)
        )
        evaluation_agg_entities_type[true["label"]]["ent_type"]["missed"] += 1
        evaluation_agg_ent_indices[true["label"]]["ent_type"]["missed_indices"].append(
            (instance_index, within_instance_index)
        )
        evaluation_agg_entities_type[true["label"]]["partial"]["missed"] += 1
        evaluation_agg_ent_indices[true["label"]]["partial"]["missed_indices"].append(
            (instance_index, within_instance_index)
        )
        evaluation_agg_entities_type[true["label"]]["exact"]["missed"] += 1
        evaluation_agg_ent_indices[true["label"]]["exact"]["missed_indices"].append(
            (instance_index, within_instance_index)
        )

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
            evaluation_agg_entities_type[entity_type][eval_type] = compute_actual_possible(entity_level[eval_type])

    return evaluation, evaluation_agg_entities_type, evaluation_ent_indices, evaluation_agg_ent_indices


def compute_actual_possible(results: dict) -> dict:
    """
    Takes a result dict that has been output by compute metrics.
    Returns the results' dict with actual, possible populated.

    When the results dicts is from partial or ent_type metrics, then
    partial_or_type=True to ensure the right calculation is used for
    calculating precision and recall.
    """

    correct = results["correct"]
    incorrect = results["incorrect"]
    partial = results["partial"]
    missed = results["missed"]
    spurious = results["spurious"]

    # Possible: number annotations in the gold-standard which contribute to the
    # final score
    possible = correct + incorrect + partial + missed

    # Actual: number of annotations produced by the NER system
    actual = correct + incorrect + partial + spurious

    results["actual"] = actual
    results["possible"] = possible

    return results


def compute_precision_recall(results: dict, partial_or_type: bool = False) -> dict:
    """
    Takes a result dict that has been output by compute metrics.
    Returns the results' dict with precision and recall populated.

    When the results dicts is from partial or ent_type metrics, then
    partial_or_type=True to ensure the right calculation is used for
    calculating precision and recall.
    """

    actual = results["actual"]
    possible = results["possible"]
    partial = results["partial"]
    correct = results["correct"]

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


def compute_precision_recall_wrapper(results: dict) -> dict:
    """
    Wraps the compute_precision_recall function and runs on a dict of results
    """

    results_a = {
        key: compute_precision_recall(value, True) for key, value in results.items() if key in ["partial", "ent_type"]
    }
    results_b = {key: compute_precision_recall(value) for key, value in results.items() if key in ["strict", "exact"]}

    results = {**results_a, **results_b}

    return results
