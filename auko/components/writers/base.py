from typing import List
from auko.components import SPOTriple


class BaseWriter:

    def __init__(self, name='Base writer'):
        self.name = name

    def write(self, triples: List[SPOTriple], **kwargs):
        pass
