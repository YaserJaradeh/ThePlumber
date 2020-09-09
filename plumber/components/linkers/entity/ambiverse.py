from plumber.components.linkers.base import BaseLinker
from plumber.components.format import Pair
from typing import List
import requests
from urllib.parse import urlencode


class AmbiverseEntityLinker(BaseLinker):

    def __init__(self, **kwargs):
        BaseLinker.__init__(self, name="Ambiverse entity linker", **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        url = "https://ambiversenlu.mpi-inf.mpg.de/wp-admin/admin-ajax.php"

        payload = f"action=tag_analyze_document&{urlencode({'text': text})}&coherentDocument=true&extractConcepts=true&confidenceThreshold=0.435&language=auto&nluUrl=http%3A%2F%2Fambprod.mpi-inf.mpg.de%3A8071%2F&kgUrl=&apiMethod=%2Fentitylinking%2F&_ajax_nonce=a884569f40"
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://ambiversenlu.mpi-inf.mpg.de',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8,de;q=0.7'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        try:
            return [Pair(ent['entity']['id'], ent['text'], 'entity') for ent in response.json()["matches"] if 'id' in ent['entity']]
        except Exception as e:
            return []


if __name__ == '__main__':
    linker = AmbiverseEntityLinker()
    x = linker.get_links("Jack founded Alibaba in Hangzhou with investments from SoftBank and Goldman.")
