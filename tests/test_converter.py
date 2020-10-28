import pathlib

import mock
import pytest
import markdown
from yaml.parser import ParserError

from bnb.config import Config
from bnb.exceptions import FolderCouldNotBeMapped
from bnb.extractor import Extractor, ExtractedContent
from bnb.converter import Converter, ConvertedContent


class TestConvertedContent:
    @pytest.mark.parametrize(
        "field, type_, value",
        [
            ["path", pathlib.Path, pathlib.PosixPath("data")],
            ["path", pathlib.Path, "data"],
            ["path", pathlib.Path, ""],
            ["path", pathlib.Path, "/"],
            ["path", pathlib.Path, ":dabbing_on_the_haters:"],
            ["content", str, 8],
            ["content", str, None],
            ["content", str, "<h1>Hi</h1>"],
            ["metadata", dict, {}],
            ["metadata", dict, {1: 2}],
            ["metadata", dict, []],
        ],
    )
    def test_it_converts_input_to_type(self, field, type_, value):
        kwargs = {
            "path": "",
            "content": [],
            "metadata": {},
        }

        kwargs[field] = value
        content = ConvertedContent(**kwargs)

        attr = getattr(content, field)
        assert isinstance(attr, type_)

    def test_it_raises_specific_when_folder_not_found(self, cfg):
        content = ConvertedContent(
            cfg=cfg, path="/", content="", metadata={"folder": "key_for_folder_one"}
        )

        # Config uses provided bnote_settings_file in tests/data, all good
        assert content.folder

        # Config without mapping file
        new_cfg = Config()
        content.cfg = new_cfg

        with pytest.raises(FolderCouldNotBeMapped):
            content.folder

        # Remove folder from metadata so nothing can be found
        content.cfg = cfg
        content.metadata = {}
        with pytest.raises(FolderCouldNotBeMapped):
            content.folder

        content.metadata["folder"] = "THIS FOLDER DOES NOT EXIST"
        with pytest.raises(FolderCouldNotBeMapped):
            content.folder


class TestConverter:
    def test_it_turns_extracted_into_converted_content(self, cfg, fpath):
        extractor = Extractor(cfg)
        converter = Converter(cfg)

        extr_content = extractor.run(fpath)
        conv_content = converter.run(extr_content)

        markdown = conv_content.content
        metadata = conv_content.metadata

        assert isinstance(markdown, str)
        assert isinstance(metadata, dict)

        assert "<h1>This is a test</h1>" in markdown
        assert "<code>python\nimport json" in markdown

        assert conv_content.title == "Test Note"
        assert conv_content.folder == "Folder One"
        assert conv_content.tags == ["tag_one"]

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
