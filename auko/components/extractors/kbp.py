from typing import List
from auko.components.clients.stanford import StanfordClient
from auko.components.extractors.base import StanfordBasedExtractor
from auko.components.format import Triple


class KBPExtractor(StanfordBasedExtractor):

    def __init__(self, stanford_client: StanfordClient):
        super().__init__(name='KBP extractor', key='kbp', client=stanford_client)

    def get_triples(self, text) -> List[Triple]:
        response = self.client.kbp(text, simple_format=False)
        return self.transform_triples(response['sentences'], text)
