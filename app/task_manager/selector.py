import random

from app.task_manager.pool import TaskPool


class TaskSelector:
    def __init__(self, pool: TaskPool):
        self.pool = pool

    def select(self, count: int = 3) -> list[dict]:
        available = self.pool.get_available_tasks()

        if not available:
            self.pool.reset_cycle()
            available = self.pool.get_available_tasks()

        selected = random.sample(
            available,
            min(count, len(available)),
        )

        return selected