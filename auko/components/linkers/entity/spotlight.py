from auko.components.linkers.base import BaseLinker, BaseWebLinker
from typing import List, Tuple


# Implementing API detailed in https://www.dbpedia-spotlight.org/api
class DBpediaSpotlightEntityLinker(BaseLinker, BaseWebLinker):

    def __init__(self, **kwargs):
        kwargs['api_url'] = "https://api.dbpedia-spotlight.org/en/annotate"
        BaseLinker.__init__(self, name="DBpedia Spotlight linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Tuple[str, str, str]]:
        result = self.client.GET(params={'text': text}, verify=False, headers={"accept": "application/json"}).json()
        return [(entity['@URI'], entity['@surfaceForm'], 'entity') for entity in result['Resources']]
