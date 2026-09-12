from app.git.client import GitClient
from app.task_manager.executor import TaskExecutor
from app.task_manager.pool import TaskPool
from app.validation.runner import Validator


class TaskRunner:
    def __init__(
        self,
        repository_path: str,
        state_repository_path: str,
        executor: TaskExecutor,
        validator: Validator,
        pool: TaskPool,
    ):
        self.repository_path = repository_path

        self.project_git = GitClient(repository_path)
        self.state_git = GitClient(state_repository_path)

        self.executor = executor
        self.validator = validator
        self.pool = pool

    def run(self, task: dict) -> None:
        print(f"\nStarting task: {task['title']}")

        # Execute
        self.executor.execute(task)

        # Validate
        if not self.validator.run():
            raise RuntimeError(
                f"Validation failed: {task['title']}"
            )

        # Check project changes
        status = self.project_git.status()

        if not status:
            raise RuntimeError(
                f"Task produced no changes: {task['title']}"
            )

        print("Project changes:")
        print(status)

        # Commit project change
        self.project_git.add_all()
        self.project_git.commit(task["commit_message"])

        print(
            f"Project commit created: "
            f"{task['commit_message']}"
        )

        # Mark task used in state
        self.pool.mark_used([task["id"]])

        # Commit state
        state_status = self.state_git.status()

        if state_status:
            self.state_git.add_all()
            self.state_git.commit(
                "chore: update task state"
            )

        print(
            f"Task {task['id']} marked as used."
        )