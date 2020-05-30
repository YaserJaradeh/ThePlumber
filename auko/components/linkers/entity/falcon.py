from auko.components.linkers.joint.falcon import FalconJointLinker
from auko.components.linkers.base import BaseEntityLinker


class FalconEntityLinkerDBpedia(BaseEntityLinker, FalconJointLinker):

    def __init__(self):
        super().__init__(name="Falcon Entity linker mode on DBpedia")
        FalconJointLinker.__init__(self)

    def get_entities(self, text: str):
        return super().get_entities_and_relations(text, kg='dbpedia', mode="short")


class FalconEntityLinkerWikidata(BaseEntityLinker, FalconJointLinker):

    def __init__(self):
        super().__init__(name="Falcon Entity linker mode on Wikidata")

    def get_entities(self, text: str):
        return super().get_entities_and_relations(text, mode="short")
