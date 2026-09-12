from pathlib import Path

from app.executors.base import BaseExecutor


class TextUtilsExecutor(BaseExecutor):
    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_normalize_text_punctuation_test": (
                self._add_normalize_text_punctuation_test
            ),
            "add_normalize_text_unicode_test": (
                self._add_normalize_text_unicode_test
            ),
            "add_reverse_text_empty_test": (
                self._add_reverse_text_empty_test
            ),
            "add_reverse_text_unicode_test": (
                self._add_reverse_text_unicode_test
            ),
            "add_word_count_whitespace_test": (
                self._add_word_count_whitespace_test
            ),
            "add_uppercase_text_empty_test": (
                self._add_uppercase_text_empty_test
            ),
            "add_character_count_unicode_test": (
                self._add_character_count_unicode_test
            ),
            "add_contains_word_case_test": (
                self._add_contains_word_case_test
            ),
            "add_contains_word_empty_test": (
                self._add_contains_word_empty_test
            ),
            "add_word_count_empty_test": self._add_word_count_empty_test,
            "add_uppercase_text_mixed_case_test": self._add_uppercase_text_mixed_case_test,
            "add_character_count_empty_test": self._add_character_count_empty_test,
            "add_reverse_text_single_character_test": self._add_reverse_text_single_character_test,
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(
                f"Unsupported text_utils action: {action}"
            )

        executor(repository)

    def _source_function_exists(
        self,
        repository: Path,
        function_name: str,
    ) -> None:
        source = repository / "src" / "text_utils.py"

        if not source.exists():
            raise FileNotFoundError(
                "src/text_utils.py not found."
            )

        content = source.read_text(encoding="utf-8")

        if f"def {function_name}(" not in content:
            raise RuntimeError(
                f"Required function not found: {function_name}"
            )

    def _get_test_file(self, repository: Path) -> Path:
        test_file = (
            repository
            / "tests"
            / "test_text_processing.py"
        )

        if not test_file.exists():
            test_file.write_text(
                """from src.text_utils import (
    normalize_text,
    reverse_text,
    word_count,
    uppercase_text,
    character_count,
    contains_word,
)


""",
                encoding="utf-8",
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

    def _add_normalize_text_punctuation_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "normalize_text",
        )

        self._append_test(
            repository,
            "def test_normalize_text_preserves_punctuation",
            """
def test_normalize_text_preserves_punctuation():
    assert normalize_text(
        "  Hello,   World!  "
    ) == "hello, world!"
""",
        )

    def _add_normalize_text_unicode_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "normalize_text",
        )

        self._append_test(
            repository,
            "def test_normalize_text_unicode",
            """
def test_normalize_text_unicode():
    assert normalize_text(
        "  Café   crème  "
    ) == "café crème"
""",
        )

    def _add_reverse_text_empty_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "reverse_text",
        )

        self._append_test(
            repository,
            "def test_reverse_text_empty_string",
            """
def test_reverse_text_empty_string():
    assert reverse_text("") == ""
""",
        )

    def _add_reverse_text_unicode_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "reverse_text",
        )

        self._append_test(
            repository,
            "def test_reverse_text_unicode",
            """
def test_reverse_text_unicode():
    assert reverse_text("café") == "éfac"
""",
        )

    def _add_word_count_whitespace_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "word_count",
        )

        self._append_test(
            repository,
            "def test_word_count_mixed_whitespace",
            """
def test_word_count_mixed_whitespace():
    assert word_count("one\\ttwo\\nthree") == 3
""",
        )

    def _add_uppercase_text_empty_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "uppercase_text",
        )

        self._append_test(
            repository,
            "def test_uppercase_text_empty_string",
            """
def test_uppercase_text_empty_string():
    assert uppercase_text("") == ""
""",
        )

    def _add_character_count_unicode_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "character_count",
        )

        self._append_test(
            repository,
            "def test_character_count_unicode",
            """
def test_character_count_unicode():
    assert character_count("café") == 4
""",
        )

    def _add_contains_word_case_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "contains_word",
        )

        self._append_test(
            repository,
            "def test_contains_word_is_case_sensitive",
            """
def test_contains_word_is_case_sensitive():
    assert contains_word(
        "Hello world",
        "hello",
    ) is False
""",
        )

    def _add_contains_word_empty_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "contains_word",
        )

        self._append_test(
            repository,
            "def test_contains_word_empty_word",
            """
def test_contains_word_empty_word():
    assert contains_word(
        "hello world",
        "",
    ) is False
""",
        )

    def _add_word_count_empty_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "word_count")
        self._append_test(
            repository,
            "def test_word_count_empty_string",
            """
def test_word_count_empty_string():
    assert word_count("") == 0
            """,
        )

    def _add_uppercase_text_mixed_case_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "uppercase_text")
        self._append_test(
            repository,
            "def test_uppercase_text_mixed_case",
            """
def test_uppercase_text_mixed_case():
    assert uppercase_text("Hello World") == "HELLO WORLD"
            """,
        )

    def _add_character_count_empty_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "character_count")
        self._append_test(
            repository,
            "def test_character_count_empty_string",
            """
def test_character_count_empty_string():
    assert character_count("") == 0
            """,
        )

    def _add_reverse_text_single_character_test(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(repository, "reverse_text")
        self._append_test(
            repository,
            "def test_reverse_text_single_character",
            """
def test_reverse_text_single_character():
    assert reverse_text("x") == "x"
            """,
        )
