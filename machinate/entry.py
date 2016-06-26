import asyncio
import functools


class Entry(object):
    def __init__(self):
        self._store = {}
        self._complete = asyncio.Future()

    def __getitem__(self, item):
        return self._store[item]

    def __setitem__(self, key, value):
        self._store[key] = value

    @property
    def completion(self):
        return self._complete

    def on_complete(self, func):
        self._complete.add_done_callback(lambda f,: func(self, f.result()))

    def succeed(self):
        self._complete.set_result("success")

    def fail(self):
        self._complete.set_result("failure")

    def ignore(self):
        self._complete.set_result("ignored")

    def __repr__(self):
        return "<Entry({})>".format(repr(self._store))
