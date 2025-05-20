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
    """Strict evaluation strategy - entities must match exactly."""

    def evaluate(
        self, true_entities: List[Entity], pred_entities: List[Entity], tags: List[str], instance_index: int = 0
    ) -> Tuple[EvaluationResult, EvaluationIndices]:
        """
        Evaluate the predicted entities against the true entities using strict matching.
        """

        result = EvaluationResult()
        indices = EvaluationIndices()

        for pred_idx, pred in enumerate(pred_entities):

            print(pred)
            print(pred.start, pred.end)
            print(pred.label)
            print(true_entities)

            if pred in true_entities:
                result.correct += 1
                indices.correct_indices.append((instance_index, pred_idx))
            else:
                result.spurious += 1
                indices.spurious_indices.append((instance_index, pred_idx))

        for true_idx, true in enumerate(true_entities):
            if true not in pred_entities:
                result.missed += 1
                indices.missed_indices.append((instance_index, true_idx))

        result.compute_metrics()
        return result, indices


class PartialEvaluation(EvaluationStrategy):
    """Partial evaluation strategy - allows for partial matches."""

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
                    if pred.label == true.label:
                        if pred.start == true.start and pred.end == true.end:
                            result.correct += 1
                            indices.correct_indices.append((instance_index, pred_idx))
                        else:
                            result.partial += 1
                            indices.partial_indices.append((instance_index, pred_idx))
                        matched_true.add(true_idx)
                        found_match = True
                        break

                    result.incorrect += 1
                    indices.incorrect_indices.append((instance_index, pred_idx))
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

    Some overlap between the system tagged entity and the gold annotation is required.
    # ToDo: define a minimum overlap threshold - see: https://github.com/MantisAI/nervaluate/pull/83
    """

    def evaluate(
        self, true_entities: List[Entity], pred_entities: List[Entity], tags: List[str], instance_index: int = 0
    ) -> Tuple[EvaluationResult, EvaluationIndices]:
        result = EvaluationResult()
        indices = EvaluationIndices()

        for pred_idx, pred in enumerate(pred_entities):
            found_match = False
            found_overlap = False
            for true_idx, true in enumerate(true_entities):

                print(f"Checking {pred} against {true}")

                # check for a minimum overlap between the system tagged entity and the gold annotation
                if pred.start <= true.end and pred.end >= true.start:
                    found_overlap = True

                # check if the labels match
                if found_overlap and pred.label == true.label:
                    result.correct += 1
                    indices.correct_indices.append((instance_index, pred_idx))
                    found_match = True
                    break

            if not found_match:
                result.spurious += 1
                indices.spurious_indices.append((instance_index, pred_idx))

        for true_idx, true in enumerate(true_entities):
            if not any(pred.label == true.label for pred in pred_entities):
                result.missed += 1
                indices.missed_indices.append((instance_index, true_idx))

        result.compute_metrics(partial_or_type=True)
        return result, indices
