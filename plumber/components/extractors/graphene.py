from typing import List
from plumber.components.extractors.base import BaseExtractor
from plumber.components.format import Triple
import requests
import os

GRAPHENE_URL = f'{"http://localhost:8088" if "GRAPHENE_ENDPOINT" not in os.environ else os.environ["GRAPHENE_ENDPOINT"]}/relationExtraction/text'


# Implementation of the API of the docker here: https://github.com/Lambda-3/Graphene
class GrapheneExtractor(BaseExtractor):

    def __init__(self, **kwargs):
        super().__init__(name='Graphene extractor', **kwargs)

    def get_triples(self, text) -> List[Triple]:
        # payload = "{\"text\": \""+text+"\", \"doCoreference\": \"true\", \"isolateSentences\": \"false\", \"format\": \"DEFAULT\"}"
        payload = self.prepare_json_request({"text": text, "doCoreference": True, "isolateSentences": False, "format": "DEFAULT"})
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", GRAPHENE_URL, headers=headers, data=payload.encode('utf-8'))
        sentences = response.json()['sentences']
        triples = []
        for sentence in sentences:
            for _, triple in sentence['extractionMap'].items():
                trp = Triple()
                # ========== Subject ==============
                if triple['arg1'] not in text:
                    continue
                start_index = text.index(triple['arg1'])
                end_index = start_index + len(triple['arg1'])
                trp.add_subject(triple['arg1'], start_index, end_index, text)
                # ========== Predicate ==============
                if triple['relation'] not in text:
                    continue
                start_index = text.index(triple['relation'])
                end_index = start_index + len(triple['relation'])
                trp.add_predicate(triple['relation'], start_index, end_index, text)
                # ========== Object ==============
                if triple['arg2'] not in text:
                    continue
                start_index = text.index(triple['arg2'])
                end_index = start_index + len(triple['arg2'])
                trp.add_object(triple['arg2'], start_index, end_index, text)
                # ========== Add triple to final output
                triples.append(trp)
        return triples


if __name__ == '__main__':
    extractor = GrapheneExtractor()
    x = extractor.get_triples('Barack Obama is the president of the United States of America')
