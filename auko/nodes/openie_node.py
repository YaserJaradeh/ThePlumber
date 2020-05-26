from consecution import Node
from auko.components.clients.stanford import StanfordClient
from typing import List


class OpenIENode(Node):
    def process(self, item):
        print('{} processing {}'.format(self.name, item))
        with StanfordClient() as client:
            text = 'Barack Obama was born in Hawaii.  He was elected president in 2008.'
            self.push(client.openie(text))


class DummyNode(Node):
    def process(self, items: List):
        print('{} processing {}'.format(self.name, items))
        self.push(["this is dummy" for i in items])


class SmartNode(Node):
    def process(self, item):
        print('{} processing {}'.format(self.name, item))
        self.push("this is smart")
