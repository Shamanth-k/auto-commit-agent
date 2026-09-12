from app.task_manager.pool import TaskPool
from app.task_manager.executor import TaskExecutor


POOL = "tasks/task_pool.json"
STATE = "tasks/state.json"

REPOSITORY = (
    "C:/Users/Shamanth Krishna VR/Desktop/"
    "auto-commit-test-repo"
)


def main():
    pool = TaskPool(POOL, STATE)

    tasks = pool.load_tasks()

    task = tasks[0]

    executor = TaskExecutor(REPOSITORY)

    print(f"Selected task: {task['title']}")

    executor.execute(task)


if __name__ == "__main__":
    main()