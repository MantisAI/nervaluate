[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
&nbsp;
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
&nbsp;
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
&nbsp;
![GitHub](https://img.shields.io/github/license/ivyleavedtoadflax/nervaluate)
&nbsp;
![Pull Requests Welcome](https://img.shields.io/badge/pull%20requests-welcome-brightgreen.svg)
&nbsp;
![PyPI](https://img.shields.io/pypi/v/nervaluate)

# nervaluate

`nervaluate` is a python module for evaluating Named Entity Recognition (NER) models as defined in the SemEval 2013 - 9.1 task.

The evaluation metrics output by nervaluate go beyond a simple token/tag based schema, and consider different scenarios 
based on whether all the tokens that belong to a named entity were classified or not, and also whether the correct 
entity type was assigned.

This full problem is described in detail in the [original blog](http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/) 
post by [David Batista](https://github.com/davidsbatista), and extends the code in the [original repository](https://github.com/davidsbatista/NER-Evaluation) which accompanied the blog post.

The code draws heavily on:

* [SemEval-2013 Task 9 : Extraction of Drug-Drug Interactions from Biomedical Texts (DDIExtraction 2013)](https://www.aclweb.org/anthology/S13-2056)

## Token level evaluation for NER is too simplistic

When running machine learning models for NER, it is common to report metrics at the individual token level. This may 
not be the best approach, as a named entity can be made up of multiple tokens, so a full-entity accuracy would be 
desirable.

When comparing the golden standard annotations with the output of a NER system different scenarios might occur:

__I. Surface string and entity type match__

|Token|Gold|Prediction|
|---|---|---|
|in|O|O|
|New|B-LOC|B-LOC|
|York|I-LOC|I-LOC|
|.|O|O|

__II. System hypothesized an incorrect entity__

|Token|Gold|Prediction|
|---|---|---|
|an|O|O|
|Awful|O|B-ORG|
|Headache|O|I-ORG|
|in|O|O|

__III. System misses an entity__

|Token|Gold|Prediction|
|---|---|---|
|in|O|O|
|Palo|B-LOC|O|
|Alto|I-LOC|O|
|,|O|O|

Based on these three scenarios we have a simple classification evaluation that can be measured in terms of false 
positives, true positives, false negatives and false positives, and subsequently compute precision, recall and 
F1-score for each named-entity type.

However, this simple schema ignores the possibility of partial matches or other scenarios when the NER system gets
the named-entity surface string correct but the type wrong, and we might also want to evaluate these scenarios 
again at a full-entity level.

For example:

__IV. System assigns the wrong entity type__

|Token|Gold|Prediction|
|---|---|---|
|I|O|O|
|live|O|O|
|in|O|O|
|Palo|B-LOC|B-ORG|
|Alto|I-LOC|I-ORG|
|,|O|O|

__V. System gets the boundaries of the surface string wrong__

|Token|Gold|Prediction|
|---|---|---|
|Unless|O|B-PER|
|Karl|B-PER|I-PER|
|Smith|I-PER|I-PER|
|resigns|O|O|

__VI. System gets the boundaries and entity type wrong__

|Token|Gold|Prediction|
|---|---|---|
|Unless|O|B-ORG|
|Karl|B-PER|I-ORG|
|Smith|I-PER|I-ORG|
|resigns|O|O|

How can we incorporate these described scenarios into evaluation metrics? See the [original blog](http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/) 
for a great explanation, a summary is included here:

We can use the following five metrics to consider difference categories of errors:

|Error type|Explanation|
|---|---|
|Correct (COR)|both are the same|
|Incorrect (INC)|the output of a system and the golden annotation don’t match|
|Partial (PAR)|system and the golden annotation are somewhat “similar” but not the same|
|Missing (MIS)|a golden annotation is not captured by a system|
|Spurious (SPU)|system produces a response which doesn’t exist in the golden annotation|

These five metrics can be measured in four different ways:

|Evaluation schema|Explanation|
|---|---|
|Strict|exact boundary surface string match and entity type|
|Exact|exact boundary match over the surface string, regardless of the type|
|Partial|partial boundary match over the surface string, regardless of the type|
|Type|some overlap between the system tagged entity and the gold annotation is required|

These five errors and four evaluation schema interact in the following ways:

|Scenario|Gold entity|Gold string|Pred entity|Pred string|Type|Partial|Exact|Strict|
|---|---|---|---|---|---|---|---|---|
|III|BRAND|tikosyn| | |MIS|MIS|MIS|MIS|
|II| | |BRAND|healthy|SPU|SPU|SPU|SPU|
|V|DRUG|warfarin|DRUG|of warfarin|COR|PAR|INC|INC|
|IV|DRUG|propranolol|BRAND|propranolol|INC|COR|COR|INC|
|I|DRUG|phenytoin|DRUG|phenytoin|COR|COR|COR|COR|
|VI|GROUP|contraceptives|DRUG|oral contraceptives|INC|PAR|INC|INC|

Then precision/recall/f1-score are calculated for each different evaluation schema. In order to achieve data, two more 
quantities need to be calculated:

```
POSSIBLE (POS) = COR + INC + PAR + MIS = TP + FN
ACTUAL (ACT) = COR + INC + PAR + SPU = TP + FP
```

Then we can compute precision/recall/f1-score, where roughly describing precision is the percentage of correct 
named-entities found by the NER system, and recall is the percentage of the named-entities in the golden annotations 
that are retrieved by the NER system. This is computed in two different ways depending on whether we want an exact 
match (i.e., strict and exact ) or a partial match (i.e., partial and type) scenario:

__Exact Match (i.e., strict and exact )__
```
Precision = (COR / ACT) = TP / (TP + FP)
Recall = (COR / POS) = TP / (TP+FN)
```
__Partial Match (i.e., partial and type)__
```
Precision = (COR + 0.5 × PAR) / ACT = TP / (TP + FP)
Recall = (COR + 0.5 × PAR)/POS = COR / ACT = TP / (TP + FN)
```

__Putting all together:__

|Measure|Type|Partial|Exact|Strict|
|---|---|---|---|---|
|Correct|3|3|3|2|
|Incorrect|2|0|2|3|
|Partial|0|2|0|0|
|Missed|1|1|1|1|
|Spurious|1|1|1|1|
|Precision|0.5|0.66|0.5|0.33|
|Recall|0.5|0.66|0.5|0.33|
|F1|0.5|0.66|0.5|0.33|


## Notes:

In scenarios IV and VI the entity type of the `true` and `pred` does not match, in both cases we only scored against 
the true entity, not the predicted one. You can argue that the predicted entity could also be scored as spurious, 
but according to the definition of `spurious`:

* Spurious (SPU) : system produces a response which does not exist in the golden annotation;

In this case there exists an annotation, but with a different entity type, so we assume it's only incorrect.

## Installation

```
pip install nervaluate
```

## Example:

The main `Evaluator` class will accept a number of formats:

* [prodi.gy](https://prodi.gy) style lists of spans.
* Nested lists containing NER labels.
* CoNLL style tab delimited strings.

### Prodigy spans

```
true = [
    [{"label": "PER", "start": 2, "end": 4}],
    [{"label": "LOC", "start": 1, "end": 2},
     {"label": "LOC", "start": 3, "end": 4}]
]

pred = [
    [{"label": "PER", "start": 2, "end": 4}],
    [{"label": "LOC", "start": 1, "end": 2},
     {"label": "LOC", "start": 3, "end": 4}]
]

from nervaluate import Evaluator

evaluator = Evaluator(true, pred, tags=['LOC', 'PER'])

# Returns overall metrics and metrics for each tag

results, results_per_tag, result_indices, result_indices_by_tag = evaluator.evaluate()

print(results)
```

```
{
    'ent_type':{
        'correct':3,
        'incorrect':0,
        'partial':0,
        'missed':0,
        'spurious':0,
        'possible':3,
        'actual':3,
        'precision':1.0,
        'recall':1.0
    },
    'partial':{
        'correct':3,
        'incorrect':0,
        'partial':0,
        'missed':0,
        'spurious':0,
        'possible':3,
        'actual':3,
        'precision':1.0,
        'recall':1.0
    },
    'strict':{
        'correct':3,
        'incorrect':0,
        'partial':0,
        'missed':0,
        'spurious':0,
        'possible':3,
        'actual':3,
        'precision':1.0,
        'recall':1.0
    },
    'exact':{
        'correct':3,
        'incorrect':0,
        'partial':0,
        'missed':0,
        'spurious':0,
        'possible':3,
        'actual':3,
        'precision':1.0,
        'recall':1.0
    }
}
```

```
print(results_by_tag)
```

```
{
    'LOC':{
        'ent_type':{
            'correct':2,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':2,
            'actual':2,
            'precision':1.0,
            'recall':1.0
        },
        'partial':{
            'correct':2,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':2,
            'actual':2,
            'precision':1.0,
            'recall':1.0
        },
        'strict':{
            'correct':2,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':2,
            'actual':2,
            'precision':1.0,
            'recall':1.0
        },
        'exact':{
            'correct':2,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':2,
            'actual':2,
            'precision':1.0,
            'recall':1.0
        }
    },
    'PER':{
        'ent_type':{
            'correct':1,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':1,
            'actual':1,
            'precision':1.0,
            'recall':1.0
        },
        'partial':{
            'correct':1,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':1,
            'actual':1,
            'precision':1.0,
            'recall':1.0
        },
        'strict':{
            'correct':1,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':1,
            'actual':1,
            'precision':1.0,
            'recall':1.0
        },
        'exact':{
            'correct':1,
            'incorrect':0,
            'partial':0,
            'missed':0,
            'spurious':0,
            'possible':1,
            'actual':1,
            'precision':1.0,
            'recall':1.0
        }
    }
}
```

```
from nervaluate import summary_report_overall_indices

print(summary_report_overall_indices(evaluation_indices=result_indices, error_schema='partial', preds=pred))
```

```
Indices for error schema 'partial':

Correct indices:
  - Instance 0, Entity 0: Label=PER, Start=2, End=4
  - Instance 1, Entity 0: Label=LOC, Start=1, End=2
  - Instance 1, Entity 1: Label=LOC, Start=3, End=4

Incorrect indices:
  - None

Partial indices:
  - None

Missed indices:
  - None

Spurious indices:
  - None
```

### Nested lists

```
true = [
    ['O', 'O', 'B-PER', 'I-PER', 'O'],
    ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O'],
]

pred = [
    ['O', 'O', 'B-PER', 'I-PER', 'O'],
    ['O', 'B-LOC', 'I-LOC', 'B-LOC', 'I-LOC', 'O'],
]

evaluator = Evaluator(true, pred, tags=['LOC', 'PER'], loader="list")

results, results_by_tag, result_indices, result_indices_by_tag = evaluator.evaluate()
```

### CoNLL style tab delimited

```

true = "word\tO\nword\tO\B-PER\nword\tI-PER\n"

pred = "word\tO\nword\tO\B-PER\nword\tI-PER\n"

evaluator = Evaluator(true, pred, tags=['PER'], loader="conll")

results, results_by_tag, result_indices, result_indices_by_tag = evaluator.evaluate()

```

## Extending the package to accept more formats

Additional formats can easily be added to the module by creating a conversion function in `nervaluate/utils.py`, 
for example `conll_to_spans()`. This function must return the spans in the prodigy style dicts shown in the prodigy 
example above.

The new function can then be added to the list of loaders in `nervaluate/nervaluate.py`, and can then be selection 
with the `loader` argument when instantiating the `Evaluator` class.

A list of formats we intend to include is included in https://github.com/ivyleavedtoadflax/nervaluate/issues/3.


## Contributing to the nervaluate package

Improvements, adding new features and bug fixes are welcome. If you wish to participate in the development of nervaluate 
please read the guidelines in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

---

Give a ⭐️ if this project helped you!
