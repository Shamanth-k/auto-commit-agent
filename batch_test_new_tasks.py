from pathlib import Path
import subprocess

from app.executors.registry import get_executor

PROJECT_REPOSITORY = Path(
    r"C:\Users\Shamanth Krishna VR\Desktop\auto-commit-test-repo"
)

TASKS = [{'id': 1, 'type': 'code_quality', 'action': 'add_calculator_add_docstring', 'title': 'document calculator add helper', 'commit_message': 'refactor: add calculator add docstring'}, {'id': 2, 'type': 'code_quality', 'action': 'add_validator_age_docstring', 'title': 'document validator age helper', 'commit_message': 'refactor: add validator age docstring'}, {'id': 3, 'type': 'code_quality', 'action': 'add_text_utils_reverse_docstring', 'title': 'document reverse text helper', 'commit_message': 'refactor: add text utils reverse docstring'}, {'id': 4, 'type': 'code_quality', 'action': 'add_config_get_value_docstring', 'title': 'document config lookup helper', 'commit_message': 'refactor: add config get value docstring'}, {'id': 5, 'type': 'code_quality', 'action': 'add_file_utils_write_docstring', 'title': 'document file write helper', 'commit_message': 'refactor: add file utils write docstring'}, {'id': 6, 'type': 'config', 'action': 'add_environment_name_config', 'title': 'add environment name configuration', 'commit_message': 'feat: add environment name config'}, {'id': 7, 'type': 'config', 'action': 'add_request_timeout_config', 'title': 'add request timeout configuration', 'commit_message': 'feat: add request timeout config'}, {'id': 8, 'type': 'config', 'action': 'add_feature_enabled_config', 'title': 'add feature enabled configuration', 'commit_message': 'feat: add feature enabled config'}, {'id': 9, 'type': 'config', 'action': 'add_region_config', 'title': 'add region configuration', 'commit_message': 'feat: add region config'}, {'id': 10, 'type': 'config', 'action': 'add_log_format_config', 'title': 'add logging format configuration', 'commit_message': 'feat: add log format config'}, {'id': 11, 'type': 'documentation', 'action': 'add_usage_section', 'title': 'document basic usage', 'commit_message': 'docs: add usage section'}, {'id': 12, 'type': 'documentation', 'action': 'add_api_reference_section', 'title': 'document API reference', 'commit_message': 'docs: add api reference section'}, {'id': 13, 'type': 'documentation', 'action': 'add_error_handling_section', 'title': 'document error handling', 'commit_message': 'docs: add error handling section'}, {'id': 14, 'type': 'documentation', 'action': 'add_development_workflow_section', 'title': 'document development workflow', 'commit_message': 'docs: add development workflow section'}, {'id': 15, 'type': 'file_utils', 'action': 'add_file_size_megabytes', 'title': 'add megabyte file size helper', 'commit_message': 'feat: add file size megabytes'}, {'id': 16, 'type': 'file_utils', 'action': 'add_file_extension_lowercase', 'title': 'add lowercase extension helper', 'commit_message': 'feat: add file extension lowercase'}, {'id': 17, 'type': 'file_utils', 'action': 'add_is_regular_file', 'title': 'add regular file helper', 'commit_message': 'feat: add is regular file'}, {'id': 18, 'type': 'file_utils', 'action': 'add_parent_name', 'title': 'add parent directory name helper', 'commit_message': 'feat: add parent name'}, {'id': 19, 'type': 'testing', 'action': 'add_divide_by_zero_test', 'title': 'test division by zero', 'commit_message': 'test: add divide by zero test'}, {'id': 20, 'type': 'testing', 'action': 'add_add_negative_numbers_test', 'title': 'test addition of negative numbers', 'commit_message': 'test: add add negative numbers test'}, {'id': 21, 'type': 'testing', 'action': 'add_multiply_zero_test', 'title': 'test multiplication by zero', 'commit_message': 'test: add multiply zero test'}, {'id': 22, 'type': 'testing', 'action': 'add_email_missing_domain_test', 'title': 'test email missing domain', 'commit_message': 'test: add email missing domain test'}, {'id': 23, 'type': 'text_utils', 'action': 'add_word_count_empty_test', 'title': 'test empty word count', 'commit_message': 'test: add word count empty test'}, {'id': 24, 'type': 'text_utils', 'action': 'add_uppercase_text_mixed_case_test', 'title': 'test mixed case uppercasing', 'commit_message': 'test: add uppercase text mixed case test'}, {'id': 25, 'type': 'text_utils', 'action': 'add_character_count_empty_test', 'title': 'test empty character count', 'commit_message': 'test: add character count empty test'}, {'id': 26, 'type': 'text_utils', 'action': 'add_reverse_text_single_character_test', 'title': 'test single character reversal', 'commit_message': 'test: add reverse text single character test'}, {'id': 27, 'type': 'validator', 'action': 'add_email_missing_at_test', 'title': 'test email missing at symbol', 'commit_message': 'test: add email missing at test'}, {'id': 28, 'type': 'validator', 'action': 'add_age_negative_test', 'title': 'test negative age', 'commit_message': 'test: add age negative test'}, {'id': 29, 'type': 'validator', 'action': 'add_username_empty_test', 'title': 'test empty username', 'commit_message': 'test: add username empty test'}, {'id': 30, 'type': 'validator', 'action': 'add_phone_letters_test', 'title': 'test phone letters rejection', 'commit_message': 'test: add phone letters test'}, {'id': 31, 'type': 'validator', 'action': 'add_password_short_test', 'title': 'test short password', 'commit_message': 'test: add password short test'}]

def run_tests():
    result = subprocess.run(
        ["python", "-m", "pytest"],
        cwd=PROJECT_REPOSITORY,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("pytest failed")


def main():
    for index, task in enumerate(TASKS, start=1):
        print(
            f"\n[{index}/{len(TASKS)}] "
            f"{task['type']}: {task['action']}"
        )
        executor = get_executor(task["type"])
        executor.execute(task, str(PROJECT_REPOSITORY))
        run_tests()
        print("PASS")

    print(f"\nAll {len(TASKS)} new tasks passed.")


if __name__ == "__main__":
    main()
