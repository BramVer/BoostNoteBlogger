import json

import attr

from bnb.config import Config
from bnb.exceptions import MarkdownBoundsNotFound


@attr.s
class ExtractedContent:
    path = attr.ib()
    markdown = attr.ib()
    metadata = attr.ib()

    cfg = attr.ib(default=attr.Factory(Config))

    def _scan_metadata(self, pattern, closing_pattern=None):
        closing_pattern = closing_pattern or self.cfg.yaml_string_indicator
        line = next(c for c in self.metadata if c.startswith(pattern))
        if not line:
            return

        return line.replace(pattern, "").rstrip(closing_pattern)

    @property
    def title(self):
        title = self._scan_metadata(self.cfg.title_indicator)

        return title

    @property
    def filename(self):
        return self.title.lower().replace(" ", "_")

    @property
    def folder(self):
        folder = self._scan_metadata(self.cfg.folder_indicator)
        return self.cfg.folders.get(folder)

    @property
    def tags(self):
        return self._scan_metadata(self.cfg.tags_indicator)


class Extractor:
    def __init__(self, config=None):
        self.cfg = config or Config()

    def run(self, path):
        content = self._read_file(path)

        return ExtractedContent(
            path=path,
            markdown=self.extract_markdown(content),
            metadata=self.extract_metadata(content),
            cfg=self.cfg,
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

        return [l.strip() for l in markdown]

    def extract_metadata(self, content):
        _from, _to = self._get_markdown_index_boundaries(content)

        first_half = content[0:_from]
        second_half = content[(_to + 1) :]

        return [l.strip() for l in (first_half + second_half)]
