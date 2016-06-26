import asyncio

from machinate.node import Node

import regex


class FilterRegex(Node):
    name = "regex"
    outputs = ["match", "no match"]
    
    def __init__(self, config):
        self.regex = regex.compile(config, flags=regex.V1)
        super(FilterRegex, self).__init__()

    async def start(self):
        while True:
            entry = await self.input("in").get()
            if self.regex.search(entry["title"]):
                print("{} matched regex".format(entry))
                await self.output("match").put(entry)
            else:
                await self.output("no match").put(entry)
