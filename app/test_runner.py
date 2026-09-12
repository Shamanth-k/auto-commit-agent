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
    "id": 3,
    "title": "Add empty word count test",
    "type": "testing",
    "action": "add_empty_word_count_test",
    "commit_message": "test: cover empty word count",
}

    runner.run(task)


if __name__ == "__main__":
    main()