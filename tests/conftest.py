import pytest


@pytest.fixture(scope="session")
def file(self):
    with open(TEST_DATA_DIR / TEST_FILE) as f:
        return f.read()
