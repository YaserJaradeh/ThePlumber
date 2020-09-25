from itertools import combinations
from typing import List

extractors = ['ClausIE', 'Dependency', 'Graphene', 'KBP', 'MinIE', 'Ollie', 'OpenIE', 'POS', 'ReVerb']
resolvers = ['StanfordCoreference', 'SpacyNeuralCoreference', 'HMTL']
dbp_linkers = ['MeaningCloudEntity', 'DBpediaSpotlightEntity', 'TagMeEntity',
           'TextRazorDBpedia', 'EARLJoint', 'ESFalconDBpediaJoint', 'ESEarlDBpediaJoint',
           'ESTagMeDBpediaJoint', 'FalconDBpediaJoint', 'DBpediaSpacyANNJoint']
wd_linkers = ['AmbiverseEntity', 'OpenTapiocaEntity', 'TextRazorWikidata', 'ESFalconWikidataJoint', 'ESEarlWikidataJoint',
              'ESTagMeWikidataJoint', 'FalconWikidataJoint', 'WikidataSpacyANNJoint']


def __choose_linkers_list(kg: str):
    if kg == 'dbp':
        return dbp_linkers
    else:
        return wd_linkers


def __get_components_recursive(ext_count: int, res_count: int, link_count: int, pipelines: List, kg):
    # print(f'depth now is: TE={ext_count}, CR={res_count}, EL/RL={link_count}'
    linkers = __choose_linkers_list(kg)
    if ext_count > len(extractors):
        return pipelines
    if res_count > len(resolvers):
        return __get_components_recursive(ext_count + 1, 1, 1, pipelines, kg)
    if link_count > len(linkers):
        return __get_components_recursive(ext_count, res_count + 1, 1, pipelines, kg)
    current_extractors = tuple(combinations(extractors, ext_count))
    current_resolvers = tuple(combinations(resolvers, res_count))
    current_linkers = tuple(combinations(linkers, link_count))
    for extractor_set in current_extractors:
        for resolver_set in current_resolvers:
            for linker_set in current_linkers:
                # print(f'depth now is: TE={extractor_set}, CR={resolver_set}, EL/RL={linker_set}')
                pipelines.append((extractor_set, resolver_set, linker_set))
    return __get_components_recursive(ext_count, res_count, link_count + 1, pipelines, kg)


def generate_all_possible_pipelines(kg: str):
    print(f'Generating Pipelines for {kg}!')
    pipes = __get_components_recursive(1, 1, 1, [], kg)
    print(f'Writing Pipelines for {kg}!')
    with open(f'pipelines-{kg}.tsv', 'a+') as out_file:
        out_file.write(f'Number\tExtractors\tResolvers\tLinkers\n')
        for index, pipe in enumerate(pipes):
            out_file.write(f'{index}\t{",".join(pipe[0])}\t{",".join(pipe[1])}\t{",".join(pipe[2])}\n')


def generate_single_pipelines(kg: str):
    print(f'Generating Single Pipelines for {kg}!')
    pipes = []
    linkers = __choose_linkers_list(kg)
    for extractor in extractors:
        for resolver in resolvers:
            for linker in linkers:
                pipes.append((extractor, resolver, linker))
    print(f'Writing Single Pipelines for {kg}!')
    with open(f'pipelines-single-{kg}.tsv', 'a+') as out_file:
        out_file.write(f'Number\tExtractors\tResolvers\tLinkers\n')
        for index, pipe in enumerate(pipes):
            out_file.write(f'{index}\t{pipe[0]}\t{pipe[1]}\t{pipe[2]}\n')


def generate_distil_pipelines(distil_extractors, distil_resolvers, distil_linkers):
    print(f'Generating distil pipelines!')
    pipes = []
    for extractor in distil_extractors:
        for resolver in distil_resolvers:
            for linker in distil_linkers:
                pipes.append((extractor, resolver, linker))
    print(f'Writing distil pipelines!')
    with open(f'pipelines-distil.tsv', 'a+') as out_file:
        out_file.write(f'Number\tExtractors\tResolvers\tLinkers\n')
        for index, pipe in enumerate(pipes):
            out_file.write(f'{index}\t{pipe[0]}\t{pipe[1]}\t{pipe[2]}\n')


if __name__ == '__main__':
    # generate_all_possible_pipelines('dbp')
    # generate_all_possible_pipelines('wd')
    ###############################
    # generate_single_pipelines('dbp')
    # generate_single_pipelines('wd')
    ###############################
    distil_extractors = ['Graphene', 'ClausIE', 'Ollie', 'OpenIE']
    distil_resolvers = ['StanfordCoreference', 'HMTL']
    distil_linkers = ['EARLJoint', 'ESFalconDBpediaJoint', 'FalconDBpediaJoint', 'DBpediaSpacyANNJoint']
    generate_distil_pipelines(distil_extractors, distil_resolvers, distil_linkers)
