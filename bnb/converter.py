import logging

import yaml
import attr
import markdown

from bnb.config import Config


logger = logging.getLogger(__name__)


@attr.s
class ConvertedContent:
    path = attr.ib()
    markdown = attr.ib(type=str)
    metadata = attr.ib(type=dict)

    cfg = attr.ib(default=attr.Factory(Config))

    @property
    def title(self):
        return self.metadata["title"]

    @property
    def folder(self):
        metafold = self.metadata["folder"]
        return self.cfg.folders.get(metafold)

    @property
    def tags(self):
        return self.metadata["tags"]


class Converter:
    _glue = "\n"

    def __init__(self, config=None):
        self.cfg = config or Config()
        self.md = markdown.Markdown(output_format="html")

    def _glue_content(self, lines):
        return self._glue.join(lines)

    def _convert_markdown(self, content):
        if not content:
            logger.warning("Content empty, cannot be converted to markdown!")

        return self.md.convert(self._glue_content(content))

    def _convert_metadata(self, content):
        if not content:
            logger.warning("Content empty, cannot be converted to metadata!")

        return yaml.safe_load(self._glue_content(content))

    def run(self, extracted_content):
        logger.info(f"Converting content at {extracted_content.path}")

        return ConvertedContent(
            cfg=self.cfg,
            path=extracted_content.path,
            markdown=self._convert_markdown(extracted_content.markdown),
            metadata=self._convert_metadata(extracted_content.metadata),
        )
