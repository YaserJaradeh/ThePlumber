from consecution import Node, Pipeline, GlobalState
from plumber.nodes.nodes import ExtractionNode, ReadingNode, ResolutionNode, ProcessingNode, WritingNode, LinkingNode, \
    AggregationNode
from plumber.components import StandardReader, OpenIEExtractor, StanfordClient, SpacyNeuralCoreferenceResolver, \
    StandardWriter, EARLJointLinker, DependencyExtractor, FalconJointLinker, StanfordCoreferenceResolver


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
            | ([LinkingNode('Linker 1', EARLJointLinker()), LinkingNode('Linker 2', FalconJointLinker())])
            | AggregationNode('Collector 2')),
           [ResolutionNode('Resolver 1', SpacyNeuralCoreferenceResolver()), ResolutionNode('Resolver 2', StanfordCoreferenceResolver(client))]
           | AggregationNode('Collector 3')]
        | ProcessingNode('Processor')
        | WritingNode('Writer', StandardWriter()),
        global_state=GlobalState(triples=[], caller=None)
    )
    pipe.plot()
    #pipe.consume([1])
    #print(pipe)
    client.__del__()
