from pathlib import Path

from app.executors.base import BaseExecutor


class ConfigExecutor(BaseExecutor):
    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_log_level_config": self._add_log_level_config,
            "add_cache_enabled_config": self._add_cache_enabled_config,
            "add_api_url_config": self._add_api_url_config,
            "add_database_timeout_config": self._add_database_timeout_config,
            "add_get_required_config": self._add_get_required_config,
            "add_config_key_exists": self._add_config_key_exists,
            "add_config_without_overrides": self._add_config_without_overrides,
            "add_config_validation": self._add_config_validation,
            "add_config_copy": self._add_config_copy,
            "add_environment_name_config": self._add_environment_name_config,
            "add_request_timeout_config": self._add_request_timeout_config,
            "add_feature_enabled_config": self._add_feature_enabled_config,
            "add_region_config": self._add_region_config,
            "add_log_format_config": self._add_log_format_config,
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(
                f"Unsupported config action: {action}"
            )

        executor(repository)

    def _get_source(self, repository: Path) -> Path:
        source = repository / "src" / "config.py"

        if not source.exists():
            raise FileNotFoundError(
                "src/config.py not found."
            )

        return source

    def _get_tests(self, repository: Path) -> Path:
        test_file = repository / "tests" / "test_config.py"

        if not test_file.exists():
            raise FileNotFoundError(
                "tests/test_config.py not found."
            )

        return test_file

    def _append_source(
        self,
        repository: Path,
        function_name: str,
        code: str,
    ) -> None:
        source = self._get_source(repository)
        content = source.read_text(encoding="utf-8")

        if f"def {function_name}(" in content:
            raise RuntimeError(
                f"Function already exists: {function_name}"
            )

        source.write_text(
            content.rstrip()
            + "\n\n"
            + code.strip()
            + "\n",
            encoding="utf-8",
        )

    def _append_config_entry(
        self,
        repository: Path,
        key: str,
        value: str,
    ) -> None:
        source = self._get_source(repository)
        content = source.read_text(encoding="utf-8")

        entry = f'    "{key}": {value},'

        if entry in content:
            raise RuntimeError(
                f"Config entry already exists: {key}"
            )

        marker = "DEFAULT_CONFIG = {\n"

        if marker not in content:
            raise RuntimeError(
                "DEFAULT_CONFIG definition not found."
            )

        content = content.replace(
            marker,
            marker + entry + "\n",
            1,
        )

        source.write_text(
            content,
            encoding="utf-8",
        )

    def _ensure_test_import(
        self,
        repository: Path,
        function_name: str,
    ) -> None:
        test_file = self._get_tests(repository)
        content = test_file.read_text(encoding="utf-8")

        if function_name in self._imported_names(content):
            return

        marker = "from src.config import ("

        if marker not in content:
            raise RuntimeError(
                "Could not find config import block."
            )

        start = content.index(marker)
        end = content.index(")", start)

        import_block = content[start:end]

        updated_import_block = (
            import_block
            + f"\n    {function_name},"
        )

        content = (
            content[:start]
            + updated_import_block
            + content[end:]
        )

        test_file.write_text(
            content,
            encoding="utf-8",
        )

    def _imported_names(self, content: str) -> set[str]:
        marker = "from src.config import ("

        if marker not in content:
            return set()

        start = content.index(marker)
        end = content.index(")", start)

        block = content[start:end]

        names = set()

        for line in block.splitlines()[1:]:
            name = line.strip().rstrip(",")

            if name:
                names.add(name)

        return names

    def _append_test(
        self,
        repository: Path,
        marker: str,
        code: str,
    ) -> None:
        test_file = self._get_tests(repository)
        content = test_file.read_text(encoding="utf-8")

        if marker in content:
            raise RuntimeError(
                f"Requested test already exists: {marker}"
            )

        test_file.write_text(
            content.rstrip()
            + "\n\n"
            + code.strip()
            + "\n",
            encoding="utf-8",
        )

    def _ensure_pytest_import(
        self,
        repository: Path,
    ) -> None:
        test_file = self._get_tests(repository)
        content = test_file.read_text(encoding="utf-8")

        if "import pytest" in content:
            return

        test_file.write_text(
            "import pytest\n\n"
            + content,
            encoding="utf-8",
        )

    def _add_log_level_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository,
            "log_level",
            '"INFO"',
        )

        self._append_test(
            repository,
            "def test_log_level_config",
            """
def test_log_level_config():
    assert get_config_value("log_level") == "INFO"
""",
        )

    def _add_cache_enabled_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository,
            "cache_enabled",
            "True",
        )

        self._append_test(
            repository,
            "def test_cache_enabled_config",
            """
def test_cache_enabled_config():
    assert get_config_value("cache_enabled") is True
""",
        )

    def _add_api_url_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository,
            "api_url",
            '"https://api.example.com"',
        )

        self._append_test(
            repository,
            "def test_api_url_config",
            """
def test_api_url_config():
    assert (
        get_config_value("api_url")
        == "https://api.example.com"
    )
""",
        )

    def _add_database_timeout_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository,
            "database_timeout",
            "10",
        )

        self._append_test(
            repository,
            "def test_database_timeout_config",
            """
def test_database_timeout_config():
    assert (
        get_config_value("database_timeout")
        == 10
    )
""",
        )

    def _add_get_required_config(
        self,
        repository: Path,
    ) -> None:
        self._append_source(
            repository,
            "get_required_config",
            """
def get_required_config(key: str):
    if key not in DEFAULT_CONFIG:
        raise KeyError(
            f"Missing required configuration: {key}"
        )

    return DEFAULT_CONFIG[key]
""",
        )

        self._ensure_test_import(
            repository,
            "get_required_config",
        )

        self._ensure_pytest_import(repository)

        self._append_test(
            repository,
            "def test_get_required_config",
            """
def test_get_required_config():
    assert (
        get_required_config("timeout")
        == 30
    )

    with pytest.raises(KeyError):
        get_required_config("missing")
""",
        )

    def _add_config_key_exists(
        self,
        repository: Path,
    ) -> None:
        self._append_source(
            repository,
            "config_key_exists",
            """
def config_key_exists(key: str) -> bool:
    return key in DEFAULT_CONFIG
""",
        )

        self._ensure_test_import(
            repository,
            "config_key_exists",
        )

        self._append_test(
            repository,
            "def test_config_key_exists",
            """
def test_config_key_exists():
    assert config_key_exists("timeout") is True
    assert config_key_exists("missing") is False
""",
        )

    def _add_config_without_overrides(
        self,
        repository: Path,
    ) -> None:
        self._append_source(
            repository,
            "build_config",
            """
def build_config() -> dict:
    return DEFAULT_CONFIG.copy()
""",
        )

        self._ensure_test_import(
            repository,
            "build_config",
        )

        self._append_test(
            repository,
            "def test_build_config",
            """
def test_build_config():
    config = build_config()

    assert config == DEFAULT_CONFIG
    assert config is not DEFAULT_CONFIG
""",
        )

    def _add_config_validation(
        self,
        repository: Path,
    ) -> None:
        self._append_source(
            repository,
            "validate_config",
            """
def validate_config(config: dict) -> bool:
    if not isinstance(config.get("debug"), bool):
        return False

    if not isinstance(config.get("timeout"), int):
        return False

    if config["timeout"] < 0:
        return False

    if not isinstance(config.get("max_retries"), int):
        return False

    if config["max_retries"] < 0:
        return False

    if not isinstance(
        config.get("environment"),
        str,
    ):
        return False

    return True
""",
        )

        self._ensure_test_import(
            repository,
            "validate_config",
        )

        self._append_test(
            repository,
            "def test_validate_config",
            """
def test_validate_config():
    assert validate_config(DEFAULT_CONFIG) is True

    invalid = DEFAULT_CONFIG.copy()
    invalid["timeout"] = -1

    assert validate_config(invalid) is False
""",
        )

    def _add_config_copy(
        self,
        repository: Path,
    ) -> None:
        self._append_source(
            repository,
            "copy_config",
            """
def copy_config(config: dict) -> dict:
    return config.copy()
""",
        )

        self._ensure_test_import(
            repository,
            "copy_config",
        )

        self._append_test(
            repository,
            "def test_copy_config",
            """
def test_copy_config():
    original = {"timeout": 30}
    copied = copy_config(original)

    assert copied == original
    assert copied is not original
""",
        )

    def _add_environment_name_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository, "environment_name", '"local"'
        )
        self._append_test(
            repository,
            "def test_environment_name_config",
            """
def test_environment_name_config():
    assert get_config_value("environment_name") == "local"
            """,
        )

    def _add_request_timeout_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository, "request_timeout", "15"
        )
        self._append_test(
            repository,
            "def test_request_timeout_config",
            """
def test_request_timeout_config():
    assert get_config_value("request_timeout") == 15
            """,
        )

    def _add_feature_enabled_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository, "feature_enabled", "False"
        )
        self._append_test(
            repository,
            "def test_feature_enabled_config",
            """
def test_feature_enabled_config():
    assert get_config_value("feature_enabled") is False
            """,
        )

    def _add_region_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository, "region", '"local"'
        )
        self._append_test(
            repository,
            "def test_region_config",
            """
def test_region_config():
    assert get_config_value("region") == "local"
            """,
        )

    def _add_log_format_config(
        self,
        repository: Path,
    ) -> None:
        self._append_config_entry(
            repository,
            "log_format",
            '"%(levelname)s:%(message)s"',
        )
        self._append_test(
            repository,
            "def test_log_format_config",
            """
def test_log_format_config():
    assert (
        get_config_value("log_format")
        == "%(levelname)s:%(message)s"
    )
            """,
        )
