from app.validation.runner import Validator


REPOSITORY = (
    "C:/Users/Shamanth Krishna VR/Desktop/"
    "auto-commit-test-repo"
)


def main():
    validator = Validator(REPOSITORY)

    if validator.run():
        print("VALIDATION SUCCESS")
    else:
        print("VALIDATION FAILED")


if __name__ == "__main__":
    main()