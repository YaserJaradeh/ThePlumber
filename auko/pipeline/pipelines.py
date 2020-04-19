from typing import List


class InputOutput(dict):

    def encapsulate(self, obj):
        pass


class PipelineComponent:
    name: str = None
    result: InputOutput = None
    is_done: bool = False

    def __init__(self, name=None):
        self.name = name

    def process(self, func, args: InputOutput):
        output = func(args)
        self.is_done = True
        result = output


class AuKoPipeline:
    components: List[PipelineComponent] = []

    def __init__(self, name):
        self.name = name

    def append(self, component: PipelineComponent):
        self.components.append(component)
        return self

    def run(self) -> InputOutput:
        pass

