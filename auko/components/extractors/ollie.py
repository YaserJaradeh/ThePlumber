from auko.components.ollie import OLLIEClient
from auko.components.extractors.base import OllieBasedExtractor


class OllieExtractor(OllieBasedExtractor):

    def __init__(self, ollie_client: OLLIEClient):
        super().__init__(name='OLLIE extractor', client=ollie_client)

    def get_triples(self, text):
        triples = self.client.get_extraction(text)
        result = []
        for triple in triples:
            result.append({
                'subject': triple['arg1'],
                'relation': triple['rel'],
                'object': triple['arg2']
            })
        return triples
