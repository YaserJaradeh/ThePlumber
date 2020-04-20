from auko.components.ollie import OLLIEClient
from auko.components.extractors.base import OllieBasedExtractor


class OllieExtractor(OllieBasedExtractor):

    def __init__(self, ollie_client: OLLIEClient, confidence=0.6):
        super().__init__(name='OLLIE extractor', client=ollie_client)
        self.confidence = confidence

    def get_triples(self, text):
        result = self.client.get_extraction(text)
        triples = []
        for triple in result:
            if triple['confidence'] >= self.confidence:
                triples.append({
                    'subject': triple['arg1'],
                    'relation': triple['rel'],
                    'object': triple['arg2']
                })
        return triples
