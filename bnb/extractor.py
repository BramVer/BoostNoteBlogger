import yaml
import logging

import attr

from bnb.config import Config
from bnb.exceptions import BoundsNotFound


logger = logging.getLogger(__name__)


@attr.s
class ExtractedContent:
    path = attr.ib()
    markdown = attr.ib()
    metadata = attr.ib()

    cfg = attr.ib(default=attr.Factory(Config))

    @property
    def title(self):
        return self.metadata["title"]

    @property
    def filename(self):
        return "{}{}".format(
            self.title.lower().replace(" ", "_"), self.cfg.markdown_extension
        )

    @property
    def folder(self):
        metafold = self.metadata["folder"]
        return self.cfg.folders.get(metafold)

    @property
    def tags(self):
        return self.metadata["tags"]


class Extractor:
    def __init__(self, config=None):
        self.cfg = config or Config()

    def extract(self, path):
        content = self._read_file(path)

        return ExtractedContent(
            path=path,
            markdown=self.extract_markdown(content),
            metadata=self.extract_metadata(content),
            cfg=self.cfg,
        )

    def _read_file(self, file):
        logger.info(f"Reading file at: {file}")
        with open(file, "r") as f:
            return f.readlines()

    def _get_content_boundaries(self, content, open_, close_):
        try:
            _from = content.index(open_)
            _to = content.index(close_)
        except ValueError as verr:
            msg = f"Boundary is missing in text-content:\n{verr}"
            raise BoundsNotFound(msg)

        return _from, _to

    def extract_markdown(self, content):
        open_ = self.cfg.markdown_open
        close_ = self.cfg.markdown_close

        _from, _to = self._get_content_boundaries(content, open_, close_)

        markdown = content[(_from + 1) : _to]

        return [l.strip() for l in markdown]

    def extract_metadata(self, content):
        open_ = self.cfg.markdown_open
        close_ = self.cfg.markdown_close

        _from, _to = self._get_content_boundaries(content, open_, close_)

        meta_start = content[0:_from]
        meta_end = content[(_to + 1) :]

        joined = "\n".join(meta_start + meta_end)

        return yaml.safe_load(joined)
