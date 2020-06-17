from .base import BaseWriter
from typing import List
from auko.components.format import SPOTriple


class StandardWriter(BaseWriter):

    def __init__(self, **kwargs):
        super().__init__(name='Writer to standard input (console)', **kwargs)

    def write(self, triples: List[SPOTriple], **kwargs):
        print(triples)


class FileWriter(BaseWriter):

    def __init__(self, **kwargs):
        super().__init__(name='Writer to a a file', **kwargs)

    def write(self, triples: List[SPOTriple], **kwargs):
        if 'file_path' not in kwargs:
            raise ValueError('file_path must be set for file writers')
        file_path = kwargs['file_path']
        with open(file_path, 'w') as out_file:
            out_file.write('\n'.join([triple.__str__() for triple in triples]))
