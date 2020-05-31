from consecution import Node, Pipeline, GlobalState
from auko.nodes.nodes import ExtractionNode, ReadingNode, ResolutionNode
from auko.components import StandardReader, OpenIEExtractor, StanfordClient, SpacyNeuralCoreferenceResolver


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
        | [ExtractionNode('Extractor', OpenIEExtractor(client)), ResolutionNode('Resolution', SpacyNeuralCoreferenceResolver())]
        | LogNode('Output'),
        global_state=GlobalState(triples=[], caller=None)
    )
    pipe.consume([1])
    print(pipe)
    client.__del__()
