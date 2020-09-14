import json
from tqdm import tqdm
import sparql


DBPEDIA_ENDPOINT = "http://node1.research.tib.eu:4001/sparql"


def clean_up_webnlg(input_file: str, output_file: str):
    results = []
    with open(input_file, 'r') as in_file:
        content = json.load(in_file)
        for entry in tqdm(content['entries']):
            statements = entry[list(entry.keys())[0]]
            category = statements['category']
            text = statements['lexicalisations'][0]['lex']
            triples = statements['modifiedtripleset']
            results.append({'category': category, 'text': text, 'triples': triples})
    with open(output_file, 'a+') as out_file:
        json.dump(results, out_file)


def get_resource_wikidata_sameas(resource: str):
    q = "SELECT ?x WHERE { <http://dbpedia.org/resource/"+resource+"> <http://www.w3.org/2002/07/owl#sameAs> ?x. FILTER regex(str(?x), \"wikidata\")}"
    # print(resource)
    result = sparql.query(DBPEDIA_ENDPOINT, q)
    if result.hasresult():
        return sparql.unpack_row(result[0])[0]
    else:
        return None


def get_predicate_wikidata_sameas(predicate: str):
    q = "ASK WHERE { <http://dbpedia.org/ontology/"+predicate+"> ?p ?o. }"
    result = sparql.query(DBPEDIA_ENDPOINT, q)
    is_ontology = result.hasresult()
    predicate_uri = f'<http://dbpedia.org/{"ontology" if is_ontology else "property"}/{predicate}>'
    q = "SELECT * WHERE { "+predicate_uri+" <http://www.w3.org/2002/07/owl#equivalentProperty> ?o. FILTER regex(str(?o), \"wikidata\")}"
    result = sparql.query(DBPEDIA_ENDPOINT, q)
    if result.hasresult():
        return sparql.unpack_row(result[0])[0]
    else:
        return None


def convert_webnlg_to_wd(input_file: str, output_file: str):
    wd_triples = []
    with open(input_file, 'r') as in_file:
        content = json.load(in_file)
        for entry in tqdm(content):
            temp_triples = []
            for triple in entry['triples']:
                sub = triple['subject'].replace(' ', '_')
                obj = triple['object'].replace(' ', '_')
                pred = triple['property'].replace(' ', '_')
                wd_subject = get_resource_wikidata_sameas(sub)
                if wd_subject is None:
                    continue
                wd_object = get_resource_wikidata_sameas(obj)
                if wd_object is None:
                    continue
                wd_predicate = get_predicate_wikidata_sameas(pred)
                if wd_predicate is None:
                    continue
                temp_triples.append({'object': wd_object, 'property': wd_predicate, 'subject': wd_subject})
            if len(temp_triples) > 0:
                wd_triples.append({'category': entry['category'], 'text': entry['text'], 'triples': temp_triples})
    with open(output_file, 'a+') as out_file:
        json.dump(wd_triples, out_file)


if __name__ == '__main__':
    convert_webnlg_to_wd('./webnlg_v2_train.json', './webnlg_v2_train_wd.json')
