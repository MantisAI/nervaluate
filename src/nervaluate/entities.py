from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Entity:
    """Represents a named entity with its position and label."""

    label: str
    start: int
    end: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.label == other.label and self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        return hash((self.label, self.start, self.end))


@dataclass
class EvaluationResult:
    """Represents the evaluation metrics for a single entity type or overall."""

    correct: int = 0
    incorrect: int = 0
    partial: int = 0
    missed: int = 0
    spurious: int = 0
    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0
    actual: int = 0
    possible: int = 0

    def compute_metrics(self, partial_or_type: bool = False) -> None:
        """Compute precision, recall and F1 score."""
        self.actual = self.correct + self.incorrect + self.partial + self.spurious
        self.possible = self.correct + self.incorrect + self.partial + self.missed

        if partial_or_type:
            precision = (self.correct + 0.5 * self.partial) / self.actual if self.actual > 0 else 0
            recall = (self.correct + 0.5 * self.partial) / self.possible if self.possible > 0 else 0
        else:
            precision = self.correct / self.actual if self.actual > 0 else 0
            recall = self.correct / self.possible if self.possible > 0 else 0

        self.precision = precision
        self.recall = recall
        self.f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0


@dataclass
class EvaluationIndices:
    """Represents the indices of entities in different evaluation categories."""

    correct_indices: List[Tuple[int, int]] = None  # type: ignore
    incorrect_indices: List[Tuple[int, int]] = None  # type: ignore
    partial_indices: List[Tuple[int, int]] = None  # type: ignore
    missed_indices: List[Tuple[int, int]] = None  # type: ignore
    spurious_indices: List[Tuple[int, int]] = None  # type: ignore

    def __post_init__(self) -> None:
        if self.correct_indices is None:
            self.correct_indices = []
        if self.incorrect_indices is None:
            self.incorrect_indices = []
        if self.partial_indices is None:
            self.partial_indices = []
        if self.missed_indices is None:
            self.missed_indices = []
        if self.spurious_indices is None:
            self.spurious_indices = []
