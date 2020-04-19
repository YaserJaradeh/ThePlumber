from auko.components import StanfordClient


class BaseExtractor:

    def __init__(self, name: str = 'Base Extractor'):
        self.name = name

    def get_triples(self, text: str):
        pass


class StanfordBasedExtractor(BaseExtractor):

    def __init__(self, client: StanfordClient, name: str = 'Stanford-based Extractor'):
        super().__init__(name)
        self.client = client

    def get_triples(self, text: str):
        pass
