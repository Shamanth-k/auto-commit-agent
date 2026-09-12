from pathlib import Path

from app.executors.base import BaseExecutor


class DocumentationExecutor(BaseExecutor):
    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_installation_section": self._add_installation_section,
            "add_project_structure_section": self._add_project_structure_section,
            "add_testing_section": self._add_testing_section,
            "add_configuration_section": self._add_configuration_section,
            "add_calculator_examples": self._add_calculator_examples,
            "add_text_utils_examples": self._add_text_utils_examples,
            "add_validator_examples": self._add_validator_examples,
            "add_file_utils_examples": self._add_file_utils_examples,
            "add_contributing_section": self._add_contributing_section,
            "add_usage_section": self._add_usage_section,
            "add_api_reference_section": self._add_api_reference_section,
            "add_error_handling_section": self._add_error_handling_section,
            "add_development_workflow_section": self._add_development_workflow_section,
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(f"Unsupported documentation action: {action}")

        executor(repository)

    def _get_readme(self, repository: Path) -> Path:
        readme = repository / "README.md"

        if not readme.exists():
            raise FileNotFoundError("README.md not found.")

        return readme

    def _append_section(self, repository: Path, heading: str, content: str) -> None:
        readme = self._get_readme(repository)
        existing = readme.read_text(encoding="utf-8")

        if heading in existing:
            raise RuntimeError(f"Documentation section already exists: {heading}")

        updated = existing.rstrip() + "\n\n" + content.strip() + "\n"
        readme.write_text(updated, encoding="utf-8")

    def _add_installation_section(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Installation",
            """
## Installation

Clone the repository and install the project dependencies:

```bash
git clone <repository-url>
cd auto-commit-test-repo
pip install -r requirements.txt
```
""",
        )

    def _add_project_structure_section(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Project Structure",
            """
## Project Structure

The project is organized into source modules and tests. Example layout:

```
src/
  calculator.py
  text_utils.py
  validator.py
  config.py
  file_utils.py

tests/
  test_calculator.py
  test_text_utils.py
  test_validator.py
  test_config.py
  test_file_utils.py
```
""",
        )

    def _add_testing_section(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Testing",
            """
## Testing

Run the complete test suite with:

```bash
python -m pytest
```

The tests cover the calculator, text utilities, validators, configuration utilities, and file utilities.
""",
        )

    def _add_configuration_section(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Configuration",
            """
## Configuration

Configuration values are defined in `src/config.py`.

The default configuration includes (example):

- debug
- timeout
- max_retries
- environment

Use `get_config_value()` to retrieve a configuration value and `merge_config()` to apply overrides.
""",
        )

    def _add_calculator_examples(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Calculator Examples",
            """
## Calculator Examples

Calculator functions can be imported from `src.calculator`:

```python
from src.calculator import add, multiply, divide

add(2, 3)
multiply(4, 5)
divide(10, 2)
```

Division by zero raises `ValueError`.
""",
        )

    def _add_text_utils_examples(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Text Utilities Examples",
            """
## Text Utilities Examples

Text helpers are available from `src.text_utils`:

```python
from src.text_utils import (
    normalize_text,
    reverse_text,
    word_count,
)

normalize_text("  Hello   World  ")
reverse_text("hello")
word_count("one two three")
```
""",
        )

    def _add_validator_examples(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Validator Examples",
            """
## Validator Examples

Validation helpers are available from `src.validator`:

```python
from src.validator import (
    is_valid_email,
    is_valid_age,
    is_valid_username,
)

is_valid_email("user@example.com")
is_valid_age(25)
is_valid_username("developer")
```
""",
        )

    def _add_file_utils_examples(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## File Utilities Examples",
            """
## File Utilities Examples

File helpers are available from `src.file_utils`:

```python
from src.file_utils import (
    file_exists,
    read_text_file,
    write_text_file,
)

write_text_file("example.txt", "hello")
file_exists("example.txt")
read_text_file("example.txt")
```
""",
        )

    def _add_contributing_section(self, repository: Path) -> None:
        self._append_section(
            repository,
            "## Contributing",
            """
## Contributing

Before submitting changes:

- Make the required code or documentation change.
- Add or update tests when appropriate.
- Run the complete test suite.
- Review the changes with Git.
- Commit the changes with a clear commit message.
""",
        )

    def _add_usage_section(
        self,
        repository: Path,
    ) -> None:
        self._append_section(
            repository,
            "## Usage",
            """
## Usage

Import the project helpers from the `src` package and call the
functions that match the operation you need.
            """,
        )

    def _add_api_reference_section(
        self,
        repository: Path,
    ) -> None:
        self._append_section(
            repository,
            "## API Reference",
            """
## API Reference

The public helpers are grouped by module:

- `src.calculator` for arithmetic operations.
- `src.text_utils` for text processing.
- `src.validator` for input validation.
- `src.config` for configuration helpers.
- `src.file_utils` for file operations.
            """,
        )

    def _add_error_handling_section(
        self,
        repository: Path,
    ) -> None:
        self._append_section(
            repository,
            "## Error Handling",
            """
## Error Handling

Helpers raise standard Python exceptions when an operation cannot
be completed with the supplied input. Callers should validate
inputs and handle expected exceptions where appropriate.
            """,
        )

    def _add_development_workflow_section(
        self,
        repository: Path,
    ) -> None:
        self._append_section(
            repository,
            "## Development Workflow",
            """
## Development Workflow

A typical development cycle is:

1. Make a focused change.
2. Add or update tests.
3. Run `python -m pytest`.
4. Review the Git diff.
5. Commit the change with a clear message.
            """,
        )
