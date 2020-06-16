from typing import List
from auko.components import StanfordClient
from auko.components.format import Chain
from auko.discovery import AuKoClass


class BaseResolver(AuKoClass):

    def __init__(self, name: str = 'Base Resolver', **kwargs):
        self.name = name

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass


class DummyResolver(AuKoClass):
    """
    Dummy resolver used for testing purposes or to fill space in the pipeline
    """

    def __init__(self, name: str = 'Dummy Resolver', **kwargs):
        self.name = name

    def get_coreference_chains(self, text: str) -> List[Chain]:
        return []


class StanfordBasedResolver(BaseResolver):

    def __init__(self, name: str = 'Stanford-based Resolver', **kwargs):
        super().__init__(name)
        if 'stanford_client' not in kwargs:
            raise ValueError('stanford_client parameter should be passed to any Stanford based resolvers')
        self.client = kwargs['stanford_client']

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass

