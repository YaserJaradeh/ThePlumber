from functools import lru_cache
from consecution import Node, Pipeline, GlobalState
from os.path import exists
from auko.components import *
from auko.user import *
from auko.discovery import get_classes_map
from typing import Dict, Union, List
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

ALLOWED_KEYS = ['reader', 'writer', 'linker', 'extractor', 'resolver']


class PipelineParser:

    @staticmethod
    @lru_cache(maxsize=128)
    def classes_map():
        return get_classes_map()

    @staticmethod
    def parse(config_file):
        if not exists(config_file):
            raise ValueError(f"Please make sure that this file exists, got {config_file}")
        with open(config_file, 'r') as in_file:
            document = load(in_file, Loader=Loader)
            if not PipelineParser.__check_structure(document):
                raise IOError('Configuration file is not in the correct format!')
            for component_type, component_name in PipelineParser.__get_components(document).items():
                print(PipelineParser.__lookup_class_name(component_name, component_type))

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

    @staticmethod
    def __lookup_class_name(class_name: Union[str, List], component_type: str):
        if component_type not in ALLOWED_KEYS:
            raise ValueError(f'component is not recognized, should be one of {ALLOWED_KEYS}, but got {component_type}')
        if isinstance(class_name, str):
            full_class_name = class_name.replace('_', '').lower().strip() + component_type.lower().strip()
            classes_map = PipelineParser.classes_map()
            keys = [key.replace('_', '').lower().strip() for key in classes_map.keys()]
            return classes_map[list(classes_map.keys())[keys.index(full_class_name)]]
        else:
            results = []
            for name in class_name:
                results.append(PipelineParser.__lookup_class_name(name, component_type))
            return results


    @staticmethod
    def __build_pipeline(components: Dict) -> Pipeline:
        pass


if __name__ == '__main__':
    x = PipelineParser.parse('config.yml')
