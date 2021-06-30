import os
import json
import typer
import spacy

from nervaluate import Evaluator

app = typer.Typer()


def create_prodigy_spans(doc):
    pred = []
    for entity in doc.ents:
        pred.append({"label": entity.label_, "start": entity.start, "end": entity.end})
    return pred


def check_labels(meta):
    labels = []
    for item in meta:
        if "label" in item:
            labels.append(item["label"])
    return labels


@app.command()
def nervaluate(model_path: str, data_path: str, results_path: str = "results/"):
    spacy_model = spacy.load(model_path)

    true = []
    pred = []
    tags = {}

    with open(data_path) as f:
        for line in f:
            pattern = json.loads(line)
            text = pattern["text"]
            meta = pattern["meta"]
            labels = check_labels(meta)
            for label in labels:
                tags[label] = ''
            true.append(meta)
            doc = spacy_model(text)
            pred.append(create_prodigy_spans(doc))

    evaluator = Evaluator(true, pred, tags=list(tags.keys()))
    global_results, aggregation_results = evaluator.evaluate()

    global_results_path = os.path.join(results_path, "global_results.json")
    with open(global_results_path, "w") as f:
        f.write(json.dumps(global_results))

    aggregation_results_path = os.path.join(results_path, "aggregation_results.json")
    with open(aggregation_results_path, "w") as f:
        f.write(json.dumps(aggregation_results))
    return


if __name__ == "__main__":
    app()
