from auko.components.linkers.base import BaseJointLinker, BaseWebLinker


class FalconJointLinker(BaseJointLinker, BaseWebLinker):

    def __init__(self):
        # TODO: replace with super call
        BaseJointLinker.__init__(self, name="Falcon Relation and Entity Linker")
        BaseWebLinker.__init__(self, api_url="https://labs.tib.eu/falcon/falcon2/api")

    def get_entities_and_relations(self, text: str, kg='wikidata', mode='long'):
        db = kg.lower().strip() if kg.lower().strip() in ['wikidata', 'dbpedia'] else 'wikidata'
        mode = mode.lower().strip() if mode.lower().strip() in ['long', 'short'] else 'long'
        params = {"mode": mode}
        if db == 'dbpedia':
            params['db'] = 1
        return self.client.POST(json={"text": text}, params=params)


class FalconJoinLinkerDBpedia(FalconJointLinker):

    def get_entities_and_relations(self, text: str):
        return super().get_entities_and_relations(text, kg='dbpedia')


class FalconJoinLinkerWikidata(FalconJointLinker):

    def get_entities_and_relations(self, text: str):
        return super().get_entities_and_relations(text)
