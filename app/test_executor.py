from app.executors.registry import EXECUTORS, get_executor


def test_all_registered_executors_are_available():
    expected_types = {
        "calculator",
        "documentation",
        "testing",
        "code_quality",
        "text_utils",
        "validator",
        "config",
        "file_utils",
    }

    assert set(EXECUTORS) == expected_types

    for task_type in expected_types:
        assert get_executor(task_type) is EXECUTORS[task_type]


def test_unknown_executor_type_raises_error():
    try:
        get_executor("unknown")
    except ValueError as error:
        assert "No executor registered" in str(error)
    else:
        raise AssertionError("Expected ValueError")
