from openai import OpenAI
import os

client = OpenAI(
    base_url="https://aqueduct.ai.datalab.tuwien.ac.at",
    api_key=os.getenv("AQUEDUCT_KEY"),
)

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"


response = client.chat.completions.create(
    model="deepseek-r1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
        }
    ]
)
print(response.choices[0].message.content)
