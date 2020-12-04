from plumber.components.linkers.base import BaseLinker, BaseWebLinker
from plumber.components.format import Pair

from typing import List


# Implementing API used in https://opentapioca.org/#
class OpenTapiocaEntityLinker(BaseLinker, BaseWebLinker):

    def __init__(self, **kwargs):
        kwargs['api_url'] = 'https://opentapioca.org/api/annotate'
        BaseLinker.__init__(self, name="Open Tapioca entity linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        payload = self.prepare_json_request({'query': text})
        result = self.client.POST(data=payload).json()
        return [
            Pair(f"http://www.wikidata.org/entity/{entity['best_qid']}", text[entity['start']:entity['end']], 'entity')
            for entity in result['annotations'] if entity['best_qid'] is not None] \
            if 'annotations' in result else []
