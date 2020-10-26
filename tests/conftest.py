import pytest

from bnb.config import Config
from . import TEST_DATA_DIR, TEST_FILE, TEST_BNOTE


@pytest.fixture
def fpath():
    return TEST_DATA_DIR / TEST_FILE


@pytest.fixture(scope="session")
def file(fpath):
    with open(fpath) as f:
        return f.read()


@pytest.fixture
def cfg():
    return Config(bnote_settings_file=TEST_DATA_DIR / TEST_BNOTE)
