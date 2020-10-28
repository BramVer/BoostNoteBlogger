import pytest

from bnb.config import Config
from . import TEST_DATA_DIR, TEST_FILE, TEST_BNOTE


@pytest.fixture
def fpath():
    return TEST_DATA_DIR / TEST_FILE


@pytest.fixture
def file(fpath):
    with open(fpath) as f:
        return f.read()


@pytest.fixture
def cfg():
    return Config(bnote_settings_file=TEST_DATA_DIR / TEST_BNOTE)


@pytest.fixture
def base_dir(tmpdir, file):
    tmpdir.mkdir("notes").mkdir("subbestfolder")
    for i in range(10):
        file = tmpdir.join("notes", f"file_{i}.cson")
        file.write(file)

    for i in range(5):
        file = tmpdir.join("notes", "subbestfolder", f"file_{i}.cson")
        file.write(file)

    return tmpdir
