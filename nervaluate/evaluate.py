import json
import typer
from wasabi import MarkdownRenderer

from nervaluate import Evaluator


def evaluate(
        true_path: str = typer.Argument(help="Path to true entity labels", default=""),
        pred_path: str = typer.Argument(help="Path to predicted entity labels", default=""),
        tags: str = typer.Argument(
            None, help="Comma separated list of tags to include in the evaluation"
        ),
        loader: str = typer.Option(
            None,
            help="Optional loader when not using prodigy style spans. One of [list, conll]",
        ),
        by_tag: bool = typer.Option(
            None,
            help="If set, will return tag level results instead of aggregated results.",
        ),
        pretty: bool = typer.Option(
            None,
            help="If set, will print the results in a pretty format instead of returning the raw json",
        ),
):
    if loader == "conll":

        with open(true_path) as true_path_file:
            true = true_path_file.readline().strip("\n").replace("\\t", "\t").replace("\\n", "\n")
        with open(pred_path) as pred_path_file:
            pred = pred_path_file.readline().strip("\n").replace("\\t", "\t").replace("\\n", "\n")

    else:

        true = []
        with open(true_path) as true_path_file:
            for line in true_path_file:
                true.append(json.loads(line))

        pred = []
        with open(pred_path) as pred_path_file:
            for line in pred_path_file:
                pred.append(json.loads(line))

    tags_list = tags.split(",")
    evaluator = Evaluator(true=true, pred=pred, tags=tags_list, loader=loader)

    results, results_by_tag = evaluator.evaluate()

    if by_tag:
        output = results_by_tag
    else:
        output = results

    if pretty:
        md = MarkdownRenderer()
        md.add(md.code_block(output))
        typer.echo(md.text)
        return md.text
    else:
        typer.echo(output)
        return output
