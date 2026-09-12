import subprocess
from pathlib import Path


class Validator:
    def __init__(self, repository_path: str):
        self.repository_path = Path(repository_path)

    def run(self) -> bool:
        print("Running tests...")

        result = subprocess.run(
            ["python", "-m", "pytest"],
            cwd=self.repository_path,
            capture_output=True,
            text=True,
        )

        print(result.stdout)

        if result.returncode != 0:
            print("Validation failed.")
            print(result.stderr)
            return False

        print("Validation passed.")
        return True