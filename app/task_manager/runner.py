from app.git.client import GitClient
from app.task_manager.executor import TaskExecutor
from app.validation.runner import Validator


class TaskRunner:
    def __init__(
        self,
        repository_path: str,
        executor: TaskExecutor,
        validator: Validator,
    ):
        self.repository_path = repository_path
        self.git = GitClient(repository_path)
        self.executor = executor
        self.validator = validator

    def run(self, task: dict) -> None:
        print(f"\nStarting task: {task['title']}")

        try:
            self.executor.execute(task)

            if not self.validator.run():
                raise RuntimeError(
                    f"Validation failed: {task['title']}"
                )

            status = self.git.status()

            if not status:
                raise RuntimeError(
                    f"Task produced no changes: {task['title']}"
                )

            print("Project changes:")
            print(status)

            self.git.add_all()
            self.git.commit(task["commit_message"])

            print(
                f"Project commit created: "
                f"{task['commit_message']}"
            )

        except Exception:
            print(
                f"\nTask failed: {task['title']}"
            )
            print("Restoring target repository...")

            try:
                self.git.restore_worktree()
                print("Target repository restored.")
            except Exception as rollback_error:
                raise RuntimeError(
                    f"Task failed and repository rollback also failed: "
                    f"{rollback_error}"
                ) from rollback_error

            raise