from plumber.components.linkers.base import BaseSpacyANNLinker


class DBpediaSpacyANNJointLinker(BaseSpacyANNLinker):

    def __init__(self, **kwargs):
        super().__init__(url='http://node4.research.tib.eu:11222', allowed_relation_types=['DB-PRP', 'DB-ONT'])


class WikidataSpacyANNJointLinker(BaseSpacyANNLinker):

    def __init__(self, **kwargs):
        super().__init__(url='http://node4.research.tib.eu:11333', allowed_relation_types=['WD-PRP'])


if __name__ == '__main__':
    linker = DBpediaSpacyANNJointLinker()
    x = linker.get_links(text="Who is the wife of Barack Obama?")
