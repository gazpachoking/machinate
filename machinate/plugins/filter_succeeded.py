import asyncio
import functools

from machinate.node import Node


class FilterSucceeded(Node):
    name = "succeeded"
    inputs = ["in"]
    outputs = ["new", "seen"]
    
    def __init__(self, config):
        # Entries which have succeeded in the past
        self._seen = set()
        # Mapping from entry title to in progress entry
        self._in_progress = {}
        super(FilterSucceeded, self).__init__()

    async def start(self):
        # This would be called by the framework when the task was activated
        while True:
            entry = await self.input("in").get()
            asyncio.ensure_future(self.process_entry(entry))

    async def process_entry(self, entry):
        if entry["title"] in self._in_progress:
            # Wait to see if previous entry was successful before processing another with the same title
            await self._in_progress[entry["title"]].completion

        if self.is_seen(entry):
            await self.output("seen").put(entry)
        else:
            print("new entry: {}".format(entry))
            self._in_progress[entry["title"]] = entry
            await self.output("new").put(entry)
            # Wait for entry to complete and store if it succeeded
            result = await entry.completion
            if result == "success":
                self.add_seen(entry)
            self._in_progress.pop(entry["title"], None)
    
    def is_seen(self, entry):
        return entry["title"] in self._seen
    
    def add_seen(self, entry):
        self._seen.add(entry["title"])
