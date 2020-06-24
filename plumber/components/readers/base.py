from typing import AnyStr
from plumber.discovery import PlumberClass


class BaseReader(PlumberClass):

    def __init__(self, name='Base reader', **kwargs):
        self.name = name
        self.kwargs = kwargs

    def read(self) -> AnyStr:
        pass
