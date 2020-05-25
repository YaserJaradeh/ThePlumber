from auko.components.resolvers.base import BaseResolver
import spacy
import neuralcoref


class SpacyNeuralCoreferenceResolver(BaseResolver):

    def __init__(self):
        super().__init__(name='Spacy Neural Coreference Resolver')
        self.nlp = spacy.load('en')
        neuralcoref.add_to_pipe(self.nlp)

    def get_coreference_chains(self, text):
        doc = self.nlp(text)
        if not doc._.has_coref:
            return []
        else:
            result = []
            clusters = doc._.coref_clusters
            for cluster in clusters:
                chain = []
                cluster.mentions
        # get sentence in output
        # get location in string
        # check if we need empty chains (or chains with only one occurrence)
        return x
