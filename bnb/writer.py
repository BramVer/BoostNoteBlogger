from bnb.config import Config


class Writer:
    def __init__(self, config=None):
        self.config = config or Config()
