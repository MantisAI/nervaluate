import warnings


def summary_report_ent(results_agg_entities_type: dict, scenario: str = "strict", digits: int = 2) -> str:
    """
    Generate a summary report of the evaluation results for a given scenario.

    :param results_agg_entities_type: Dictionary containing the evaluation results.
    :param scenario: The scenario to report on. Must be one of: 'strict', 'ent_type', 'partial', 'exact'.
                    Defaults to 'strict'.
    :param digits: The number of digits to round the results to.

    :returns:
        A string containing the summary report.

    :raises ValueError:
        If the scenario is invalid.
    """
    warnings.warn(
        "summary_report_ent() is deprecated and will be removed in a future release. "
        "In the future the Evaluator will contain a method `summary_report` with the same functionality.",
        DeprecationWarning,
        stacklevel=2
    )

    valid_scenarios = {"strict", "ent_type", "partial", "exact"}
    if scenario not in valid_scenarios:
        raise ValueError(f"Invalid scenario: must be one of {valid_scenarios}")

    target_names = sorted(results_agg_entities_type.keys())
    headers = ["correct", "incorrect", "partial", "missed", "spurious", "precision", "recall", "f1-score"]
    rows = [headers]

    # Aggregate results by entity type for the specified scenario
    for ent_type in target_names:
        if scenario not in results_agg_entities_type[ent_type]:
            raise ValueError(f"Scenario '{scenario}' not found in results for entity type '{ent_type}'")

        results = results_agg_entities_type[ent_type][scenario]
        rows.append(
            [
                ent_type,
                results["correct"],
                results["incorrect"],
                results["partial"],
                results["missed"],
                results["spurious"],
                results["precision"],
                results["recall"],
                results["f1"],
            ]
        )

    name_width = max(len(cn) for cn in target_names)
    width = max(name_width, digits)
    head_fmt = "{:>{width}s} " + " {:>11}" * len(headers)
    report = head_fmt.format("", *headers, width=width)
    report += "\n\n"
    row_fmt = "{:>{width}s} " + " {:>11}" * 5 + " {:>11.{digits}f}" * 3 + "\n"

    for row in rows[1:]:
        report += row_fmt.format(*row, width=width, digits=digits)

    return report


def summary_report_overall(results: dict, digits: int = 2) -> str:
    """
    Generate a summary report of the evaluation results for the overall scenario.

    :param results: Dictionary containing the evaluation results.
    :param digits: The number of digits to round the results to.

    :returns:
        A string containing the summary report.
    """
    warnings.warn(
        "summary_report_overall() is deprecated and will be removed in a future. "
        "In the future the Evaluator will contain a method `summary_report` with the same functionality.",
        DeprecationWarning,
        stacklevel=2
    )


    headers = ["correct", "incorrect", "partial", "missed", "spurious", "precision", "recall", "f1-score"]
    rows = [headers]

    for k, v in results.items():
        rows.append(
            [
                k,
                v["correct"],
                v["incorrect"],
                v["partial"],
                v["missed"],
                v["spurious"],
                v["precision"],
                v["recall"],
                v["f1"],
            ]
        )

    target_names = sorted(results.keys())
    name_width = max(len(cn) for cn in target_names)
    width = max(name_width, digits)
    head_fmt = "{:>{width}s} " + " {:>11}" * len(headers)
    report = head_fmt.format("", *headers, width=width)
    report += "\n\n"
    row_fmt = "{:>{width}s} " + " {:>11}" * 5 + " {:>11.{digits}f}" * 3 + "\n"

    for row in rows[1:]:
        report += row_fmt.format(*row, width=width, digits=digits)

    return report


def summary_report_ents_indices(evaluation_agg_indices: dict, error_schema: str, preds: list | None = None) -> str:
    """
    Generate a summary report of the evaluation results for the overall scenario.

    :param evaluation_agg_indices: Dictionary containing the evaluation results.
    :param error_schema: The error schema to report on.
    :param preds: List of predicted named entities.

    :returns:
        A string containing the summary report.
    """
    warnings.warn(
        "summary_report_ents_indices() is deprecated and will be made part of the Evaluator class in the future. "
        "In the future the Evaluator will contain a method `summary_report_indices` with the same functionality.",
        DeprecationWarning,
        stacklevel=2
    )


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
    warnings.warn(
        "summary_report_ents_indices() is deprecated and will be removed in a future release. "
        "In the future the Evaluator will contain a method `summary_report_indices` with the same functionality.",
        DeprecationWarning,
        stacklevel=2
    )
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
