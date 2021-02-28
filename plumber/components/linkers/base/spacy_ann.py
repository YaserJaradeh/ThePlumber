from .base import BaseLinker
from .web import BaseWebLinker
from plumber.components.format import Pair
from typing import List


class BaseSpacyANNLinker(BaseLinker, BaseWebLinker):

    allowed_relation_types = []
    exclusion_types = []

    def __init__(self, url: str, allowed_relation_types, exclusion_types=None, **kwargs):
        self.allowed_relation_types = allowed_relation_types
        if exclusion_types is None:
            self.exclusion_types = []
        else:
            self.exclusion_types = exclusion_types
        kwargs['api_url'] = url
        BaseLinker.__init__(self, name="Base Spacy ANN Linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        result = self.client.link.POST(json={"text": text}).json()
        links = []
        for entry in result:
            if entry['type'] in self.allowed_relation_types:
                link_type = 'relation'
            else:
                link_type = 'entity'
            links.append(Pair(entry['uri'], entry['text'], link_type))
        return links
