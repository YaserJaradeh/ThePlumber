from auko.components.linkers.base import BaseLinker, BaseWebLinker
from typing import List, Tuple


# Implementing API used in https://opentapioca.org/#
class OpenTapiocaEntityLinker(BaseLinker, BaseWebLinker):

    def __init__(self, **kwargs):
        kwargs['api_url'] = 'https://opentapioca.org/api/annotate'
        BaseLinker.__init__(self, name="Open Tapioca entity linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Tuple[str, str, str]]:
        result = self.client.POST(data={'query': text}).json()
        return [(f"http://www.wikidata.org/entity/{entity['best_qid']}", text[entity['start']:entity['end']], 'entity')
                for entity in result['annotations'] if entity['best_qid'] is not None] \
            if 'annotations' in result else []
