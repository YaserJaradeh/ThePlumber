from .base import BaseWriter
from typing import List, AnyStr
from auko.components.format import SPOTriple


class StandardWriter(BaseWriter):

    def __init__(self):
        super().__init__(name='Writer to standard input (console)')

    def write(self, triples: List[SPOTriple]):
        print(triples)


class FileWriter(BaseWriter):

    def __init__(self):
        super().__init__(name='Writer to a a file')

    def write(self, triples: List[SPOTriple], file_path: AnyStr):
        with open(file_path, 'w') as out_file:
            out_file.write('\n'.join([triple.__str__() for triple in triples]))
