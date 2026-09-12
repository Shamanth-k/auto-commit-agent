import os

from app.git.client import GitClient
from app.task_manager.executor import TaskExecutor
from app.task_manager.pool import TaskPool
from app.task_manager.runner import TaskRunner
from app.task_manager.selector import TaskSelector
from app.validation.runner import Validator


PROJECT_REPOSITORY = os.environ.get(
    "PROJECT_REPOSITORY",
    "C:/Users/Shamanth Krishna VR/Desktop/auto-commit-test-repo",
)

AGENT_REPOSITORY = os.environ.get(
    "AGENT_REPOSITORY",
    "C:/Users/Shamanth Krishna VR/Desktop/auto-commit-agent",
)

POOL = os.environ.get(
    "TASK_POOL",
    "tasks/task_pool.json",
)

STATE = os.environ.get(
    "TASK_STATE",
    "tasks/state.json",
)


def main():
    pool = TaskPool(POOL, STATE)

    # Start a new cycle only when the previous cycle
    # was completely consumed.
    if pool.is_cycle_complete():
        pool.reset_cycle()
        print("\nPrevious cycle completed.")
        print("Started a new task cycle.")

    selector = TaskSelector(pool)

    executor = TaskExecutor(PROJECT_REPOSITORY)
    validator = Validator(PROJECT_REPOSITORY)

    runner = TaskRunner(
        repository_path=PROJECT_REPOSITORY,
        executor=executor,
        validator=validator,
    )

    state_git = GitClient(AGENT_REPOSITORY)

    tasks = selector.select(3)

    print("\nToday's tasks:")

    for task in tasks:
        print(f"{task['id']}: {task['title']}")

    completed_tasks = []

    for task in tasks:
        try:
            runner.run(task)
            completed_tasks.append(task)

        except Exception as error:
            print(f"\nTask {task['id']} failed:")
            print(error)
            break

    if completed_tasks:
        pool.mark_used(
            [task["id"] for task in completed_tasks]
        )

        state_git.add_all()
        state_git.commit("chore: update task state")

        print("\nState committed.")

    print(
        f"\nCompleted "
        f"{len(completed_tasks)}/{len(tasks)} tasks."
    )


if __name__ == "__main__":
    main()
