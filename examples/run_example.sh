#!/bin/bash

pip install nltk
pip install sklearn
pip install sklearn_crfsuite
python -m nltk.downloader conll2002
python example_no_loader.py
