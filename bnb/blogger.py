from pathlib import Path

from bnb.config import Config
from bnb.writer import Writer
from bnb.scanner import Scanner
from bnb.extractor import Extractor
from bnb.converter import Converter
from bnb.exceptions import CofigurationError


class Blogger:
    def __init__(self, home, config=None):
        self.cfg = config or Config()
        self.home = Path(home)

    def _create_index_file(self, files):
        pass

    def _assert_settings_file(self, path):
        settings = Path(path / self.bnote_settings_file)
        if not settings.exists():
            msg = f"{self.bnote_settings_file} could not be found at {path}."
            raise CofigurationError(msg)

    def _assert_notes_folder(self, path):
        notes = Path(path / self.notes_folder)
        if not notes.exists():
            msg = f"No notes folder found at {path}."
            raise CofigurationError(msg)

    def run(self):
        pass
        # Sniff valid init
        # Create index.html
        # Loop over files
