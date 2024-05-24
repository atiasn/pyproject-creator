import shutil
import sys
from pathlib import Path

import pytest

from pyproject_creator.cli import BASE_PATH


@pytest.fixture
def rootdir(request):
    return Path(request.config.rootdir)


@pytest.fixture(scope='session', autouse=True)
def add_python_path():
    sys.path.insert(0, str(BASE_PATH.parent.resolve()))


@pytest.fixture(scope="function")
def project_name(rootdir):
    _name = "a-test-create-project"
    _path = rootdir / _name
    if _path.exists():
        shutil.rmtree(_path)
    yield _name
