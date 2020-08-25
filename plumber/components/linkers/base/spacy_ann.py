from .base import BaseLinker
from .web import BaseWebLinker
from plumber.components.format import Pair
from typing import List


class BaseSpacyANNLinker(BaseLinker, BaseWebLinker):

    allowed_relation_types = []

    def __init__(self, url: str, allowed_relation_types=None, **kwargs):
        if allowed_relation_types is None:
            self.allowed_relation_types = []
        kwargs['api_url'] = url
        BaseLinker.__init__(self, name="Base Spacy ANN Linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        result = self.client.link.POST(json={"text": text}).json()
        links = []
        for entry in result:
            link_type = None
            if entry['type'] in self.allowed_relation_types:
                link_type = 'relation'
            else:
                link_type = 'entity'
            links.append(Pair(entry['uri'], entry['text'], link_type))
        return links
