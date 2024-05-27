import sys
import shutil
from pathlib import Path

import pytest

from pyproject_creator.cli import BASE_PATH


@pytest.fixture(scope="session")  # type: ignore
def rootdir(request) -> Path:
    return Path(request.config.rootdir)


@pytest.fixture(scope="session", autouse=True)  # type: ignore
def add_python_path() -> None:
    sys.path.insert(0, str(BASE_PATH.parent.resolve()))


@pytest.fixture(scope="session")  # type: ignore
def project_names(rootdir: Path) -> list[str]:
    _names = ["a-test-create-project", "a-test-create-project-without"]
    for _name in _names:
        _path = rootdir / _name
        if _path.exists():
            shutil.rmtree(_path.resolve())
    return _names
