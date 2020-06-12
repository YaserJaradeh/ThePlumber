from typing import AnyStr
from auko.discovery import AuKoClass


class BaseReader(AuKoClass):

    def __init__(self, name='Base reader'):
        self.name = name

    def read(self, **kwargs) -> AnyStr:
        pass
