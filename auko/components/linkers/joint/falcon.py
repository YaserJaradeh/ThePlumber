from auko.components.linkers.base import BaseJointLinker, BaseWebLinker
from typing import List, Tuple


# Implementing API detailed in https://labs.tib.eu/falcon/falcon2/api-use
# TODO: Use Top-K because it is supported
class FalconJointLinker(BaseJointLinker, BaseWebLinker):

    def __init__(self):
        # TODO: replace with super call
        BaseJointLinker.__init__(self, name="Falcon Relation and Entity Linker")
        BaseWebLinker.__init__(self, api_url="https://labs.tib.eu/falcon/falcon2/api")

    def get_entities_and_relations(self, text: str, kg='wikidata', mode='long') -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        db = kg.lower().strip() if kg.lower().strip() in ['wikidata', 'dbpedia'] else 'wikidata'
        mode = mode.lower().strip() if mode.lower().strip() in ['long', 'short'] else 'long'
        params = {"mode": mode}
        if db == 'dbpedia':
            params['db'] = 1
        result = self.client.POST(json={"text": text}, params=params).json()
        ent_key = f'entities_{kg}'
        rel_key = f'relations_{kg}'
        entities = [(entity[0], entity[1]) for entity in result[ent_key]] if ent_key in result else []
        relations = [(relation[0], relation[1]) for relation in result[rel_key]] if rel_key in result else []
        return entities, relations


class FalconDBpediaJoinLinker(FalconJointLinker):

    def get_entities_and_relations(self, text: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        return super().get_entities_and_relations(text, kg='dbpedia')


class FalconWikidataJoinLinker(FalconJointLinker):

    def get_entities_and_relations(self, text: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        return super().get_entities_and_relations(text)
