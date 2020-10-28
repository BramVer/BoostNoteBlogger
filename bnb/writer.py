import os
from pathlib import Path

from bnb.config import Config
from bnb.exceptions import PathConstructionError


class Writer:
    def __init__(self, config=None):
        self.cfg = config or Config()

    def _create_if_not_present(self, path):
        if not os.path.exists(path.parent):
            os.makedirs(path.parent)

    def _create_file(self, path, content):
        self._create_if_not_present(path)
        with open(path, "w") as f:
            f.write(content)

    def _construct_new_path(self, conv_content):
        injection = self.cfg.output_folder
        fname = conv_content.filename
        folder = conv_content.folder

        parts = conv_content.path.absolute().parts
        notes = parts.index(self.cfg.notes_folder)

        return Path(*parts[:notes]).joinpath(injection, folder, fname)

    def run(self, converted_content):
        # write
        path = self._construct_new_path(converted_content)
        self._create_file(path, converted_content.content)
