from app.task_manager.pool import TaskPool
from app.task_manager.selector import TaskSelector


POOL = "tasks/task_pool.json"
STATE = "tasks/state.json"


def main():
    pool = TaskPool(POOL, STATE)
    selector = TaskSelector(pool)

    tasks = selector.select(3)

    print("\nSelected tasks:")

    for task in tasks:
        print(
            f"{task['id']}: "
            f"{task['title']}"
        )


if __name__ == "__main__":
    main()