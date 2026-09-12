from app.executors.registry import get_executor


class TaskExecutor:

    def __init__(self, repository_path: str):
        self.repository_path = repository_path

    def execute(self, task: dict) -> None:
        executor = get_executor(task["type"])

        print(f"Executing: {task['title']}")

        executor.execute(
            task,
            self.repository_path,
        )

        print("Task execution completed.")