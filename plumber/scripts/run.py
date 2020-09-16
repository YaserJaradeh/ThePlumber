import json
import os


def create_directory_structure():
    if not os.path.exists('../results'):
        os.mkdir('../results')
    if not os.path.exists('../results/dbp'):
        os.mkdir('../results/dbp')
    if not os.path.exists('../results/wd'):
        os.mkdir('../results/wd')


def run_webnlg_on_all_dbp_pipelines(webnlg_file: str):
    with open(webnlg_file, 'r') as in_file:
        content = json.load(in_file)



if __name__ == '__main__':
    create_directory_structure()
