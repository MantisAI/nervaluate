Changelog
=========


0.1.8 (2020-10-16)
------------------

New
~~~
- Add test for whole span length entities (see #32) [Matthew Upson]
- Summarise blog post in README. [Matthew Upson]

Changes
~~~~~~~
- Fix tests to match #32. [Matthew Upson]

Fix
~~~
- Correct catch sequence of just one entity. [Matthew Upson]

  Incorporate edits in #28 but includes tests.

Other
~~~~~
- Add code coverage. [ivyleavedtoadflax]
- Crucial fixes for evaluation. [Alex Flückiger]
- Update utils.py. [ivyleavedtoadflax]

  Tiny change to kick off CI
- Fix to catch last entites Small change to catch entities that go up
  until last character when there is no tag. [pim]


0.1.7 (2019-12-07)
------------------

New
~~~
- Add tests. [Matthew Upson]

  * Linting
  * Rename existing tests to disambiguate
- Add loaders to nervaluate. [Matthew Upson]

  * Add list and conll formats

Changes
~~~~~~~
- Update README. [Matthew Upson]

Fix
~~~
- Issue with setup.py. [Matthew Upson]

  * Add docstring to __version__.py


0.1.6 (2019-12-07)
------------------

New
~~~
- Add gitchangelog and Makefile recipe. [Matthew Upson]

Changes
~~~~~~~
- Bump version to 0.1.6. [Matthew Upson]
- Remove examples. [Matthew Upson]

  These are not accessible from the package in any case.
- Add dev requirements. [Matthew Upson]


0.1.5 (2019-12-06)
------------------

Changes
~~~~~~~
- Bump version to 0.1.5. [Matthew Upson]
- Update setup.py. [Matthew Upson]
- Update package url to point at pypi. [Matthew Upson]


0.1.4 (2019-12-06)
------------------

New
~~~
- Add dist to .gitignore. [Matthew Upson]
- Create pypi friendly README/long description. [Matthew Upson]
- Clean entity dicts of extraneous keys. [Matthew Upson]

  * Failing to do this can cause problems in evaluations
  * Add tests

Changes
~~~~~~~
- Bump version to 0.1.4. [Matthew Upson]
- Make setup.py pypi compliant. [Matthew Upson]


0.1.2 (2019-12-04)
------------------

New
~~~
- Add missing prodigy format tests. [Matthew Upson]
- Pass argument when using list. [Matthew Upson]
- Setup module structure. [Matthew Upson]
- Add get_tags() and tests. [Matthew Upson]

  Adds function to extract all the NER tags from a list of sentences.
- Add Evaluator class. [Matthew Upson]

  * Add some logging statements
  * Add input checks on number of documents and tokens per document
  * Allow target labels to be passed as argument to compute_metrics. Note
      that if a label is predicted and it is not in this list, then it
      will be classed as spurious for the aggregated scores, and on each
      entity level result (because it is unclear where the spurious value
      should be applied, it is applied to all)
  * linting
  * Add many new tests
- Don't evaluate precision and recall for each sentence. [Matthew Upson]

  Rather than automatically calculate precision and recall at the sentence
  level, this change adds a new function compute_precision_recall_wrapper
  which can be run after all the metrics whether for 1 document, or 1000,
  have been calculated. This has the benefit that we can reuse the same
  code for calculating precision/recall, and allows us to calculate entity
  level precision/recall if required.
- Calculate entity level score. [Matthew Upson]
- Add compute_actual_possible function. [Matthew Upson]
- Record results for each entity type. [Matthew Upson]
- Add scenario comments matching blog table. [Matthew Upson]
- Test results at individual entity level. [Matthew Upson]
- Add .gitinore file. [Matthew Upson]
- Add requirements.txt. [Matthew Upson]

Changes
~~~~~~~
- Bump version to 0.1.2. [Matthew Upson]
- Bump version number to 0.1.1. [Matthew Upson]
- Reduce logging verbosity. [ivyleavedtoadflax]
- Add example to README.md. [Matthew Upson]
- Create virtualenv recipe. [Matthew Upson]

  * Move example dependencies to requirements_example.txt
  * Add virtualenv recipe to Makefile
  * Update .gitignore
- Remove unused dependencies. [Matthew Upson]

  * Dependencies for the examples should not be included in setup.py, instead
  move them to requirements_examples.txt
- Update example notebook. [Matthew Upson]
- Remove unwanted tags from pred_named_entities. [Matthew Upson]
- Remove superfluous get_tags() function. [Matthew Upson]
- Update notebook. [Matthew Upson]
- Update notebook. [Matthew Upson]
- Update tests. [Matthew Upson]
- Update .gitignore. [Matthew Upson]
- Replace spurius with spurious. [Matthew Upson]
- Update README with requirements and test info. [Matthew Upson]
- Update setup.cfg with source and omit paths. [Matthew Upson]
- Use pytest instead of unittest. [Matthew Upson]

Other
~~~~~
- Revert "Remove tox and use pytest" [Matthew Upson]

  * Better to keep tox for local testing in the Makefile and resolve
    issues running tox on the developers machine.

  This reverts commit 8578795e62ca384adf054c1b85a1c1d7f0d089d5.
- Remove tox and use pytest. [Elizabeth Gallagher]
- Add f1 output to nervaluate and update all tests. [Elizabeth
  Gallagher]
- Update .travis.yml. [ivyleavedtoadflax]
- Update README.md. [Matt Upson]
- Build(deps): bump nltk from 3.4.4 to 3.4.5. [dependabot[bot]]

  Bumps [nltk](https://github.com/nltk/nltk) from 3.4.4 to 3.4.5.
  - [Release notes](https://github.com/nltk/nltk/releases)
  - [Changelog](https://github.com/nltk/nltk/blob/develop/ChangeLog)
  - [Commits](https://github.com/nltk/nltk/compare/3.4.4...3.4.5)
- Update __version__.py. [Matt Upson]
- PEPed8 things a bit. [David Soares Batista]
- Update README.md. [David S. Batista]
- Update README.md. [David S. Batista]
- Notebook. [David Soares Batista]
- Updated notebook. [David Soares Batista]
- Update README.md. [David S. Batista]
- Update README.md. [David S. Batista]
- Renamed notebook. [David Soares Batista]
- Bug fixing. [David Soares Batista]
- Test. [David Soares Batista]
- Typo in comment. [David Soares Batista]
- Use find_overlap to find all overlap cases. [Matthew Upson]

  Adds the find_overlap function which captures the three possible overlap
  scenarios (Total, Start, and End). This is examplained in graph below.

  Character Offset:   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
  True:               |   |   |   |LOC|LOC|LOC|LOC|LOC|   |   |
  Total Overlap:      |   |   |LOC|LOC|LOC|LOC|LOC|LOC|LOC|   |
  Start Overlap:      |   |   |LOC|LOC|LOC|   |   |   |   |   |
  End Overlap:        |   |   |   |   |   |   |LOC|LOC|LOC|   |
- Removed debug stamt. [David Soares Batista]
- Added partial and exact evaluation and tests. [David Soares Batista]
- Update. [David Soares Batista]
- Updated README. [David Soares Batista]
- - fixed bugs and added tests - added pytest. [David Soares Batista]
- Update ner_evaluation.py. [David S. Batista]
- Redefined evaluation according to discussion here:
  https://github.com/davidsbatista/NER-Evaluation/issues/2. [David
  Soares Batista]
- Fixed a BUG in collect_named_entites() issued by
  rjlotok.dblma@gmail.com. [David Soares Batista]
- Update README.md. [David S. Batista]
- Update README.md. [David S. Batista]
- Major refactoring. [David Soares Batista]
- Create README.md. [David S. Batista]
- Initial import. [David Soares Batista]
- Initial commit. [David S. Batista]


