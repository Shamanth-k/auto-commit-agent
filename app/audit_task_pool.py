import ast
import json
import subprocess
import sys
from pathlib import Path

from app.executors.registry import EXECUTORS
from app.task_manager.executor import TaskExecutor
from app.task_manager.runner import TaskRunner
from app.validation.runner import Validator
from app.git.client import GitClient


AGENT_REPOSITORY = Path(__file__).resolve().parent.parent

TARGET_REPOSITORY = Path(
    r"C:\Users\Shamanth Krishna VR\Desktop\auto-commit-test-repo"
)

POOL_PATH = AGENT_REPOSITORY / "tasks" / "task_pool.json"


def load_tasks():
    with POOL_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_structure(tasks):
    print("\n=== STRUCTURE AUDIT ===")

    errors = []

    ids = [task["id"] for task in tasks]
    actions = [task["action"] for task in tasks]

    if len(tasks) != 108:
        errors.append(
            f"Expected 108 tasks, found {len(tasks)}"
        )

    if len(set(ids)) != len(ids):
        errors.append("Duplicate task IDs found")

    if len(set(actions)) != len(actions):
        errors.append("Duplicate task actions found")

    required = {
        "id",
        "title",
        "type",
        "action",
        "commit_message",
    }

    for task in tasks:
        missing = required - task.keys()

        if missing:
            errors.append(
                f"Task {task.get('id')} missing fields: "
                f"{sorted(missing)}"
            )

        if task.get("type") not in EXECUTORS:
            errors.append(
                f"Task {task.get('id')} has unknown type: "
                f"{task.get('type')}"
            )

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return False

    print("PASS: 108 tasks")
    print("PASS: IDs are unique")
    print("PASS: actions are unique")
    print("PASS: all task types are registered")

    return True


def extract_registered_actions():
    files = {
        "calculator": "calculator.py",
        "code_quality": "code_quality.py",
        "config": "config.py",
        "documentation": "documentation.py",
        "file_utils": "file_utils.py",
        "testing": "testing.py",
        "text_utils": "text_utils.py",
        "validator": "validator.py",
    }

    registered = {}

    for task_type, filename in files.items():
        path = (
            AGENT_REPOSITORY
            / "app"
            / "executors"
            / filename
        )

        tree = ast.parse(
            path.read_text(encoding="utf-8")
        )

        actions = set()

        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue

            for key in node.keys:
                if (
                    isinstance(key, ast.Constant)
                    and isinstance(key.value, str)
                    and key.value.startswith("add_")
                ):
                    actions.add(key.value)

        registered[task_type] = actions

    return registered


def validate_actions(tasks):
    print("\n=== ACTION AUDIT ===")

    registered = extract_registered_actions()
    missing = []

    for task in tasks:
        if task["action"] not in registered[task["type"]]:
            missing.append(
                (
                    task["id"],
                    task["type"],
                    task["action"],
                )
            )

    if missing:
        for item in missing:
            print(
                f"FAIL: task {item[0]} -> "
                f"{item[1]} -> {item[2]}"
            )

        return False

    print("PASS: all 108 task actions are registered")

    pool_actions = {
        task["action"]
        for task in tasks
    }

    unused = set()

    for actions in registered.values():
        unused.update(actions - pool_actions)

    if unused:
        print(
            "INFO: registered actions not in pool:",
            sorted(unused),
        )

    return True


def git_commit_count(git):
    output = git.run(
        "rev-list",
        "--count",
        "HEAD",
    )

    return int(output)


def reset_to_baseline(git, baseline_commit):
    git.run(
        "reset",
        "--hard",
        baseline_commit,
    )

    git.run("clean", "-fd")


def run_task(task):
    executor = TaskExecutor(
        str(TARGET_REPOSITORY)
    )

    validator = Validator(
        str(TARGET_REPOSITORY)
    )

    runner = TaskRunner(
        repository_path=str(TARGET_REPOSITORY),
        executor=executor,
        validator=validator,
    )

    runner.run(task)


def audit_execution(tasks):
    print("\n=== EXECUTION AUDIT ===")
    print(
        "Every task will be executed independently "
        "from the exact same baseline commit."
    )
    print()

    git = GitClient(str(TARGET_REPOSITORY))

    branch = git.current_branch()

    if branch != "main":
        print(
            f"FAIL: target repository is on "
            f"'{branch}', expected 'main'"
        )
        return False

    if git.status():
        print(
            "FAIL: target repository is not clean:"
        )
        print(git.status())
        return False

    baseline_commit = git.run(
        "rev-parse",
        "HEAD",
    )

    baseline_count = git_commit_count(git)

    print(
        f"Baseline commit: {baseline_commit}"
    )
    print(
        f"Baseline commit count: {baseline_count}"
    )

    failures = []

    for index, task in enumerate(tasks, start=1):
        print()
        print(
            "=" * 60
        )
        print(
            f"[{index}/108] "
            f"Task {task['id']}: "
            f"{task['title']}"
        )
        print(
            "=" * 60
        )

        try:
            reset_to_baseline(
                git,
                baseline_commit,
            )

            run_task(task)

            current_commit = git.run(
                "rev-parse",
                "HEAD",
            )

            commit_count = git_commit_count(git)

            if commit_count != baseline_count + 1:
                raise RuntimeError(
                    "Expected exactly one new project commit, "
                    f"but commit count changed from "
                    f"{baseline_count} to {commit_count}"
                )

            if current_commit == baseline_commit:
                raise RuntimeError(
                    "Task completed without creating "
                    "a new commit."
                )

            if git.status():
                raise RuntimeError(
                    "Task left the target repository dirty:\n"
                    + git.status()
                )

            print(
                f"PASS: task created commit "
                f"{current_commit}"
            )

        except Exception as error:
            print(
                f"FAIL: task {task['id']}:"
            )
            print(error)

            failures.append(
                (
                    task["id"],
                    task["action"],
                    str(error),
                )
            )

        finally:
            try:
                reset_to_baseline(
                    git,
                    baseline_commit,
                )

                final_commit = git.run(
                    "rev-parse",
                    "HEAD",
                )

                final_count = git_commit_count(git)

                if final_commit != baseline_commit:
                    print(
                        "CRITICAL: repository was not "
                        "restored to baseline."
                    )
                    return False

                if final_count != baseline_count:
                    print(
                        "CRITICAL: commit count was not "
                        "restored to baseline."
                    )
                    return False

                if git.status():
                    print(
                        "CRITICAL: repository is dirty "
                        "after rollback."
                    )
                    print(git.status())
                    return False

            except Exception as rollback_error:
                print(
                    "CRITICAL: rollback failed:"
                )
                print(rollback_error)
                return False

    print("\n=== EXECUTION RESULT ===")

    if failures:
        print(
            f"FAIL: {len(failures)} tasks failed"
        )

        for task_id, action, error in failures:
            print(
                f"  Task {task_id} | "
                f"{action} | "
                f"{error}"
            )

        return False

    print(
        "PASS: all 108 tasks executed successfully"
    )

    return True


def validate_final_state():
    print("\n=== FINAL STATE AUDIT ===")

    git = GitClient(str(TARGET_REPOSITORY))

    if git.status():
        print(
            "FAIL: target repository is dirty:"
        )
        print(git.status())
        return False

    print("PASS: target repository is clean")

    return True


def main():
    print("========================================")
    print("       AUTOMATION TASK POOL AUDIT")
    print("========================================")

    tasks = load_tasks()

    if not validate_structure(tasks):
        sys.exit(1)

    if not validate_actions(tasks):
        sys.exit(1)

    if not audit_execution(tasks):
        validate_final_state()
        sys.exit(1)

    if not validate_final_state():
        sys.exit(1)

    print("\n========================================")
    print("AUDIT RESULT: PASS")
    print("All 108 tasks passed independent execution.")
    print("========================================")

    sys.exit(0)


if __name__ == "__main__":
    main()