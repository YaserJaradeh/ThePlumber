from typing import List
from auko.components import StanfordClient
from auko.components.format import Chain


class BaseResolver:

    def __init__(self, name: str = 'Base Resolver'):
        self.name = name

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass


class StanfordBasedResolver(BaseResolver):

    def __init__(self, client: StanfordClient, name: str = 'Stanford-based Resolver'):
        super().__init__(name)
        self.client = client

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass

