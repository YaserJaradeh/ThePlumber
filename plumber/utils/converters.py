import json
from typing import Dict
from tqdm import tqdm


class EsDumpConverter:
    def __init__(self, es_dump: str):
        self.es_dump = es_dump
        self.content = []

    def to_tsv(self, destination_file: str):
        with open(self.es_dump, 'r') as dump:
            for line in dump.readlines():
                obj = json.loads(line)
                uri = obj['_source']['uri']
                label = obj['_source']['label']
                self.content.append((uri, label))
        dic = self.group_by_uri()
        with open(destination_file, 'w') as output:
            output.write(f'uri\tlabels\n')
            for key, value in dic.items():
                output.write(f'{key}\t{"|||".join(value)}\n')

    def group_by_uri(self) -> Dict:
        result = {}
        for uri, label in self.content:
            result.setdefault(uri.strip().replace('\n', ''), []).append(label.strip().replace('\n', ''))
        return result


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


if __name__ == '__main__':
    clean_up_webnlg('/home/jaradeh/Downloads/release_v2_json_webnlg_release_v2_train.json', './webnlg_v2_train.json')
