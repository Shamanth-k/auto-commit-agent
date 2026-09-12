from app.validation.runner import Validator


def test_validator_accepts_passing_repository(tmp_path):
    validator = Validator(str(tmp_path))

    (tmp_path / "test_sample.py").write_text(
        "def test_example():\n    assert 1 + 1 == 2\n",
        encoding="utf-8",
    )

    assert validator.run() is True


def test_validator_rejects_failing_repository(tmp_path):
    validator = Validator(str(tmp_path))

    (tmp_path / "test_sample.py").write_text(
        "def test_example():\n    assert 1 + 1 == 3\n",
        encoding="utf-8",
    )

    assert validator.run() is False
