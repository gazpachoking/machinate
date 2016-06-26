import asyncio
import datetime

import aiohttp
import feedparser

from machinate.entry import Entry
from machinate.node import Node


class InputRSS(Node):
    name = "rss"
    inputs = []

    def __init__(self, config):
        self.interval = datetime.timedelta(minutes=10)
        self.url = config
        self.session = aiohttp.ClientSession()
        super(InputRSS, self).__init__()

    async def start(self):
        asyncio.ensure_future(self.trigger())

    async def trigger(self):
        response = await self.session.get(self.url)
        if response.status == 200:
            parsed = feedparser.parse(await response.text())
            for item in parsed.entries:
                entry = Entry()
                entry["title"] = item["title"]
                print("created entry {}".format(entry))
                await self.output("out").put(entry)
        #loop.call_later(self.interval.total_seconds(), loop.create_task(self.trigger()))
