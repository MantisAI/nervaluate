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
pip install git+https://github.com/ivyleavedtoadflax/nervaluate
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

You can see a working example in the following notebook:

- [examples/example-full-named-entity-evaluation.ipynb](examples/example-full-named-entity-evaluation.ipynb)

