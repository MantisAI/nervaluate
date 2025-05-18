# Contributing to `nervaluate`

Thank you for your interest in contributing to `nervaluate`! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/nervaluate.git
   cd nervaluate
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Adding Tests

`nervaluate` uses pytest for testing. Here are the guidelines for adding tests:

1. All new features and bug fixes should include tests
2. Tests should be placed in the `tests/` directory
3. Test files should be named `test_*.py`
4. Test functions should be named `test_*`
5. Use pytest fixtures when appropriate for test setup and teardown


## Changelog Management

`nervaluate` uses gitchangelog to maintain the CHANGELOG.rst file. Here's how to use it:

1. Make your changes in a new branch
2. Write your commit messages following these conventions:
   - Use present tense ("Add feature" not "Added feature")
   - Use imperative mood ("Move cursor to..." not "Moves cursor to...")
   - Limit the first line to 72 characters or less
   - Reference issues and pull requests liberally after the first line

3. The commit message format should be:
   ```
   type(scope): subject

   body
   ```

   Where type can be:
   - feat: A new feature
   - fix: A bug fix
   - docs: Documentation changes
   - style: Changes that do not affect the meaning of the code
   - refactor: A code change that neither fixes a bug nor adds a feature
   - perf: A code change that improves performance
   - test: Adding missing tests or correcting existing tests
   - chore: Changes to the build process or auxiliary tools

4. After committing your changes, you can generate the changelog:
   ```bash
   gitchangelog > CHANGELOG.rst
   ```

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the CHANGELOG.rst using gitchangelog
3. The PR will be merged once you have the sign-off of at least one other developer
4. Make sure all tests pass and there are no linting errors

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Run pre-commit hooks before committing:
  ```bash
  pre-commit run --all-files
  ```

## Questions?

Feel free to open an issue if you have any questions about contributing to `nervaluate`. 