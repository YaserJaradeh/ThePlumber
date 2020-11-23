from plumber.components.linkers.base import BaseLinker, BaseWebLinker
from plumber.components.format import Pair
from typing import List


# Implementing API detailed in https://www.dbpedia-spotlight.org/api
class DBpediaSpotlightEntityLinker(BaseLinker, BaseWebLinker):

    def __init__(self, **kwargs):
        # kwargs['api_url'] = "http://localhost:33311/rest/annotate"
        kwargs['api_url'] = "https://api.dbpedia-spotlight.org/en/annotate"
        BaseLinker.__init__(self, name="DBpedia Spotlight linker", **kwargs)
        BaseWebLinker.__init__(self, **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        result = self.client.GET(params={'text': text}, verify=False, headers={"accept": "application/json"}).json()
        if 'Resources' in result:
            return [Pair(entity['@URI'], entity['@surfaceForm'], 'entity') for entity in result['Resources']]
        else:
            return []


if __name__ == '__main__':
    linker = DBpediaSpotlightEntityLinker()
    x = linker.get_links("Barack Obama was the president of the USA.")
