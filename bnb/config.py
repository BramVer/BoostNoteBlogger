from enum import Enum

from smart_getenv import getenv


class _Defaults(Enum):
    """This is purely used to store the default config options."""
    MARKDOWN_START = "content: '''",
    MARKDOWN_END = "'''",
    TITLE_INDICATOR = "title: \"",
    FOLDER_INDICATOR = "folder: \"",
    YAML_STRING_INDICATOR = "\"",
    CSON_EXTENSION = ".cson",
    MARKDOWN_EXTENSION = ".md",
    METADATA_EXTENSION = ".yml",
    METADATA_FOLDER = "meta",
    BNOTE_SETTINGS_FILE = "boostnote.json",


class Config:
    def __init__(self):
        for name, value in _Defaults.__members__.items():
            self.setattr(name, self.get(name, value))

    def get(self, key, _type=None):
        kwargs = {"name": key, "default": self._defaults.get(key)}

        if _type:
            kwargs["type"] = _type

        return getenv(**kwargs)
