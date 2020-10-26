import json

import attr

from bnb.config import Config
from bnb.exceptions import MarkdownBoundsNotFound


@attr.s
class ExtractedContent:
    path = attr.ib()
    content = attr.ib()
    markdown = attr.ib()
    metadata = attr.ib()

    def _scan_content_for_pattern(self, start, end=None):
        end = end or self.cfg.yaml_string_indicator
        line = next(c for c in self.content if c.startswith(start))
        if not line:
            return

        return line.replace(start, "").rstrip(end)

    @property
    def title(self):
        title = self._scan_content(self.cfg.title_indicator)

        return title

    @property
    def filename(self):
        return self.title.lower().replace(" ", "_")

    @property
    def folder(self):
        return self._scan_content(self.cfg.folder_indicator)

    @property
    def tags(self):
        return self._scan_content(self.cfg.tags_indicator)


class Extractor:
    def __init__(self, config=None):
        self.cfg = config or Config()

    def run(self, path):
        content = self._read_file(path)

        return ExtractedContent(
            path=path,
            content=content,
            markdown=self.extract_markdown(content),
            metadata=self.extract_metadata(content),
        )

    def _read_file(self, file):
        with open(file, "r") as f:
            return f.readlines()

    def _get_markdown_index_boundaries(self, content):
        try:
            _from = content.index(self.cfg.markdown_start)
            _to = content.index(self.cfg.markdown_end)
        except ValueError as verr:
            msg = f"Markdown boundary is missing in content:\n{verr}"
            raise MarkdownBoundsNotFound(msg)

        return _from, _to

    def extract_markdown(self, content):
        _from, _to = self._get_markdown_index_boundaries(content)

        markdown = content[(_from + 1) : _to]

        return [c.lstrip() for c in markdown]

    def extract_metadata(self, content):
        _from, _to = self._get_markdown_index_boundaries(content)

        first_half = content[0:_from]
        second_half = content[(_to + 1) :]

        return json.load(first_half + second_half)
