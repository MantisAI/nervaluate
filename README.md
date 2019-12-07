# nervaluate

nervaluate is a python module for evaluating Named Entity Recognition (NER) models as defined in the SemEval 2013 - 9.1 task.

The evaluation metrics output by nervaluate go beyond a simple token/tag based schema, and consider diferent scenarios based on wether all the tokens that belong to a named entity were classified or not, and also wether the correct entity type was assigned.

This problem is described in detail in the [original blog](http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/) post by [David Batista](https://github.com/davidsbatista), and extends the code in the [original repository](https://github.com/davidsbatista/NER-Evaluation) which accompanied the blog post.

The code draws heavily on:

* Segura-bedmar, I., & Mart, P. (2013). 2013 SemEval-2013 Task 9 Extraction of Drug-Drug Interactions from. Semeval, 2(DDIExtraction), 341–350. [link](https://www.aclweb.org/anthology/S13-2056)
* https://www.cs.york.ac.uk/semeval-2013/task9/data/uploads/semeval_2013-task-9_1-evaluation-metrics.pdf

## Notes:

In scenarios IV and VI the entity type of the `true` and `pred` does not match, in both cases we only scored against the true entity, not the predicted one. You can argue that the predicted entity could also be scored as spurious, but according to the definition of `spurius`:

* Spurius (SPU) : system produces a response which doesn’t exist in the golden annotation;

In this case there exists an annotation, but with a different entity type, so we assume it's only incorrect.

## Installation

To install the package:

```
pip install nervaluate
```

To create a virtual environment for development:

```
make virtualenv

# Then to activate the virtualenv:

source /build/virtualenv/bin/activate
```

Alternatively you can use your own virtualenv manager and simply `make reqs` to install requirements.

To run tests:

```
# Will run tox

make test
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

results, results_per_tag = evaluator.evaluate()

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

results, results_by_tag = evaluator.evaluate()
```

### CoNLL style tab delimited

```

true = "word\tO\nword\tO\B-PER\nword\tI-PER\n"

pred = "word\tO\nword\tO\B-PER\nword\tI-PER\n"

evaluator = Evaluator(true, pred, tags=['PER'], loader="conll")

results, results_by_tag = evaluator.evaluate()

```

## Extending the package to accept more formats

Additional formats can easily be added to the module by creating a converstion function in `nervaluate/utils.py`, for example `conll_to_spans()`. This function must return the spans in the prodigy style dicts shown in the prodigy example above.

The new function can then be added to the list of loaders in `nervaluate/nervaluate.py`, and can then be selection with the `loader` argument when instantiating the `Evaluator` class.

A list of formats we intend to include is included in https://github.com/ivyleavedtoadflax/nervaluate/issues/3.
