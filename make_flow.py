import json

with open("example_api.json", "r") as file:
    data = json.load(file)


for node_id, node in data.items():
    if "exposed" in node["_meta"]["title"]:
        print(f"Exposed Nodes : '{node['_meta']['title']}':")
        print(node["inputs"])


"""
print("example processing it")
for node_id, node in data.items():
    if "exposed" in node["_meta"]["title"]:
        node["inputs"]["text"] = "changedinputs"
        print(node["inputs"])
    """
