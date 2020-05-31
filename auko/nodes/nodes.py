from consecution import Node
from auko.components import BaseExtractor, BaseReader, BaseResolver, BaseWriter
from auko.components import BaseRelationLinker, BaseEntityLinker, BaseJointLinker
from auko.components import SPOTriple
from typing import List


class ReadingNode(Node):
    """
    A reader node, should be first node in a pipeline
    """

    def __init__(self, name: str, reader: BaseReader, **kwargs):
        super().__init__(name, **kwargs)
        self.reader = reader

    def process(self, item):
        # Get text from source, item here is most likely path or uri for some Web-based reader
        # read data into result
        result = self.reader.read(path=item)
        # pass result to next component
        self.push(result)


class ExtractionNode(Node):
    """
    An extractor node, part of a pipeline
    """

    def __init__(self, name: str, extractor: BaseExtractor, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = extractor

    def process(self, item: str):
        # item here is the text (str)
        # process text into triples using extractor
        result = self.extractor.get_triples(text=item)
        # pass results to next component
        self.push(result)


class ResolutionNode(Node):
    """
    A resolution node, part of a pipeline
    """

    def __init__(self, name: str, resolver: BaseResolver, **kwargs):
        super().__init__(name, **kwargs)
        self.resolver = resolver

    def process(self, item: str):
        # item here is the text (str)
        # Get coreference resolution chains
        result = self.resolver.get_coreference_chains(text=item)
        # pass results (chains) to next component
        self.push(result)


class RelationLinkingNode(Node):
    """
    A relation linking node, part of a pipeline
    """

    def __init__(self, name: str, rel_linker: BaseRelationLinker, **kwargs):
        super().__init__(name, **kwargs)
        self.rel_linker = rel_linker

    def process(self, item: str):
        # item here is the text (str)
        # Get Relations from linker
        result = self.rel_linker.get_relations(item)
        # pass results to next component
        self.push(result)


class EntityLinkingNode(Node):
    """
    An entity linking node, part of a pipeline
    """

    def __init__(self, name: str, ent_linker: BaseEntityLinker, **kwargs):
        super().__init__(name, **kwargs)
        self.ent_linker = ent_linker

    def process(self, item: str):
        # item here is the text (str)
        # Get entities from linker
        result = self.ent_linker.get_entities(item)
        # pass results to next component
        self.push(result)


class JointLinkingNode(Node):
    """
    A joint linking (entities and relations) node, part of a pipeline
    """

    def __init__(self, name: str, linker: BaseJointLinker, **kwargs):
        super().__init__(name, **kwargs)
        self.linker = linker

    def process(self, item: str):
        # item here is the text (str)
        # Get entities from linker
        result = self.linker.get_entities_and_relations(item)
        # pass results to next component
        self.push(result)


class WritingNode(Node):
    """
    An output node (writing), end of a pipeline
    """

    def __init__(self, name: str, writer: BaseWriter, **kwargs):
        super().__init__(name, **kwargs)
        self.writer = writer

    def process(self, item: List[SPOTriple]):
        # item here is the list of final triples
        # Get final triples
        result = self.writer.write(triples=item)
        # pass results to next component (No need this is the end)
        # Used in case the pipeline framework needs this
        self.push(result)
