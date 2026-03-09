Changelog
=========


(unreleased)
------------
- EntityType strategy: when multiple true entities of the same type overlap a prediction,
  the matched true entity is now chosen by closest boundaries (not list order). Aggregate
  counts (correct, missed, etc.) are unchanged; ``missed_indices`` may list a different
  true-entity index in those cases. [David S. Batista]
- Testing for single character entities. [David S. Batista]
- Fixing linting issues. [David S. Batista]
- Defining a min ground truth percentage to be considered an overlap.
  [David S. Batista]
- Chore: removing script to compare old and new version outputs. [David
  S. Batista]


1.0.0 (2025-08-18)
------------------
- 1.0.0 release. [David S. Batista]
- Bumping version. [David S. Batista]
- Removing pandas dependency. [David S. Batista]
- Relaxing tests invalid mode and scenario. [David S. Batista]
- Saving to CSV file or return CSV string. [David S. Batista]
- Adds tests for result indices in all strategies. [Jack Boylan]
- Adds indices tests for `ent_type` strategy. [Jack Boylan]
- Linting import statment. [David S. Batista]
- Wip: using hatch in contributing. [David S. Batista]
- Updating CITATION and removing flake. [David S. Batista]
- Renaming evaluation_strategies to strategies and improving README.
  [David S. Batista]
- Removing old files. [David S. Batista]
- Removing old files. [David S. Batista]
- Updating README.MD. [David S. Batista]
- One more use case. [David S. Batista]
- Comparative indices report overall. [David S. Batista]
- Wip: fixing report indices. [David S. Batista]
- Wip. [David S. Batista]
- Wip: fixing report for entities. [David S. Batista]
- Adding function to generate synthetic data. [David S. Batista]
- Wip: fixing report for entities. [David S. Batista]
- Wip: fixing report for entities. [David S. Batista]
- Only showing entities report for entities that actually apper on
  either true or pred data. [David S. Batista]
- Wip: checking summary with aggregated entities and a specific
  scenario. [David S. Batista]
- Wip: checking summary with aggregated entities and a specific
  scenario. [David S. Batista]
- Updating evaluation strategies tests. [David S. Batista]
- Correcting and fixing type strategy. [David S. Batista]
- Correcting and fixing strict strategy. [David S. Batista]
- Correcting and fixing partial strategy. [David S. Batista]
- Adding partial to evaluation strategies. [David S. Batista]
- Fixing docs lenghts tests. [David S. Batista]
- Fixing docs lenghts tests. [David S. Batista]
- Working on comparative example. [David S. Batista]
- Fixes. [David S. Batista]
- Fxing empty entities. [David S. Batista]
- Fixing imports. [David S. Batista]
- Moving reporting to the Evaluator class. [David S. Batista]
- Working on new versions of summary reports. [David S. Batista]
- Cleaning up README.MD. [David S. Batista]
- Adding missed pyproject.toml. [David S. Batista]
- Type checking. [David S. Batista]
- Fixing all tests. [David S. Batista]
- Adding refactored code. [David S. Batista]
- Separating new and old evaluator logic. [David S. Batista]
- Fixing loaders. [David S. Batista]
- Fixing loading test_conll_loader. [David S. Batista]
- Fixing loading test_dict_loader. [David S. Batista]
- Fixing loading test_list_loader. [David S. Batista]
- Adding tests. [David S. Batista]


0.3.1 (2025-06-05)
------------------
- Fixing pandas dependency. [David S. Batista]
- Fixing pandas dependency. [David S. Batista]


0.3.0 (2025-06-05)
------------------

Changes
~~~~~~~
- Update changelog for 0.2.0 release. [Matthew Upson]

Fix
~~~
- Mypy configuration error. [angelo-digian]
- Typo in type annotation. [angelo-digian]
- Switched order of imports. [angelo-digian]

Other
~~~~~
- 0.3.0 release. [David S. Batista]
- Adding deprecation warnings. [David S. Batista]
- Create pull_request_template.md. [David S. Batista]
- Upgrading dev tools versions. [David S. Batista]
- Initial import. [David S. Batista]
- Adding scenario type for summary report. [David S. Batista]
- Update README.md. [David S. Batista]
- Updating README.MD. [David S. Batista]
- Removing unused variable. [David S. Batista]
- Update src/nervaluate/reporting.py. [Copilot, David S. Batista]
- Update src/nervaluate/reporting.py. [Copilot, David S. Batista]
- Removing Makefile. [David S. Batista]
- Drafting CONTRIBUTE.md. [David S. Batista]
- Drafting CONTRIBUTE.md. [David S. Batista]
- Removing flake8. [David S. Batista]
- Removing old config files. [David S. Batista]
- Running on ubuntu, windows and macos. [David S. Batista]
- Reverting to ubuntu only. [David S. Batista]
- Adding new file. [David S. Batista]
- Removing old workflow file. [David S. Batista]
- Adding windows and macos to CI. [David S. Batista]
- Streamlining CI checks. [David S. Batista]
- Disabling old github workflow and triggering new one. [David S.
  Batista]
- Changing github workflow. [David S. Batista]
- Fixing linting and typing issues. [David S. Batista]
- Adding pytest-cov as dependency. [David S. Batista]
- Adding hatch as project manager; linting and typing. [David S.
  Batista]
- Fixing type hints. [David S. Batista]
- Wip. [David S. Batista]
- Adding docstrings. [David S. Batista]
- Adding more tests. [David S. Batista]
- Adding more tests. [David S. Batista]
- Adding docstrings and increasing test coverage. [David S. Batista]
- Removing requirements_dev.txt. [David S. Batista]
- Blackening for py311. [David S. Batista]
- Fixing pyprojec.toml dependencies. [David S. Batista]
- Fixing pyprojec.toml dependencies. [David S. Batista]
- Fixing pyprojec.toml dependencies. [David S. Batista]
- Fixing pyprojec.toml dependencies. [David S. Batista]
- Fixing pyprojec.toml dependencies. [David S. Batista]
- Refactor: move dev dependencies to pyproject.toml and update CI
  workflow. [David S. Batista]
- Adding wrongly removed pre-commit. [David S. Batista]
- Fixing type hints. [David S. Batista]
- Removing unused imports and mutuable default arguments. [David S.
  Batista]
- Update README.md. [Tim Miller]
- Update README.md. [adgianv]
- Update README.md - change the pdf link. [adgianv]
- Added type annotations to functions. [angelo-digian]
- Pandas version downgraded to 2.0.1 because incompatible with python
  version. [angelo-digian]
- Fixed pandas version to 2.2.1. [angelo-digian]
- Add pandas as a dependency in pyproject.toml. [angelo-digian]
- Adding pandas in the requirements file. [angelo-digian]
- Update tests/test_evaluator.py. [David S. Batista]
- Modified results_to_df method and added test. [angelo-digian]
- Expanded evaluator class: added method to return results of the nested
  dictionary as a dataframe. [angelo-digian]


0.2.0 (2024-04-10)
------------------

New
~~~
- Add pre-commit. [Matthew Upson]
- Add CITATION.cff file. [Matthew Upson]
- Upload artefacts to codecov. [Matthew Upson]
- Run tests on windows instance. [Matthew Upson]

Changes
~~~~~~~
- Add codecov config. [Matthew Upson]
- Remove .travis.yml. [Matthew Upson]
- Update tox.ini. [Matthew Upson]
- Update versions to test. [Matthew Upson]
- Add tox tests as github action. [Matthew Upson]

Fix
~~~
- Grant write permission to CICD workflow. [Matthew Upson]
- Run on windows and linux matrix. [Matthew Upson]

Other
~~~~~
- Updates README to reflect new functionality. [Jack Boylan]
- Removes extra 'indices' printed. [Jack Boylan]
- Bump black from 23.3.0 to 24.3.0. [dependabot[bot]]

  Bumps [black](https://github.com/psf/black) from 23.3.0 to 24.3.0.
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/23.3.0...24.3.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:development
  ...
- Fixed Typo in README. [Giovanni Casari]
- Reformats quotes in `test_nervaluate.py` [Jack Boylan]
- Initial import. [David S. Batista]
- Handles case when `predictions` is empty. [Jack Boylan]
- Adds unit tests for evaluation indices output. [Jack Boylan]
- Adds summary print functions for overall indices and per-entity
  indices results. [Jack Boylan]
- Adds `within_instance_index` to evaluation indices outputs. [Jack
  Boylan]
- Ensures compatibility with existing unit tests. [Jack Boylan]
- Adheres to code quality checks. [Jack Boylan]
- Adds more descriptive variable names. [Jack Boylan]
- Adds correct indices to result indices output. [Jack Boylan]
- Moves evaluation indices to separate data structures. [Jack Boylan]
- Adds index lists to output for examples with incorrect, partial,
  spurious, and missed entities. [Jack Boylan]
- Docs: fix typo "spurius" > "spurious" [DanShatford]
- Added test for issue #40. [g.casari]
- Solved issue #40. [g.casari]
- Update README.md. [David S. Batista]
- Cleaning README.MD. [David S. Batista]
- Attending PR comments. [David S. Batista]
- Fixing links on README.MD. [David S. Batista]
- Updating pyproject.toml. [David S. Batista]
- Updating pyproject.toml. [David S. Batista]
- Updating README.MD and bumping version to 0.2.0. [David S. Batista]
- Updating README.MD. [David S. Batista]
- Reverting to Python 3.8. [David S. Batista]
- Adding some badges to the README. [David S. Batista]
- Initial commit. [David S. Batista]
- Wip: adding poetry. [David S. Batista]
- Full working example. [David S. Batista]
- Nit. [David S. Batista]
- Wip: adding summary report and examples. [David S. Batista]
- Wip: adding summary report and examples. [David S. Batista]
- Wip: adding summary report and examples. [David S. Batista]
- Wip: adding summary report and examples. [David S. Batista]
- Wip: adding summary report and examples. [David S. Batista]
- Wip: adding summary report. [David S. Batista]
- Wip: adding summary report. [David S. Batista]
- Removed codecov from requirements.txt. [David S. Batista]
- Removing duplicated code and fixing type hit. [David S. Batista]
- Updated Makefile: install package in editable mode. [David S. Batista]
- Updated name. [David S. Batista]
- Minimum version Python 3.8. [David S. Batista]
- Fixing Makefile and pre-commit. [David S. Batista]
- Adding DS_Store and .idea to gitignore. [David S. Batista]
- Updating Makefile. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- WIP: pre-commit. [David S. Batista]
- Fixing types. [David S. Batista]
- Finished adding type hints, some were skipped, code needs refactoring.
  [David S. Batista]
- WIP: adding type hints. [David S. Batista]
- WIP: adding type hints. [David S. Batista]
- WIP: adding type hints. [David S. Batista]
- WIP: adding type hints. [David S. Batista]
- Adding some execptions, code needs refactoring. [David S. Batista]
- Fixing pyling and flake8 issues. [David S. Batista]
- Replaced setup.py with pyproject.toml. [David S. Batista]
- Reverting utils import. [David S. Batista]
- Fixing types and wrappint at 120 characters. [David S. Batista]
- Update CITATION.cff. [David S. Batista]

  updating orcid
- Fix recall formula readme. [fgh95]
- Update LICENSE. [ivyleavedtoadflax]
- Update LICENSE. [ivyleavedtoadflax]
- Delete .python-version. [ivyleavedtoadflax]


0.1.8 (2020-10-16)
------------------

New
~~~
- Add test for whole span length entities (see #32) [Matthew Upson]
- Summarise blog post in README. [Matthew Upson]

Changes
~~~~~~~
- Bump version in setup.py. [Matthew Upson]
- Update CHANGELOG (#36) [ivyleavedtoadflax]
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


