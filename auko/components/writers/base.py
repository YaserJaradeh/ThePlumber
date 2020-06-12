from typing import List
from auko.components.format import SPOTriple
from auko.discovery import AuKoClass


class BaseWriter(AuKoClass):

    def __init__(self, name='Base writer'):
        self.name = name

    def write(self, triples: List[SPOTriple], **kwargs):
        pass
