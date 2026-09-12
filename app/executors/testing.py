from pathlib import Path

from app.executors.base import BaseExecutor


class TestingExecutor(BaseExecutor):
    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_power_tests": self._add_power_tests,
            "add_absolute_tests": self._add_absolute_tests,
            "add_percentage_tests": self._add_percentage_tests,
            "add_normalize_text_tests": self._add_normalize_text_tests,
            "add_reverse_text_tests": self._add_reverse_text_tests,
            "add_contains_word_tests": self._add_contains_word_tests,
            "add_username_validation_tests": self._add_username_validation_tests,
            "add_phone_validation_tests": self._add_phone_validation_tests,
            "add_password_length_tests": self._add_password_length_tests,
            "add_divide_by_zero_test": self._add_divide_by_zero_test,
            "add_add_negative_numbers_test": self._add_add_negative_numbers_test,
            "add_multiply_zero_test": self._add_multiply_zero_test,
            "add_email_missing_domain_test": self._add_email_missing_domain_test,
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(
                f"Unsupported testing action: {action}"
            )

        executor(repository)

    def _test_file(self, repository: Path, filename: str) -> Path:
        test_file = repository / "tests" / filename

        if not test_file.exists():
            raise FileNotFoundError(
                f"Test file not found: tests/{filename}"
            )

        return test_file

    def _append_test(
        self,
        test_file: Path,
        marker: str,
        test_code: str,
    ) -> None:
        content = test_file.read_text(encoding="utf-8")

        if marker in content:
            raise RuntimeError(
                f"Requested test already exists: {marker}"
            )

        if not content.endswith("\n"):
            content += "\n"

        updated = (
            content.rstrip()
            + "\n\n"
            + test_code.strip()
            + "\n"
        )

        test_file.write_text(
            updated,
            encoding="utf-8",
        )

    def _require_source_function(
        self,
        repository: Path,
        filename: str,
        function_name: str,
    ) -> None:
        source_file = repository / "src" / filename

        if not source_file.exists():
            raise FileNotFoundError(
                f"Source file not found: src/{filename}"
            )

        content = source_file.read_text(encoding="utf-8")

        if f"def {function_name}(" not in content:
            raise RuntimeError(
                f"Required function not found: {function_name}"
            )

    def _add_power_tests(self, repository: Path) -> None:
        self._require_source_function(
            repository,
            "calculator.py",
            "power",
        )

        test_file = self._test_file(
            repository,
            "test_calculator.py",
        )

        self._append_test(
            test_file,
            "def test_power_with_fractional_exponent",
            """
def test_power_with_fractional_exponent():
    assert power(9, 0.5) == 3
""",
        )

    def _add_absolute_tests(self, repository: Path) -> None:
        self._require_source_function(
            repository,
            "calculator.py",
            "absolute",
        )

        test_file = self._test_file(
            repository,
            "test_calculator.py",
        )

        self._append_test(
            test_file,
            "def test_absolute_with_zero",
            """
def test_absolute_with_zero():
    assert absolute(0) == 0
""",
        )

    def _add_percentage_tests(self, repository: Path) -> None:
        self._require_source_function(
            repository,
            "calculator.py",
            "percentage",
        )

        test_file = self._test_file(
            repository,
            "test_calculator.py",
        )

        self._append_test(
            test_file,
            "def test_percentage_fraction",
            """
def test_percentage_fraction():
    assert percentage(80, 12.5) == 10
""",
        )

    def _add_normalize_text_tests(self, repository: Path) -> None:
        self._require_source_function(
            repository,
            "text_utils.py",
            "normalize_text",
        )

        test_file = self._test_file(
            repository,
            "test_text_utils.py",
        )

        self._append_test(
            test_file,
            "def test_normalize_text_with_tabs",
            """
def test_normalize_text_with_tabs():
    assert normalize_text("\\thello\\tworld\\n") == "hello world"
""",
        )

    def _add_reverse_text_tests(self, repository: Path) -> None:
        self._require_source_function(
            repository,
            "text_utils.py",
            "reverse_text",
        )

        test_file = self._test_file(
            repository,
            "test_text_utils.py",
        )

        self._append_test(
            test_file,
            "def test_reverse_text_with_spaces",
            """
def test_reverse_text_with_spaces():
    assert reverse_text("hello world") == "dlrow olleh"
""",
        )

    def _add_contains_word_tests(self, repository: Path) -> None:
        self._require_source_function(
            repository,
            "text_utils.py",
            "contains_word",
        )

        test_file = self._test_file(
            repository,
            "test_text_utils.py",
        )

        self._append_test(
            test_file,
            "def test_contains_word_rejects_partial_match",
            """
def test_contains_word_rejects_partial_match():
    assert contains_word("cat catalog", "at") is False
""",
        )

    def _add_username_validation_tests(
        self,
        repository: Path,
    ) -> None:
        self._require_source_function(
            repository,
            "validator.py",
            "is_valid_username",
        )

        test_file = self._test_file(
            repository,
            "test_validator.py",
        )

        self._append_test(
            test_file,
            "def test_username_with_four_characters",
            """
def test_username_with_four_characters():
    assert is_valid_username("user") is True
""",
        )

    def _add_phone_validation_tests(
        self,
        repository: Path,
    ) -> None:
        self._require_source_function(
            repository,
            "validator.py",
            "is_valid_phone",
        )

        test_file = self._test_file(
            repository,
            "test_validator.py",
        )

        self._append_test(
            test_file,
            "def test_phone_with_spaces_and_dashes",
            """
def test_phone_with_spaces_and_dashes():
    assert is_valid_phone("98765 43210") is True
""",
        )

    def _add_password_length_tests(
        self,
        repository: Path,
    ) -> None:
        self._require_source_function(
            repository,
            "validator.py",
            "has_valid_password_length",
        )

        test_file = self._test_file(
            repository,
            "test_validator.py",
        )

        self._append_test(
            test_file,
            "def test_password_exactly_eight_characters",
            """
def test_password_exactly_eight_characters():
    assert has_valid_password_length("12345678") is True
""",
        )

    def _add_divide_by_zero_test(
        self,
        repository: Path,
    ) -> None:
        self._require_source_function(
            repository, "calculator.py", "divide"
        )
        test_file = self._test_file(repository, "test_calculator.py")
        self._append_test(
            test_file,
            "def test_divide_by_zero_raises",
            """
def test_divide_by_zero_raises():
    import pytest
    from src.calculator import divide

    with pytest.raises(ValueError):
        divide(10, 0)
            """,
        )

    def _add_add_negative_numbers_test(
        self,
        repository: Path,
    ) -> None:
        self._require_source_function(
            repository, "calculator.py", "add"
        )
        test_file = self._test_file(repository, "test_calculator.py")
        self._append_test(
            test_file,
            "def test_add_negative_numbers",
            """
def test_add_negative_numbers():
    from src.calculator import add

    assert add(-5, -3) == -8
            """,
        )

    def _add_multiply_zero_test(
        self,
        repository: Path,
    ) -> None:
        self._require_source_function(
            repository, "calculator.py", "multiply"
        )
        test_file = self._test_file(repository, "test_calculator.py")
        self._append_test(
            test_file,
            "def test_multiply_by_zero",
            """
def test_multiply_by_zero():
    from src.calculator import multiply

    assert multiply(123, 0) == 0
            """,
        )

    def _add_email_missing_domain_test(
        self,
        repository: Path,
    ) -> None:
        self._require_source_function(
            repository, "validator.py", "is_valid_email"
        )
        test_file = self._test_file(repository, "test_validator.py")
        self._append_test(
            test_file,
            "def test_email_missing_domain",
            """
def test_email_missing_domain():
    from src.validator import is_valid_email

    assert is_valid_email("user@") is False
            """,
        )
