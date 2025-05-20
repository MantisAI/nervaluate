from typing import Union
from xml.dom.minidom import Entity


def summary_report(results: dict, mode: str = "overall", scenario: str = "strict", digits: int = 2) -> str:
    """
    Generate a summary report of the evaluation results.

    :param results: Dictionary containing the evaluation results.
    :param mode: Either 'overall' for overall metrics or 'entities' for per-entity metrics.
    :param scenario: The scenario to report on. Must be one of: 'strict', 'ent_type', 'partial', 'exact'.
                     Only used when mode is 'entities'. Defaults to 'strict'.
    :param digits: The number of digits to round the results to.

    :returns:
        A string containing the summary report.

    :raises:
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

    if mode == "overall":
        # Process overall results
        for eval_schema in valid_scenarios:
            if eval_schema not in results:
                continue
            results_schema = results[eval_schema]
            rows.append(
                [
                    eval_schema,
                    results_schema["correct"],
                    results_schema["incorrect"],
                    results_schema["partial"],
                    results_schema["missed"],
                    results_schema["spurious"],
                    results_schema["precision"],
                    results_schema["recall"],
                    results_schema["f1"],
                ]
            )
    else:
        # Process entity-specific results
        target_names = sorted(results.keys())
        for ent_type in target_names:
            if scenario not in results[ent_type]:
                raise ValueError(f"Scenario '{scenario}' not found in results for entity type '{ent_type}'")

            results_ent = results[ent_type][scenario]
            rows.append(
                [
                    ent_type,
                    results_ent["correct"],
                    results_ent["incorrect"],
                    results_ent["partial"],
                    results_ent["missed"],
                    results_ent["spurious"],
                    results_ent["precision"],
                    results_ent["recall"],
                    results_ent["f1"],
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


# For backward compatibility
def summary_report_ent(results_agg_entities_type: dict, scenario: str = "strict", digits: int = 2) -> str:
    """Alias for summary_report with mode='entities'"""
    return summary_report(results_agg_entities_type, mode="entities", scenario=scenario, digits=digits)


def summary_report_overall(results: dict, digits: int = 2) -> str:
    """Alias for summary_report with mode='overall'"""
    return summary_report(results, mode="overall", digits=digits)


def summary_report_ents_indices(evaluation_agg_indices: dict, error_schema: str, preds: list | None = None) -> str:
    """
    Generate a summary report of the evaluation results for the overall scenario.

    :param evaluation_agg_indices: Dictionary containing the evaluation results.
    :param error_schema: The error schema to report on.
    :param preds: List of predicted named entities.

    :returns:
        A string containing the summary report.
    """
    if preds is None:
        preds = [[]]
    report = ""
    for entity_type, entity_results in evaluation_agg_indices.items():
        report += f"\nEntity Type: {entity_type}\n"
        error_data = entity_results[error_schema]
        report += f"  Error Schema: '{error_schema}'\n"
        for category, indices in error_data.items():
            category_name = category.replace("_", " ").capitalize()
            report += f"    ({entity_type}) {category_name}:\n"
            if indices:
                for instance_index, entity_index in indices:
                    if preds is not None and preds != [[]]:
                        pred = preds[instance_index][entity_index]
                        prediction_info = f"Label={pred['label']}, Start={pred['start']}, End={pred['end']}"
                        report += f"      - Instance {instance_index}, Entity {entity_index}: {prediction_info}\n"
                    else:
                        report += f"      - Instance {instance_index}, Entity {entity_index}\n"
            else:
                report += "      - None\n"
    return report


def summary_report_overall_indices(evaluation_indices: dict, error_schema: str, preds: list | None = None) -> str:
    """
    Generate a summary report of the evaluation results for the overall scenario.

    :param evaluation_indices: Dictionary containing the evaluation results.
    :param error_schema: The error schema to report on.
    :param preds: List of predicted named entities.

    :returns:
        A string containing the summary report.
    """
    report = ""
    assert error_schema in evaluation_indices, f"Error schema '{error_schema}' not found in the results."

    error_data = evaluation_indices[error_schema]
    report += f"Indices for error schema '{error_schema}':\n\n"

    for category, indices in error_data.items():
        category_name = category.replace("_", " ").capitalize()
        report += f"{category_name}:\n"
        if indices:
            for instance_index, entity_index in indices:
                if preds != [[]]:
                    # Retrieve the corresponding prediction
                    pred = preds[instance_index][entity_index]  # type: ignore
                    prediction_info = f"Label={pred['label']}, Start={pred['start']}, End={pred['end']}"
                    report += f"  - Instance {instance_index}, Entity {entity_index}: {prediction_info}\n"
                else:
                    report += f"  - Instance {instance_index}, Entity {entity_index}\n"
        else:
            report += "  - None\n"
        report += "\n"

    return report


def summary_report_v2(results: dict, mode: str = "overall", scenario: str = "strict", digits: int = 2) -> str:
    """
    Generate a summary report of the evaluation results for the new Evaluator class.

    Args:
        results: Dictionary containing the evaluation results from the new Evaluator class.
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

    if mode == "overall":
        # Process overall results
        results_data = results["overall"]
        for eval_schema in valid_scenarios:
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


def summary_report_indices_v2(  # pylint: disable=too-many-branches
    results: dict, mode: str = "overall", scenario: str = "strict", preds: list | None = None
) -> str:
    """
    Generate a summary report of the evaluation indices for the new Evaluator class.

    Args:
        results: Dictionary containing the evaluation results from the new Evaluator class.
        mode: Either 'overall' for overall metrics or 'entities' for per-entity metrics.
        scenario: The scenario to report on. Must be one of: 'strict', 'ent_type', 'partial', 'exact'.
                 Only used when mode is 'entities'. Defaults to 'strict'.
        preds: List of predicted named entities. Can be either:
              - List of lists of entity objects with label, start, end attributes
              - List of lists of strings (BIO tags)

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

    if preds is None:
        preds = [[]]

    def get_prediction_info(pred: Union[Entity, str]) -> str:
        """Helper function to get prediction info based on pred type."""
        if isinstance(pred, Entity):
            return f"Label={pred.label}, Start={pred.start}, End={pred.end}"  # type: ignore
        # String (BIO tag)
        return f"Tag={pred}"

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
                    if preds != [[]]:
                        pred = preds[instance_index][entity_index]
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
                        if preds != [[]]:
                            pred = preds[instance_index][entity_index]
                            prediction_info = get_prediction_info(pred)
                            report += f"      - Instance {instance_index}, Entity {entity_index}: {prediction_info}\n"
                        else:
                            report += f"      - Instance {instance_index}, Entity {entity_index}\n"
                else:
                    report += "      - None\n"

    return report
