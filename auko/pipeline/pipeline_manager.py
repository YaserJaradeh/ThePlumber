from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from consecution import Node, Pipeline, GlobalState
from os.path import exists
from auko import AuKoClass
from auko.components import *
from auko.user import *
from auko.discovery import get_classes_map
import os


class PipelineParser:

    def parse(self, config_file):
        if not exists(config_file):
            raise ValueError(f"Please make sure that this file exists, got {config_file}")
        with open(config_file, 'r') as in_file:
            document = load(in_file, Loader=Loader)
            return document


if __name__ == '__main__':
    parser = PipelineParser()
    x = parser.parse('config.yml')
    x = get_classes_map()
