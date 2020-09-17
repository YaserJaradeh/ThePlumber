from typing import List
from plumber.components.extractors.base import BaseExtractor
from plumber.components.format import Triple
import requests


MINIE_URL = "http://localhost:8080/minie/query"


class MinIEExtractor(BaseExtractor):

    def __init__(self, **kwargs):
        super().__init__(name='MinIE extractor', **kwargs)

    def get_triples(self, text) -> List[Triple]:

        payload = text
        headers = {
            'Content-Type': 'text/plain'
        }

        response = requests.request("POST", MINIE_URL, headers=headers, data=payload.encode('utf-8'))
        facts = response.json()['facts']

        triples = []
        for fact in facts:
            triple = Triple()
            # ========== Subject ==============
            subj = fact['subject']
            if subj not in text:
                start_index = -1
                end_index = -1
            else:
                start_index = text.index(subj)
                end_index = start_index + len(subj)
            triple.add_subject(subj, start_index, end_index, text)
            # ========== Predicate ==============
            pred = fact['predicate']
            if pred not in text:
                start_index = -1
                end_index = -1
            else:
                start_index = text.index(pred)
                end_index = start_index + len(pred)
            triple.add_predicate(pred, start_index, end_index, text)
            # ========== Object ==============
            obj = fact['object']
            if obj not in text:
                start_index = -1
                end_index = -1
            else:
                start_index = text.index(obj)
                end_index = start_index + len(obj)
            triple.add_object(obj, start_index, end_index, text)
            # ========== Add triple to final output
            triples.append(triple)
        return triples


if __name__ == "__main__":
    sentence = 'The Joker believes that the hero Batman was not actually born in foggy Gotham City.'
    extractor = MinIEExtractor()
    x = extractor.get_triples(sentence)
