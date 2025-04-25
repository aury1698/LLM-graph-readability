import base64
import json
import os
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from google import genai
from google.genai import types


# 1. Initialize the model
def initialize_model(model_name):
    """Initialize the model based on the model name."""
    if model_name == "gpt-4o":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        return ChatOpenAI(model="gpt-4o")
    elif model_name == "gemini-2.5-pro-exp-03-25":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
        return genai.Client(api_key=api_key)
    else:
        raise ValueError(f"Unsupported model: {model_name}")


# 2. Load the json file
def load_task_data(task_file):
    """Load task data from a JSON file."""
    try:
        with open(task_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Task file not found: {task_file}")


# 3. Create the prompt
def create_prompt(model_name, system_msg, user_msg, file_uri, mode):
    """Create a prompt compatible with the specified model and mode."""
    if model_name == "gpt-4o":
        return HumanMessage(
            content=[
                {"type": "text", "text": system_msg},
                {"type": "text", "text": user_msg},
                {"type": "image_url", "image_url": {"url": file_uri}},
            ]
        )
    elif model_name == "gemini-2.5-pro-exp-03-25":
        combined_message = f"{system_msg}\n\n{user_msg}"
        return [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=combined_message),
                    types.Part.from_uri(file_uri=file_uri, mime_type="image/png"),
                ],
            ),
        ]
    else:
        raise ValueError(f"Unsupported model: {model_name}")


# 4.Configure the model
def configure_model(model_name, system_msg, mode):
    """Configure the model based on the mode and system message."""
    if model_name == "gemini-2.5-pro-exp-03-25":
        return types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="text/plain",
            system_instruction=[types.Part.from_text(text=system_msg)],
        )
    elif model_name == "gpt-4o":
        return None  # GPT-4o non richiede configurazioni aggiuntive
    else:
        raise ValueError(f"Unsupported model: {model_name}")


# 5. Invoke the model
def invoke_model(model_name, model, prompt, config=None):
    """Invoke the model with the given prompt."""
    if model_name == "gpt-4o":
        response = model.invoke([prompt])
        return response.content, None
    elif model_name == "gemini-2.5-pro-exp-03-25":
        start_time = time.time()
        response = model.models.generate_content(
            model="gemini-2.5-pro-exp-03-25", contents=prompt, config=config
        )
        end_time = time.time()
        latency = end_time - start_time

        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count
        total_tokens = input_tokens + output_tokens

        metrics = {
            "Response Time": f"{latency:.2f} seconds",
            "Input Tokens": input_tokens,
            "Output Tokens": output_tokens,
            "Total Tokens": total_tokens,
        }

        return response.text, metrics
    else:
        raise ValueError(f"Unsupported model: {model_name}")


# 6. Main function
def main(task, mode, cot_mode, model_name):
    
    # Map the task to the corresponding JSON file
    task_files = {
        "task1_shortest_path_length": "tasks/T1_shortest_path_lenght/task1_shortest_path_length.json",
        "task2_min_nodes_removal": "tasks/T2_nodes_remove/task2_min_nodes_removal.json",
        "task3_min_edges_removal": "tasks/T3_edges_remove/task3_min_edges_removal.json",
    }


    # Carica i dati del task
    task_file = task_files.get(task)
    if not task_file:
        raise ValueError(f"Unsupported task: {task}")
    data = load_task_data(task_file)

    # Extract system and user messages based on mode and cot_mode
    try:
        system_msg = data[task]["prompts"][mode][cot_mode]["system_message"]
        user_msg = data[task]["prompts"][mode][cot_mode]["user_message"]
    except KeyError as e:
        raise KeyError(f"Key error: {e}. Please check the JSON structure for task '{task}', mode '{mode}', and cot_mode '{cot_mode}'.")
        

    # Initialize the model
    model = initialize_model(model_name)

    # Load the desided image
    image_path = "images_graphs/yellow_test_graphs/FD-FR.png"
    uploaded_file = model.files.upload(file=image_path)
    file_uri = uploaded_file.uri
    

    
    config = configure_model(model_name, system_msg, mode)

    print("\n--- System context ---")
    print("\n"+system_msg + "\n")


    print("\n--- User prompt ---")
    print("\n"+user_msg + "\n")

    prompt = create_prompt(model_name, system_msg, user_msg, file_uri, mode)


    # Invoke the model and get the response
    try:
        response, metrics = invoke_model(model_name, model, prompt, config=config)
        print("\n--- Model Response ---")
        print(response)

        # print metrics 
        if metrics:
            print("\n--- Metrics ---")
            for key, value in metrics.items():
                print(f"{key}: {value}")
    except Exception as e:
        print(f"Error during model invocation: {e}")


if __name__ == "__main__":
    # Parameters
    task = "task1_shortest_path_length"  # Choose between task1_shortest_path_length, task2_min_nodes_removal, task3_min_edges_removal
    mode = "zero_shot"  # Choose between "zero_shot" and "few_shot"
    cot_mode ="cot" # Choose between "no_cot" and "cot"
    model_name = "gemini-2.5-pro-exp-03-25"  # Change to "gpt-4o" or other models as needed
    
    main(task, mode, cot_mode, model_name)