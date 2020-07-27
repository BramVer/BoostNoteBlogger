from pathlib import Path
from typing import Generator

from bnb.config import Config


class Scanner:
    """Scans the directory and returns a dictionary with its structure.

    {
        "folder": {
            "subfolder_one": {
                "file_one": {
                    "full_path": "...",
                    "tags": [],
                    "links": [
                        "folder/subfolder_one/file_two",
                    ],
                    "metadata": "metadata",
                },
                "file_two": {
                    "tags": [],
                    "links": [],
                    "metadata": "metadata",
                }
            }
        }
    }
    """
    def __init__(self, config=None):
        self.config = config or Config()

    def _scan_path_for_pattern_matches(self, path: str) -> Generator:
        pattern = f"*{self.config.CSON_PATTERN}"

        return Path(path).rglob(pattern)

    # Add caching for path
    def run(self, path):
        result = {}
        matches = self._scan_path_for_pattern_matches(path)

        for match in matches:


            self._handle_cson_content(content)

    def get_subfolders(self):
        pass

    def get_files(self, subfolder):
        pass

    def get_tags_for_file(self, file):
        pass

    def get_links_for_file(self, file):
        pass
