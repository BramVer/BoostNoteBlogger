import attr
from smart_getenv import getenv


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
    ConfigOption("MARKDOWN_START", "content: '''"),
    ConfigOption("MARKDOWN_END", "'''"),
    ConfigOption("TITLE_INDICATOR", "title: \""),
    ConfigOption("FOLDER_INDICATOR", "folder: \""),
    ConfigOption("YAML_STRING_INDICATOR", "\""),
    ConfigOption("CSON_EXTENSION", ".cson"),
    ConfigOption("MARKDOWN_EXTENSION", ".md"),
    ConfigOption("METADATA_EXTENSION", ".yml"),
    ConfigOption("METADATA_FOLDER", "meta"),
    ConfigOption("BNOTE_SETTINGS_FILE", "boostnote.json"),
    ConfigOption("TAGS_INDICATOR", "tags: \""),
)


class Config:
    def __init__(self, **kwargs):
        for option in _defaults:
            setattr(self, option.key, option.value)

        for key, value in kwargs.items():
            setattr(self, key, value)
