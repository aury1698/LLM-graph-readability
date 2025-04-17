import getpass
import base64
import os
from prompts import GRAPH_SYSTEM_PROMPT, GRAPH_E_TO_I_USER_PROMPT
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


model = init_chat_model("gpt-4o", model_provider="openai")

image_path = "dataset_png/o-.png"
base64_encoded_image = encode_image(image_path)

# https://platform.openai.com/docs/guides/images?api-mode=responses&format=base64-encoded
# https://github.com/langchain-ai/langchain/discussions/17631

messages = [
    SystemMessage(GRAPH_SYSTEM_PROMPT),
    HumanMessage(
        content=[
            {
                "type": "text",
                "text": f"{GRAPH_E_TO_I_USER_PROMPT}",
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_encoded_image}",
                    "detail": "high",
                },
            },
        ]
    ),
]

resp = model.invoke(messages)
print(resp)
print(resp.content)
