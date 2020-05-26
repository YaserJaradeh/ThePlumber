from typing import List
from auko.components.clients.stanford import StanfordClient
from auko.components.extractors.base import StanfordBasedExtractor
from auko.components.format import Triple


class OpenIEExtractor(StanfordBasedExtractor):

    def __init__(self, stanford_client: StanfordClient):
        super().__init__(name='Open IE extractor', key='openie', client=stanford_client)

    def get_triples(self, text) -> List[Triple]:
        response = self.client.openie(text, simple_format=False)
        return self.transform_triples(response['sentences'], text)
