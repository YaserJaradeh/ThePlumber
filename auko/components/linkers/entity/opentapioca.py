from auko.components.linkers.base import BaseEntityLinker, BaseWebLinker
from typing import List, Tuple


class OpenTapiocaEntityLinker(BaseEntityLinker, BaseWebLinker):

    def __init__(self):
        BaseEntityLinker.__init__(self, name="Open Tapioca entity linker")
        BaseWebLinker.__init__(self, api_url="https://opentapioca.org/api/annotate")

    def get_entities(self, text: str) -> List[Tuple[str, str]]:
        result = self.client.POST(data={'query': text}).json()
        return [(f"http://www.wikidata.org/entity/{entity['best_qid']}", text[entity['start']:entity['end']])
                for entity in result['annotations'] if entity['best_qid'] is not None] \
            if 'annotations' in result else []
