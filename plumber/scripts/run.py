import json
import os
from tqdm import tqdm
from plumber.pipeline.pipeline_manager import PipelineParser
from plumber.components import *
import multiprocessing as mp
from functools import partial


def create_directory_structure():
    if not os.path.exists('../results'):
        os.mkdir('../results')
    if not os.path.exists('../results/dbp'):
        os.mkdir('../results/dbp')
    if not os.path.exists('../results/wd'):
        os.mkdir('../results/wd')

kwargs = {}
stan = StanfordClient()
ollie = OLLIEClient()
kwargs['stanford_client'] = stan
kwargs['ollie_client'] = ollie


def run_webnlg_on_pipelines(pipelines_file: str, webnlg_file: str):
    pool = mp.Pool(mp.cpu_count()-2)
    with open(pipelines_file, 'r') as pipe_file:
        pipes = [pipe.strip().split('\t') for idx, pipe in enumerate(pipe_file) if idx > 0]
        print(pipes[:10])
        pool.map(partial(run_dbp_pipeline, webnlg_file=webnlg_file), pipes)
        pool.close()
        # for index, line in enumerate(tqdm(pipe_file)):
        #     if index == 0:
        #         continue
        #     run_dbp_pipeline(dataset, kwargs, line)
    PipelineParser.clean_up(kwargs)


def run_webnlg_on_all_single_dbp_pipelines(webnlg_file: str):
    run_webnlg_on_pipelines('pipelines-single-dbp.tsv', webnlg_file)


def run_dbp_pipeline(parts, webnlg_file):
    # print(line)
    # parts = line.strip().split('\t')
    if not os.path.exists('../results/dbp/plumber'):
        os.mkdir('../results/dbp/plumber')
    output_file_path = f'../results/dbp/plumber/pipeline-{parts[0]}.tsv'
    if os.path.exists(output_file_path):
        return
    with open(output_file_path, 'a+'):
        with open(webnlg_file, 'r') as in_file:
            dataset = json.load(in_file)
            for entry in tqdm(dataset):
                config = {
                    "pipeline": {
                        "name": "dbp-pipeline-" + str(parts[0]),
                        "components": {
                            "extractor": parts[1].split(',') if len(parts[1].split(',')) > 0 else parts[1],
                            "linker": parts[3].split(',') if len(parts[3].split(',')) > 0 else parts[3],
                            "resolver": parts[2].split(',') if len(parts[2].split(',')) > 0 else parts[2],
                            "reader": "feed",
                            "writer": "append_tsv"
                        },
                        "parameters": {
                            "content": entry['text'],
                            "output_tsv": output_file_path
                        }
                    }
                }
                pipeline, params = PipelineParser.create(config, **kwargs)
                pipeline.consume([1])


if __name__ == '__main__':
    # create_directory_structure()
    # run_webnlg_on_all_single_dbp_pipelines('../datasets/WebNLG/webnlg_v2_test.json')
    run_webnlg_on_pipelines('pipelines-dbp-distil.tsv', '../datasets/WebNLG/webnlg_v2_train.json')
