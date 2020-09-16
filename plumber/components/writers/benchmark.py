from .base import BaseWriter
from typing import List
from plumber.components.format import SPOTriple


class AppendTSVWriter(BaseWriter):

    def __init__(self, **kwargs):
        super().__init__(name='Append triple to TSV writer', **kwargs)

    def write(self, triples: List[SPOTriple]):
        if 'output_tsv' not in self.kwargs:
            raise ValueError('output_tsv must be set for AppendTSV writers')
        file_path = self.kwargs['output_tsv']
        with open(file_path, 'a+') as out_file:
            line = '\t'.join([triple.short_form() for triple in triples])
            out_file.write(f'{line}\n')
            out_file.flush()
