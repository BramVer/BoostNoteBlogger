import os
import logging
from pathlib import Path

from bnb.config import Config


logger = logging.getLogger(__name__)


class Scanner:
    def __init__(self, config=None):
        self.cfg = config or Config()

    def _scan_path(self, path):
        pattern = f"*{self.cfg.cson_extension}"
        return Path(path).rglob(pattern)

    def run(self, path):
        logger.info(f"Scanning for files at {path}")

        return list(self._scan_path(path))
