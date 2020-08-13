from pathlib import Path
import spacy
import json
from spacy.kb import KnowledgeBase
from spacy.pipeline import EntityLinker
from spacy.vocab import Vocab


def _print_kb(kb):
    print(kb.get_size_entities(), "kb entities:", kb.get_entity_strings())
    print(kb.get_size_aliases(), "kb aliases:", kb.get_alias_strings())


def _to_jsonl_dbpedia():
    entities_file = open('./output/DBpedia/kb_dir/entities.jsonl', 'w')
    alias_file = open('./output/DBpedia/kb_dir/aliases.jsonl', 'w')
    with open('./DBpedia-class.tsv', 'r') as in_file:
        _write_jsonl_entities_and_aliases(alias_file, entities_file, in_file)
    with open('./DBpedia-ontology.tsv', 'r') as in_file:
        _write_jsonl_entities_and_aliases(alias_file, entities_file, in_file)
    with open('./DBpedia-property.tsv', 'r') as in_file:
        _write_jsonl_entities_and_aliases(alias_file, entities_file, in_file)
    with open('./DBpedia-entity.tsv', 'r') as in_file:
        _write_jsonl_entities_and_aliases(alias_file, entities_file, in_file)
    entities_file.flush()
    entities_file.close()
    alias_file.flush()
    alias_file.close()


def _to_jsonl_wikidata():
    entities_file = open('./output/Wikidata/kb_dir/entities.jsonl', 'w')
    alias_file = open('./output/Wikidata/kb_dir/aliases.jsonl', 'w')
    with open('./Wikidata-property.tsv', 'r') as in_file:
        _write_jsonl_entities_and_aliases(alias_file, entities_file, in_file)
    with open('./Wikidata-entity.tsv', 'r') as in_file:
        _write_jsonl_entities_and_aliases(alias_file, entities_file, in_file)
    entities_file.flush()
    entities_file.close()
    alias_file.flush()
    alias_file.close()


def _write_jsonl_entities_and_aliases(alias_file, entities_file, in_file):
    for index, line in enumerate(in_file.readlines()):
        if index == 0:
            continue
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue
        qid = parts[0]
        entity_entry = {"id": qid, "description": parts[1]}
        entities_file.write(f"{json.dumps(entity_entry)}\n")
        aliases = list(filter(lambda x: len(x) > 0, parts[1].split('|||')))
        for alias in aliases:
            alias_entry = {"alias": alias, "entities": [qid], "probabilities": [1.0 / len(aliases)]}
            alias_file.write(f"{json.dumps(alias_entry)}\n")


def get_aliases(in_file):
    for index, line in enumerate(in_file.readlines()):
        if index == 0:
            continue
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue
        for alias in parts[1].split('|||'):
            yield alias

# Use this
# https://microsoft.github.io/spacy-ann-linker/


if __name__ == '__main__':
    # _to_jsonl_dbpedia()
    # nlp = spacy.load('en_core_web_lg')
    # kb = KnowledgeBase(vocab=nlp.vocab, entity_vector_length=300)
    #
    # with open('./DBpedia-class.tsv', 'r') as in_file:
    #     for index, line in enumerate(in_file.readlines()):
    #         if index == 0:
    #             continue
    #         parts = line.strip().split('\t')
    #         if len(parts) < 2:
    #             continue
    #         qid = parts[0]
    #         kb.add_entity(entity=qid, entity_vector=nlp(parts[1]).vector, freq=100)
    #         for alias in parts[1].split('|||'):
    #             kb.add_alias(alias=alias, entities=[qid], probabilities=[1])
    #
    #     print(f'Entities in the KB: {kb.get_entity_strings()}')
    #     print(f'Aliases in the KB: {kb.get_alias_strings()}')

    # model_dir = "/media/jaradeh/HDD/AUKO/AutoKomplete/plumber/data/models/ann_linker"
    model_dir = "./output/my_nlp_lite"
    nlp = spacy.load(model_dir)
    # nlp = spacy.blank("en")
    # ruler = nlp.create_pipe('entity_ruler', {"overwrite_ents": True})
    # # ruler = nlp.create_pipe('entity_ruler')
    # files = [("DB-CLS", './DBpedia-class.tsv'), ("DB-ONT", './DBpedia-ontology.tsv'), ("DB-PRP", './DBpedia-property.tsv'), ("DB-ENT", './DBpedia-entity.tsv')]
    # for lbl, path in files:
    #     print(f'doing {path}')
    #     with open(path, 'r') as in_file:
    #         patterns = [
    #             {"label": lbl, "pattern": alias}
    #             for alias in get_aliases(in_file)
    #         ]
    #         ruler.add_patterns(patterns)
    # nlp.add_pipe(ruler)
    # remote_ann_linker = nlp.create_pipe('remote_ann_linker', {
    #     'base_url': "http://localhost:8080/link"
    # })
    # nlp.add_pipe(remote_ann_linker)
    # # nlp.add_pipe(ruler, before="ann_linker")
    # nlp.to_disk('./output/my_nlp_lite')

    doc = nlp("Who painted The Storm on the Sea of Galilee?")
    for ent in doc.ents:
        print(ent.text, ent.label_, ent.kb_id_)

