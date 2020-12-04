from plumber.components.linkers.base import BaseLinker
from plumber.components.format import Pair
from typing import List
import requests
from urllib.parse import urlencode

AMBIVERSE_URL = 'http://node4.research.tib.eu:12321/factextraction/analyze/'


class AmbiverseEntityLinker(BaseLinker):

    def __init__(self, **kwargs):
        BaseLinker.__init__(self, name="Ambiverse entity linker", **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        payload = self.prepare_json_request({"docId": "doc1", "text": text, "extractConcepts": True, "language": "en"})
        # payload = "{\"docId\": \"doc1\", \"text\": \""+text+"\", \"extractConcepts\": \"true\", \"language\": \"en\" }"
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        response = requests.request("POST", AMBIVERSE_URL, headers=headers, data=payload.encode('utf-8'))
        try:
            return [Pair(ent['entity']['id'], ent['text'], 'entity') for ent in response.json()["matches"] if 'id' in ent['entity']]
        except Exception as e:
            return []


if __name__ == '__main__':
    linker = AmbiverseEntityLinker()
    x = linker.get_links("Jack founded Alibaba in Hangzhou with investments from SoftBank and Goldman.")
