from app.task_manager.executor import TaskExecutor
from app.task_manager.pool import TaskPool
from app.task_manager.runner import TaskRunner
from app.validation.runner import Validator


PROJECT_REPOSITORY = (
    "C:/Users/Shamanth Krishna VR/Desktop/"
    "auto-commit-test-repo"
)

AGENT_REPOSITORY = (
    "C:/Users/Shamanth Krishna VR/Desktop/"
    "auto-commit-agent"
)

POOL = "tasks/task_pool.json"
STATE = "tasks/state.json"


def main():
    pool = TaskPool(POOL, STATE)
    executor = TaskExecutor(PROJECT_REPOSITORY)
    validator = Validator(PROJECT_REPOSITORY)

    runner = TaskRunner(
        repository_path=PROJECT_REPOSITORY,
        state_repository_path=AGENT_REPOSITORY,
        executor=executor,
        validator=validator,
        pool=pool,
    )

    task = {
        "id": 2,
        "title": "Add negative calculator tests",
        "type": "testing",
        "action": "add_negative_calculator_tests",
        "commit_message": "test: add negative calculator coverage",
    }

    runner.run(task)


if __name__ == "__main__":
    main()