from auko.components.stanford import StanfordClient
from auko.components.resolvers.base import StanfordBasedResolver


class StanfordCoreferenceResolver(StanfordBasedResolver):

    def __init__(self, stanford_client: StanfordClient):
        super().__init__(name='Stanford Coreference Resolver', client=stanford_client)

    def get_coreference_chains(self, text):
        x = self.client.coref(text)
        # get sentence in output
        # get location in string
        # check if we need empty chains (or chains with only one occurrence)
        return x
