from consecution import Node, Pipeline
from auko.nodes.openie_node import DummyNode, OpenIENode, SmartNode


# This is the same node class we defined above
class LogNode(Node):
    def process(self, item):
        print('{} processing {}'.format(self.name, item))
        self.push(item)


if __name__ == '__main__':
    # Connect nodes with pipe symbols to create pipeline for consuming any iterable.
    pipe = Pipeline(
        OpenIENode('extract') | DummyNode('transform') | SmartNode('load') | LogNode("write")
    )
    pipe.consume([[1,2,3]])
