from typing import List
from auko.components.clients.ollie import OLLIEClient
from auko.components.extractors.base import OllieBasedExtractor
from auko.components.format import Triple
import nltk


class OllieExtractor(OllieBasedExtractor):

    def __init__(self, ollie_client: OLLIEClient, confidence=0.6):
        super().__init__(name='OLLIE extractor', client=ollie_client)
        self.confidence = confidence

    def get_triples(self, text) -> List[Triple]:
        sentences = nltk.sent_tokenize(text)
        triples = []
        for idx, sentence in enumerate(sentences):
            result = self.client.get_extraction(sentence)
            for text_triple in result:
                if text_triple['confidence'] >= self.confidence:
                    triple = self.create_auko_triple(text, sentence, text_triple['arg1'], text_triple['rel'],
                                                     text_triple['arg2'], sum([len(s) for s in sentences[:idx]]) + (
                                                             text[:text.find(sentence) + len(sentence)].count(' ')
                                                             - sum([s.count(' ') for s in sentences[:idx + 1]])))
                    triples.append(triple)
        return triples

    @staticmethod
    def create_auko_triple(text: str, sentence: str, subj: str, pred: str, obj: str, padding: int) -> Triple:
        """
        Packs the text triple into an auko triple object
        :param text: the original text where the triple is extracted from
        :param sentence: the sentence this triple belongs to (used for surface form indexing)
        :param subj: the surface from on the subject
        :param pred: the surface from on the predicate
        :param obj: the surface from on the object
        :param padding: the number of chars to add to the indexing, due to tokenizing
        :return: an AUKO triple object
        """
        triple = Triple()
        ###########################
        start_idx = sentence.find(subj) + padding
        end_idx = start_idx + len(subj)
        triple.add_subject(subj, start_idx, end_idx, text)
        ###########################
        start_idx = sentence.find(pred) + padding
        end_idx = start_idx + len(pred)
        triple.add_predicate(pred, start_idx, end_idx, text)
        ###########################
        start_idx = sentence.find(obj) + padding
        end_idx = start_idx + len(obj)
        triple.add_object(obj, start_idx, end_idx, text)
        ###########################
        return triple
