from typing import List
from auko.components.format import SPOTriple
from auko.discovery import AuKoClass


class BaseWriter(AuKoClass):

    def __init__(self, name='Base writer', **kwargs):
        self.name = name
        self.kwargs = kwargs

    def write(self, triples: List[SPOTriple]):
        pass
