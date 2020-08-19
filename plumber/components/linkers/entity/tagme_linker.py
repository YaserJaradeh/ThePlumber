from plumber.components.linkers.base import BaseLinker
from plumber.components.format import Pair
from typing import List
import tagme


class TagMeEntityLinker(BaseLinker):

    def __init__(self, **kwargs):
        # Set the authorization token for subsequent calls.
        tagme.GCUBE_TOKEN = "41a30b59-c285-4303-8522-61c9760b4cae-843339462"
        BaseLinker.__init__(self, name="TagMe entity linker", **kwargs)

    def get_links(self, text: str) -> List[Pair]:
        annotations = tagme.annotate(text)

        return [Pair(f'http://dbpedia.org/resource/{ann.entity_title.replace(" ", "_")}', ann.mention, 'entity')
                for ann in annotations.get_annotations(0.1)]


if __name__ == '__main__':
    linker = TagMeEntityLinker()
    x = linker.get_links("My favourite meal is Mexican burritos.")
