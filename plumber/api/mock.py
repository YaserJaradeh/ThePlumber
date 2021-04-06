from typing import List, Tuple, Dict
import time
import random


mock_entities = {
    'barack obama':
        {'dbp': 'http://dbpedia.org/resource/Barack_Obama', 'wd': 'http://www.wikidata.org/entity/Q76', 'orkg': None},
    'usa':
        {'dbp': 'http://dbpedia.org/resource/United_States', 'wd': 'http://www.wikidata.org/entity/Q30', 'orkg': None},
    'hawaii':
        {'dbp': 'http://dbpedia.org/resource/Hawaii', 'wd': 'http://www.wikidata.org/entity/Q782', 'orkg': None},
    '44th president':
        {'dbp': None, 'wd': 'http://www.wikidata.org/entity/Q116139', 'orkg': None},
}

mock_relations = {
    'is president of':
        {'dbp': 'https://dbpedia.org/ontology/president', 'wd': 'http://www.wikidata.org/entity/P6', 'orkg': None},
    'was born in':
        {'dbp': 'http://dbpedia.org/property/placeOfBirth', 'wd': 'http://www.wikidata.org/entity/P19', 'orkg': None},
    'mean incubation period':
        {'dbp': None, 'wd': None, 'orkg': 'https://www.orkg.org/orkg/property/P16024'},
    'mean serial interval':
        {'dbp': None, 'wd': None, 'orkg': 'https://www.orkg.org/orkg/property/P16025'},
    'R0 estimates (average)':
        {'dbp': None, 'wd': None, 'orkg': 'https://www.orkg.org/orkg/property/P16022'},
    '95% confidence interval':
        {'dbp': None, 'wd': None, 'orkg': 'https://www.orkg.org/orkg/property/P9044'},
}

mock_pipelines = {
    'barack obama is the 44th president of the usa. he was born in hawaii':
        (['OpenIE'], ['spacy_neural_coreference'], ['FalconWikidataJoint']),
    'background: as the covid-19 epidemic is spreading, incoming data all':
        (['r0'], [], ['ORKGSpacyANN'])
}


def mess_with_response(response: List[Dict], text: str) -> List[Dict]:
    if any(['dbpedia.org' in t['object']['uri'].lower() if t['object']['uri'] is not None else False for t in response] +
           ['dbpedia.org' in t['subject']['uri'].lower() if t['subject']['uri'] is not None else False for t in response] +
           ['dbpedia.org' in t['predicate']['uri'].lower() if t['predicate']['uri'] is not None else False for t in response]):
        return response
    if 'covid' in text.lower():
        kg = 'orkg'
    else:
        kg = 'wd'
    for triple in response:
        if triple['object']['label'].lower() in mock_entities:
            triple['object']['uri'] = mock_entities[triple['object']['label'].lower()][kg]
        if triple['subject']['label'].lower() in mock_entities:
            triple['subject']['uri'] = mock_entities[triple['subject']['label'].lower()][kg]
        if triple['predicate']['label'].lower() in mock_relations:
            triple['predicate']['uri'] = mock_relations[triple['predicate']['label'].lower()][kg]
    return response


def get_suitable_pipeline(text: str) -> Tuple[List[str], List[str], List[str]]:
    time.sleep(5)
    if text[:68].lower().strip() in mock_pipelines:
        return mock_pipelines[text[:68].lower().strip()]
    else:
        if 'covid' in text.lower():
            return ['r0'], [], ['ORKGSpacyANN']
        else:
            percentage = random.random()
            return ['ClausIE' if percentage > 0.4 else 'MinIE'],\
                   ['hmtl' if percentage > 0.4 else 'spacy_neural_coreference'],\
                   ['FalconDBpediaJoint' if percentage > 0.45 else 'EARLJoint']

