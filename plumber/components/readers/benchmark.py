from .base import BaseReader
from typing import AnyStr


class FeedReader(BaseReader):

    def __init__(self, **kwargs):
        super().__init__(name='Reader from a string', **kwargs)

    def read(self) -> AnyStr:
        if 'content' not in self.kwargs:
            raise ValueError('content must be set for feed readers')
        return self.kwargs['content']
