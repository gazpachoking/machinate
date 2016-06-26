import asyncio


node_types = {}


class NodeType(type):
    def __init__(cls, name, bases, nmspc):
        if hasattr(cls, "name"):
            node_types[cls.name] = cls
        super(NodeType, cls).__init__(name, bases, nmspc)


class Node(metaclass=NodeType):
    inputs = ["in"]
    outputs = ["out"]

    def __init__(self, config=None):
        self._input_queues = {name: asyncio.Queue() for name in self.inputs}
        self._output_queues = {}

    def wire(self, out, queue):
        self._output_queues[out] = queue

    def input(self, name):
        return self._input_queues[name]

    def output(self, name):
        return self._output_queues[name]


class NullNode(Node):
    name = "null"
    out = []

    async def start(self):
        while True:
            entry = await self.input("in").get()
            entry.ignore()
            print("nullified entry {}".format(entry))


class SuccessNode(Node):
    name = "success"
    out = []

    async def start(self):
        while True:
            entry = await self.input("in").get()
            entry.succeed()
            print("succeeded entry {}".format(entry))
