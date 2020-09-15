from typing import List
from plumber.components.format import Chain
from plumber.discovery import PlumberClass


class BaseResolver(PlumberClass):

    def __init__(self, name: str = 'Base Resolver', **kwargs):
        self.name = name
        self.kwargs = kwargs

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass


class DummyResolver(BaseResolver):
    """
    Dummy resolver used for testing purposes or to fill space in the pipeline
    """
    def __init__(self, name: str = 'Dummy Resolver', **kwargs):
        super().__init__(name, **kwargs)

    def get_coreference_chains(self, text: str) -> List[Chain]:
        return []


class StanfordBasedResolver(BaseResolver):

    def __init__(self, name: str = 'Stanford-based Resolver', **kwargs):
        super().__init__(name, **kwargs)
        if 'stanford_client' not in kwargs:
            raise ValueError('stanford_client parameter should be passed to any Stanford based resolvers')
        self.client = kwargs['stanford_client']

    def get_coreference_chains(self, text: str) -> List[Chain]:
        pass

