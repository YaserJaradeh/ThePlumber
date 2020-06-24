from typing import List
from plumber.components.resolvers.base import StanfordBasedResolver
from plumber.components.format import Chain


class StanfordCoreferenceResolver(StanfordBasedResolver):

    def __init__(self, **kwargs):
        super().__init__(name='Stanford Coreference Resolver', **kwargs)

    def get_coreference_chains(self, text) -> List[Chain]:
        response = self.client.coref(text, simple_format=False)
        result = []
        for _, coref in response['corefs'].items():
            if len(coref) > 1:
                chain = Chain(coref[0]['text'])
                for chunk in coref[1:]:
                    sentence = response['sentences'][chunk['sentNum']-1]
                    start = sentence['tokens'][chunk['startIndex']-1]['characterOffsetBegin']
                    end = sentence['tokens'][chunk['endIndex']-2]['characterOffsetEnd']
                    chain.add_alias(chunk['text'], start, end, text)
                result.append(chain)
        return result
