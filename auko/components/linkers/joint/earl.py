from auko.components.linkers.base import BaseJointLinker, BaseWebLinker
from typing import List, Tuple


# Implementing API detailed in https://earldemo.sda.tech/pages/api.html?
# TODO: Use Top-K because it is supported
class EARLJointLinker(BaseJointLinker, BaseWebLinker):

    def __init__(self):
        BaseJointLinker.__init__(self, name="EARL Relation and Entity Linker")
        BaseWebLinker.__init__(self, api_url="https://earldemo.sda.tech/earl/api/processQuery")

    def get_entities_and_relations(self, text: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        result = self.client.POST(json={"nlquery": text, "pagerankflag": False}).json()
        entities = []
        relations = []
        for idx, chunk in enumerate(result['chunktext']):
            target = entities if chunk['class'] == 'entity' else relations
            target.append((result['rerankedlists'][str(idx)][0][1],
                           text[chunk['surfacestart']:chunk['surfacestart']+chunk['surfacelength']]))
        return entities, relations
