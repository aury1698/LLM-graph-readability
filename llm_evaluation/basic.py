import getpass
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage


if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


model = init_chat_model("gpt-4o", model_provider="openai")


messages = [
    SystemMessage("Translate the following from English into Italian. Try to use italian idioms where appropriate."),
    HumanMessage("hi, how are you? The weather is damn cold this week."),
]

resp = model.invoke(messages)
print(resp)
print(resp.content)