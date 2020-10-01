from typing import List
from components.format import SPOTriple
from discovery import PlumberClass


class BaseWriter(PlumberClass):

    def __init__(self, name='Base writer', **kwargs):
        self.name = name
        self.kwargs = kwargs

    def write(self, triples: List[SPOTriple]):
        pass
