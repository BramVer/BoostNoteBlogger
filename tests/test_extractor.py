from pathlib import Path

import pytest

from bnb.config import Config
from bnb.extractor import Extractor, ExtractedContent


TEST_FILE = "test_file.cson"
TEST_BNOTE = "boostnote.json"
TEST_DATA_DIR = Path(__file__).resolve().parent / "data"


@pytest.fixture(scope="session")
def file(self):
    with open(TEST_DATA_DIR / TEST_FILE) as f:
        return f.read()


# class TestExtractedContent:
#     @pytest.fixture
#     def metadata(self):
#         return (
#             'createdAt: "2020-10-26T12:26:31.560Z"\n',
#             'updatedAt: "2020-10-26T12:27:42.273Z"\n',
#             'type: "MARKDOWN_NOTE"\n',
#             'folder: "key_for_folder_one"\n',
#             'title: "Test Note"\n',
#             'tags: [\n',
#             '\t'

#         )

#     def test_it_extracts_all_parts(self, metadata):
#         markdown = "# This is a markdown file\n## Subtitle\nWow cool"
#         path = "path/path"
#         ec = ExtractedContent()


class TestExtractor:
    def test_it_extracts_all_parts(self):
        cfg = Config(bnote_settings_file=TEST_DATA_DIR / TEST_BNOTE)

        extractor = Extractor(config=cfg)
        result = extractor.run(TEST_DATA_DIR / TEST_FILE)

        assert isinstance(result, ExtractedContent)
        assert result.path == TEST_DATA_DIR / TEST_FILE

        assert "## Content" in result.markdown

        assert result.title == "Test Note"
        assert result.filename == "test_note.md"
        assert result.folder == "Folder One"
