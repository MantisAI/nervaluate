from typing import List, Dict, Any, Union
import pandas as pd

from .entities import EvaluationResult, EvaluationIndices
from .evaluation_strategies import EvaluationStrategy, StrictEvaluation, PartialEvaluation, EntityTypeEvaluation
from .loaders import DataLoader, ConllLoader, ListLoader, DictLoader
from .entities import Entity

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
        indices = {}
        entity_indices: Dict[str, Dict[str, EvaluationIndices]] = {tag: {} for tag in self.tags}

        # Evaluate each document
        for doc_idx, (true_doc, pred_doc) in enumerate(zip(self.true, self.pred)):
            # Filter entities by valid tags
            true_doc = [e for e in true_doc if e.label in self.tags]
            pred_doc = [e for e in pred_doc if e.label in self.tags]

            # Evaluate with each strategy
            for strategy_name, strategy in self.strategies.items():
                result, doc_indices = strategy.evaluate(true_doc, pred_doc, self.tags, doc_idx)

                # Update overall results
                if strategy_name not in results:
                    results[strategy_name] = result
                    indices[strategy_name] = doc_indices
                else:
                    self._merge_results(results[strategy_name], result)
                    self._merge_indices(indices[strategy_name], doc_indices)

                # Update entity-specific results
                for tag in self.tags:
                    if tag not in entity_results:
                        entity_results[tag] = {}
                        entity_indices[tag] = {}
                    if strategy_name not in entity_results[tag]:
                        entity_results[tag][strategy_name] = result
                        entity_indices[tag][strategy_name] = doc_indices
                    else:
                        self._merge_results(entity_results[tag][strategy_name], result)
                        self._merge_indices(entity_indices[tag][strategy_name], doc_indices)

        return {
            "overall": results,
            "entities": entity_results,
            "overall_indices": indices,
            "entity_indices": entity_indices,
        }

    @staticmethod
    def _merge_results(target: EvaluationResult, source: EvaluationResult) -> None:
        """Merge two evaluation results."""
        target.correct += source.correct
        target.incorrect += source.incorrect
        target.partial += source.partial
        target.missed += source.missed
        target.spurious += source.spurious
        target.compute_metrics()

    @staticmethod
    def _merge_indices(target: EvaluationIndices, source: EvaluationIndices) -> None:
        """Merge two evaluation indices."""
        target.correct_indices.extend(source.correct_indices)
        target.incorrect_indices.extend(source.incorrect_indices)
        target.partial_indices.extend(source.partial_indices)
        target.missed_indices.extend(source.missed_indices)
        target.spurious_indices.extend(source.spurious_indices)

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

    def summary_report(self, mode: str = "overall", scenario: str = "strict", digits: int = 2) -> str:
        """
        Generate a summary report of the evaluation results.

        Args:
            mode: Either 'overall' for overall metrics or 'entities' for per-entity metrics.
            scenario: The scenario to report on. Must be one of: 'strict', 'ent_type', 'partial', 'exact'.
                     Only used when mode is 'entities'. Defaults to 'strict'.
            digits: The number of digits to round the results to.

        Returns:
            A string containing the summary report.

        Raises:
            ValueError: If the scenario or mode is invalid.
        """
        valid_scenarios = {"strict", "ent_type", "partial", "exact"}
        valid_modes = {"overall", "entities"}

        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: must be one of {valid_modes}")

        if mode == "entities" and scenario not in valid_scenarios:
            raise ValueError(f"Invalid scenario: must be one of {valid_scenarios}")

        headers = ["correct", "incorrect", "partial", "missed", "spurious", "precision", "recall", "f1-score"]
        rows = [headers]

        results = self.evaluate()
        if mode == "overall":
            # Process overall results
            results_data = results["overall"]
            for eval_schema in sorted(valid_scenarios):  # Sort to ensure consistent order
                if eval_schema not in results_data:
                    continue
                results_schema = results_data[eval_schema]
                rows.append(
                    [
                        eval_schema,
                        results_schema.correct,
                        results_schema.incorrect,
                        results_schema.partial,
                        results_schema.missed,
                        results_schema.spurious,
                        results_schema.precision,
                        results_schema.recall,
                        results_schema.f1,
                    ]
                )
        else:
            # Process entity-specific results
            results_data = results["entities"]
            target_names = sorted(results_data.keys())
            for ent_type in target_names:
                if scenario not in results_data[ent_type]:
                    raise ValueError(f"Scenario '{scenario}' not found in results for entity type '{ent_type}'")

                results_ent = results_data[ent_type][scenario]
                rows.append(
                    [
                        ent_type,
                        results_ent.correct,
                        results_ent.incorrect,
                        results_ent.partial,
                        results_ent.missed,
                        results_ent.spurious,
                        results_ent.precision,
                        results_ent.recall,
                        results_ent.f1,
                    ]
                )

        # Format the report
        name_width = max(len(str(row[0])) for row in rows)
        width = max(name_width, digits)
        head_fmt = "{:>{width}s} " + " {:>11}" * len(headers)
        report = head_fmt.format("", *headers, width=width)
        report += "\n\n"
        row_fmt = "{:>{width}s} " + " {:>11}" * 5 + " {:>11.{digits}f}" * 3 + "\n"

        for row in rows[1:]:
            report += row_fmt.format(*row, width=width, digits=digits)

        return report

    def summary_report_indices(self, mode: str = "overall", scenario: str = "strict") -> str:
        """
        Generate a summary report of the evaluation indices.

        Args:
            mode: Either 'overall' for overall metrics or 'entities' for per-entity metrics.
            scenario: The scenario to report on. Must be one of: 'strict', 'ent_type', 'partial', 'exact'.
                     Only used when mode is 'entities'. Defaults to 'strict'.

        Returns:
            A string containing the summary report of indices.

        Raises:
            ValueError: If the scenario or mode is invalid.
        """
        valid_scenarios = {"strict", "ent_type", "partial", "exact"}
        valid_modes = {"overall", "entities"}

        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: must be one of {valid_modes}")

        if mode == "entities" and scenario not in valid_scenarios:
            raise ValueError(f"Invalid scenario: must be one of {valid_scenarios}")

        def get_prediction_info(pred: Union[Entity, str]) -> str:
            """Helper function to get prediction info based on pred type."""
            if isinstance(pred, Entity):
                return f"Label={pred.label}, Start={pred.start}, End={pred.end}"  # type: ignore
            # String (BIO tag)
            return f"Tag={pred}"

        results = self.evaluate()
        report = ""
        if mode == "overall":
            # Get the indices from the overall results
            indices_data = results["overall_indices"][scenario]
            report += f"Indices for error schema '{scenario}':\n\n"

            for category, indices in indices_data.__dict__.items():
                if not category.endswith("_indices"):
                    continue
                category_name = category.replace("_indices", "").replace("_", " ").capitalize()
                report += f"{category_name}:\n"
                if indices:
                    for instance_index, entity_index in indices:
                        if self.pred != [[]]:
                            pred = self.pred[instance_index][entity_index]
                            prediction_info = get_prediction_info(pred)
                            report += f"  - Instance {instance_index}, Entity {entity_index}: {prediction_info}\n"
                        else:
                            report += f"  - Instance {instance_index}, Entity {entity_index}\n"
                else:
                    report += "  - None\n"
                report += "\n"
        else:
            # Get the indices from the entity-specific results
            for entity_type, entity_results in results["entity_indices"].items():
                report += f"\nEntity Type: {entity_type}\n"
                error_data = entity_results[scenario]
                report += f"  Error Schema: '{scenario}'\n"

                for category, indices in error_data.__dict__.items():
                    if not category.endswith("_indices"):
                        continue
                    category_name = category.replace("_indices", "").replace("_", " ").capitalize()
                    report += f"    ({entity_type}) {category_name}:\n"
                    if indices:
                        for instance_index, entity_index in indices:
                            if self.pred != [[]]:
                                pred = self.pred[instance_index][entity_index]
                                prediction_info = get_prediction_info(pred)
                                report += f"      - Instance {instance_index}, Entity {entity_index}: {prediction_info}\n"
                            else:
                                report += f"      - Instance {instance_index}, Entity {entity_index}\n"
                    else:
                        report += "      - None\n"

        return report
