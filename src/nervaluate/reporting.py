def summary_report_ent(results_agg_entities_type: dict, scenario: str = "strict", digits: int = 2) -> str:
    """
    Generate a summary report of the evaluation results for a given scenario.

    :param results_agg_entities_type: Dictionary containing the evaluation results.
    :param scenario: The scenario to report on.
    :param digits: The number of digits to round the results to.

    :returns:
        A string containing the summary report.

    :raises Exception:
        If the scenario is invalid.
    """
    if scenario not in {"strict", "ent_type", "partial", "exact"}:
        raise ValueError("Invalid scenario: must be one of 'strict', 'ent_type', 'partial', 'exact'")

    target_names = sorted(results_agg_entities_type.keys())
    headers = ["correct", "incorrect", "partial", "missed", "spurious", "precision", "recall", "f1-score"]
    rows = [headers]

    for ent_type, results in sorted(results_agg_entities_type.items()):
        for _, v in results.items():
            rows.append(
                [
                    ent_type,
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
                    if preds != [[]]:
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
