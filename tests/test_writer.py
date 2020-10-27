import pytest

from bnb.scanner import Scanner
from bnb.writer import Writer


class TestWriter:
    def test_it_can_run(self, tmp_path):
        writer = Writer()
        assert hasattr(writer, "run")

    def test_it_processes_files(self, cfg, base_dir):
        scanner = Scanner(cfg)
        writer = Writer(cfg)

        files = scanner.run(base_dir)
        writer.run(files)
