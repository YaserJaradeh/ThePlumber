from plumber.components.linkers.base import BaseLinker
from plumber.components.linkers.joint import FalconWikidataJointLinker, FalconDBpediaJointLinker
from plumber.components.linkers.joint import EARLJointLinker
from plumber.components.linkers.entity import TagMeEntityLinker
from plumber.components.format import Pair
from typing import List, Tuple
from elasticsearch import Elasticsearch

ES_endpoint = 'http://node1.research.tib.eu:9200/'


class ElasticSearchLookUp:

    def __init__(self):
        self.es = Elasticsearch([ES_endpoint])
        self.doc_type = "doc"

    def search_in_es(self, index_name: str, recognized_strings: List[str]) -> List[Tuple[str, str]]:
        results = []
        for query in recognized_strings:
            elastic_results = self.es.search(index=index_name, doc_type=self.doc_type, body={
                "query": {
                    "match": {"label": query}
                }
                , "size": 10
            })
            for result in elastic_results['hits']['hits']:
                results.append((result["_source"]["uri"], query))
                break
        return results


class ElasticSearchLinker(BaseLinker, ElasticSearchLookUp):
    linker: BaseLinker
    entity_es_index_name: str
    relation_es_index_name: str

    def __init__(self, name="Elastic Search Based linker", **kwargs):
        ElasticSearchLookUp.__init__(self)
        BaseLinker.__init__(self, name=name, **kwargs)

    @staticmethod
    def strip_to_ner(links: List[Pair]) -> Tuple[List[str], List[str]]:
        entities = [entity.span for entity in filter(lambda x: x.link_type == 'entity', links)]
        relations = [relation.span for relation in filter(lambda x: x.link_type == 'relation', links)]
        return entities, relations

    def check_execution_safety(self):
        if self.linker is None or self.entity_es_index_name is None or self.relation_es_index_name is None:
            raise RuntimeError("Linker property should be set correctly, as well as the entity/relation ES index name")

    def get_links(self, text: str) -> List[Pair]:
        self.check_execution_safety()
        from_ner = self.linker.get_links(text=text)
        ents, preds = self.strip_to_ner(from_ner)
        linked_entities = [Pair(ent[0], ent[1], 'entity') for ent in
                           self.search_in_es(self.entity_es_index_name, ents)]
        linked_relations = [Pair(rel[0], rel[1], 'relation') for rel in
                            self.search_in_es(self.relation_es_index_name, preds)]
        return linked_entities + linked_relations


class ESFalconDBpediaJointLinker(ElasticSearchLinker):

    def __init__(self, **kwargs):
        super().__init__(name="Falcon NER + ES (DBpedia) linker", **kwargs)
        self.linker = FalconDBpediaJointLinker(**kwargs)
        self.entity_es_index_name = "dbentityindex"
        self.relation_es_index_name = "dbontologyindex"


class ESFalconWikidataJointLinker(ElasticSearchLinker):

    def __init__(self, **kwargs):
        super().__init__(name="Falcon NER + ES (Wikidata) linker", **kwargs)
        self.linker = FalconWikidataJointLinker(**kwargs)
        self.entity_es_index_name = "wikidataentityindex"
        self.relation_es_index_name = "wikidatapropertyindex"


class ESEarlDBpediaJointLinker(ElasticSearchLinker):

    def __init__(self, **kwargs):
        super().__init__(name="EARL NER + ES (DBpedia) linker", **kwargs)
        self.linker = EARLJointLinker(**kwargs)
        self.entity_es_index_name = "dbentityindex"
        self.relation_es_index_name = "dbontologyindex"


class ESEarlWikidataJointLinker(ElasticSearchLinker):

    def __init__(self, **kwargs):
        super().__init__(name="EARL NER + ES (Wikidata) linker", **kwargs)
        self.linker = EARLJointLinker(**kwargs)
        self.entity_es_index_name = "wikidataentityindex"
        self.relation_es_index_name = "wikidatapropertyindex"


class ESTagMeDBpediaJointLinker(ElasticSearchLinker):

    def __init__(self, **kwargs):
        super().__init__(name="TagMe NER + ES (DBpedia) linker", **kwargs)
        self.linker = TagMeEntityLinker(**kwargs)
        self.entity_es_index_name = "dbentityindex"
        self.relation_es_index_name = "dbontologyindex"


class ESTagMeWikidataJointLinker(ElasticSearchLinker):

    def __init__(self, **kwargs):
        super().__init__(name="TagMe NER + ES (Wikidata) linker", **kwargs)
        self.linker = TagMeEntityLinker(**kwargs)
        self.entity_es_index_name = "wikidataentityindex"
        self.relation_es_index_name = "wikidatapropertyindex"


if __name__ == '__main__':
    linker = ESFalconWikidataJointLinker()
    x = linker.get_links(text="who is the wife of Barack Obama?")
