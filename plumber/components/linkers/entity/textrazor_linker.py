from plumber.components.linkers.base import BaseLinker
from plumber.components.format import Pair
from typing import List
from textrazor import TextRazor
from random import randint


class TextRazorEntityLinker(BaseLinker):
    keys = ["04fd9a5a817266cc2912266cd152da35a25d08c95f9b5edefb94ed97",
            "9d0ac08f05f6f546d230e05f634efe26fc035479d130231dad4fd5cb",
            "785231deddf38c8f5b8e73adfa9d3b3b6b3f6859e391c63b84786afc",
            "b8871f52ee4c442a6435ed7b142600c00fed4cccfcf2bc6747bb8cb0",
            "233a4d7450ba94588f67301490603aaa4c1d973f5cfdb2c445165a61",
            "875417a3adfb35e2b0c9d76e16bb92e1974547605e72d66c20f4b4ce",
            "2d3680ab6b46fa81ff6293ee6e924fcbdbe9658d61c107e17b4669b3",
            "6559f7ac589ff5f014e4c4058ba0531987a9a83e067427a2768a2fc9",
            "f0c1f18fbb833cc10a6dfe7295616e8d6120f1fd4180173e93d0c7a7",
            "fe1930d48b3b520da0b820cfa6ad01d26c8dd9d6c62a06f7dede09a0",
            "8ca44890eb757ac572861b40845e88e5fdb65d2894acc9cac9ac3d20",
            "803dc1c05746b1296d397a465f71f95e9cb89fcf98fc1e875bec7eb6",
            "8f8dbf8b93a96d12c178fd06c08be95af67c6c2e58e2e3650447d0c6",
            "fee2861b8a669c3804ff0d00e39e9cbc1f8e96942ab6f9a082674535"]

    def __init__(self, **kwargs):
        BaseLinker.__init__(self, name="TextRazor entity linker", **kwargs)

    def get_links(self, text: str, kg='wikidata') -> List[Pair]:
        graph = kg.lower().strip() if kg.lower().strip() in ['wikidata', 'dbpedia'] else 'wikidata'
        client = TextRazor(self.get_api_key(), extractors=['entities'])
        links = []
        response = client.analyze(text)
        for entity in response.entities():
            link = None
            if graph == 'wikidata':
                link = f'http://www.wikidata.org/entity/{entity.wikidata_id}'
            else:
                link = f'http://dbpedia.org/resource/{entity.wikipedia_link[entity.wikipedia_link.rfind("/")+1:]}'
            span = entity.matched_text
            links.append(Pair(link, span, 'entity'))
        return links

    def get_api_key(self) -> str:
        index = randint(0, len(self.keys)-1)
        return self.keys[index]


class TextRazorDBpediaLinker(TextRazorEntityLinker):

    def get_links(self, text: str) -> List[Pair]:
        return super().get_links(text, kg='dbpedia')


class TextRazorWikidataLinker(TextRazorEntityLinker):

    def get_links(self, text: str) -> List[Pair]:
        return super().get_links(text)


if __name__ == '__main__':
    linker = TextRazorWikidataLinker()
    x = linker.get_links("My favourite meal is Mexican burritos.")
