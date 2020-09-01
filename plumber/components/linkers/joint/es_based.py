from plumber.components.linkers.base import BaseLinker
from plumber.components.linkers.joint import FalconWikidataJointLinker, FalconDBpediaJointLinker
from plumber.components.format import Pair
from typing import List, Tuple
from elasticsearch import Elasticsearch

ES_endpoint = 'http://node1.research.tib.eu:9200/'


class ElasticSearchLookUp:

    def __init__(self):
        self.es = Elasticsearch([ES_endpoint])
        self.doc_type = "doc"

    def __search_in_es(self, index_name: str, recognized_strings: List[str]) -> List[Tuple[str, str]]:
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


class ElasticSearchLinker(BaseLinker):
    linker: BaseLinker

    def __init__(self, **kwargs):
        super().__init__(name="Elastic Search Based linker", **kwargs)

    @staticmethod
    def __strip_to_ner(links: List[Pair]) -> Tuple[List[str], List[str]]:
        entities = [entity.span for entity in filter(lambda x: x.link_type == 'entity', links)]
        relations = [relation.span for relation in filter(lambda x: x.link_type == 'relation', links)]
        return entities, relations

    def get_links(self, text: str) -> List[Pair]:
        return self.linker.get_links(text=text)


class ESFalconDBpediaJointLinker(ElasticSearchLinker, ElasticSearchLookUp):

    def __init__(self, **kwargs):
        ElasticSearchLinker.__init__(self, **kwargs)
        ElasticSearchLookUp.__init__(self)
        self.linker = FalconDBpediaJointLinker(**kwargs)

    def get_links(self, text: str) -> List[Pair]:
        from_ner = super().get_links(text=text)
        ents, preds = self.__strip_to_ner(from_ner)
        linked_entities = [Pair(ent[0], ent[1], 'entity') for ent in self.__search_in_es("dbentityindex", ents)]
        linked_relations = [Pair(rel[0], rel[1], 'relation') for rel in self.__search_in_es("dbontologyindex", preds)]
        return linked_entities + linked_relations


class ESFalconWikidataJointLinker(ElasticSearchLinker, ElasticSearchLookUp):

    def __init__(self, **kwargs):
        ElasticSearchLinker.__init__(self, **kwargs)
        ElasticSearchLookUp.__init__(self)
        self.linker = FalconWikidataJointLinker(**kwargs)

    def get_links(self, text: str) -> List[Pair]:
        from_ner = super().get_links(text=text)
        ents, preds = self.__strip_to_ner(from_ner)
        linked_entities = [Pair(ent[0], ent[1], 'entity') for ent in self.__search_in_es("wikidataentityindex", ents)]
        linked_relations = [Pair(rel[0], rel[1], 'relation') for rel in self.__search_in_es("wikidatapropertyindex", preds)]
        return linked_entities + linked_relations


if __name__ == '__main__':
    linker = ESFalconDBpediaJointLinker()
    x = linker.get_links(text="who is the wife of Barack Obama?")
