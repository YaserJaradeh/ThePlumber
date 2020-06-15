from typing import List, Tuple
from auko.discovery import AuKoClass


class BaseEntityLinker(AuKoClass):
    """
    Base entity linking class, other entity linkers will inherit this one
    """
    def __init__(self, name: str = 'Base Entity Linker', **kwargs):
        self.name = name

    def get_entities(self, text: str) -> List[Tuple[str, str]]:
        pass


class BaseRelationLinker(AuKoClass):
    """
    Base relation linking class, other relation linkers will inherit this one
    """
    def __init__(self, name: str = 'Base Relation Linker', **kwargs):
        self.name = name

    def get_relations(self, text: str) -> List[Tuple[str, str]]:
        pass


class BaseJointLinker(AuKoClass):
    """
    Base joint linking class, other joint linkers will inherit this one
    """
    def __init__(self, name: str = 'Base Joint (relation and entity) Linker', **kwargs):
        self.name = name

    def get_entities_and_relations(self, text: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        pass


class DummyLinker(AuKoClass):
    """
    Dummy Linker used for testing purposes or to fill space in the pipeline
    """

    def __init__(self, name: str = 'Dummy Linker', **kwargs):
        self.name = name

    def get_entities_and_relations(self, text: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        return [], []

    def get_relations(self, text: str) -> List[Tuple[str, str]]:
        return []

    def get_entities(self, text: str) -> List[Tuple[str, str]]:
        return []
