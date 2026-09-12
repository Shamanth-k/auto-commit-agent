from pathlib import Path

from app.executors.base import BaseExecutor


class FileUtilsExecutor(BaseExecutor):

    def execute(self, task: dict, repository_path: str) -> None:
        repository = Path(repository_path)
        action = task["action"]

        actions = {
            "add_file_name_without_extension": self._add_file_name_without_extension,
            "add_absolute_file_path": self._add_absolute_file_path,
            "add_parent_directory": self._add_parent_directory,
            "add_file_is_empty": self._add_file_is_empty,
            "add_read_lines": self._add_read_lines,
            "add_append_text_file": self._add_append_text_file,
            "add_create_directory": self._add_create_directory,
            "add_delete_file": self._add_delete_file,
            "add_file_size_kilobytes": self._add_file_size_kilobytes,
            "add_file_size_megabytes": self._add_file_size_megabytes,
            "add_file_extension_lowercase": self._add_file_extension_lowercase,
            "add_is_regular_file": self._add_is_regular_file,
            "add_parent_name": self._add_parent_name,
        }

        executor = actions.get(action)

        if executor is None:
            raise ValueError(
                f"Unsupported file_utils action: {action}"
            )

        executor(repository)

    def _source_function_exists(
        self,
        repository: Path,
        function_name: str,
    ) -> None:
        source = repository / "src" / "file_utils.py"

        if not source.exists():
            raise FileNotFoundError(
                "src/file_utils.py not found."
            )

        content = source.read_text(encoding="utf-8")

        if f"def {function_name}(" not in content:
            raise RuntimeError(
                f"Required function not found: {function_name}"
            )

    def _append_source_function(
        self,
        repository: Path,
        function_name: str,
        function_code: str,
    ) -> None:
        source = repository / "src" / "file_utils.py"
        content = source.read_text(encoding="utf-8")

        if f"def {function_name}(" in content:
            raise RuntimeError(
                f"Function already exists: {function_name}"
            )

        updated = (
            content.rstrip()
            + "\n\n"
            + function_code.strip()
            + "\n"
        )

        source.write_text(
            updated,
            encoding="utf-8",
        )

    def _get_test_file(self, repository: Path) -> Path:
        test_file = repository / "tests" / "test_file_utils.py"

        if not test_file.exists():
            raise FileNotFoundError(
                "tests/test_file_utils.py not found."
            )

        return test_file

    def _add_test_import(
        self,
        repository: Path,
        function_name: str,
    ) -> None:
        test_file = self._get_test_file(repository)
        content = test_file.read_text(encoding="utf-8")

        import_start = "from src.file_utils import ("

        if import_start not in content:
            raise RuntimeError(
                "Expected file_utils import block "
                "was not found."
            )

        start = content.index(import_start)
        end = content.index(")", start)
        import_block = content[start:end]

        if function_name in import_block:
            return

        updated_import_block = (
            import_block.rstrip()
            + f"\n    {function_name},\n"
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

    def _append_test(
        self,
        repository: Path,
        marker: str,
        test_code: str,
    ) -> None:
        test_file = self._get_test_file(repository)
        content = test_file.read_text(encoding="utf-8")

        if marker in content:
            raise RuntimeError(
                f"Requested test already exists: {marker}"
            )

        updated = (
            content.rstrip()
            + "\n\n"
            + test_code.strip()
            + "\n"
        )

        test_file.write_text(
            updated,
            encoding="utf-8",
        )

    def _add_file_name_without_extension(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "get_file_name",
        )

        self._append_source_function(
            repository,
            "get_file_stem",
            """
def get_file_stem(path: str) -> str:
    return Path(path).stem
""",
        )

        self._add_test_import(
            repository,
            "get_file_stem",
        )

        self._append_test(
            repository,
            "def test_get_file_stem",
            """
def test_get_file_stem():
    assert get_file_stem("reports/data.csv") == "data"
    assert get_file_stem("README") == "README"
""",
        )

    def _add_absolute_file_path(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "file_exists",
        )

        self._append_source_function(
            repository,
            "get_absolute_path",
            """
def get_absolute_path(path: str) -> str:
    return str(Path(path).resolve())
""",
        )

        self._add_test_import(
            repository,
            "get_absolute_path",
        )

        self._append_test(
            repository,
            "def test_get_absolute_path",
            """
def test_get_absolute_path():
    from pathlib import Path

    result = get_absolute_path("example.txt")
    assert Path(result).is_absolute()
""",
        )

    def _add_parent_directory(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "get_file_name",
        )

        self._append_source_function(
            repository,
            "get_parent_directory",
            """
def get_parent_directory(path: str) -> str:
    return str(Path(path).parent)
""",
        )

        self._add_test_import(
            repository,
            "get_parent_directory",
        )

        self._append_test(
            repository,
            "def test_get_parent_directory",
            """
def test_get_parent_directory():
    assert get_parent_directory(
        "reports/data.csv"
    ) == "reports"
""",
        )

    def _add_file_is_empty(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "file_exists",
        )

        self._append_source_function(
            repository,
            "is_file_empty",
            """
def is_file_empty(path: str) -> bool:
    return Path(path).stat().st_size == 0
""",
        )

        self._add_test_import(
            repository,
            "is_file_empty",
        )

        self._append_test(
            repository,
            "def test_is_file_empty",
            """
def test_is_file_empty(tmp_path):
    empty_file = tmp_path / "empty.txt"
    content_file = tmp_path / "content.txt"

    empty_file.write_text("", encoding="utf-8")
    content_file.write_text("data", encoding="utf-8")

    assert is_file_empty(str(empty_file)) is True
    assert is_file_empty(str(content_file)) is False
""",
        )

    def _add_read_lines(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "read_text_file",
        )

        self._append_source_function(
            repository,
            "read_text_lines",
            """
def read_text_lines(path: str) -> list[str]:
    return Path(path).read_text(
        encoding="utf-8"
    ).splitlines()
""",
        )

        self._add_test_import(
            repository,
            "read_text_lines",
        )

        self._append_test(
            repository,
            "def test_read_text_lines",
            """
def test_read_text_lines(tmp_path):
    file = tmp_path / "lines.txt"

    file.write_text(
        "first\\nsecond\\nthird\\n",
        encoding="utf-8",
    )

    assert read_text_lines(str(file)) == [
        "first",
        "second",
        "third",
    ]
""",
        )

    def _add_append_text_file(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "write_text_file",
        )

        self._append_source_function(
            repository,
            "append_text_file",
            """
def append_text_file(path: str, content: str) -> None:
    with Path(path).open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(content)
""",
        )

        self._add_test_import(
            repository,
            "append_text_file",
        )

        self._append_test(
            repository,
            "def test_append_text_file",
            """
def test_append_text_file(tmp_path):
    file = tmp_path / "append.txt"

    file.write_text(
        "hello",
        encoding="utf-8",
    )

    append_text_file(
        str(file),
        " world",
    )

    assert file.read_text(
        encoding="utf-8"
    ) == "hello world"
""",
        )

    def _add_create_directory(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "file_exists",
        )

        self._append_source_function(
            repository,
            "ensure_directory",
            """
def ensure_directory(path: str) -> None:
    Path(path).mkdir(
        parents=True,
        exist_ok=True,
    )
""",
        )

        self._add_test_import(
            repository,
            "ensure_directory",
        )

        self._append_test(
            repository,
            "def test_ensure_directory",
            """
def test_ensure_directory(tmp_path):
    directory = tmp_path / "nested" / "folder"

    ensure_directory(str(directory))

    assert directory.is_dir()
""",
        )

    def _add_delete_file(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "file_exists",
        )

        self._append_source_function(
            repository,
            "delete_file",
            """
def delete_file(path: str) -> None:
    file = Path(path)

    if file.exists():
        file.unlink()
""",
        )

        self._add_test_import(
            repository,
            "delete_file",
        )

        self._append_test(
            repository,
            "def test_delete_file",
            """
def test_delete_file(tmp_path):
    file = tmp_path / "delete.txt"

    file.write_text(
        "data",
        encoding="utf-8",
    )

    delete_file(str(file))

    assert file.exists() is False
""",
        )

    def _add_file_size_kilobytes(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "get_file_size",
        )

        self._append_source_function(
            repository,
            "get_file_size_kb",
            """
def get_file_size_kb(path: str) -> float:
    return get_file_size(path) / 1024
""",
        )

        self._add_test_import(
            repository,
            "get_file_size_kb",
        )

        self._append_test(
            repository,
            "def test_get_file_size_kb",
            """
def test_get_file_size_kb(tmp_path):
    file = tmp_path / "data.bin"

    file.write_bytes(
        b"a" * 2048
    )

    assert get_file_size_kb(
        str(file)
    ) == 2.0
""",
        )

    def _add_file_size_megabytes(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "get_file_size",
        )

        self._append_source_function(
            repository,
            "get_file_size_mb",
            """
def get_file_size_mb(path: str) -> float:
    return get_file_size(path) / (1024 * 1024)
""",
        )

        self._add_test_import(
            repository,
            "get_file_size_mb",
        )

        self._append_test(
            repository,
            "def test_get_file_size_mb",
            """
def test_get_file_size_mb(tmp_path):
    file = tmp_path / "data.bin"

    file.write_bytes(
        b"a" * (1024 * 1024)
    )

    assert get_file_size_mb(
        str(file)
    ) == 1.0
""",
        )

    def _add_file_extension_lowercase(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "get_file_extension",
        )

        self._append_source_function(
            repository,
            "get_file_extension_lower",
            """
def get_file_extension_lower(path: str) -> str:
    return Path(path).suffix.lower()
""",
        )

        self._add_test_import(
            repository,
            "get_file_extension_lower",
        )

        self._append_test(
            repository,
            "def test_get_file_extension_lower",
            """
def test_get_file_extension_lower():
    assert get_file_extension_lower(
        "Report.PDF"
    ) == ".pdf"
""",
        )

    def _add_is_regular_file(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "file_exists",
        )

        self._append_source_function(
            repository,
            "is_regular_file",
            """
def is_regular_file(path: str) -> bool:
    return Path(path).is_file()
""",
        )

        self._add_test_import(
            repository,
            "is_regular_file",
        )

        self._append_test(
            repository,
            "def test_is_regular_file",
            """
def test_is_regular_file(tmp_path):
    file = tmp_path / "data.txt"
    directory = tmp_path / "folder"

    file.write_text(
        "data",
        encoding="utf-8",
    )

    directory.mkdir()

    assert is_regular_file(
        str(file)
    ) is True

    assert is_regular_file(
        str(directory)
    ) is False
""",
        )

    def _add_parent_name(
        self,
        repository: Path,
    ) -> None:
        self._source_function_exists(
            repository,
            "get_file_name",
        )

        self._append_source_function(
            repository,
            "get_parent_name",
            """
def get_parent_name(path: str) -> str:
    return Path(path).parent.name
""",
        )

        self._add_test_import(
            repository,
            "get_parent_name",
        )

        self._append_test(
            repository,
            "def test_get_parent_name",
            """
def test_get_parent_name():
    assert get_parent_name(
        "reports/data.csv"
    ) == "reports"
""",
        )