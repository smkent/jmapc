import os


class Config(object):
    def __init__(self) -> None:
        self.hostname = os.environ.get("JMAP_HOSTNAME")
        self.username = os.environ.get("JMAP_USERNAME")
        self.password = os.environ.get("JMAP_PASSWORD")
        assert self.hostname
        assert self.username
        assert self.password
