from functools import lru_cache
from consecution import Node, Pipeline, GlobalState
from os.path import exists
from auko.components import *
from auko.user import *
from auko.discovery import get_classes_map
from typing import Dict, Union, List
from yaml import load
from auko.nodes import ReadingNode, ResolutionNode, AggregationNode, ProcessingNode, ExtractionNode, Lin

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
            return PipelineParser.__build_pipeline(PipelineParser.__get_components(document))

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
        stan = StanfordClient()
        kwargs = {'stanford_client': stan}
        reader_node = ReadingNode('reader', PipelineParser.__lookup_class_name(components['reader'], 'reader')())
        main_node = ProcessingNode('CPU')
        pipe = Pipeline(reader_node, global_state=GlobalState(triples=[], caller=None))
        ####################################
        resolvers = components['resolver']
        if isinstance(resolvers, list):
            collector_node = AggregationNode('resolvers collector')
            collector_node.add_downstream(main_node)
            types = PipelineParser.__lookup_class_name(components['resolver'], 'resolver')
            for resolver_type in types:
                resolver_node = ResolutionNode('resolver', resolver_type())
                reader_node.add_downstream(resolver_node)
                resolver_node.add_downstream(collector_node)
        else:
            resolver_node = ResolutionNode('resolver',
                                           PipelineParser.__lookup_class_name(components['resolver'], 'resolver')())
            reader_node.add_downstream(resolver_node)
            resolver_node.add_downstream(main_node)
        ####################################
        extractors = components['extractor']
        if isinstance(extractors, list):
            collector_node = AggregationNode('extractors collector')
            collector_node.add_downstream(main_node)
            types = PipelineParser.__lookup_class_name(components['extractor'], 'extractor')
            for extractor_type in types:
                extractor_node = ExtractionNode('extractor', extractor_type(**kwargs))
                reader_node.add_downstream(extractor_node)
                extractor_node.add_downstream(collector_node)
        else:
            extractor_node = ExtractionNode('extractor',
                                            PipelineParser.__lookup_class_name(components['extractor'], 'extractor')(**kwargs))
            reader_node.add_downstream(extractor_node)
        ####################################
        linkers = components['linker']
        if isinstance(linkers, list):
            collector_node = AggregationNode('extractors collector')
            collector_node.add_downstream(main_node)
            types = PipelineParser.__lookup_class_name(components['extractor'], 'extractor')
            for extractor_type in types:
                extractor_node = ExtractionNode('extractor', extractor_type(**kwargs))
                reader_node.add_downstream(extractor_node)
                extractor_node.add_downstream(collector_node)
        else:
            extractor_node = ExtractionNode('extractor',
                                            PipelineParser.__lookup_class_name(components['extractor'], 'extractor')(
                                                **kwargs))
            reader_node.add_downstream(extractor_node)
        ####################################
        return pipe


if __name__ == '__main__':
    x = PipelineParser.parse('config.yml')
    x.plot()
