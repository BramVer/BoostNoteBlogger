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

    def _scan_metadata(self, open_, close_=None, match_one=True):
        close_ = close_ or self.cfg.string_in_yaml

        if match_one:
            line = next(c for c in self.metadata if c.startswith(open_))
            return line.replace(open_, "").rstrip(close_)

        start = self.metadata.index(open_)
        end = self.metadata.index(close_)

        return [
            l.strip(self.cfg.string_in_yaml) for l in self.metadata[start + 1 : end]
        ]

    @property
    def title(self):
        title = self._scan_metadata(self.cfg.title_indicator)

        return title

    @property
    def filename(self):
        return "{}{}".format(
            self.title.lower().replace(" ", "_"), self.cfg.markdown_extension
        )

    @property
    def folder(self):
        folder = self._scan_metadata(self.cfg.folder_indicator)
        return self.cfg.folders.get(folder)

    @property
    def tags(self):
        return self._scan_metadata(
            self.cfg.tags_open, self.cfg.tags_close, match_one=False
        )


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
            _from = content.index(self.cfg.markdown_open)
            _to = content.index(self.cfg.markdown_close)
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
