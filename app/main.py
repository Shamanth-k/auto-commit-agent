from app.git.client import GitClient
from app.coder import Coder
from app.agent.planner import TaskPlanner
from app.validation.runner import Validator


REPOSITORY = "C:/Users/Shamanth Krishna VR/Desktop/auto-commit-test-repo"

COMMITS_PER_RUN = 3


def main():
    git = GitClient(REPOSITORY)
    planner = TaskPlanner(REPOSITORY)
    coder = Coder(REPOSITORY)
    validator = Validator(REPOSITORY)

    print("=" * 50)
    print("AUTO COMMIT AGENT")
    print("=" * 50)

    print(f"\nRepository: {REPOSITORY}")
    print(f"Branch: {git.current_branch()}")

    print("\nAnalyzing repository...")

    tasks = planner.generate_tasks(COMMITS_PER_RUN)

    print(f"Generated {len(tasks)} tasks.")

    for number, task in enumerate(tasks, start=1):

        print(f"\n--- Task {number}/{len(tasks)} ---")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")

        # Execute task
        coder.execute(task)

        # Show changes
        print("\nChanges:")
        print(git.diff())

        # Validate
        if not validator.run():
            print("Validation failed. Task will not be committed.")
            break

        # Stage
        git.add_all()

        # Commit
        git.commit(task.commit_message)

        print(f"Committed: {task.commit_message}")

    print("\n--- Final Git History ---")
    print(git.log(10))


if __name__ == "__main__":
    main()