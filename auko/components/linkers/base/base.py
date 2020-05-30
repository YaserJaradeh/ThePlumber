from auko.components.format import Triple, Pair
from typing import List


class BaseEntityLinker:
    """
    Base entity linking class, other entity linkers will inherit this one
    """
    def __init__(self, name: str = 'Base Entity Linker'):
        self.name = name

    def get_entities(self, text: str):
        pass


class BaseRelationLinker:
    """
    Base relation linking class, other relation linkers will inherit this one
    """
    def __init__(self, name: str = 'Base Relation Linker'):
        self.name = name

    def get_relations(self, text: str):
        pass


class BaseJointLinker:
    """
    Base joint linking class, other joint linkers will inherit this one
    """
    def __init__(self, name: str = 'Base Joint (relation and entity) Linker'):
        self.name = name

    def get_entities_and_relations(self, text: str):
        pass
