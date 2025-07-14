from typing import List, Dict, Any, Union, Optional
import csv
import io

from .entities import EvaluationResult, EvaluationIndices
from .strategies import (
    EvaluationStrategy,
    StrictEvaluation,
    PartialEvaluation,
    EntityTypeEvaluation,
    ExactEvaluation,
)
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
            "exact": ExactEvaluation(),
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

        # For list loader, check document lengths before loading
        if loader == "list":
            if len(true) != len(pred):
                raise ValueError("Number of predicted documents does not equal true")

            # Check that each document has the same length
            for i, (true_doc, pred_doc) in enumerate(zip(true, pred)):
                if len(true_doc) != len(pred_doc):
                    raise ValueError(f"Document {i} has different lengths: true={len(true_doc)}, pred={len(pred_doc)}")

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
        # Get unique tags that appear in either true or predicted data
        used_tags = set()  # type: ignore
        for doc in self.true:
            used_tags.update(e.label for e in doc)
        for doc in self.pred:
            used_tags.update(e.label for e in doc)
        # Only keep tags that are both used and in the allowed tags list
        used_tags = used_tags.intersection(set(self.tags))

        entity_results: Dict[str, Dict[str, EvaluationResult]] = {tag: {} for tag in used_tags}
        indices = {}
        entity_indices: Dict[str, Dict[str, EvaluationIndices]] = {tag: {} for tag in used_tags}

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
                for tag in used_tags:
                    # Filter entities for this specific tag
                    true_tag_doc = [e for e in true_doc if e.label == tag]
                    pred_tag_doc = [e for e in pred_doc if e.label == tag]

                    # Evaluate only entities of this tag
                    tag_result, tag_indices = strategy.evaluate(true_tag_doc, pred_tag_doc, [tag], doc_idx)

                    if tag not in entity_results:
                        entity_results[tag] = {}
                        entity_indices[tag] = {}
                    if strategy_name not in entity_results[tag]:
                        entity_results[tag][strategy_name] = tag_result
                        entity_indices[tag][strategy_name] = tag_indices
                    else:
                        self._merge_results(entity_results[tag][strategy_name], tag_result)
                        self._merge_indices(entity_indices[tag][strategy_name], tag_indices)

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

    def results_to_csv(
        self, mode: str = "overall", scenario: str = "strict", file_path: Optional[str] = None
    ) -> Union[str, None]:
        """
        Convert results to CSV format.

        Args:
            mode: Either 'overall' for overall metrics or 'entities' for per-entity metrics
            scenario: The scenario to report on (only used when mode is 'entities')
            file_path: Optional path to save CSV file. If None, returns CSV as string

        Returns:
            CSV content as string if file_path is None, otherwise None (saves to file)
        """
        valid_modes = {"overall", "entities"}
        valid_scenarios = {"strict", "ent_type", "partial", "exact"}

        if mode not in valid_modes:
            raise ValueError(f"Invalid mode: must be one of {valid_modes}")

        if mode == "entities" and scenario not in valid_scenarios:
            raise ValueError(f"Invalid scenario: must be one of {valid_scenarios}")

        results = self.evaluate()

        if mode == "overall":
            # For overall mode, include all scenarios
            csv_data = [
                ["Strategy", "Correct", "Incorrect", "Partial", "Missed", "Spurious", "Precision", "Recall", "F1-Score"]
            ]
            results_data = results["overall"]
            for strategy_name, strategy_result in results_data.items():
                csv_data.append(
                    [
                        strategy_name,
                        strategy_result.correct,
                        strategy_result.incorrect,
                        strategy_result.partial,
                        strategy_result.missed,
                        strategy_result.spurious,
                        strategy_result.precision,
                        strategy_result.recall,
                        strategy_result.f1,
                    ]
                )
        else:
            csv_data = [
                ["Entity", "Correct", "Incorrect", "Partial", "Missed", "Spurious", "Precision", "Recall", "F1-Score"]
            ]
            results_data = results["entities"]
            for entity_type, entity_results in results_data.items():
                if scenario in entity_results:
                    strategy_result = entity_results[scenario]
                    csv_data.append(
                        [
                            entity_type,
                            strategy_result.correct,
                            strategy_result.incorrect,
                            strategy_result.partial,
                            strategy_result.missed,
                            strategy_result.spurious,
                            strategy_result.precision,
                            strategy_result.recall,
                            strategy_result.f1,
                        ]
                    )

        if file_path:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(csv_data)
            return None

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(csv_data)
        return output.getvalue()

    def summary_report(self, mode: str = "overall", scenario: str = "strict", digits: int = 2) -> str:
        """
        Generate a summary report of the evaluation results.

        Args:
            mode: Either 'overall' for overall metrics or 'entities' for per-entity metrics.
            scenario: The scenario to report on. Only used when mode is 'entities'.
                      Must be one of:
                        - 'strict' exact boundary surface string match and entity type;
                        - 'exact': exact boundary match over the surface string and entity type;
                        - 'partial': partial boundary match over the surface string, regardless of the type;
                        - 'ent_type': exact boundary match over the surface string, regardless of the type;
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
            # Process overall results - show all scenarios
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
            # Process entity-specific results for the specified scenario only
            results_data = results["entities"]
            target_names = sorted(results_data.keys())
            for ent_type in target_names:
                if scenario not in results_data[ent_type]:
                    continue  # Skip if scenario not available for this entity type

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
        report = f"Scenario: {scenario if mode == 'entities' else 'all'}\n\n" + head_fmt.format(
            "", *headers, width=width
        )
        report += "\n\n"
        row_fmt = "{:>{width}s} " + " {:>11}" * 5 + " {:>11.{digits}f}" * 3 + "\n"

        for row in rows[1:]:
            report += row_fmt.format(*row, width=width, digits=digits)

        return report

    def summary_report_indices(  # pylint: disable=too-many-branches
        self, mode: str = "overall", scenario: str = "strict", colors: bool = False
    ) -> str:
        """
        Generate a summary report of the evaluation indices.

        Args:
            mode: Either 'overall' for overall metrics or 'entities' for per-entity metrics.
            scenario: The scenario to report on. Must be one of: 'strict', 'ent_type', 'partial', 'exact'.
                     Only used when mode is 'entities'. Defaults to 'strict'.
            colors: Whether to use colors in the output. Defaults to False.

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

        # ANSI color codes
        COLORS = {
            "reset": "\033[0m",
            "bold": "\033[1m",
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
        }

        def colorize(text: str, color: str) -> str:
            """Helper function to colorize text if colors are enabled."""
            if colors:
                return f"{COLORS[color]}{text}{COLORS['reset']}"
            return text

        def get_prediction_info(pred: Union[Entity, str]) -> str:
            """Helper function to get prediction info based on pred type."""
            if isinstance(pred, Entity):
                return f"Label={pred.label}, Start={pred.start}, End={pred.end}"
            # String (BIO tag)
            return f"Tag={pred}"

        results = self.evaluate()
        report = ""

        # Create headers for the table
        headers = ["Category", "Instance", "Entity", "Details"]
        header_fmt = "{:<20} {:<10} {:<8} {:<25}"
        row_fmt = "{:<20} {:<10} {:<8} {:<10}"

        if mode == "overall":
            # Get the indices from the overall results
            indices_data = results["overall_indices"][scenario]
            report += f"\n{colorize('Indices for error schema', 'bold')} '{colorize(scenario, 'cyan')}':\n\n"
            report += colorize(header_fmt.format(*headers), "bold") + "\n"
            report += colorize("-" * 78, "white") + "\n"

            for category, indices in indices_data.__dict__.items():
                if not category.endswith("_indices"):
                    continue
                category_name = category.replace("_indices", "").replace("_", " ").capitalize()

                # Color mapping for categories
                category_colors = {
                    "Correct": "green",
                    "Incorrect": "red",
                    "Partial": "yellow",
                    "Missed": "magenta",
                    "Spurious": "blue",
                }

                if indices:
                    for instance_index, entity_index in indices:
                        if self.pred != [[]]:
                            pred = self.pred[instance_index][entity_index]
                            prediction_info = get_prediction_info(pred)
                            report += (
                                row_fmt.format(
                                    colorize(category_name, category_colors.get(category_name, "white")),
                                    f"{instance_index}",
                                    f"{entity_index}",
                                    prediction_info,
                                )
                                + "\n"
                            )
                        else:
                            report += (
                                row_fmt.format(
                                    colorize(category_name, category_colors.get(category_name, "white")),
                                    f"{instance_index}",
                                    f"{entity_index}",
                                    "No prediction info",
                                )
                                + "\n"
                            )
                else:
                    report += (
                        row_fmt.format(
                            colorize(category_name, category_colors.get(category_name, "white")), "-", "-", "None"
                        )
                        + "\n"
                    )
        else:
            # Get the indices from the entity-specific results
            for entity_type, entity_results in results["entity_indices"].items():
                report += f"\n{colorize('Entity Type', 'bold')}: {colorize(entity_type, 'cyan')}\n"
                report += f"{colorize('Error Schema', 'bold')}: '{colorize(scenario, 'cyan')}'\n\n"
                report += colorize(header_fmt.format(*headers), "bold") + "\n"
                report += colorize("-" * 78, "white") + "\n"

                error_data = entity_results[scenario]
                for category, indices in error_data.__dict__.items():
                    if not category.endswith("_indices"):
                        continue
                    category_name = category.replace("_indices", "").replace("_", " ").capitalize()

                    # Color mapping for categories
                    category_colors = {
                        "Correct": "green",
                        "Incorrect": "red",
                        "Partial": "yellow",
                        "Missed": "magenta",
                        "Spurious": "blue",
                    }

                    if indices:
                        for instance_index, entity_index in indices:
                            if self.pred != [[]]:
                                pred = self.pred[instance_index][entity_index]
                                prediction_info = get_prediction_info(pred)
                                report += (
                                    row_fmt.format(
                                        colorize(category_name, category_colors.get(category_name, "white")),
                                        f"{instance_index}",
                                        f"{entity_index}",
                                        prediction_info,
                                    )
                                    + "\n"
                                )
                            else:
                                report += (
                                    row_fmt.format(
                                        colorize(category_name, category_colors.get(category_name, "white")),
                                        f"{instance_index}",
                                        f"{entity_index}",
                                        "No prediction info",
                                    )
                                    + "\n"
                                )
                    else:
                        report += (
                            row_fmt.format(
                                colorize(category_name, category_colors.get(category_name, "white")), "-", "-", "None"
                            )
                            + "\n"
                        )

        return report
