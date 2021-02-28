from plumber.components.resolvers.base import BaseResolver
# import spacy
# import neuralcoref
from plumber.components.format import Chain
from typing import List
import requests
import os


# class SpacyNeuralCoreferenceResolver(BaseResolver):
#
#     def __init__(self, **kwargs):
#         super().__init__(name='Spacy Neural Coreference Resolver', **kwargs)
#         self.nlp = spacy.load('en')  # TODO: expose this in configuration so it can be changed
#         neuralcoref.add_to_pipe(self.nlp)
#
#     def get_coreference_chains(self, text) -> List[Chain]:
#         doc = self.nlp(text)
#         if not doc._.has_coref:
#             return []
#         else:
#             result = []
#             clusters = doc._.coref_clusters
#             for cluster in clusters:
#                 chain = Chain(cluster.main)
#                 for mention in cluster.mentions[1:]:
#                     chain.add_alias(mention.orth_, mention.start_char, mention.end_char, text)
#                 result.append(chain)
#             return result

SERVICE_URL = f'{"http://localhost:22222" if "NEURAL_COREF_ENDPOINT" not in os.environ else os.environ["NEURAL_COREF_ENDPOINT"]}/'


class SpacyNeuralCoreferenceResolver(BaseResolver):

    def __init__(self, **kwargs):
        super().__init__(name='Spacy Neural Coreference Resolver', **kwargs)

    def get_coreference_chains(self, text) -> List[Chain]:
        payload = self.prepare_json_request({"text": text})
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", SERVICE_URL, headers=headers, data=payload.encode('utf-8'))
        as_json = response.json()
        chains = []
        if 'mentions' in as_json:
            mentions = {as_json['mentions'][i]['text']: i for i in range(len(as_json['mentions']))}
            for cluster in as_json['clusters']:
                chain = Chain(cluster[0])
                for alias in cluster[1:]:
                    chain.add_alias(alias,
                                    as_json['mentions'][mentions[alias]]['start'],
                                    as_json['mentions'][mentions[alias]]['end'],
                                    text)
                chains.append(chain)
        return chains


if __name__ == '__main__':
    kwargs = {}
    resolver = SpacyNeuralCoreferenceResolver(**kwargs)
    chains = resolver.get_coreference_chains(
        'My sister has a dog. She loves him.')
    print(resolver.name)
    print('^' * 30)
    print(chains)
