from functools import lru_cache
from consecution import Pipeline, GlobalState
from os.path import exists
from plumber.components import *
from plumber.user import *
from plumber.discovery import get_classes_map
from typing import Dict, Union, List, Tuple
from yaml import load
from plumber.nodes import ReadingNode, ResolutionNode, AggregationNode, ProcessingNode
from plumber.nodes import ExtractionNode, LinkingNode, WritingNode
from plumber.nodes import LinksAggregationNode, ChainsAggregationNode, TriplesAggregationNode

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

ALLOWED_KEYS = ['reader', 'writer', 'linker', 'extractor', 'resolver']


class PipelineParser:

    @staticmethod
    @lru_cache(maxsize=128)
    def classes_map() -> Dict:
        """
        Lists available AuKo components in the AuKo package and user custom package
        :return: a dictionary of the results (name -> type)
        """
        return get_classes_map()

    @staticmethod
    def parse(config_file) -> Tuple[Pipeline, Dict]:
        """
        Parses the yml file into a fully working auko pipeline
        :param config_file: the path of the yml config file
        :return: pipeline object ready for run
        """
        if not exists(config_file):
            raise ValueError(f"Please make sure that this file exists, got {config_file}")
        with open(config_file, 'r') as in_file:
            document = load(in_file, Loader=Loader)
            if not PipelineParser.__check_structure(document):
                raise IOError('Configuration file is not in the correct format!')
            return PipelineParser.create(document)

    @staticmethod
    def create(config_document: Dict, **kwargs) -> Tuple[Pipeline, Dict]:
        components = PipelineParser.__get_components(config_document)
        params = PipelineParser.__get_parameters(config_document)
        if kwargs is not None:
            params = {**params, **kwargs}
        return PipelineParser.__build_pipeline(components, **params)

    @staticmethod
    def parse_and_run(config_file):
        """
        Creates and runs the pipeline from the yml file with the given path
        :param config_file: the path of the yml file
        """
        pipeline, params = PipelineParser.parse(config_file)
        pipeline.consume([1])
        PipelineParser.clean_up(params)

    @staticmethod
    def clean_up(params: Dict):
        params['stanford_client'].__del__()
        params['ollie_client'].__del__()

    @staticmethod
    def __check_structure(document: Dict) -> bool:
        """
        Checks if the yml file is in the correct format to be parsed
        :param document: the yml document
        :return: True if the structure is ok, false otherwise
        """
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
        """
        Extracts components from the yml file and create the suitable data structure
        :param document: the yml document
        :return: dictionary with component type and it's user specified class
        """
        components = document['pipeline']['components']
        result = {'writer': 'standard', 'reader': 'standard'}
        for key, value in components.items():
            result[key] = value
        return result

    @staticmethod
    def __get_parameters(document: Dict) -> Dict:
        """
        Get the parameters passed by in the yml file
        :param document: the document of the yml file
        :return: returns a dictionary (key, value) of variable name and value
        """
        return document['pipeline']['parameters']

    @staticmethod
    def __lookup_class_name(class_name: Union[str, List], component_type: str) -> Union[
        List[Tuple[type, str]], Tuple[type, str]]:
        """
        Looks up the class name in components dictionary
        :param class_name: the class name (str) or a list of class names (strings)
        :param component_type: the component type to filter lookup
        :return: either a tuple of the type and it's name or a list of the same type
        """
        if component_type not in ALLOWED_KEYS:
            raise ValueError(f'component is not recognized, should be one of {ALLOWED_KEYS}, but got {component_type}')
        if isinstance(class_name, str):
            full_class_name = class_name.replace('_', '').lower().strip() + component_type.lower().strip()
            classes_map = PipelineParser.classes_map()
            keys = [key.replace('_', '').lower().strip() for key in classes_map.keys()]
            return classes_map[list(classes_map.keys())[keys.index(full_class_name)]], class_name
        else:
            results = []
            for name in class_name:
                results.append(PipelineParser.__lookup_class_name(name, component_type))
            return results

    @staticmethod
    def __build_pipeline(components: Dict, **kwargs) -> Tuple[Pipeline, Dict]:
        """
        Builds the pipeline from the list of components
        appends all suitable nodes in the default order
        the pipeline will be of the shape
        |-- reader
        |-- extractor(s)
        |---- Linker(s)
        |-- resolver(s)
        |-- processor
        |-- writer
        :param components: a dictionary of components
        :param kwargs: arguments used throughout the pipeline's life span
        :return: Returns the pipeline object
        """
        names_repo = {}
        # stan = StanfordClient()
        # ollie = OLLIEClient()
        # kwargs['stanford_client'] = stan
        # kwargs['ollie_client'] = ollie
        reader_node = ReadingNode(PipelineParser.__get_name(names_repo, 'reader', components['reader']),
                                  PipelineParser.__lookup_class_name(components['reader'], 'reader')[0](**kwargs))
        main_node = ProcessingNode(PipelineParser.__get_name(names_repo, 'Processor'))
        pipe = Pipeline(reader_node, global_state=GlobalState(triples=[], chains=[], links=[], caller=None))
        ####################################
        resolvers = components['resolver']
        if isinstance(resolvers, list):
            collector_node = ChainsAggregationNode(PipelineParser.__get_name(names_repo, 'resolvers collector'))
            collector_node.add_downstream(main_node)
            types = PipelineParser.__lookup_class_name(components['resolver'], 'resolver')
            for resolver_type in types:
                resolver_node = ResolutionNode(PipelineParser.__get_name(names_repo, 'resolver', resolver_type[1]),
                                               resolver_type[0](**kwargs))
                reader_node.add_downstream(resolver_node)
                resolver_node.add_downstream(collector_node)
        else:
            resolver_node = ResolutionNode(PipelineParser.__get_name(names_repo, 'resolver', components['resolver']),
                                           PipelineParser.__lookup_class_name(components['resolver'], 'resolver')[0](
                                               **kwargs))
            reader_node.add_downstream(resolver_node)
            resolver_node.add_downstream(main_node)
        ####################################
        extractors = components['extractor']
        last_extractor = None
        if isinstance(extractors, list):
            collector_node = TriplesAggregationNode(PipelineParser.__get_name(names_repo, 'extractors collector'))
            types = PipelineParser.__lookup_class_name(components['extractor'], 'extractor')
            for extractor_type in types:
                extractor_node = ExtractionNode(PipelineParser.__get_name(names_repo, 'extractor', extractor_type[1]),
                                                extractor_type[0](**kwargs))
                reader_node.add_downstream(extractor_node)
                extractor_node.add_downstream(collector_node)
            last_extractor = collector_node
        else:
            extractor_node = ExtractionNode(PipelineParser.__get_name(names_repo, 'extractor', components['extractor']),
                                            PipelineParser.__lookup_class_name(components['extractor'], 'extractor')[0]
                                            (**kwargs))
            reader_node.add_downstream(extractor_node)
            last_extractor = extractor_node
        ####################################
        linkers = components['linker']
        last_linker = None
        if isinstance(linkers, list):
            collector_node = LinksAggregationNode(PipelineParser.__get_name(names_repo, 'linkers collector'))
            types = PipelineParser.__lookup_class_name(components['linker'], 'linker')
            for linker_type in types:
                linker_node = LinkingNode(PipelineParser.__get_name(names_repo, 'linker', linker_type[1]),
                                          linker_type[0](**kwargs))
                last_extractor.add_downstream(linker_node)
                linker_node.add_downstream(collector_node)
            last_linker = collector_node
        else:
            linker_node = LinkingNode(PipelineParser.__get_name(names_repo, 'linker', components['linker']),
                                      PipelineParser.__lookup_class_name(components['linker'], 'linker')[0](**kwargs))
            last_extractor.add_downstream(linker_node)
            last_linker = linker_node
        last_linker.add_downstream(main_node)
        ####################################
        writer = WritingNode(PipelineParser.__get_name(names_repo, 'writer', components['writer']),
                             PipelineParser.__lookup_class_name(components['writer'], 'writer')[0](**kwargs))
        main_node.add_downstream(writer)
        return pipe, kwargs

    @staticmethod
    def __get_name(repo: Dict, node_type: str, postfix: str = None):
        """
        Create a unique name for a node in the pipeline
        :param repo: the repo where the numbers are appended from
        :param node_type: the type of the node used to create the name
        :param postfix: a postfix (optional) can be used to add more info to the name of the node
        :return: returns a string which is the name of the node
        """
        if node_type in repo:
            counter = repo[node_type] + 1
            repo[node_type] = counter
            return f'{node_type} {counter}' + (f' ({postfix})' if postfix is not None else '')
        else:
            repo[node_type] = 1
            return f'{node_type} 1' + (f' ({postfix})' if postfix is not None else '')


if __name__ == '__main__':
    #pipe = PipelineParser.parse('config.yml')
    #pipe.plot()
    resources = ["R12220", "R12223", "R12226", "R12231", "R12233", "R12235", "R12237", "R12241", "R12243", "R12245", "R12247", "R25005", "R36109", "R36114", "R36123", "R36138", "R36151", "R37001", "R37003", "R37006", "R37008"]
    config = {
        "pipeline": {
            "name": "test",
            "components": {
                "extractor": "user",
                "linker": "dummy",
                "resolver": "dummy",
                "reader": "raw_file",
                "writer": "file"
            },
            "parameters": {
                "input_file": './text/R36138.txt',
                "output_file": './text/R36138-triples.txt'
            }
        }
    }
    for resource in resources:
        config["pipeline"]["parameters"]["input_file"] = f"./text/{resource}.txt"
        config["pipeline"]["parameters"]["output_file"] = f"./text/{resource}-triples.txt"
        pipeline, params = PipelineParser.create(config)
        pipeline.consume([1])
        PipelineParser.clean_up(params)

