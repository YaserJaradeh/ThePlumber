from consecution import Node
from auko.components import BaseExtractor


class ExtractorNode(Node):
    """
    An extractor node, part of a pipeline
    """

    def __init__(self, name: str, extractor: BaseExtractor, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = extractor

    def process(self, item: str):
        # item here is the text (str)
        # process text into triples using extractor
        # if not isinstance(str, item):
        #     raise ValueError("The input for the extractor nodes should be string")
        result = self.extractor.get_triples(item)
        # pass results to next component
        self.push(result)
        pass
