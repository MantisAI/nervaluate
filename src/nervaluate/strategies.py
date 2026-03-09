from abc import ABC, abstractmethod
from typing import List, Tuple

from .entities import Entity, EvaluationResult, EvaluationIndices


class EvaluationStrategy(ABC):
    """Abstract base class for evaluation strategies."""

    def __init__(self, min_overlap_percentage: float = 1.0):
        """
        Initialize strategy with minimum overlap threshold.

        Args:
            min_overlap_percentage: Minimum overlap percentage required (1-100)
        """
        if not 1.0 <= min_overlap_percentage <= 100.0:
            raise ValueError("min_overlap_percentage must be between 1.0 and 100.0")
        self.min_overlap_percentage = min_overlap_percentage

    @staticmethod
    def _calculate_overlap_percentage(pred: Entity, true: Entity) -> float:
        """
        Calculate the percentage overlap between predicted and true entities.

        Returns:
            Overlap percentage based on true entity span (0-100)
        """
        # Check if there's any overlap first
        if pred.start > true.end or pred.end < true.start:
            return 0.0

        # Calculate overlap boundaries
        overlap_start = max(pred.start, true.start)
        overlap_end = min(pred.end, true.end)

        # Calculate spans (adding 1 because end is inclusive)
        overlap_span = overlap_end - overlap_start + 1
        true_span = true.end - true.start + 1

        # Calculate percentage based on true entity span
        return (overlap_span / true_span) * 100.0

    @staticmethod
    def _calculate_boundaries_distance(pred: Entity, true: Entity) -> float:
        """
        Calculate distance between predicted and true entities boundaries.

        Returns:
            Distance between predicted and true boundaries
        """
        # Calculate boundaries gaps
        distance_starts = abs(pred.start - true.start)
        distance_ends = abs(pred.end - true.end)

        return distance_starts + distance_ends

    def _has_sufficient_overlap(self, pred: Entity, true: Entity) -> bool:
        """Check if entities have sufficient overlap based on threshold."""
        overlap_percentage = EvaluationStrategy._calculate_overlap_percentage(pred, true)
        return overlap_percentage >= self.min_overlap_percentage

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
                # Check for sufficient overlap with min threshold
                if self._has_sufficient_overlap(pred, true) and not found_incorrect:
                    incorrect_true_idx = true_idx
                    incorrect_pred_idx = pred_idx
                    found_incorrect = True

            if not found_match:
                if found_incorrect:
                    result.incorrect += 1
                    indices.incorrect_indices.append((instance_index, incorrect_pred_idx))
                    matched_true.add(incorrect_true_idx)
                else:
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
    If there's a predicted entity that doesn't match any true entity and that has some minimum
    overlap with a true entity we mark it as partial.
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
            found_partial = False

            for true_idx, true in enumerate(true_entities):
                if true_idx in matched_true:
                    continue

                # Check for sufficient overlap with min threshold
                if self._has_sufficient_overlap(pred, true):
                    if pred.start == true.start and pred.end == true.end:
                        result.correct += 1
                        indices.correct_indices.append((instance_index, pred_idx))
                        matched_true.add(true_idx)
                        found_match = True
                        break
                    if not found_partial:
                        partial_pred_idx = pred_idx
                        partial_true_idx = true_idx
                        found_partial = True

            if not found_match:
                if found_partial:
                    result.partial += 1
                    indices.partial_indices.append((instance_index, partial_pred_idx))
                    matched_true.add(partial_true_idx)
                else:
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

    In strategy, we check for overlap between the predicted entity and the true entity.

    If there's a predicted entity that perfectly matches or only some minimum overlap with a
    true entity, and the same label, we mark it as correct. If there are multiple entities
    with at least some minimum overlap, we mark as correct the one with boundaries closest to
    a true entity.
    If there's a predicted entity that doesn't match any true entity and that has some minimum
    overlap or perfectly matches but has the wrong label we mark it as incorrect.
    If there's a predicted entity that doesn't match any true entity, we mark it as spurious.
    If there's a true entity that doesn't match any predicted entity, we mark it as missed.

    When multiple true entities of the same label overlap a prediction, the match is chosen by
    closest boundaries (minimum sum of start and end offset differences), so which true entity
    is considered "missed" may differ from list order.
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
            current_match_boundaries_distance = None

            for true_idx, true in enumerate(true_entities):
                if true_idx in matched_true:
                    continue

                # Check for sufficient overlap with min threshold
                if self._has_sufficient_overlap(pred, true):
                    boundaries_distance = self._calculate_boundaries_distance(pred, true)
                    if pred.label == true.label:
                        if (
                            current_match_boundaries_distance is None
                            or boundaries_distance < current_match_boundaries_distance
                        ):
                            correct_true_idx = true_idx
                            correct_pred_idx = pred_idx
                            current_match_boundaries_distance = boundaries_distance
                            found_match = True

                    elif not found_incorrect:
                        incorrect_true_idx = true_idx
                        incorrect_pred_idx = pred_idx
                        found_incorrect = True

            if found_match:
                result.correct += 1
                indices.correct_indices.append((instance_index, correct_pred_idx))
                matched_true.add(correct_true_idx)
            else:
                if found_incorrect:
                    result.incorrect += 1
                    indices.incorrect_indices.append((instance_index, incorrect_pred_idx))
                    matched_true.add(incorrect_true_idx)
                else:
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
    If there's a predicted entity that doesn't match any true entity and that has only some minimum
    overlap with a true entity, we mark it as incorrect.
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
                # Check for sufficient overlap with min threshold
                if self._has_sufficient_overlap(pred, true) and not found_incorrect:
                    incorrect_true_idx = true_idx
                    incorrect_pred_idx = pred_idx
                    found_incorrect = True

            if not found_match:
                if found_incorrect:
                    result.incorrect += 1
                    indices.incorrect_indices.append((instance_index, incorrect_pred_idx))
                    matched_true.add(incorrect_true_idx)
                else:
                    result.spurious += 1
                    indices.spurious_indices.append((instance_index, pred_idx))

        for true_idx, true in enumerate(true_entities):
            if true_idx not in matched_true:
                result.missed += 1
                indices.missed_indices.append((instance_index, true_idx))

        result.compute_metrics()
        return result, indices
