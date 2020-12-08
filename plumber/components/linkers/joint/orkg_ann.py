from plumber.components.linkers.base import BaseLinker, BaseWebLinker
from plumber.components.format import Pair
from typing import List
import os
import re


ENDPOINT_URL = f'{"http://localhost:11111" if "ORKG_ANN_ENDPOINT" not in os.environ else os.environ["ORKG_ANN_ENDPOINT"]}'


class ORKGSpacyANNLinker(BaseLinker, BaseWebLinker):

    def __init__(self, **kwargs):
        kwargs['api_url'] = ENDPOINT_URL
        BaseLinker.__init__(self, name="ORKG Spacy ANN Linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        result = self.client.link.POST(json={"text": text}).json()
        links = []
        for entry in result:
            if entry['uri'] is None or len(entry['uri']) == 0:
                continue
            if re.search(r"R\d+", entry['uri']) is not None:
                link_type = 'entity'
                uri = f"https://www.orkg.org/orkg/resource/{entry['uri']}"
            else:
                link_type = 'relation'
                uri = f"https://www.orkg.org/orkg/predicate/{entry['uri']}"
            links.append(Pair(uri, entry['text'], link_type))
        return links


if __name__ == '__main__':
    linker = ORKGSpacyANNLinker()
    x = linker.get_links(text="This contribution is addressing basic reproduction numbers of the COVID 19 virus")
