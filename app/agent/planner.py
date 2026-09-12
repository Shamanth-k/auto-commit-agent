from pathlib import Path

from app.agent.task import Task


class TaskPlanner:
    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    def analyze_repository(self) -> dict:
        files = []

        for path in self.repository_path.rglob("*"):
            if not path.is_file():
                continue

            if ".git" in path.parts:
                continue

            files.append(path.relative_to(self.repository_path))

        return {
            "files": files,
            "file_count": len(files),
        }

    def generate_tasks(self, count: int = 3) -> list[Task]:
        analysis = self.analyze_repository()

        tasks = []

        readme = self.repository_path / "README.md"

        if readme.exists():
            tasks.append(
                Task(
                    title="Improve README documentation",
                    description=(
                        "Add a project structure section to README.md "
                        "that explains the purpose of the repository."
                    ),
                    commit_message="docs: improve project documentation",
                )
            )

        if analysis["file_count"] > 0:
            tasks.append(
                Task(
                    title="Add repository information",
                    description=(
                        "Add a section to README.md describing the "
                        "current repository contents."
                    ),
                    commit_message="docs: add repository information",
                )
            )

        tasks.append(
            Task(
                title="Add development notes",
                description=(
                    "Add a development section to README.md explaining "
                    "that automated development tasks are being tested."
                ),
                commit_message="docs: add development notes",
            )
        )

        return tasks[:count]