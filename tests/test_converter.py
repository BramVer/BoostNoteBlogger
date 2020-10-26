import yaml

import markdown

from bnb.extractor import Extractor
from bnb.converter import Converter, ConvertedContent


class TestConverter:
    def test_it_turns_extracted_into_converted_content(self, cfg, fpath):
        extractor = Extractor(cfg)
        converter = Converter(cfg)

        extr_content = extractor.run(fpath)
        content = converter.run(extr_content)

        markdown = content.markdown
        metadata = content.metadata

        assert isinstance(markdown, str)
        assert isinstance(metadata, dict)

        assert "<h1>This is a test</h1>" in markdown
        assert "<code>python\nimport json" in markdown

        assert content.title == "Test Note"
        assert content.folder == "Folder One"
        assert content.tags == ["tag_one"]
