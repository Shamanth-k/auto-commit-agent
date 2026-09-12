from pathlib import Path

from app.executors.base import BaseExecutor


class TestingExecutor(BaseExecutor):
    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        action = task["action"]

        if action == "add_division_zero_test":
            self._add_division_zero_test(repository)

        elif action == "add_negative_calculator_tests":
            self._add_negative_calculator_tests(repository)

        elif action == "add_empty_word_count_test":
            self._add_empty_word_count_test(repository)

        else:
            raise ValueError(
                f"Unsupported testing action: {action}"
            )

    def _append_to_test_file(
        self,
        test_file: Path,
        test_code: str,
    ) -> None:
        content = test_file.read_text(encoding="utf-8")

        if test_code.strip() not in content:
            if not content.endswith("\n"):
                content += "\n"

            content += "\n" + test_code.strip() + "\n"

            test_file.write_text(
                content,
                encoding="utf-8",
            )

    def _add_division_zero_test(self, repository: Path) -> None:
        test_file = repository / "tests" / "test_calculator.py"

        test_code = """def test_divide_by_zero():
    import pytest

    with pytest.raises(ValueError):
        divide(10, 0)
"""

        self._append_to_test_file(test_file, test_code)

    def _add_negative_calculator_tests(self, repository: Path) -> None:
        test_file = repository / "tests" / "test_calculator.py"

        test_code = """def test_add_negative_numbers():
    assert add(-5, -3) == -8


def test_subtract_negative_numbers():
    assert subtract(-5, -3) == -2


def test_multiply_negative_numbers():
    assert multiply(-5, -3) == 15
"""

        self._append_to_test_file(test_file, test_code)

    def _add_empty_word_count_test(self, repository: Path) -> None:
        test_file = repository / "tests" / "test_text_utils.py"

        test_code = """def test_word_count_empty_string():
    assert word_count("") == 0
"""

        self._append_to_test_file(test_file, test_code)