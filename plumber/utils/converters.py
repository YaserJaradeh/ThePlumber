import json
from typing import Dict


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
