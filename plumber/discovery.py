from typing import Dict
import json


class PlumberClass:
    subclasses = []
    map = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)
        name = str(cls)[1:-2]
        key = name[name.rfind('.')+1:]
        cls.map[key] = cls

    def prepare_json_request(self, obj: Dict) -> str:
        return json.dumps(obj).replace('\\n', ' ')


def get_classes_map() -> Dict:
    return PlumberClass.map
