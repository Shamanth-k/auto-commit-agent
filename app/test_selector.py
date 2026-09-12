from app.task_manager.pool import TaskPool
from app.task_manager.selector import TaskSelector


def test_selector_returns_three_unique_unused_tasks(tmp_path):
    pool_path = tmp_path / "task_pool.json"
    state_path = tmp_path / "state.json"

    pool_path.write_text(
        """
[
  {"id": 1, "type": "calculator", "action": "a", "title": "A", "commit_message": "a"},
  {"id": 2, "type": "calculator", "action": "b", "title": "B", "commit_message": "b"},
  {"id": 3, "type": "calculator", "action": "c", "title": "C", "commit_message": "c"},
  {"id": 4, "type": "calculator", "action": "d", "title": "D", "commit_message": "d"}
]
""",
        encoding="utf-8",
    )

    state_path.write_text(
        '{"cycle": 1, "used_tasks": [1], "total_tasks": 4}',
        encoding="utf-8",
    )

    pool = TaskPool(str(pool_path), str(state_path))
    selector = TaskSelector(pool)

    selected = selector.select(3)
    selected_ids = [task["id"] for task in selected]

    assert len(selected) == 3
    assert len(selected_ids) == len(set(selected_ids))
    assert 1 not in selected_ids


def test_selector_rejects_insufficient_tasks(tmp_path):
    pool_path = tmp_path / "task_pool.json"
    state_path = tmp_path / "state.json"

    pool_path.write_text(
        """
[
  {"id": 1, "type": "calculator", "action": "a", "title": "A", "commit_message": "a"},
  {"id": 2, "type": "calculator", "action": "b", "title": "B", "commit_message": "b"}
]
""",
        encoding="utf-8",
    )

    state_path.write_text(
        '{"cycle": 1, "used_tasks": [], "total_tasks": 2}',
        encoding="utf-8",
    )

    pool = TaskPool(str(pool_path), str(state_path))
    selector = TaskSelector(pool)

    try:
        selector.select(3)
    except RuntimeError as error:
        assert "Only 2 tasks remain" in str(error)
    else:
        raise AssertionError("Expected RuntimeError")
