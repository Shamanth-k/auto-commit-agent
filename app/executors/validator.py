from pathlib import Path

from app.executors.base import BaseExecutor


class ValidatorExecutor(BaseExecutor):
    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_email_whitespace_tests": (
                self._add_email_whitespace_tests
            ),
            "add_email_boundary_tests": (
                self._add_email_boundary_tests
            ),
            "add_age_boundary_tests": (
                self._add_age_boundary_tests
            ),
            "add_empty_string_validation_tests": (
                self._add_empty_string_validation_tests
            ),
            "add_username_boundary_tests": (
                self._add_username_boundary_tests
            ),
            "add_username_special_character_tests": (
                self._add_username_special_character_tests
            ),
            "add_phone_format_tests": (
                self._add_phone_format_tests
            ),
            "add_phone_invalid_length_tests": (
                self._add_phone_invalid_length_tests
            ),
            "add_password_boundary_tests": (
                self._add_password_boundary_tests
            ),
            "add_email_missing_at_test": self._add_email_missing_at_test,
            "add_age_negative_test": self._add_age_negative_test,
            "add_username_empty_test": self._add_username_empty_test,
            "add_phone_letters_test": self._add_phone_letters_test,
            "add_password_short_test": self._add_password_short_test,
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(
                f"Unsupported validator action: {action}"
            )

        executor(repository)

    def _source_function_exists(
        self,
        repository: Path,
        function_name: str,
    ) -> None:
        source = repository / "src" / "validator.py"

        if not source.exists():
            raise FileNotFoundError(
                "src/validator.py not found."
            )

        content = source.read_text(encoding="utf-8")

        if f"def {function_name}(" not in content:
            raise RuntimeError(
                f"Required function not found: {function_name}"
            )

    def _get_test_file(self, repository: Path) -> Path:
        test_file = repository / "tests" / "test_validator.py"

        if not test_file.exists():
            raise FileNotFoundError(
                "tests/test_validator.py not found."
            )

        return test_file

    def _append_test(
        self,
        repository: Path,
        marker: str,
        test_code: str,
    ) -> None:
        test_file = self._get_test_file(repository)
        content = test_file.read_text(encoding="utf-8")

        if marker in content:
            raise RuntimeError(
                f"Requested test already exists: {marker}"
            )

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

    def _add_email_whitespace_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_valid_email",
        )

        self._append_test(
            repository,
            "def test_email_with_whitespace",
            """
def test_email_with_whitespace():
    assert is_valid_email(" user@example.com ") is False
""",
        )

    def _add_email_boundary_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_valid_email",
        )

        self._append_test(
            repository,
            "def test_email_with_subdomain",
            """
def test_email_with_subdomain():
    assert is_valid_email(
        "user@mail.example.com"
    ) is True
""",
        )

    def _add_age_boundary_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_valid_age",
        )

        self._append_test(
            repository,
            "def test_age_upper_boundary",
            """
def test_age_upper_boundary():
    assert is_valid_age(120) is True
    assert is_valid_age(121) is False
""",
        )

    def _add_empty_string_validation_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_non_empty_string",
        )

        self._append_test(
            repository,
            "def test_non_empty_string_whitespace",
            """
def test_non_empty_string_whitespace():
    assert is_non_empty_string("   ") is False
""",
        )

    def _add_username_boundary_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_valid_username",
        )

        self._append_test(
            repository,
            "def test_username_minimum_length",
            """
def test_username_minimum_length():
    assert is_valid_username("abc") is True
    assert is_valid_username("ab") is False
""",
        )

    def _add_username_special_character_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_valid_username",
        )

        self._append_test(
            repository,
            "def test_username_rejects_special_characters",
            """
def test_username_rejects_special_characters():
    assert is_valid_username("user_name") is False
    assert is_valid_username("user-name") is False
""",
        )

    def _add_phone_format_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_valid_phone",
        )

        self._append_test(
            repository,
            "def test_phone_with_spaces",
            """
def test_phone_with_spaces():
    assert is_valid_phone("98765 43210") is True
""",
        )

    def _add_phone_invalid_length_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "is_valid_phone",
        )

        self._append_test(
            repository,
            "def test_phone_invalid_length",
            """
def test_phone_invalid_length():
    assert is_valid_phone("123456789") is False
    assert is_valid_phone("12345678901") is False
""",
        )

    def _add_password_boundary_tests(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "has_valid_password_length",
        )

        self._append_test(
            repository,
            "def test_password_length_boundary",
            """
def test_password_length_boundary():
    assert has_valid_password_length("1234567") is False
    assert has_valid_password_length("12345678") is True
""",
        )

    def _add_email_missing_at_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "is_valid_email")
        self._append_test(
            repository,
            "def test_email_missing_at_symbol",
            """
def test_email_missing_at_symbol():
    from src.validator import is_valid_email

    assert is_valid_email("user.example.com") is False
            """,
        )

    def _add_age_negative_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "is_valid_age")
        self._append_test(
            repository,
            "def test_age_negative",
            """
def test_age_negative():
    from src.validator import is_valid_age

    assert is_valid_age(-1) is False
            """,
        )

    def _add_username_empty_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "is_valid_username")
        self._append_test(
            repository,
            "def test_username_empty",
            """
def test_username_empty():
    from src.validator import is_valid_username

    assert is_valid_username("") is False
            """,
        )

    def _add_phone_letters_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "is_valid_phone")
        self._append_test(
            repository,
            "def test_phone_rejects_letters",
            """
def test_phone_rejects_letters():
    from src.validator import is_valid_phone

    assert is_valid_phone("98765abc210") is False
            """,
        )

    def _add_password_short_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository, "has_valid_password_length"
        )
        self._append_test(
            repository,
            "def test_password_short_value",
            """
def test_password_short_value():
    from src.validator import has_valid_password_length

    assert has_valid_password_length("short") is False
            """,
        )
