from auko.components.linkers.joint.falcon import FalconJointLinker
from auko.components.linkers.base import BaseEntityLinker
from typing import List, Tuple


class FalconDBpediaEntityLinker(BaseEntityLinker, FalconJointLinker):

    def __init__(self):
        super().__init__(name="Falcon Entity linker mode on DBpedia")
        FalconJointLinker.__init__(self)

    def get_entities(self, text: str) -> List[Tuple[str, str]]:
        return super().get_entities_and_relations(text, kg='dbpedia', mode="short")[0]


class FalconWikidataEntityLinker(BaseEntityLinker, FalconJointLinker):

    def __init__(self):
        super().__init__(name="Falcon Entity linker mode on Wikidata")

    def get_entities(self, text: str) -> List[Tuple[str, str]]:
        return super().get_entities_and_relations(text, mode="short")[0]
        # Why short mode returns <uri, number> while long mode returns <uri, string(label)>
