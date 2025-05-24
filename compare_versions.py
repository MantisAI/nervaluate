from nervaluate.evaluator import Evaluator

true = [
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
    ['O', 'B-LOC', 'B-PER', 'I-PER', 'O', 'O', 'B-DATE'],
]

pred = [
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
    ['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'O', 'B-DATE'],
]

# Example text for reference:
# "The John Smith who works at Google Inc"
# "In Paris Marie Curie lived in 1895"

new_evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")

print(new_evaluator.summary_report())

# The old evaluator for comparison

from nervaluate import Evaluator
old_evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")

from nervaluate.reporting import summary_report_overall_indices, summary_report_ents_indices, summary_report_overall
results = old_evaluator.evaluate()[0]  # Get the first element which contains the overall results
print(summary_report_overall(results))