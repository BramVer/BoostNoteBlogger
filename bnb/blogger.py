from pathlib import Path
from datetime import datetime
from collections import defaultdict

import markdown
import questionary

from bnb.config import Config
from bnb.writer import Writer
from bnb.scanner import Scanner
from bnb.wrapper import Wrapper
from bnb.extractor import Extractor
from bnb.converter import Converter
from bnb.exceptions import ConfigurationError


def cli():
    cfg = Config()

    msg = "Hi there! What folder should we set as the home of your blog?"
    home = questionary.text(msg, default=cfg.home_folder).ask()

    blogger = Blogger(home)
    blogger.run()


class Blogger:
    def __init__(self, home, config=None):
        self.home = Path(home)
        self.cfg = config or Config(home)

    def _assert_settings_file(self):
        settings = Path(self.home / self.cfg.bnote_settings_file)
        if not settings.exists():
            msg = f"{self.cfg.bnote_settings_file} could not be found at {self.home}."
            raise ConfigurationError(msg)

    def _assert_notes_folder(self):
        notes = Path(self.home / self.cfg.notes_folder)
        if not notes.exists():
            msg = f"No notes folder found at {self.home}."
            raise ConfigurationError(msg)

    def assert_setup(self):
        try:
            self._assert_notes_folder()
            self._assert_settings_file()
        except ConfigurationError as e:
            msg = (
                f"Something went wrong trying to set the blog-home:\n"
                f"{e}\n"
                f"Exiting."
            )
            print(msg)
            exit()

    def scan_files(self, scanner=None):
        scanner = scanner or Scanner(self.cfg)

        return scanner.run(self.home)

    def process_files(self, files, extractor=None, converter=None):
        processed = []

        extractor = extractor or Extractor(self.cfg)
        converter = converter or Converter(self.cfg)

        for file in files:
            extracted = extractor.run(file)
            processed.append(converter.run(extracted))

        return processed

    def confirm_for_conversion(self, files):
        msg = f"We found {len(files)} files, deselect to omit."
        choices = [questionary.Choice(f, checked=True) for f in files]

        return questionary.checkbox(msg, choices=choices).ask()

    def _get_chronological_file_map(self, files):
        result = defaultdict(list)
        files.sort(key=lambda f: f.metadata["createdAt"][:7], reverse=True)

        for file in files:
            created = datetime.strptime(file.metadata["createdAt"][:7], "%Y-%m")
            result[created.strftime("%B %Y")].append(file.md_link)

        return result

    def get_files_overview(self, files):
        sidebar_md = []
        mapping = self._get_chronological_file_map(files)

        for key, values in mapping.items():
            links = "\n    * ".join(values)
            sidebar_md.append(f"## {key}{links}")

        return markdown.Markdown(output_format="html").convert("\n".join(sidebar_md))

    def wrap_in_html(self, content, overview, wrapper=None):
        wrapper = wrapper or Wrapper(self.cfg)
        for file in content:
            wrapped = wrapper.run(file, overview)
            file.content = wrapped

        return content

    def write_output(self, content, writer=None):
        writer = writer or Writer(self.cfg)
        for file in content:
            writer.run(file)

    def run(self):
        self.assert_setup()

        scanned = self.scan_files()
        processed = self.process_files(scanned)
        confirmed = self.confirm_for_conversion(processed)
        overview = self.get_files_overview(confirmed)
        wrapped_content = self.wrap_in_html(confirmed, overview)

        self.write_output(wrapped_content)
