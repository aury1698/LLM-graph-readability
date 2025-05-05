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
def create_prompt(model_name, system_msg, user_msg, file_uri):
    """Create a prompt compatible with the specified model"""
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
def configure_model(model_name, system_msg):
    """Configure the model and return the configuration."""
    if model_name == "gemini-2.5-pro-exp-03-25":
        return types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="text/plain",
            system_instruction=[types.Part.from_text(text=system_msg)],
        )
    elif model_name == "gpt-4o":
        return None  #add config for gpt-4o if needed (need to check the documentation) 
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

#6. Parse the model response
import re

def parse_model_response(response, task):
    if task == "task1_shortest_path_length":
        # Search "Length: X, Path: [A, B, C]"
        match = re.search(r"Length:\s*(\d+),\s*Path:\s*\[([A-Z,\s]+)\]", response)
        if match:
            length = int(match.group(1))
            path = match.group(2).replace(" ", "").split(",")
            return {"length": length, "path": path}
        else:
            print(f"Warning: Unable to parse response for task '{task}'. Response: {response}")
            return None

    elif task == "task2_min_nodes_removal":
        # Search "Nodes to remove: [A, B], Cut Set: [C, D]" (it considers the case where the cut set is empty)
        match = re.search(r"Nodes to remove:\s*(\d+),\s*Cut Set:\s*\[([\w,\s]*)\]", response)
        if match:
            nodes_to_remove = int(match.group(1))

            # Decomment the following lines if we want to consider the accuracy of the cut set as well in the future
            # cut_set_raw = match.group(2).strip()
            # # Handle the case where the cut set is empty
            # if not cut_set_raw:  
            #     cut_set = []
            # else:
            #     cut_set = cut_set_raw.replace(" ", "").split(",")

            return {"nodes_to_remove": nodes_to_remove}
        else:
            print(f"Warning: Unable to parse response for task '{task}'. Response: {response}")
            return None
        
    elif task == "task3_min_edges_removal":
        # Search "Edges to remove: [(A, B), (C, D)], Cut Set: [(E, F), (G, H)]"
        match = re.search(r"Edges to remove:\s*(\d+),\s*Cut Set:\s*\[(.*?)\]", response)
        if match:
            edges_to_remove = int(match.group(1))
            cut_set_raw = match.group(2)
            # Parsing the cut set
            cut_set = []
            for edge in re.findall(r"\(([^)]+)\)", cut_set_raw):
                node1, node2 = edge.replace(" ", "").split(",")
                cut_set.append((node1, node2))
            
            return {"edges_to_remove": edges_to_remove, "cut_set": cut_set}

    else:
        print(f"Error: Unsupported task '{task}' in parse_model_response.")
        return None



def is_path_correct(predicted_path, ground_truth_paths):
    for gt_path in ground_truth_paths:
        if predicted_path == gt_path or predicted_path == gt_path[::-1]:
            return True
    return False


def calculate_accuracy(task, parsed_response, ground_truth):
    ##For now the accuracy only checks whether the number is correct, not if the path/cut set itself is correct
    if task == "task1_shortest_path_length":
        is_correct_length = parsed_response["length"] == ground_truth["length"]
        is_correct_path = (
            parsed_response["path"] == ground_truth["path"] or
            parsed_response["path"] == ground_truth["path"][::-1]  # To consider the reverse path
        )
        return 1.0 if is_correct_length else 0.0
    
    elif task == "task2_min_nodes_removal":
        # Verify that the nodes are the same regardless of the order
        is_correct_nodes = parsed_response["nodes_to_remove"] == ground_truth["length"] 
        return 1.0 if is_correct_nodes else 0.0
    
    elif task == "task3_min_edges_removal":
        # Verify that the edges are the same regardless of the order and inversion
        is_correct_edges = parsed_response["edges_to_remove"] == ground_truth["length"]
        return 1.0 if is_correct_edges else 0.0
    return 0.0


def load_ground_truth(data, task, image_name):
    try:
        return data[task]["ground_truth"][image_name]
    except KeyError as e:
        raise KeyError(f"Key error: {e}. Please check the JSON structure for task '{task}' and image '{image_name}'.")

def compute_metrics(task, response, ground_truth, base_metrics=None):
    """
    Compute all metrics, including accuracy, and return them as a dictionary.
    """
    #Initialize the metrics dictionary
    metrics = base_metrics if base_metrics else {}

    # Compare the model response with the ground truth
    parsed_response = parse_model_response(response, task)


    if not parsed_response:
        print(f"Error: Unable to parse the model response for task '{task}'.")
    else:
        accuracy = calculate_accuracy(task, parsed_response, ground_truth)
        metrics["Accuracy"] = accuracy

    return metrics



def main(task, mode, cot_mode, model_name, image_path):
    
    # Map the task to the corresponding JSON file
    task_files = {
        "task1_shortest_path_length": "tasks/T1_shortest_path_lenght/task1_shortest_path_length.json",
        "task2_min_nodes_removal": "tasks/T2_nodes_remove/task2_min_nodes_removal.json",
        "task3_min_edges_removal": "tasks/T3_edges_remove/task3_min_edges_removal.json",
    }


    # Load the task data
    task_file = task_files.get(task)
    if not task_file:
        raise ValueError(f"Unsupported task: {task}")
    data = load_task_data(task_file)

    # Extract system and user messages based on mode and cot_mode
    try:
        system_msg = data[task]["prompts"][mode][cot_mode]["system_message"]
        user_msg = data[task]["prompts"][mode][cot_mode]["user_message"]
        examples = data[task]["prompts"][mode][cot_mode].get("examples", [])
    except KeyError as e:
        raise KeyError(f"Key error: {e}. Please check the JSON structure for task '{task}', mode '{mode}', and cot_mode '{cot_mode}'.")
        

    # Initialize the model
    model = initialize_model(model_name)

    # Load the desided image
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    uploaded_file = model.files.upload(file=image_path)
    file_uri = uploaded_file.uri
    print(f"Image name: {image_name}")

    
    config = configure_model(model_name, system_msg)

    #TEST: Few Shot Mode
    # Prepare the examples for "few_shot" mode
    examples_text = ""
    if mode == "few_shot" and examples:
        examples_text += (
            "Carefully review the following examples of graph visualizations. "
            "They demonstrate how I expect you to reason through the task and format your answers. "
            "The real test image will come afterward.\n\n"
        )
        for example in examples:
            example_image_path = example["image_path"]
            example_output = example["output"]
            examples_text += f"Example:\nImage: {example_image_path}\nOutput: {example_output}\n\n"

    # Combine examples with the user message
    if mode == "few_shot":
        user_msg = f"{examples_text}{user_msg}"


    print("\n--- System context ---")
    print("\n"+system_msg + "\n")

    print("\n--- User prompt ---")
    print("\n"+user_msg + "\n")

    prompt = create_prompt(model_name, system_msg, user_msg, file_uri)

    # Invoke the model and get the response
    try:
        response, base_metrics = invoke_model(model_name, model, prompt, config=config)
        print("\n--- Model Response ---")
        print(response)
    except Exception as e:
        print(f"Error during model invocation: {e}")


    # Evaluate the response comparing it with the ground truth
    ground_truth = load_ground_truth(data, task, image_name)
    print("\n--- Ground Truth ---")
    print(ground_truth)


    # compute all metrics
    metrics = compute_metrics(task, response, ground_truth, base_metrics)

    print("\n--- Metrics ---")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    


if __name__ == "__main__":
    # Parameters
    task = "task3_min_edges_removal"  # Choose between task1_shortest_path_length, task2_min_nodes_removal, task3_min_edges_removal
    mode = "zero_shot"  # Choose between "zero_shot" and "few_shot"
    cot_mode ="cot" # Choose between "no_cot" and "cot"
    model_name = "gemini-2.5-pro-exp-03-25"  # Change to "gpt-4o" or other models as needed
    image_path = "images_graphs/yellow_version/yellow_test_graphs/Tu.png" # Change to the path of the image you want to test

    main(task, mode, cot_mode, model_name, image_path)