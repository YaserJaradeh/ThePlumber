from typing import AnyStr


class BaseReader:

    def __init__(self, name='Base reader'):
        self.name = name

    def read(self, **kwargs) -> AnyStr:
        pass
