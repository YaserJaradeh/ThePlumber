from typing import List
from auko.components import StanfordClient
from auko.components.format import Chain
from auko.discovery import AuKoClass


class BaseResolver(AuKoClass):

    def __init__(self, name: str = 'Base Resolver'):
        self.name = name

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass


class DummyResolver(AuKoClass):
    """
    Dummy resolver used for testing purposes or to fill space in the pipeline
    """

    def __init__(self, name: str = 'Dummy Resolver'):
        self.name = name

    def get_coreference_chains(self, text: str) -> List[Chain]:
        return []


class StanfordBasedResolver(BaseResolver):

    def __init__(self, client: StanfordClient, name: str = 'Stanford-based Resolver'):
        super().__init__(name)
        self.client = client

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass

