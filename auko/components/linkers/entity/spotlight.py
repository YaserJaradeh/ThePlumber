from auko.components.linkers.base import BaseEntityLinker, BaseWebLinker
from typing import List, Tuple


# Implementing API detailed in https://www.dbpedia-spotlight.org/api
class DBpediaSpotlightEntityLinker(BaseEntityLinker, BaseWebLinker):

    def __init__(self):
        BaseEntityLinker.__init__(self, name="DBpedia Spotlight linker")
        BaseWebLinker.__init__(self, api_url="https://api.dbpedia-spotlight.org/en/annotate")

    def get_entities(self, text: str) -> List[Tuple[str, str]]:
        result = self.client.GET(params={'text': text}, verify=False, headers={"accept": "application/json"}).json()
        return [(entity['@URI'], entity['@surfaceForm']) for entity in result['Resources']]
