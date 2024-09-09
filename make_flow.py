import argparse
import json

parser = argparse.ArgumentParser(description="takes the path for the workflow")
parser.add_argument("-q", "--queue", type=str, help="The path of the workflow")
args = parser.parse_args()

with open(args.queue, "r") as file:
    data = json.load(file)


for node_id, node in data.items():
    if "exposed" in node["_meta"]["title"]:
        print(f"Exposed Nodes : '{node['_meta']['title']}':")
        print(f" Node Id :{node_id}")


"""
print("example processing it")
for node_id, node in data.items():
    if "exposed" in node["_meta"]["title"]:
        node["inputs"]["text"] = "changedinputs"
        print(node["inputs"])
    """

queue_prompt = """
import random
import websocket
import uuid
import json
import urllib.request
import urllib.parse
import requests

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())


def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode("utf-8")
    req = urllib.request.Request(
        "http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen(
        "http://{}/view?{}".format(server_address, url_values)
    ) as response:
        return response.read()


def get_history(prompt_id):
    with urllib.request.urlopen(
        "http://{}/history/{}".format(server_address, prompt_id)
    ) as response:
        return json.loads(response.read())


def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)["prompt_id"]
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message["type"] == "executing":
                data = message["data"]
                if data["node"] is None and data["prompt_id"] == prompt_id:
                    break  # Execution is done
        else:
            continue  # previews are binary data

    history = get_history(prompt_id)[prompt_id]
    for o in history["outputs"]:
        for node_id in history["outputs"]:
            node_output = history["outputs"][node_id]
            if "images" in node_output:
                images_output = []
                for image in node_output["images"]:
                    image_data = get_image(
                        image["filename"], image["subfolder"], image["type"]
                    )
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images


# load workflow from file
with open("workflow_api.json", "r", encoding="utf-8") as f:
    workflow_data = f.read()

workflow = json.loads(workflow_data)

# set the text prompt for our positive CLIPTextEncode
workflow["6"]["inputs"]["text"] = (
    "masterpiece, best quality, perfect man"
)
workflow["7"]["inputs"]["text"] = (
    "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry , deformed,nsfw, deformed legs"
)

ws = websocket.WebSocket()
ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
images = get_images(ws, workflow)

        """

option_prompt_file = input("make a prompt file ? (y/n) :")
if option_prompt_file == "y":
    with open("queue_prompt.py", "w") as file:
        file.write(queue_prompt)
else:
    pass
