from app.executors.documentation import DocumentationExecutor
from app.executors.testing import TestingExecutor


EXECUTORS = {
    "documentation": DocumentationExecutor(),
    "testing": TestingExecutor(),
}


def get_executor(task_type: str):
    executor = EXECUTORS.get(task_type)

    if executor is None:
        raise ValueError(
            f"No executor registered for task type: {task_type}"
        )

    return executor