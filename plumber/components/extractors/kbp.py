from typing import List
from plumber.components.extractors.base import StanfordBasedExtractor
from plumber.components.format import Triple


class KBPExtractor(StanfordBasedExtractor):

    def __init__(self, **kwargs):
        kwargs['key'] = 'kbp'
        super().__init__(name='KBP extractor', **kwargs)

    def get_triples(self, text) -> List[Triple]:
        response = self.client.kbp(text, simple_format=False)
        return self.transform_triples(response['sentences'], text)
