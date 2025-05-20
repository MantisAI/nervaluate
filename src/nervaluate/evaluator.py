from typing import List, Dict, Any
import pandas as pd

from .entities import EvaluationResult
from .evaluation_strategies import EvaluationStrategy, StrictEvaluation, PartialEvaluation, EntityTypeEvaluation
from .loaders import DataLoader, ConllLoader, ListLoader, DictLoader


class Evaluator:
    """Main evaluator class for NER evaluation."""

    def __init__(self, true: Any, pred: Any, tags: List[str], loader: str = "default") -> None:
        """
        Initialize the evaluator.

        Args:
            true: True entities in any supported format
            pred: Predicted entities in any supported format
            tags: List of valid entity tags
            loader: Name of the loader to use
        """
        self.tags = tags
        self._setup_loaders()
        self._load_data(true, pred, loader)
        self._setup_evaluation_strategies()

    def _setup_loaders(self) -> None:
        """Setup available data loaders."""
        self.loaders: Dict[str, DataLoader] = {"conll": ConllLoader(), "list": ListLoader(), "dict": DictLoader()}

    def _setup_evaluation_strategies(self) -> None:
        """Setup evaluation strategies."""
        self.strategies: Dict[str, EvaluationStrategy] = {
            "strict": StrictEvaluation(),
            "partial": PartialEvaluation(),
            "ent_type": EntityTypeEvaluation(),
        }

    def _load_data(self, true: Any, pred: Any, loader: str) -> None:
        """Load the true and predicted data."""
        if loader == "default":
            # Try to infer the loader based on input type
            if isinstance(true, str):
                loader = "conll"
            elif isinstance(true, list) and true and isinstance(true[0], list):
                if isinstance(true[0][0], dict):
                    loader = "dict"
                else:
                    loader = "list"
            else:
                raise ValueError("Could not infer loader from input type")

        if loader not in self.loaders:
            raise ValueError(f"Unknown loader: {loader}")

        self.true = self.loaders[loader].load(true)
        self.pred = self.loaders[loader].load(pred)

        if len(self.true) != len(self.pred):
            raise ValueError("Number of predicted documents does not equal true")

    def evaluate(self) -> Dict[str, Any]:
        """
        Run the evaluation.

        Returns:
            Dictionary containing evaluation results for each strategy and entity type
        """
        results = {}
        entity_results: Dict[str, Dict[str, EvaluationResult]] = {tag: {} for tag in self.tags}

        # Evaluate each document
        for doc_idx, (true_doc, pred_doc) in enumerate(zip(self.true, self.pred)):
            # Filter entities by valid tags
            true_doc = [e for e in true_doc if e.label in self.tags]
            pred_doc = [e for e in pred_doc if e.label in self.tags]

            # Evaluate with each strategy
            for strategy_name, strategy in self.strategies.items():
                result, _ = strategy.evaluate(true_doc, pred_doc, self.tags, doc_idx)

                # Update overall results
                if strategy_name not in results:
                    results[strategy_name] = result
                else:
                    self._merge_results(results[strategy_name], result)

                # Update entity-specific results
                for tag in self.tags:
                    if tag not in entity_results:
                        entity_results[tag] = {}
                    if strategy_name not in entity_results[tag]:
                        entity_results[tag][strategy_name] = result
                    else:
                        self._merge_results(entity_results[tag][strategy_name], result)

        return {"overall": results, "entities": entity_results}

    def _merge_results(self, target: EvaluationResult, source: EvaluationResult) -> None:
        """Merge two evaluation results."""
        target.correct += source.correct
        target.incorrect += source.incorrect
        target.partial += source.partial
        target.missed += source.missed
        target.spurious += source.spurious
        target.compute_metrics()

    def results_to_dataframe(self) -> Any:
        """Convert results to a pandas DataFrame."""
        results = self.evaluate()

        # Flatten the results structure
        flat_results = {}
        for category, category_results in results.items():
            for strategy, strategy_results in category_results.items():
                for metric, value in strategy_results.__dict__.items():
                    key = f"{category}.{strategy}.{metric}"
                    flat_results[key] = value

        return pd.DataFrame([flat_results])
