from typing import AnyStr
from auko.discovery import AuKoClass


class BaseReader(AuKoClass):

    def __init__(self, name='Base reader', **kwargs):
        self.name = name
        self.kwargs = kwargs

    def read(self) -> AnyStr:
        pass
