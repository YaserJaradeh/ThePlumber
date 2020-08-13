import bigjson
import bz2
from typing import List


class WikidataDumpReader:

    def __init__(self, dump_file: str):
        self.dump_file = dump_file

    def convert_to_tsv(self, destination_file: str):
        with bz2.open(self.dump_file, "rb") as bzinput:
            with open(destination_file, 'w') as output:
                output.write(f'type\tid\tlabel\tdescription\taliases\n')
                j = bigjson.load(bzinput)
                for index, element in enumerate(j):
                    if index % 1000 == 0:
                        print(f'done up until {index}!')
                    entity_type = self.extract_type(element)
                    entity_id = self.extract_id(element)
                    entity_label = self.extract_label(element)
                    entity_description = self.extract_description(element)
                    entity_aliases = self.extract_aliases(element)
                    try:
                        output.write(f'{entity_type}\t{entity_id}\t{entity_label}\t{entity_description}\t{"|||".join(entity_aliases)}\n')
                    except UnicodeEncodeError:
                        print('skipped!')
                        continue

    @staticmethod
    def extract_type(element) -> str:
        if 'type' in element:
            return element['type']
        return ''

    @staticmethod
    def extract_id(element) -> str:
        if 'id' in element:
            return element['id']
        return ''

    @staticmethod
    def extract_label(element) -> str:
        if 'labels' in element and 'en' in element['labels']:
            return element['labels']['en']['value']
        return ''

    @staticmethod
    def extract_description(element) -> str:
        if 'descriptions' in element and 'en' in element['descriptions']:
            return element['descriptions']['en']['value']
        return ''

    @staticmethod
    def extract_aliases(element) -> List[str]:
        try:
            if 'aliases' in element and 'en' in element['aliases']:
                return list(filter(lambda x: x[:2] != '??', [x['value'].encode('utf-8', 'replace').decode() for x in element['aliases']['en'].to_python()]))
            return []
        except UnicodeEncodeError:
            return []


if __name__ == '__main__':
    reader = WikidataDumpReader('/media/jaradeh/HDD/latest-all.json.bz2')
    reader.convert_to_tsv('./test.tsv')
