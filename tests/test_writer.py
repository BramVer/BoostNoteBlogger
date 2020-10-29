import os
from pathlib import Path

import pytest

from bnb.config import Config
from bnb.writer import Writer
from bnb.converter import ConvertedContent


class TestWriter:
    def test_it_can_run(self, tmp_path):
        writer = Writer()
        assert hasattr(writer, "run")

    def test_it_properly_builds_new_paths(self, cfg):
        writer = Writer(cfg)
        content = ConvertedContent(
            cfg=cfg,
            path=Path("/one/two/three/notes/file.cson"),
            content="",
            metadata={
                "title": "Hello there",
                "folder": "key_for_folder_two",
            },
        )
        expected = Path("/one/two/three/build/Folder Two/hello_there.html")
        actual = writer._construct_new_path(content)

        assert expected == actual

    def test_it_creates_folders_when_they_dont_exist(self, cfg, tmpdir):
        writer = Writer(cfg)
        path = tmpdir.join("one", "two", "three", "four", "notes", "file.cson")
        content = ConvertedContent(
            cfg=cfg,
            path=path,
            content="haha",
            metadata={
                "title": "Hello there",
                "folder": "key_for_folder_two",
            },
        )

        writer.run(content)
        assert os.path.exists(tmpdir)

    def test_it_can_write_a_file(self, cfg, tmpdir):
        writer = Writer(cfg)

        tmpdir.mkdir(cfg.notes_folder)
        tmpdir.mkdir(cfg.output_folder)
        fpath = tmpdir.join(cfg.notes_folder, "file.cson")
        content = ConvertedContent(
            cfg=cfg,
            path=fpath,
            content="<h1>Hello there</h1>",
            metadata={
                "title": "Hello there",
                "folder": "key_for_folder_two",
            },
        )
        writer.run(content)

        # new_fpath = tmpdir / cfg.output_folder / content.folder / content.filename
        new_fpath = tmpdir / "build" / "Folder Two" / "hello_there.html"
        assert new_fpath.exists()
        with open(new_fpath) as f:
            assert f.read() == content.content
