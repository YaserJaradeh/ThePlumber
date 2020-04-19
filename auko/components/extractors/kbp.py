from auko.components.stanford import StanfordClient
from auko.components.extractors.base import StanfordBasedExtractor


class KBPExtractor(StanfordBasedExtractor):

    def __init__(self, stanford_client: StanfordClient):
        super().__init__(name='KBP extractor', client=stanford_client)

    def get_triples(self, text):
        triples = self.client.kbp(text)
        return triples
