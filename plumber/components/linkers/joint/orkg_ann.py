from plumber.components.linkers.base import BaseLinker, BaseWebLinker
from plumber.components.format import Pair
from typing import List
import os


ENDPOINT_URL = f'{"http://localhost:11111" if "ORKG_ANN_ENDPOINT" not in os.environ else os.environ["ORKG_ANN_ENDPOINT"]}/'


class ORKGSpacyANNLinker(BaseLinker, BaseWebLinker):

    def __init__(self, **kwargs):
        kwargs['api_url'] = ENDPOINT_URL
        BaseLinker.__init__(self, name="ORKG Spacy ANN Linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        result = self.client.link.POST(json={"text": text}).json()
        links = []
        for entry in result:
            if entry['type'] in ['ORKG-REL']:
                link_type = 'relation'
            elif entry['type'] in ['ORKG-ENT']:
                link_type = 'entity'
            else:
                continue
            links.append(Pair(entry['uri'], entry['text'], link_type))
        return links


if __name__ == '__main__':
    linker = ORKGSpacyANNLinker()
    x = linker.get_links(text="This contribution is addressing basic reproduction numbers of the COVID 19 virus")
