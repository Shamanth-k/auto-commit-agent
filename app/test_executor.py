import sys

from app.executors.calculator import CalculatorExecutor


PROJECT_REPOSITORY = (
    "C:/Users/Shamanth Krishna VR/Desktop/"
    "auto-commit-test-repo"
)


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python -m app.test_executor <action>"
        )
        raise SystemExit(1)

    action = sys.argv[1]

    executor = CalculatorExecutor()

    task = {
        "id": 0,
        "title": action,
        "type": "calculator",
        "action": action,
        "commit_message": (
            "test: validate calculator executor"
        ),
    }

    print(f"Executing action: {action}")

    executor.execute(
        task,
        PROJECT_REPOSITORY,
    )

    print("Task execution completed.")


if __name__ == "__main__":
    main()