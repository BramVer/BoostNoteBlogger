from pathlib import Path

import pytest

from bnb.config import Config
from bnb.exceptions import BoundsNotFound
from bnb.extractor import Extractor, ExtractedContent


TEST_FILE = "test_file.cson"
TEST_BNOTE = "boostnote.json"
TEST_DATA_DIR = Path(__file__).resolve().parent / "data"


@pytest.fixture(scope="session")
def file(self):
    with open(TEST_DATA_DIR / TEST_FILE) as f:
        return f.read()


class TestExtractor:
    def test_it_extracts_properly(self):
        cfg = Config(bnote_settings_file=TEST_DATA_DIR / TEST_BNOTE)

        extractor = Extractor(config=cfg)
        result = extractor.extract(TEST_DATA_DIR / TEST_FILE)

        assert isinstance(result, ExtractedContent)
        assert result.path == TEST_DATA_DIR / TEST_FILE

        assert "## Content" in result.markdown

        assert result.title == "Test Note"
        assert result.filename == "test_note.md"
        assert result.folder == "Folder One"
        assert result.tags == ["tag_one"]

    def test_extracting_missing_markdown_raises(self):
        cfg = Config(
            markdown_open="beep-beep", bnote_settings_file=TEST_DATA_DIR / TEST_BNOTE
        )

        extractor = Extractor(config=cfg)
        with pytest.raises(BoundsNotFound):
            extractor.extract(TEST_DATA_DIR / TEST_FILE)
