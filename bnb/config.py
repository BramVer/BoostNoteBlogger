import os
import json
import logging
from functools import cached_property

import attr
from smart_getenv import getenv

from bnb.exceptions import FolderCouldNotBeMapped


logger = logging.getLogger(__name__)


@attr.s
class ConfigOption:
    name = attr.ib()
    default = attr.ib()
    _type = attr.ib(default=str)

    @property
    def key(self):
        return self.name.lower()

    @property
    def value(self):
        return getenv(name=self.name, type=self._type, default=self.default)


# This is purely used to store the default config options
_defaults = (
    ConfigOption("MARKDOWN_OPEN", "content: '''\n"),
    ConfigOption("MARKDOWN_CLOSE", "'''\n"),
    ConfigOption("MARKDOWN_EXTENSION", ".md"),
    ConfigOption("METADATA_EXTENSION", ".yml"),
    ConfigOption("CSON_EXTENSION", ".cson"),
    ConfigOption("OUTPUT_EXTENSION", ".html"),
    ConfigOption("METADATA_FOLDER", "meta"),
    ConfigOption("OUTPUT_FOLDER", "build"),
    ConfigOption("NOTES_FOLDER", "notes"),
    ConfigOption("BNOTE_SETTINGS_FILE", "boostnote.json"),
)


class Config:
    def __init__(self, **kwargs):
        for option in _defaults:
            setattr(self, option.key, option.value)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.bnote_settings = None

    def read_boostnote_settings(self):
        try:
            with open(
                self.bnote_settings_file,
            ) as f:
                data = json.load(f)
        except FileNotFoundError:
            msg = "Error: Could not locate the Boostnote Settings File at '{}'"
            logger.error(msg.format(self.bnote_settings_file))
            raise FolderCouldNotBeMapped(msg)

        self.bnote_settings = data
        return data

    @cached_property
    def folders(self):
        if not self.bnote_settings:
            self.read_boostnote_settings()

        return {f["key"]: f["name"] for f in self.bnote_settings["folders"]}

    def setup(self):
        # Create necessary folders
        # Create index.html
        pass
