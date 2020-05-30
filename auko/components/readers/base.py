
class BaseReader:

    def __init__(self, name='Base reader'):
        self.name = name

    def read(self, **kwargs) -> str:
        pass
