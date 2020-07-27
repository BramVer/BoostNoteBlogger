from pathlib import Path
from typing import Generator

from bnb.config import Config


class Scanner:
    """Scans the directory recursively for matching files."""
    def __init__(self, config=None):
        self.config = config or Config()

    def _scan_path_for_pattern_matches(self, path: str) -> Generator:
        pattern = f"*{self.config.CSON_PATTERN}"

        return Path(path).rglob(pattern)

    def run(self, path: str) -> dict:
        matches = self._scan_path_for_pattern_matches(path)

        return list(matches)
