import pytest
import markdown

from bnb.config import Config
from bnb.exceptions import BoundsNotFound
from bnb.extractor import Extractor, ExtractedContent
from . import TEST_FILE, TEST_BNOTE, TEST_DATA_DIR


class TestExtractor:
    def test_it_reads_and_extracts_properly(self):
        cfg = Config(bnote_settings_file=TEST_DATA_DIR / TEST_BNOTE)

        extractor = Extractor(config=cfg)
        result = extractor.run(TEST_DATA_DIR / TEST_FILE)

        assert isinstance(result, ExtractedContent)
        assert result.path == TEST_DATA_DIR / TEST_FILE
        assert "## Content" in result.markdown
        assert 'title: "Test Note"' in result.metadata

    def test_extracting_missing_markdown_raises(self):
        cfg = Config(
            markdown_open="beep-beep", bnote_settings_file=TEST_DATA_DIR / TEST_BNOTE
        )

        extractor = Extractor(config=cfg)
        with pytest.raises(BoundsNotFound):
            extractor.run(TEST_DATA_DIR / TEST_FILE)
