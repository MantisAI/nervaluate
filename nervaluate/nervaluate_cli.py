import json
import typer

from nervaluate import Evaluator

app = typer.Typer()


@app.command()
def nervaluate(
        data_path: str,
        show_results_by_tag: bool = False):
    with open(data_path) as f:
        line = f.readline()
        example = json.loads(line)
        true = example["true"]
        pred = example["pred"]
        tags = example["tags"]
        loader = example["loader"]
        loader = None if loader == 'None' else loader

    evaluator = Evaluator(true, pred, tags=tags, loader=loader)

    results, results_by_tag = evaluator.evaluate()

    if show_results_by_tag:
        output = {
            "results": results,
            "results_by_tag": results_by_tag
        }
    else:
        output = {
            "results": results
        }

    return output


if __name__ == "__main__":
    app()
