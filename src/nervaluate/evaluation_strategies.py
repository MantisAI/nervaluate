from abc import ABC, abstractmethod
from typing import List, Tuple

from .entities import Entity, EvaluationResult, EvaluationIndices


class EvaluationStrategy(ABC):
    """Abstract base class for evaluation strategies."""

    @abstractmethod
    def evaluate(
        self, true_entities: List[Entity], pred_entities: List[Entity], tags: List[str], instance_index: int = 0
    ) -> Tuple[EvaluationResult, EvaluationIndices]:
        """Evaluate the predicted entities against the true entities."""


class StrictEvaluation(EvaluationStrategy):
    """
    Strict evaluation strategy - entities must match exactly.

    If there's a predicted entity that perfectly matches a true entity and they have the same label
    we mark it as correct.
    If there's a predicted entity that doesn't perfectly match any true entity, we mark it as spurious.
    If there's a true entity that doesn't perfecly match any predicted entity, we mark it as missed.
    All other cases are marked as incorrect.
    """

    def evaluate(
        self, true_entities: List[Entity], pred_entities: List[Entity], tags: List[str], instance_index: int = 0
    ) -> Tuple[EvaluationResult, EvaluationIndices]:
        """
        Evaluate the predicted entities against the true entities using strict matching.
        """
        result = EvaluationResult()
        indices = EvaluationIndices()
        matched_true = set()

        for pred_idx, pred in enumerate(pred_entities):
            found_match = False
            found_incorrect = False

            for true_idx, true in enumerate(true_entities):
                if true_idx in matched_true:
                    continue

                # Check for perfect match (same boundaries and label)
                if pred.label == true.label and pred.start == true.start and pred.end == true.end:
                    result.correct += 1
                    indices.correct_indices.append((instance_index, pred_idx))
                    matched_true.add(true_idx)
                    found_match = True
                    break
                # Check for any overlap
                if pred.start <= true.end and pred.end >= true.start:
                    result.incorrect += 1
                    indices.incorrect_indices.append((instance_index, pred_idx))
                    matched_true.add(true_idx)
                    found_incorrect = True
                    break

            if not found_match and not found_incorrect:
                result.spurious += 1
                indices.spurious_indices.append((instance_index, pred_idx))

        for true_idx, true in enumerate(true_entities):
            if true_idx not in matched_true:
                result.missed += 1
                indices.missed_indices.append((instance_index, true_idx))

        result.compute_metrics()
        return result, indices


class PartialEvaluation(EvaluationStrategy):
    """
    Partial evaluation strategy - allows for partial matches.

    If there's a predicted entity that perfectly matches a true entity, we mark it as correct.
    If there's a predicted entity that has some minimum overlap with a true entity we mark it as partial.
    If there's a predicted entity that doesn't match any true entity, we mark it as spurious.
    If there's a true entity that doesn't match any predicted entity, we mark it as missed.

    There's never entity type/label checking in this strategy, and there's never an entity marked as incorrect.
    """

    def evaluate(
        self, true_entities: List[Entity], pred_entities: List[Entity], tags: List[str], instance_index: int = 0
    ) -> Tuple[EvaluationResult, EvaluationIndices]:
        result = EvaluationResult()
        indices = EvaluationIndices()
        matched_true = set()

        for pred_idx, pred in enumerate(pred_entities):
            found_match = False

            for true_idx, true in enumerate(true_entities):
                if true_idx in matched_true:
                    continue

                # Check for overlap
                if pred.start <= true.end and pred.end >= true.start:
                    if pred.start == true.start and pred.end == true.end:
                        result.correct += 1
                        indices.correct_indices.append((instance_index, pred_idx))
                    else:
                        result.partial += 1
                        indices.partial_indices.append((instance_index, pred_idx))
                    matched_true.add(true_idx)
                    found_match = True
                    break

            if not found_match:
                result.spurious += 1
                indices.spurious_indices.append((instance_index, pred_idx))

        for true_idx, true in enumerate(true_entities):
            if true_idx not in matched_true:
                result.missed += 1
                indices.missed_indices.append((instance_index, true_idx))

        result.compute_metrics(partial_or_type=True)
        return result, indices


class EntityTypeEvaluation(EvaluationStrategy):
    """
    Entity type evaluation strategy - only checks entity types.

    In in strategy, we check for overlap between the predicted entity and the true entity.

    If there's a predicted entity that perfectly matches or only some minimum overlap with a
    true entity, and the same label, we mark it as correct.
    If there's a predicted entity that has some minimum overlap or perfectly matches but has
    the wrong label we mark it as inccorrect.
    If there's a predicted entity that doesn't match any true entity, we mark it as spurious.
    If there's a true entity that doesn't match any predicted entity, we mark it as missed.

    # ToDo: define a minimum overlap threshold - see: https://github.com/MantisAI/nervaluate/pull/83
    """

    def evaluate(
        self, true_entities: List[Entity], pred_entities: List[Entity], tags: List[str], instance_index: int = 0
    ) -> Tuple[EvaluationResult, EvaluationIndices]:
        result = EvaluationResult()
        indices = EvaluationIndices()
        matched_true = set()

        for pred_idx, pred in enumerate(pred_entities):
            found_match = False
            found_incorrect = False

            for true_idx, true in enumerate(true_entities):
                if true_idx in matched_true:
                    continue

                # Check for any overlap (perfect or minimum)
                if pred.start <= true.end and pred.end >= true.start:
                    if pred.label == true.label:
                        result.correct += 1
                        indices.correct_indices.append((instance_index, pred_idx))
                        matched_true.add(true_idx)
                        found_match = True
                    else:
                        result.incorrect += 1
                        indices.incorrect_indices.append((instance_index, pred_idx))
                        matched_true.add(true_idx)
                        found_incorrect = True
                    break

            if not found_match and not found_incorrect:
                result.spurious += 1
                indices.spurious_indices.append((instance_index, pred_idx))

        for true_idx, true in enumerate(true_entities):
            if true_idx not in matched_true:
                result.missed += 1
                indices.missed_indices.append((instance_index, true_idx))

        result.compute_metrics(partial_or_type=True)
        return result, indices


class ExactEvaluation(EvaluationStrategy):
    """
    Exact evaluation strategy - exact boundary match over the surface string, regardless of the type.

    If there's a predicted entity that perfectly matches a true entity, regardless of the label, we mark it as correct.
    If there's a predicted entity that has only some minimum overlap with a true entity, we mark it as incorrect.
    If there's a predicted entity that doesn't match any true entity, we mark it as spurious.
    If there's a true entity that doesn't match any predicted entity, we mark it as missed.
    """

    def evaluate(
        self, true_entities: List[Entity], pred_entities: List[Entity], tags: List[str], instance_index: int = 0
    ) -> Tuple[EvaluationResult, EvaluationIndices]:
        """
        Evaluate the predicted entities against the true entities using exact boundary matching.
        Entity type is not considered in the matching.
        """
        result = EvaluationResult()
        indices = EvaluationIndices()
        matched_true = set()

        for pred_idx, pred in enumerate(pred_entities):
            found_match = False
            found_incorrect = False

            for true_idx, true in enumerate(true_entities):
                if true_idx in matched_true:
                    continue

                # Check for exact boundary match (regardless of label)
                if pred.start == true.start and pred.end == true.end:
                    result.correct += 1
                    indices.correct_indices.append((instance_index, pred_idx))
                    matched_true.add(true_idx)
                    found_match = True
                    break
                # Check for any overlap
                if pred.start <= true.end and pred.end >= true.start:
                    result.incorrect += 1
                    indices.incorrect_indices.append((instance_index, pred_idx))
                    matched_true.add(true_idx)
                    found_incorrect = True
                    break

            if not found_match and not found_incorrect:
                result.spurious += 1
                indices.spurious_indices.append((instance_index, pred_idx))

        for true_idx, true in enumerate(true_entities):
            if true_idx not in matched_true:
                result.missed += 1
                indices.missed_indices.append((instance_index, true_idx))

        result.compute_metrics()
        return result, indices
