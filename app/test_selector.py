from app.task_manager.pool import TaskPool
from app.task_manager.selector import TaskSelector


POOL = "tasks/task_pool.json"
STATE = "tasks/state.json"


def main():
    pool = TaskPool(POOL, STATE)
    selector = TaskSelector(pool)

    available = pool.get_available_tasks()

    print(f"Available tasks: {len(available)}")

    selected = selector.select(3)

    print("\nSelected tasks:")

    for task in selected:
        print(
            f'{task["id"]}: '
            f'{task["title"]}'
        )


if __name__ == "__main__":
    main()