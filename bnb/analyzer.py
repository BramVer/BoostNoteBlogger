import os
import json
from pathlib import Path
from collections import defaultdict

from bnb.config import Config
from bnb.extractor import Extractor


class Analyzer:
    """
    Analyzes content and extracts information.
    {
        "folder_one": {
            "file_one": {
                "full_path": "...",
                "tags": [],
                "links": [
                    "folder_one/file_two",
                ],
                "metadata": "metadata",
            },
            "file_two": {
                "full_path": "...",
                "tags": [],
                "links": [],
                "metadata": "metadata",
            }
        }
    }
    """
    def __init__(self, config=None):
        self.cfg = config or Config()
        self.extractor = Extractor()

    def _scan_path_for_matches(self, path, pattern):
        return Path(path).rglob(f"*{pattern}")

    def _get_folder_mapping(self, path):
        mapping = {}
        path = os.path.join(path, self.config.get("BNOTE_SETTINGS_FILE"))
        if not os.path.exists(path):
            return mapping

        with open(path, "r") as dt:
            data = json.load(dt)

            for f in data.get("folders", []):
                mapping[f["key"]] = f["name"]

        return mapping

    def run(self, path: str) -> dict:
        result = defaultdict(list)

        folders = self._get_folder_mapping(path)
        matches = self._scan_path_for_matches(path, self.cfg["CSON_PATTERN"])

        for match in matches:
            extracted = self.extractor.run(match)
            folder = folders[extracted.folder]

            result[folder].append(extracted)

        return result
