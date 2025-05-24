from nervaluate.evaluator import Evaluator

true = [
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
    ['O', 'B-LOC', 'B-PER', 'I-PER', 'O', 'O', 'B-DATE'],
]

pred = [
    # ['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG'],
    ['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'O', 'B-DATE'],
]

"""

['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG']
['O', 'B-PER', 'I-PER', 'O', 'O', 'O', 'B-ORG', 'I-ORG']


              correct   incorrect     partial      missed    spurious   precision      recall    f1-score

ent_type           4           0           0           0           0        1.00        1.00        1.00
   exact           4           0           0           0           0        1.00        1.00        1.00
 partial           4           0           0           0           0        1.00        1.00        1.00
  strict           4           0           0           0           0        1.00        1.00        1.00

  
['O', 'B-LOC', 'B-PER', 'I-PER', 'O', 'O', 'B-DATE']
['O', 'B-LOC', 'I-LOC', 'O', 'B-PER', 'O', 'B-DATE']

              correct   incorrect     partial      missed    spurious   precision      recall    f1-score

ent_type         2          1           0            1           1
   exact         2          1           0            1           1
 partial         3          0           0            1           1
  strict         2          1           0            1           1
"""


# Strict 	exact boundary surface string match and entity type
# Exact 	exact boundary match over the surface string, regardless of the type
# Type 	    some overlap between the system tagged entity and the gold annotation is required
# Partial 	partial boundary match over the surface string, regardless of the type


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