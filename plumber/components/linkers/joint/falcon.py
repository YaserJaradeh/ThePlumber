from json import JSONDecodeError

from plumber.components.linkers.base import BaseLinker, BaseWebLinker
from plumber.components.format import Pair
from typing import List


# Implementing API detailed in https://labs.tib.eu/falcon/falcon2/api-use
# TODO: Use Top-K because it is supported
class FalconJointLinker(BaseLinker, BaseWebLinker):

    def __init__(self, **kwargs):
        kwargs['api_url'] = 'https://labs.tib.eu/falcon/falcon2/api'
        BaseLinker.__init__(self, name="Falcon Relation and Entity Linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str, kg='wikidata', mode='long') -> List[Pair]:
        db = kg.lower().strip() if kg.lower().strip() in ['wikidata', 'dbpedia'] else 'wikidata'
        mode = mode.lower().strip() if mode.lower().strip() in ['long', 'short'] else 'long'
        params = {"mode": mode}
        if db == 'dbpedia':
            params['db'] = 1
        try:
            result = self.client.POST(json={"text": text}, params=params).json()
            ent_key = f'entities_{kg}'
            rel_key = f'relations_{kg}'
            entities = [Pair(entity[0], entity[1], 'entity') for entity in result[ent_key]] if ent_key in result else []
            relations = [Pair(relation[0], relation[1], 'relation') for relation in result[rel_key]] if rel_key in result else []
            return entities + relations
        except JSONDecodeError as ex:
            print(ex)
            return []


class FalconDBpediaJointLinker(FalconJointLinker):

    def get_links(self, text: str) -> List[Pair]:
        return super().get_links(text, kg='dbpedia')


class FalconWikidataJointLinker(FalconJointLinker):

    def get_links(self, text: str) -> List[Pair]:
        return super().get_links(text)


if __name__ == '__main__':
    linker = FalconDBpediaJointLinker()
    x = linker.get_links("Who is the wife of Barack Obama?")
