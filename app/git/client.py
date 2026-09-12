import subprocess
from pathlib import Path


class GitClient:
    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

        if not self.repository_path.exists():
            raise FileNotFoundError(
                f"Repository does not exist: {self.repository_path}"
            )

    def run(self, *args: str) -> str:
        command = ["git", *args]

        result = subprocess.run(
            command,
            cwd=self.repository_path,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Git command failed:\n"
                f"Command: {' '.join(command)}\n"
                f"Error: {result.stderr.strip()}"
            )

        return result.stdout.strip()

    def status(self) -> str:
        return self.run("status", "--short")

    def current_branch(self) -> str:
        return self.run("branch", "--show-current")

    def diff(self) -> str:
        return self.run("diff")

    def add_all(self) -> None:
        self.run("add", ".")

    def commit(self, message: str) -> str:
        return self.run("commit", "-m", message)

    def log(self, count: int = 10) -> str:
        return self.run(
            "log",
            f"-{count}",
            "--oneline",
        )