from bnb.config import Config


class Converter:
    """Converts cson files to html files"""
    def __init__(self, config=None):
        self.cfg = config or Config()

    def run(self, path=None):
        pass
