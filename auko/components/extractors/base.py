from typing import List
from auko.components import StanfordClient, OLLIEClient
from auko.discovery import AuKoClass
from auko.components.format import Triple


class BaseExtractor(AuKoClass):

    def __init__(self, name: str = 'Base Extractor'):
        self.name = name

    def get_triples(self, text: str) -> List[Triple]:
        pass


class StanfordBasedExtractor(BaseExtractor):

    def __init__(self, client: StanfordClient, key: str = None, name: str = 'Stanford-based Extractor'):
        super().__init__(name)
        self.client = client
        self.json_key = key

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

    def __init__(self, client: OLLIEClient, name: str = 'Ollie-based Extractor'):
        super().__init__(name)
        self.client = client

    def get_triples(self, text: str):
        pass
