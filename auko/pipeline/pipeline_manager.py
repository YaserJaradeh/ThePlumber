from consecution import Node, Pipeline, GlobalState
from os.path import exists
from auko.components import *
from auko.user import *
from auko.discovery import get_classes_map
from typing import Dict
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


ALLOWED_KEYS = ['reader', 'writer', 'linker', 'extractor', 'resolver']


class PipelineParser:

    @staticmethod
    def parse(config_file):
        if not exists(config_file):
            raise ValueError(f"Please make sure that this file exists, got {config_file}")
        with open(config_file, 'r') as in_file:
            document = load(in_file, Loader=Loader)
            if not PipelineParser.__check_structure(document):
                raise IOError('Configuration file is not in the correct format!')
            return PipelineParser.__get_components(document)

    @staticmethod
    def __check_structure(document: Dict) -> bool:
        if 'pipeline' not in document:
            return False
        if 'components' not in document['pipeline']:
            return False
        components = document['pipeline']['components']
        if 'extractor' not in components or 'linker' not in components or 'resolver' not in components:
            return False
        if not all(key in ALLOWED_KEYS for key in components.keys()):
            return False
        return True

    @staticmethod
    def __get_components(document: Dict) -> Dict:
        components = document['pipeline']['components']
        result = {'writer': 'standard', 'reader': 'standard'}
        for key, value in components.items():
            result[key] = value
        return result


if __name__ == '__main__':
    x = PipelineParser.parse('config.yml')
