from consecution import Node
from auko.components import BaseExtractor, BaseReader, BaseResolver, BaseWriter
from auko.components import BaseLinker
from auko.components import SPOTriple
from typing import List, AnyStr
import itertools


class AggregationNode(Node):
    """
    An aggregation node, generic node can be used to collect results from other nodes
    """

    def __init__(self, name: AnyStr, **kwargs):
        super().__init__(name, **kwargs)

    def begin(self):
        self.results = None

    def process(self, item):
        if self.results is None:
            self.results = type(item)()
        self.results = self.results + item

    def end(self):
        self.global_state.caller = self
        self.push(self.results)


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
        if len(self.global_state.triples) == 0:
            self.global_state.triples = result
        else:
            self.global_state.triples += result
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


class LinkingNode(Node):
    """
    A generic linking node, part of a pipeline
    """

    def __init__(self, name: AnyStr, linker: BaseLinker, **kwargs):
        super().__init__(name, **kwargs)
        self.linker = linker
        self.results = []

    def begin(self):
        self.results = []

    def process(self, item: List[AnyStr]):
        # item here is the text (str)
        # Get all links from linker
        for triple in item:
            self.results.append(self.linker.get_links(triple))

    def end(self):
        self.global_state.caller = self
        self.push(list(itertools.chain(*self.results)))


class WritingNode(Node):
    """
    An output node (writing), end of a pipeline
    """

    def __init__(self, name: AnyStr, writer: BaseWriter, **kwargs):
        super().__init__(name, **kwargs)
        self.writer = writer
        self.kwargs = kwargs

    def process(self, item: List[SPOTriple]):
        # item here is the list of final triples
        # Get final triples
        result = self.writer.write(triples=item, **self.kwargs)
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
        self.links = []
        self.chains = []

    def process(self, item):
        caller = self.global_state.caller
        if isinstance(caller, ResolutionNode):
            self.chains = item
        if isinstance(caller, LinkingNode):
            self.links = item

    def end(self):
        self.triples = self.global_state.triples
        final_result = self.process_data()
        self.global_state.caller = self
        self.push(final_result)

    def process_data(self) -> List[SPOTriple]:
        return [t.as_text for t in self.triples]
