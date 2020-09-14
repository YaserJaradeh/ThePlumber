import json
from tqdm import tqdm


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


def convert_webnlg_to_wd(input_file: str, output_file: str):
    pass


if __name__ == '__main__':
    clean_up_webnlg('/home/jaradeh/Downloads/release_v2_json_webnlg_release_v2_train.json', './webnlg_v2_train.json')
