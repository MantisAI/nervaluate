from nervaluate.evaluator import Evaluator

true = [
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
    ['O', 'B-LOC', 'B-PER', 'I-PER', 'O', 'O', 'B-DATE'],
]

pred = [
    ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
    ['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'I-PER', 'O', 'B-DATE', 'I-DATE', 'O'],
]

# Example text for reference:
# "The John Smith who works at Google Inc"
# "In Paris Marie Curie lived in 1895"

new_evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")

print(new_evaluator.summary_report())

from nervaluate import Evaluator
old_evaluator = Evaluator(true, pred, tags=['PER', 'ORG', 'LOC', 'DATE'], loader="list")