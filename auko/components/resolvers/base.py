from auko.components import StanfordClient


class BaseResolver:

    def __init__(self, name: str = 'Base Resolver'):
        self.name = name

    def get_coreference_chains(self, text: str):
        pass


class StanfordBasedResolver(BaseResolver):

    def __init__(self, client: StanfordClient, name: str = 'Stanford-based Resolver'):
        super().__init__(name)
        self.client = client

    def get_coreference_chains(self, text: str):
        pass

