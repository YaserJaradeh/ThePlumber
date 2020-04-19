from auko.components.stanford import StanfordClient
from auko.components.extractors.base import StanfordBasedExtractor


class OpenIEExtractor(StanfordBasedExtractor):

    def __init__(self, stanford_client: StanfordClient):
        super().__init__(name='Open IE extractor', client=stanford_client)

    def get_triples(self, text):
        triples = self.client.openie(text)
        # == Unify Output
        # location in string
        # sentence ID or number
        return triples
