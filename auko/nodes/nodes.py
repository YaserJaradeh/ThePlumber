from consecution import Node
from auko.components import BaseExtractor, BaseReader, BaseResolver, BaseWriter
from auko.components import BaseRelationLinker, BaseEntityLinker, BaseJointLinker
from auko.components import SPOTriple
from typing import List, AnyStr
import itertools


class ReadingNode(Node):
    """
    A reader node, should be first node in a pipeline
    """

    def __init__(self, name: AnyStr, reader: BaseReader, **kwargs):
        super().__init__(name, **kwargs)
        self.reader = reader

    def process(self, item):
        # Get text from source, item here is most likely path or uri for some Web-based reader
        # read data into result
        result = self.reader.read(path=item)
        # pass result to next component
        self.global_state.caller = self
        self.push(result)


class ExtractionNode(Node):
    """
    An extractor node, part of a pipeline
    """

    def __init__(self, name: AnyStr, extractor: BaseExtractor, **kwargs):
        super().__init__(name, **kwargs)
        self.extractor = extractor

    def process(self, item: AnyStr):
        # item here is the text (str)
        # process text into triples using extractor
        result = self.extractor.get_triples(text=item)
        self.global_state.triples = result
        # pass results to next component
        self.global_state.caller = self
        self.push([t.as_text for t in result])


class ResolutionNode(Node):
    """
    A resolution node, part of a pipeline
    """

    def __init__(self, name: AnyStr, resolver: BaseResolver, **kwargs):
        super().__init__(name, **kwargs)
        self.resolver = resolver

    def process(self, item: AnyStr):
        # item here is the text (str)
        # Get coreference resolution chains
        result = self.resolver.get_coreference_chains(text=item)
        # pass results (chains) to next component
        self.global_state.caller = self
        self.push(result)


class RelationLinkingNode(Node):
    """
    A relation linking node, part of a pipeline
    """

    def __init__(self, name: AnyStr, rel_linker: BaseRelationLinker, **kwargs):
        super().__init__(name, **kwargs)
        self.rel_linker = rel_linker
        self.results = []

    def begin(self):
        self.results = []

    def process(self, item: List[AnyStr]):
        # item here is the text (str)
        # Get relations from linker
        for triple in item:
            self.results.append(self.rel_linker.get_relations(triple))

    def end(self):
        self.global_state.caller = self
        self.push(list(itertools.chain(*self.results)))


class EntityLinkingNode(Node):
    """
    An entity linking node, part of a pipeline
    """

    def __init__(self, name: AnyStr, ent_linker: BaseEntityLinker, **kwargs):
        super().__init__(name, **kwargs)
        self.ent_linker = ent_linker
        self.results = []

    def begin(self):
        self.results = []

    def process(self, item: List[AnyStr]):
        # item here is the text (str)
        # Get entities from linker
        for triple in item:
            self.results.append(self.ent_linker.get_entities(triple))

    def end(self):
        self.global_state.caller = self
        self.push(list(itertools.chain(*self.results)))


class JointLinkingNode(Node):
    """
    A joint linking (entities and relations) node, part of a pipeline
    """

    def __init__(self, name: AnyStr, linker: BaseJointLinker, **kwargs):
        super().__init__(name, **kwargs)
        self.linker = linker
        self.entities = []
        self.relations = []

    def begin(self):
        self.entities = []
        self.relations = []

    def process(self, item: List[AnyStr]):
        # item here is the text (str)
        # Get entities and relations from linker
        for triple in item:
            ents, rels = self.linker.get_entities_and_relations(triple)
            self.entities.append(ents)
            self.relations.append(rels)

    def end(self):
        self.global_state.caller = self
        self.push((list(itertools.chain(*self.entities)), list(itertools.chain(*self.relations))))


class WritingNode(Node):
    """
    An output node (writing), end of a pipeline
    """

    def __init__(self, name: AnyStr, writer: BaseWriter, **kwargs):
        super().__init__(name, **kwargs)
        self.writer = writer

    def process(self, item: List[SPOTriple]):
        # item here is the list of final triples
        # Get final triples
        result = self.writer.write(triples=item)
        # pass results to next component (No need this is the end)
        self.global_state.caller = self
        # Used in case the pipeline framework needs this
        self.push(result)


class ProcessingNode(Node):
    """
    A processing node, part of a pipeline
    collects information from extractors, linkers, and resolvers and then it produces the final triples
    """

    def begin(self):
        self.triples = []
        self.relations = []
        self.entities = []
        self.chains = []

    def process(self, item):
        caller = self.global_state.caller
        if isinstance(caller, ResolutionNode):
            self.chains = item
        if isinstance(caller, EntityLinkingNode):
            self.entities = item
        if isinstance(caller, RelationLinkingNode):
            self.relations = item
        if isinstance(caller, JointLinkingNode):
            self.entities = item[0]
            self.relations = item[1]

    def end(self):
        self.triples = self.global_state.triples
        final_result = self.process_data()
        self.global_state.caller = self
        self.push(final_result)

    def process_data(self) -> List[SPOTriple]:
        return [t.as_text for t in self.triples]

