import json
from pathlib import Path


class TaskPool:
    def __init__(self, pool_path: str, state_path: str):
        self.pool_path = Path(pool_path)
        self.state_path = Path(state_path)

    def load_tasks(self) -> list[dict]:
        with self.pool_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def load_state(self) -> dict:
        with self.state_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def save_state(self, state: dict) -> None:
        with self.state_path.open("w", encoding="utf-8") as file:
            json.dump(state, file, indent=2)

    def get_available_tasks(self) -> list[dict]:
        tasks = self.load_tasks()
        state = self.load_state()

        used_ids = set(state["used_tasks"])

        return [
            task
            for task in tasks
            if task["id"] not in used_ids
        ]

    def mark_used(self, task_ids: list[int]) -> None:
        state = self.load_state()

        state["used_tasks"].extend(task_ids)

        self.save_state(state)

    def reset_cycle(self) -> None:
        state = self.load_state()

        state["cycle"] += 1
        state["used_tasks"] = []

        self.save_state(state)