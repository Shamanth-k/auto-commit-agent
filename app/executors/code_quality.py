from pathlib import Path

from app.executors.base import BaseExecutor


class CodeQualityExecutor(BaseExecutor):
    def execute(
        self,
        task: dict,
        repository_path: str,
    ) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_calculator_subtract_docstring": (
                self._add_calculator_subtract_docstring
            ),
            "add_config_module_docstring": (
                self._add_config_module_docstring
            ),
            "add_file_utils_read_docstring": (
                self._add_file_utils_read_docstring
            ),
            "add_validator_phone_length_constant": (
                self._add_validator_phone_length_constant
            ),
            "add_text_utils_module_docstring": (
                self._add_text_utils_module_docstring
            ),
            "add_validator_module_docstring": (
                self._add_validator_module_docstring
            ),
            "add_config_module_docstring": (
                self._add_config_module_docstring
            ),
            "add_calculator_module_docstring": (
                self._add_calculator_module_docstring
            ),
            "add_validator_username_length_constant": (
                self._add_validator_username_length_constant
            ),
            "add_text_utils_separator_constant": (
                self._add_text_utils_separator_constant
            ),
            "add_calculator_add_docstring": (
                self._add_calculator_add_docstring
            ),
            "add_validator_age_docstring": (
                self._add_validator_age_docstring
            ),
            "add_text_utils_reverse_docstring": (
                self._add_text_utils_reverse_docstring
            ),
            "add_config_get_value_docstring": (
                self._add_config_get_value_docstring
            ),
            "add_file_utils_write_docstring": (
                self._add_file_utils_write_docstring
            ),
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(
                f"Unsupported code_quality action: {action}"
            )

        executor(repository)

    def _get_source(
        self,
        repository: Path,
        filename: str,
    ) -> Path:
        source = repository / "src" / filename

        if not source.exists():
            raise FileNotFoundError(
                f"src/{filename} not found."
            )

        return source

    def _replace_once(
        self,
        source: Path,
        old: str,
        new: str,
        description: str,
    ) -> None:
        content = source.read_text(
            encoding="utf-8"
        )

        if old not in content:
            raise RuntimeError(
                f"Expected code not found for: {description}"
            )

        if content.count(old) != 1:
            raise RuntimeError(
                f"Expected exactly one match for: {description}"
            )

        source.write_text(
            content.replace(old, new, 1),
            encoding="utf-8",
        )

    def _add_calculator_subtract_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "calculator.py",
        )

        old = (
            "def subtract(a: float, b: float) -> float:\n"
            "    return a - b"
        )

        new = (
            "def subtract(a: float, b: float) -> float:\n"
            '    """Return the difference between two numbers."""\n'
            "    return a - b"
        )

        self._replace_once(
            source,
            old,
            new,
            "calculator subtract docstring",
        )

    def _add_validator_phone_length_constant(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "validator.py",
        )

        content = source.read_text(
            encoding="utf-8"
        )

        constant = "PHONE_NUMBER_LENGTH = 10"

        if constant in content:
            raise RuntimeError(
                "Validator phone length constant already exists."
            )

        old = (
            "def is_valid_phone(phone: str) -> bool:\n"
            '    digits = phone.replace("-", "").replace(" ", "")\n'
            "    return digits.isdigit() and len(digits) == 10"
        )

        new = (
            "PHONE_NUMBER_LENGTH = 10\n\n\n"
            "def is_valid_phone(phone: str) -> bool:\n"
            '    digits = phone.replace("-", "").replace(" ", "")\n'
            "    return (\n"
            "        digits.isdigit()\n"
            "        and len(digits) == PHONE_NUMBER_LENGTH\n"
            "    )"
        )

        self._replace_once(
            source,
            old,
            new,
            "validator phone length constant",
        )

    def _add_text_utils_module_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "text_utils.py",
        )

        content = source.read_text(
            encoding="utf-8"
        )

        if content.startswith('"""'):
            raise RuntimeError(
                "Text utilities already has a module docstring."
            )

        source.write_text(
            '"""Text processing utilities."""\n\n'
            + content.lstrip(),
            encoding="utf-8",
        )

    def _add_validator_module_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "validator.py",
        )

        content = source.read_text(
            encoding="utf-8"
        )

        if content.startswith('"""'):
            raise RuntimeError(
                "Validator already has a module docstring."
            )

        source.write_text(
            '"""Validation helpers for common input checks."""\n\n'
            + content.lstrip(),
            encoding="utf-8",
        )

    def _add_config_module_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "config.py",
        )

        old = '"""Config utilities."""'

        new = (
            '"""Configuration defaults and helper functions."""'
        )

        self._replace_once(
            source,
            old,
            new,
            "config module docstring",
        )

    def _add_file_utils_read_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "file_utils.py",
        )

        old = (
            "def read_text_file(path: str) -> str:\n"
            '    return Path(path).read_text(encoding="utf-8")'
        )

        new = (
            "def read_text_file(path: str) -> str:\n"
            '    """Read UTF-8 text from a file."""\n'
            '    return Path(path).read_text(encoding="utf-8")'
        )

        self._replace_once(
            source,
            old,
            new,
            "file read docstring",
        )

    def _add_calculator_module_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "calculator.py",
        )

        old = '"""Calculator utilities."""'

        new = (
            '"""Basic arithmetic utilities for numeric values."""'
        )

        self._replace_once(
            source,
            old,
            new,
            "calculator module docstring",
        )

    def _add_validator_username_length_constant(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "validator.py",
        )

        content = source.read_text(
            encoding="utf-8"
        )

        marker = "USERNAME_MIN_LENGTH = 3"

        if marker in content:
            raise RuntimeError(
                "Validator username constant already exists."
            )

        old = (
            "def is_valid_username(username: str) -> bool:\n"
            "    return username.isalnum() and len(username) >= 3"
        )

        new = (
            "USERNAME_MIN_LENGTH = 3\n\n\n"
            "def is_valid_username(username: str) -> bool:\n"
            "    return (\n"
            "        username.isalnum()\n"
            "        and len(username) >= USERNAME_MIN_LENGTH\n"
            "    )"
        )

        self._replace_once(
            source,
            old,
            new,
            "validator username length constant",
        )

    def _add_text_utils_separator_constant(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(
            repository,
            "text_utils.py",
        )

        content = source.read_text(
            encoding="utf-8"
        )

        constant = 'NORMALIZED_SEPARATOR = " "'

        if constant in content:
            raise RuntimeError(
                "Text separator constant already exists."
            )

        old = (
            "def normalize_text(text: str) -> str:\n"
            '    return " ".join('
        )

        new = (
            'NORMALIZED_SEPARATOR = " "\n\n\n'
            "def normalize_text(text: str) -> str:\n"
            "    return NORMALIZED_SEPARATOR.join("
        )

        self._replace_once(
            source,
            old,
            new,
            "text normalization separator",
        )

    def _add_calculator_add_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(repository, "calculator.py")

        old = (
            "def add(a: float, b: float) -> float:\n"
            "    return a + b"
        )

        new = (
            "def add(a: float, b: float) -> float:\n"
            '    """Return the sum of two numbers."""\n'
            "    return a + b"
        )

        self._replace_once(
            source,
            old,
            new,
            "calculator add docstring",
        )

    def _add_validator_age_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(repository, "validator.py")

        old = (
            "def is_valid_age(age: int) -> bool:\n"
            "    return 0 <= age <= 120"
        )

        new = (
            "def is_valid_age(age: int) -> bool:\n"
            '    """Return whether age is within the supported range."""\n'
            "    return 0 <= age <= 120"
        )

        self._replace_once(
            source,
            old,
            new,
            "validator age docstring",
        )

    def _add_text_utils_reverse_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(repository, "text_utils.py")

        old = (
            "def reverse_text(text: str) -> str:\n"
            "    return text[::-1]"
        )

        new = (
            "def reverse_text(text: str) -> str:\n"
            '    """Return text with its characters reversed."""\n'
            "    return text[::-1]"
        )

        self._replace_once(
            source,
            old,
            new,
            "text reverse docstring",
        )

    def _add_config_get_value_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(repository, "config.py")

        old = (
            "def get_config_value(key: str):\n"
            "    return DEFAULT_CONFIG.get(key)"
        )

        new = (
            "def get_config_value(key: str):\n"
            '    """Return a configuration value by key."""\n'
            "    return DEFAULT_CONFIG.get(key)"
        )

        self._replace_once(
            source,
            old,
            new,
            "config get value docstring",
        )

    def _add_file_utils_write_docstring(
        self,
        repository: Path,
    ) -> None:
        source = self._get_source(repository, "file_utils.py")

        old = (
            "def write_text_file(path: str, content: str) -> None:\n"
            '    Path(path).write_text(content, encoding="utf-8")'
        )

        new = (
            "def write_text_file(path: str, content: str) -> None:\n"
            '    """Write content to a UTF-8 text file."""\n'
            '    Path(path).write_text(content, encoding="utf-8")'
        )

        self._replace_once(
            source,
            old,
            new,
            "file write docstring",
        )
