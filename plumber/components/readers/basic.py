from os.path import exists
from .base import BaseReader
from typing import AnyStr


class StandardReader(BaseReader):

    def __init__(self, **kwargs):
        super().__init__(name='Reader from standard input (console)', **kwargs)

    def read(self) -> AnyStr:
        return input('Please enter the input text')


class RawFileReader(BaseReader):

    def __init__(self, **kwargs):
        super().__init__(name='Reader from a file', **kwargs)

    def read(self) -> AnyStr:
        if 'input_file' not in self.kwargs:
            raise ValueError('input_file must be set for file reader')
        file_path = self.kwargs['input_file']
        if not exists(file_path):
            raise ValueError(f"File path provided is non existence ({file_path})")
        with open(file_path, 'r') as input_file:
            return '\n'.join(input_file.readlines())
