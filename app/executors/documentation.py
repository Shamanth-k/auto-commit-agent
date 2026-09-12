from pathlib import Path

from app.executors.base import BaseExecutor


class DocumentationExecutor(BaseExecutor):

    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        readme = repository / "README.md"

        if not readme.exists():
            raise FileNotFoundError("README.md not found.")

        action = task["action"]

        if action == "add_usage_section":
            self._add_usage_section(readme)

        elif action == "add_development_section":
            self._add_development_section(readme)

        else:
            raise ValueError(
                f"Unsupported documentation action: {action}"
            )

    def _add_usage_section(self, readme: Path) -> None:
        content = readme.read_text(encoding="utf-8")

        addition = (
            "\n## Usage\n\n"
            "The project provides utility functions for calculator operations,\n"
            "text processing, validation, and configuration management.\n\n"
            "Example:\n\n"
            "```python\n"
            "from src.calculator import add\n\n"
            "result = add(2, 3)\n"
            "print(result)\n"
            "```\n"
        )

        if "## Usage" not in content:
            readme.write_text(
                content.rstrip() + "\n\n" + addition,
                encoding="utf-8",
            )

    def _add_development_section(self, readme: Path) -> None:
        content = readme.read_text(encoding="utf-8")

        addition = (
            "\n## Development\n\n"
            "Development setup and contribution guidelines.\n\n"
            "1. Create and activate a virtual environment:\n\n"
            "```bash\n"
            "python -m venv .venv\n"
            "# On Windows: .venv\\Scripts\\activate\n"
            "# On Unix/macOS: source .venv/bin/activate\n"
            "```\n\n"
            "2. Install dependencies:\n\n"
            "```bash\n"
            "pip install -r requirements.txt\n"
            "```\n\n"
            "3. Run tests:\n\n"
            "```bash\n"
            "python -m pytest\n"
            "```\n"
        )

        if "## Development" not in content:
            readme.write_text(
                content.rstrip() + "\n\n" + addition,
                encoding="utf-8",
            )