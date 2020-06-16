from auko.components.resolvers.base import BaseResolver
import spacy
import neuralcoref
from auko.components.format import Chain
from typing import List


class SpacyNeuralCoreferenceResolver(BaseResolver):

    def __init__(self, **kwargs):
        super().__init__(name='Spacy Neural Coreference Resolver', **kwargs)
        self.nlp = spacy.load('en')  # TODO: expose this in configuration so it can be changed
        neuralcoref.add_to_pipe(self.nlp)

    def get_coreference_chains(self, text) -> List[Chain]:
        doc = self.nlp(text)
        if not doc._.has_coref:
            return []
        else:
            result = []
            clusters = doc._.coref_clusters
            for cluster in clusters:
                chain = Chain(cluster.main)
                for mention in cluster.mentions[1:]:
                    chain.add_alias(mention.orth_, mention.start_char, mention.end_char, text)
                result.append(chain)
            return result
