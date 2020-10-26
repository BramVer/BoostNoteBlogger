import mock
import pytest
import markdown
from yaml.parser import ParserError

from bnb.extractor import Extractor, ExtractedContent
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

    def test_it_raises_on_incorrect_data(self, cfg, fpath):
        incorrect_data = {
            "cfg": cfg,
            "path": fpath,
            "markdown": [],
            "metadata": {},
        }

        converter = Converter(cfg)
        with pytest.raises(AttributeError):
            converter.run(incorrect_data)

    @mock.patch("bnb.converter.logger")
    def test_it_warns_on_empty_lines(self, mock_logger, cfg, fpath):
        converter = Converter(cfg)
        bad_content = ExtractedContent(path=fpath, markdown=[], metadata=[])

        assert mock_logger.warning.call_count == 0

        converter._convert_markdown(bad_content.markdown)
        assert mock_logger.warning.call_count == 1

        converter._convert_metadata(bad_content.metadata)
        assert mock_logger.warning.call_count == 2

    @pytest.mark.parametrize(
        "prop, exc, lines",
        [
            ["metadata", TypeError, ["title: 'title_one'", None]],
            [
                "metadata",
                ParserError,
                [
                    "'title' = 'title_one'",
                ],
            ],
            ["markdown", TypeError, [8]],
            ["markdown", TypeError, ["This is valid markdown", None]],
        ],
    )
    def test_it_raises_on_incorrect_lines(self, prop, exc, lines, cfg, fpath):
        extractor = Extractor(cfg)
        converter = Converter(cfg)

        content = extractor.run(fpath)
        kwargs = {
            "path": content.path,
            "markdown": content.markdown,
            "metadata": content.metadata,
        }

        kwargs[prop] = lines

        with pytest.raises(exc):
            converter.run(ExtractedContent(**kwargs))
