import subprocess
from pathlib import Path

from app.task_manager.executor import TaskExecutor
from app.task_manager.runner import TaskRunner
from app.validation.runner import Validator


def create_git_repo(path: Path) -> None:
    (path / "src").mkdir()

    subprocess.run(
        ["git", "init", "-b", "main"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )

    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=path,
        check=True,
    )

    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=path,
        check=True,
    )

    (path / "README.md").write_text(
        "# Test Repository\n",
        encoding="utf-8",
    )

    (path / "src" / "calculator.py").write_text(
        '"""Calculator utilities."""\n\n'
        "def add(a, b):\n"
        "    return a + b\n",
        encoding="utf-8",
    )

    subprocess.run(
        ["git", "add", "."],
        cwd=path,
        check=True,
    )

    subprocess.run(
        ["git", "commit", "-m", "initial"],
        cwd=path,
        check=True,
        capture_output=True,
        text=True,
    )


def test_runner_rolls_back_when_validation_fails(tmp_path):
    repository = tmp_path / "repo"
    repository.mkdir()

    create_git_repo(repository)

    executor = TaskExecutor(str(repository))
    validator = Validator(str(repository))

    runner = TaskRunner(
        repository_path=str(repository),
        executor=executor,
        validator=validator,
    )

    task = {
        "id": 999,
        "title": "Create invalid change",
        "type": "calculator",
        "action": "add_factorial_function",
        "commit_message": "test: invalid change",
    }

    original_execute = executor.execute

    def execute_and_break(task):
        original_execute(task)

        (repository / "test_invalid.py").write_text(
            "this is not valid python !!!\n",
            encoding="utf-8",
        )

    executor.execute = execute_and_break

    try:
        runner.run(task)
    except RuntimeError as error:
        assert "Validation failed" in str(error)
    else:
        raise AssertionError("Expected validation failure")

    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    assert status == ""

    calculator = (
        repository / "src" / "calculator.py"
    ).read_text(encoding="utf-8")

    assert "def factorial" not in calculator
    assert (repository / "test_invalid.py").exists() is False