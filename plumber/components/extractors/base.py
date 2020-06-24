from typing import List
from plumber.components import StanfordClient, OLLIEClient
from plumber.discovery import PlumberClass
from plumber.components.format import Triple


class BaseExtractor(PlumberClass):

    def __init__(self, name: str = 'Base Extractor', **kwargs):
        self.name = name
        self.kwargs = kwargs

    def get_triples(self, text: str) -> List[Triple]:
        pass


class DummyExtractor(BaseExtractor):
    """
    Dummy extractor used for testing purposes or to fill space in the pipeline
    """

    def __init__(self):
        super().__init__(name='dummy extractor')

    def get_triples(self, text) -> List[Triple]:
        return []


class StanfordBasedExtractor(BaseExtractor):

    def __init__(self, name: str = 'Stanford-based Extractor', **kwargs):
        super().__init__(name)
        if 'stanford_client' not in kwargs:
            raise ValueError('stanford_client parameter should be passed to any Stanford based component')
        self.client = kwargs['stanford_client']
        self.json_key = kwargs['key'] if 'key' in kwargs else None

    def get_triples(self, text: str) -> List[Triple]:
        pass

    def transform_triples(self, sentences: List[dict], text: str) -> List[Triple]:
        """
        transform triples from Stanford JSON format to auko Triple objects
        :param sentences: sentences list chuncked by stanford core nlp server
        :param text: the original text were extraction occurred
        :return: list of auko triples
        """
        if self.json_key is None:
            raise ValueError("key should be set to use this functionality")
        triples = []
        for sentence in sentences:
            for text_triple in sentence[self.json_key]:
                triple = Triple()
                start = sentence['tokens'][text_triple['subjectSpan'][0]]['characterOffsetBegin']
                end = sentence['tokens'][text_triple['subjectSpan'][1] - 1]['characterOffsetEnd']
                triple.add_subject(text_triple['subject'], start, end, text)
                ####################################
                if text_triple['relationSpan'][0] < 0:
                    start = None
                    end = None
                else:
                    start = sentence['tokens'][text_triple['relationSpan'][0]]['characterOffsetBegin']
                    end = sentence['tokens'][text_triple['relationSpan'][1] - 1]['characterOffsetEnd']
                triple.add_predicate(text_triple['relation'], start, end, text)
                #####################################
                start = sentence['tokens'][text_triple['objectSpan'][0]]['characterOffsetBegin']
                end = sentence['tokens'][text_triple['objectSpan'][1] - 1]['characterOffsetEnd']
                triple.add_object(text_triple['object'], start, end, text)
                triples.append(triple)
        return triples


class OllieBasedExtractor(BaseExtractor):

    def __init__(self, name: str = 'Ollie-based Extractor', **kwargs):
        super().__init__(name)
        if 'ollie_client' not in kwargs:
            raise ValueError('ollie_client parameter should be passed to any Ollie based component')
        self.client = kwargs['ollie_client']

    def get_triples(self, text: str):
        pass
