from typing import Dict


class AuKoClass:
    subclasses = []
    map = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)
        name = str(cls)[1:-2]
        key = name[name.rfind('.')+1:]
        cls.map[key] = cls


def get_classes_map() -> Dict:
    return AuKoClass.map
