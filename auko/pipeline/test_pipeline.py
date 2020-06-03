from consecution import Node, Pipeline, GlobalState
from auko.nodes.nodes import ExtractionNode, ReadingNode, ResolutionNode, ProcessingNode, WritingNode, JointLinkingNode, \
    AggregationNode
from auko.components import StandardReader, OpenIEExtractor, StanfordClient, SpacyNeuralCoreferenceResolver, \
    StandardWriter, EARLJointLinker, DependencyExtractor, FalconJointLinker


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
        | [([ExtractionNode('Extractor 1', OpenIEExtractor(client)),
             ExtractionNode('Extractor 2', DependencyExtractor(client))]
            | AggregationNode('Collector 1')
            | ([JointLinkingNode('Linker 1', EARLJointLinker()), JointLinkingNode('Linker 2', FalconJointLinker())])
            | AggregationNode('Collector 2')),
           ResolutionNode('Resolver', SpacyNeuralCoreferenceResolver())]
        | ProcessingNode('Processor')
        | WritingNode('Writer', StandardWriter()),
        global_state=GlobalState(triples=[], caller=None)
    )
    pipe.consume([1])
    print(pipe)
    client.__del__()
