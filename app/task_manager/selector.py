import random

from app.task_manager.pool import TaskPool


class TaskSelector:
    def __init__(self, pool: TaskPool):
        self.pool = pool

    def select(self, count: int = 3) -> list[dict]:
        available = self.pool.get_available_tasks()

        if len(available) < count:
            raise RuntimeError(
                f"Only {len(available)} tasks remain in the current cycle; "
                f"{count} required."
            )

        return random.sample(available, count)
