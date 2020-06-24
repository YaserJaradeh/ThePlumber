from plumber.components.linkers.joint.falcon import FalconJointLinker
from typing import List, Tuple


class FalconDBpediaEntityLinker(FalconJointLinker):

    def __init__(self, **kwargs):
        super().__init__(name="Falcon Entity linker mode on DBpedia", **kwargs)

    def get_links(self, text: str) -> List[Tuple[str, str, str]]:
        return super().get_links(text, kg='dbpedia', mode="short")


class FalconWikidataEntityLinker(FalconJointLinker):

    def __init__(self, **kwargs):
        super().__init__(name="Falcon Entity linker mode on Wikidata", **kwargs)

    def get_links(self, text: str) -> List[Tuple[str, str, str]]:
        return super().get_links(text, mode="short")
        # Why short mode returns <uri, number> while long mode returns <uri, string(label)>
