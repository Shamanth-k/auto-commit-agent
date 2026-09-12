from pathlib import Path

from app.agent.task import Task


class Coder:
    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    def execute(self, task: Task):
        readme = self.repository_path / "README.md"

        if not readme.exists():
            raise FileNotFoundError("README.md not found.")

        content = readme.read_text(encoding="utf-8")

        section = (
            f"\n\n## {task.title}\n"
            f"{task.description}\n"
        )

        readme.write_text(
            content + section,
            encoding="utf-8",
        )

        print(f"Executed task: {task.title}")