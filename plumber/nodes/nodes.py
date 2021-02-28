from consecution import Node
from plumber.components import BaseExtractor, BaseReader, BaseResolver, BaseWriter, Triple, Chain, Pair
from plumber.components import BaseLinker
from plumber.components import SPOTriple
from typing import List, AnyStr
import itertools
import logging


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
        # self.global_state.caller = self  # Remove so last caller is still valid and processing node can guess which
        self.push(self.results)


class TriplesAggregationNode(AggregationNode):
    """
    A triple aggregation node, to collect the triples in the global state
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
        self.global_state.triples = self.results
        self.push(self.results)


class ChainsAggregationNode(AggregationNode):
    """
    A chain aggregation node, to collect the chains in the global state
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
        self.global_state.chains = self.results
        self.push(self.results)


class LinksAggregationNode(AggregationNode):
    """
    A link aggregation node, to collect the links in the global state
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
        self.global_state.links = self.results
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
        result = self.reader.read()
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
        try:
            result = self.extractor.get_triples(text=item)
        except Exception as exp:
            result = []
            logging.error('Error at %s', f'Extraction Node {self.name}', exc_info=exp)
        # if len(self.global_state.triples) == 0:
        #     self.global_state.triples = result
        # else:
        #     self.global_state.triples += result
        # pass results to next component
        self.global_state.caller = self
        # self.push([t.as_text for t in result])
        self.push(result)


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
        try:
            result = self.resolver.get_coreference_chains(text=item)
        except Exception as exp:
            result = []
            logging.error('Error at %s', f'Resolution Node {self.name}', exc_info=exp)
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

    def process(self, item: List[Triple]):
        # item here is the text (str)
        # Get all links from linker
        try:
            for triple in item:
                self.results.append(self.linker.get_links(triple.as_text))
        except Exception as exp:
            self.results.append([])
            logging.error('Error at %s', f'Linking Node {self.name}', exc_info=exp)

    def end(self):
        self.global_state.caller = self
        self.push(list(itertools.chain(*self.results)))


class WritingNode(Node):
    """
    An output node (writing), end of a pipeline
    """

    result = []

    def __init__(self, name: AnyStr, writer: BaseWriter, **kwargs):
        super().__init__(name, **kwargs)
        self.writer = writer

    def process(self, item: List[SPOTriple]):
        # item here is the list of final triples
        # Get final triples
        self.result = self.writer.write(triples=item)
        # pass results to next component (No need this is the end)
        self.global_state.caller = self
        # Used in case the pipeline framework needs this
        # self.push(self.result)

    def end(self):
        return self.result


class ProcessingNode(Node):
    """
    A processing node, part of a pipeline
    collects information from extractors, linkers, and resolvers and then it produces the final triples
    """

    triples: List[Triple] = []
    links: List[Pair] = []
    chains: List[Chain] = []

    def begin(self):
        self.triples = []
        self.links = []
        self.chains = []

    def process(self, item):
        # caller = self.global_state.caller
        # if isinstance(caller, ResolutionNode):
        #     self.chains = item
        # if isinstance(caller, LinkingNode):
        #     self.links = item
        pass

    def end(self):
        self.triples = self.global_state.triples
        self.links = self.global_state.links
        self.chains = self.global_state.chains
        self.global_state.caller = self
        final_result = self.process_data()
        self.push(final_result)

    def process_data(self) -> List[SPOTriple]:
        dereferenced_tiples = self.process_chains()
        linked_triples = self.process_links(dereferenced_tiples)
        final_triples = map(lambda t: SPOTriple.from_triple(t), linked_triples)
        return list(final_triples)

    def process_chains(self):
        new_triples = self.triples
        chain_dict = {}
        for chain in self.chains:
            for alias in chain.aliases:
                chain_dict[alias] = chain.main
        if len(chain_dict) > 0:
            for triple in new_triples:
                if triple.subject in chain_dict:
                    triple.subject.surface_form = chain_dict[triple.subject]
                if triple.object in chain_dict:
                    triple.object.surface_form = chain_dict[triple.object]
        return new_triples

    def process_links(self, triples: List[Triple]):
        new_triples = triples
        try:
            if len(self.links) > 0:
                so_spans = {}
                p_spans = {}
                for triple in triples:
                    # Add Subject spans
                    if triple.subject.surface_form.lower() not in so_spans:
                        so_spans[triple.subject.surface_form.lower()] = [triple.subject]
                    else:
                        so_spans[triple.subject.surface_form.lower()].append(triple.subject)
                    # Add object spans
                    if triple.object.surface_form.lower() not in so_spans:
                        so_spans[triple.object.surface_form.lower()] = [triple.object]
                    else:
                        so_spans[triple.object.surface_form.lower()].append(triple.object)
                    # add predicate spans
                    if triple.predicate.surface_form.lower() not in p_spans:
                        p_spans[triple.predicate.surface_form.lower()] = [triple.predicate]
                    else:
                        p_spans[triple.predicate.surface_form.lower()].append(triple.predicate)
                for link in self.links:
                    if link.link_type == 'entity':
                        spans = so_spans
                    else:
                        spans = p_spans
                    if link.span.lower() in spans:
                        for span in spans[link.span.lower()]:
                            span.mapping = link.mapping
                            # span.surface_form = link.mapping
        except Exception as exp:
            raise exp
        finally:
            return new_triples
