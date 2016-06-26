import asyncio
import importlib

from path import Path
import yaml

import machinate.node

nodes = {"null": machinate.node.NullNode(), "success": machinate.node.SuccessNode()}


if __name__ == "__main__":
    for f in Path.joinpath(".", "machinate", "plugins").listdir():
        if f.endswith(".py"):
            importlib.import_module("machinate.plugins." + f.basename()[:-3])
    with open("config.yml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        for n, c in config["nodes"].items():
            nodes[n] = machinate.node.node_types[c["type"]](c.get("config"))
        for n in nodes.values():
            for out in n.outputs:
                n.wire(out, nodes["null"].input("in"))
        for input, output in config["wires"].items():
            in_node_name, in_name = input.split(".")
            out_node_name, out_name = output.split(".")
            nodes[in_node_name].wire(in_name, nodes[out_node_name].input(out_name))
        for n in nodes.values():
            asyncio.ensure_future(n.start())
        asyncio.get_event_loop().run_forever()
