from app.task_manager.executor import TaskExecutor
from app.task_manager.runner import TaskRunner
from app.validation.runner import Validator


PROJECT_REPOSITORY = (
    "C:/Users/Shamanth Krishna VR/Desktop/"
    "auto-commit-test-repo"
)


def main():
    executor = TaskExecutor(PROJECT_REPOSITORY)
    validator = Validator(PROJECT_REPOSITORY)

    runner = TaskRunner(
        repository_path=PROJECT_REPOSITORY,
        executor=executor,
        validator=validator,
    )

    task = {
    "id": 12,
    "title": "Add percentage operation",
    "type": "calculator",
    "action": "add_percentage_operation",
    "commit_message": "feat: add percentage operation",
    }

    runner.run(task)


if __name__ == "__main__":
    main()