from app.executors.calculator import CalculatorExecutor
from app.executors.code_quality import CodeQualityExecutor
from app.executors.config import ConfigExecutor
from app.executors.documentation import DocumentationExecutor
from app.executors.file_utils import FileUtilsExecutor
from app.executors.testing import TestingExecutor
from app.executors.text_utils import TextUtilsExecutor
from app.executors.validator import ValidatorExecutor


EXECUTORS = {
    "calculator": CalculatorExecutor(),
    "documentation": DocumentationExecutor(),
    "testing": TestingExecutor(),
    "code_quality": CodeQualityExecutor(),
    "text_utils": TextUtilsExecutor(),
    "validator": ValidatorExecutor(),
    "config": ConfigExecutor(),
    "file_utils": FileUtilsExecutor(),
}


def get_executor(task_type: str):
    executor = EXECUTORS.get(task_type)

    if executor is None:
        raise ValueError(
            f"No executor registered for task type: {task_type}"
        )

    return executor