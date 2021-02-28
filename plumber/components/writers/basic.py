from .base import BaseWriter
from typing import List
from plumber.components.format import SPOTriple


class StandardWriter(BaseWriter):

    def __init__(self, **kwargs):
        super().__init__(name='Writer to standard input (console)', **kwargs)

    def write(self, triples: List[SPOTriple]):
        print(triples)


class FileWriter(BaseWriter):

    def __init__(self, **kwargs):
        super().__init__(name='Writer to a a file', **kwargs)

    def write(self, triples: List[SPOTriple]):
        if 'output_file' not in self.kwargs:
            raise ValueError('output_file must be set for file writers')
        file_path = self.kwargs['output_file']
        with open(file_path, 'w') as out_file:
            out_file.write('\n'.join([triple.__str__() for triple in triples]))


class ReturnWriter(BaseWriter):

    def __init__(self, **kwargs):
        super().__init__(name='Return output as string', **kwargs)

    def write(self, triples: List[SPOTriple]):
        return [triple.to_json() for triple in triples]
