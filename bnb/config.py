from smart_getenv import getenv


# This is purely used to store the default config options
_defaults = {
    "MARKDOWN_START": "content: '''",
    "MARKDOWN_END": "'''",
    "TITLE_INDICATOR": "title: \"",
    "FOLDER_INDICATOR": "folder: \"",
    "YAML_STRING_INDICATOR": "\"",
    "CSON_EXTENSION": ".cson",
    "MARKDOWN_EXTENSION": ".md",
    "METADATA_EXTENSION": ".yml",
    "METADATA_FOLDER": "meta",
    "BNOTE_SETTINGS_FILE": "boostnote.json",
}


class Config:
    def __getitem__(self, key, _type=None):
        kwargs = {"name": key, "default": _defaults.get(key)}

        if _type:
            kwargs["type"] = _type

        return getenv(**kwargs)
