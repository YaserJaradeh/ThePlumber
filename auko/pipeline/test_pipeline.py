from consecution import Node, Pipeline, GlobalState
from auko.nodes.nodes import ExtractionNode, ReadingNode, ResolutionNode, ProcessingNode, WritingNode, JointLinkingNode
from auko.components import StandardReader, OpenIEExtractor, StanfordClient, SpacyNeuralCoreferenceResolver, StandardWriter, EARLJointLinker


# This is the same node class we defined above
class LogNode(Node):
    def process(self, item):
        print('{} processing {}'.format(self.name, item))
        self.push(item)


if __name__ == '__main__':
    # Connect nodes with pipe symbols to create pipeline for consuming any iterable.
    client = StanfordClient()
    pipe = Pipeline(
        ReadingNode('Reader', StandardReader())
        | [(ExtractionNode('Extractor', OpenIEExtractor(client)) | JointLinkingNode('Linker', EARLJointLinker())),
           ResolutionNode('Resolution', SpacyNeuralCoreferenceResolver())]
        | ProcessingNode('Processer')
        | WritingNode('Writer', StandardWriter()),
        global_state=GlobalState(triples=[], caller=None)
    )
    pipe.consume([1])
    print(pipe)
    client.__del__()
