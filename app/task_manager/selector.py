import random

from app.task_manager.pool import TaskPool


class TaskSelector:
    def __init__(self, pool: TaskPool):
        self.pool = pool

    def select(self, count: int = 3) -> list[dict]:
        selected = []
        excluded_ids = set()

        while len(selected) < count:
            available = [
                task
                for task in self.pool.get_available_tasks()
                if task["id"] not in excluded_ids
            ]

            if not available:
                self.pool.reset_cycle()
                excluded_ids.clear()
                available = self.pool.get_available_tasks()

            remaining = count - len(selected)

            batch = random.sample(
                available,
                min(remaining, len(available)),
            )

            selected.extend(batch)

            excluded_ids.update(
                task["id"] for task in batch
            )

        return selected