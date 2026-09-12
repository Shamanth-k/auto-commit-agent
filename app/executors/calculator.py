from pathlib import Path

from app.executors.base import BaseExecutor


class CalculatorExecutor(BaseExecutor):
    def execute(
        self,
        task: dict,
        repository_path: str,
    ) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_round_function": self._add_round_function,
            "add_clamp_function": self._add_clamp_function,
            "add_average_function": self._add_average_function,
            "add_minimum_function": self._add_minimum_function,
            "add_maximum_function": self._add_maximum_function,
            "add_percentage_validation": (
                self._add_percentage_validation
            ),
            "add_calculator_docstrings": (
                self._add_calculator_docstrings
            ),
            "add_calculator_constants": (
                self._add_calculator_constants
            ),
            "add_calculator_operations": (
                self._add_calculator_operations
            ),
            "add_square_function": self._add_square_function,
            "add_cube_function": self._add_cube_function,
            "add_reciprocal_function": (
                self._add_reciprocal_function
            ),
            "add_sum_function": self._add_sum_function,
            "add_median_function": self._add_median_function,
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(
                f"Unsupported calculator action: {action}"
            )

        executor(repository)

    def _calculator_file(
        self,
        repository: Path,
    ) -> Path:
        calculator = (
            repository
            / "src"
            / "calculator.py"
        )

        if not calculator.exists():
            raise FileNotFoundError(
                "src/calculator.py not found."
            )

        return calculator

    def _append_once(
        self,
        file: Path,
        marker: str,
        addition: str,
    ) -> None:
        content = file.read_text(
            encoding="utf-8"
        )

        if marker in content:
            raise RuntimeError(
                "Requested calculator change already exists: "
                f"{marker}"
            )

        updated = (
            content.rstrip()
            + "\n\n\n"
            + addition.strip()
            + "\n"
            )

        file.write_text(
            updated,
            encoding="utf-8",
        )

    def _add_round_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def round_value(",
            """
def round_value(value: float, digits: int = 2) -> float:
    return round(value, digits)
""",
        )

    def _add_clamp_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def clamp(",
            """
def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    if minimum > maximum:
        raise ValueError(
            "minimum cannot exceed maximum"
        )
    return max(
        minimum,
        min(value, maximum),
    )
""",
        )

    def _add_average_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def average(",
            """
def average(values: list[float]) -> float:
    if not values:
        raise ValueError(
            "values cannot be empty"
        )
    return sum(values) / len(values)
""",
        )

    def _add_minimum_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def minimum(",
            """
def minimum(values: list[float]) -> float:
    if not values:
        raise ValueError(
            "values cannot be empty"
        )
    return min(values)
""",
        )

    def _add_maximum_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def maximum(",
            """
def maximum(values: list[float]) -> float:
    if not values:
        raise ValueError(
            "values cannot be empty"
        )
    return max(values)
""",
        )

    def _add_percentage_validation(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        content = calculator.read_text(
            encoding="utf-8"
        )

        marker = "def percentage("

        if marker not in content:
            raise RuntimeError(
                "percentage function is required "
                "for this task."
            )

        if (
            "if percent < 0 or percent > 100:"
            in content
        ):
            raise RuntimeError(
                "Percentage validation already exists."
            )

        old = (
            "def percentage("
            "value: float, percent: float"
            ") -> float:\n"
            "    return value * percent / 100"
        )

        new = (
            "def percentage("
            "value: float, percent: float"
            ") -> float:\n"
            "    if percent < 0 or percent > 100:\n"
            '        raise ValueError('
            '"percent must be between 0 and 100"'
            ")\n"
            "    return value * percent / 100"
        )

        if old not in content:
            raise RuntimeError(
                "Expected percentage implementation "
                "was not found."
            )

        calculator.write_text(
            content.replace(old, new, 1),
            encoding="utf-8",
        )

    def _add_calculator_docstrings(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        content = calculator.read_text(
            encoding="utf-8"
        )

        if "Calculator operations." in content:
            raise RuntimeError(
                "Calculator module documentation "
                "already exists."
            )

        if content.startswith('"""'):
            raise RuntimeError(
                "Calculator already has a module docstring."
            )

        updated = (
            '"""Calculator operations."""\n\n'
            + content
        )

        calculator.write_text(
            updated,
            encoding="utf-8",
        )

    def _add_calculator_constants(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        content = calculator.read_text(
            encoding="utf-8"
        )

        marker = "PERCENTAGE_SCALE = 100"

        if marker in content:
            raise RuntimeError(
                "Calculator constants already exist."
            )

        insertion = (
            "\nPERCENTAGE_SCALE = 100\n"
        )

        calculator.write_text(
            content.rstrip() + insertion,
            encoding="utf-8",
        )

    def _add_calculator_operations(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        content = calculator.read_text(
            encoding="utf-8"
        )

        marker = "def calculate("

        if marker in content:
            raise RuntimeError(
                "calculate function already exists."
            )

        addition = """
def calculate(
    operation: str,
    a: float,
    b: float,
) -> float:
    operations = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    if operation not in operations:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    return operations[operation](a, b)
"""

        self._append_once(
            calculator,
            marker,
            addition,
        )

    def _add_square_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def square(",
            """
def square(value: float) -> float:
    return value * value
""",
        )

    def _add_cube_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def cube(",
            """
def cube(value: float) -> float:
    return value * value * value
""",
        )

    def _add_reciprocal_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def reciprocal(",
            """
def reciprocal(value: float) -> float:
    if value == 0:
        raise ValueError(
            "Cannot calculate reciprocal of zero"
        )
    return 1 / value
""",
        )

    def _add_sum_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def sum_values(",
            """
def sum_values(values: list[float]) -> float:
    return sum(values)
""",
        )

    def _add_median_function(
        self,
        repository: Path,
    ) -> None:
        calculator = self._calculator_file(
            repository
        )

        self._append_once(
            calculator,
            "def median(",
            """
def median(values: list[float]) -> float:
    if not values:
        raise ValueError(
            "values cannot be empty"
        )

    ordered = sorted(values)
    middle = len(ordered) // 2

    if len(ordered) % 2:
        return ordered[middle]

    return (
        ordered[middle - 1]
        + ordered[middle]
    ) / 2
""",
        )