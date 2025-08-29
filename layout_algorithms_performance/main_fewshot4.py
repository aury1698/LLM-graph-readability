import base64
import json
import os
import random
import re
import time
from mimetypes import guess_type

import pandas as pd
from google.genai import types
from langchain.schema import HumanMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


# 1. Initialize the model
def initialize_model(model_name):
    """Initialize the model based on the model name."""
    if model_name == "gpt-4o":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        return ChatOpenAI(model="gpt-4o")
    elif model_name.startswith("gemini"):
        api_key = os.getenv("GEMINI_API_KEY_SECONDARY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY_SECONDARY is not set in the environment variables."
            )
        return ChatGoogleGenerativeAI(
            model=model_name, temperature=0.1, api_key=api_key
        )
    # add proxied requests to tuwien aqueduct
    elif model_name == "mistral-small-3.1-24b" or model_name == "qwen-32b":
        api_key = os.getenv("AQUEDUCT_KEY")
        return ChatOpenAI(
            model=model_name,
            base_url="https://aqueduct.ai.datalab.tuwien.ac.at",
            api_key=SecretStr(api_key),
        )
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
def create_prompt(model_name, system_msg, user_msg, image_url, few_shots = []):
    content = [{"type": "text", "text": system_msg}]
    content.extend(few_shots)
    content.append({"type": "text", "text": user_msg})
    content.append({"type": "image_url", "image_url": {"url": image_url}})

    return HumanMessage(
        content=content
    )


# 4.Configure the model
def configure_model(model_name, system_msg):
    """Configure the model and return the configuration."""
    return types.GenerateContentConfig(
        temperature=0.1,
        response_mime_type="text/plain",
        system_instruction=[types.Part.from_text(text=system_msg)],
    )


# 5. Invoke the model
def invoke_model(model_name, model, prompt, config=None):
    """Invoke the model with the given prompt."""

    start_time = time.time()
    response = model.invoke([prompt])  # method of the class ChatGoogleGenerativeAI
    end_time = time.time()
    latency = end_time - start_time
    usage_metadata = response.usage_metadata
    input_tokens = usage_metadata["input_tokens"]
    output_tokens = usage_metadata["output_tokens"]
    total_tokens = usage_metadata["total_tokens"]

    metrics = {
        "Response Time": f"{latency:.2f} seconds",
        "Input Tokens": input_tokens,
        "Output Tokens": output_tokens,
        "Total Tokens": total_tokens,
    }

    return response.content, metrics


# 6. Parse the model response
def parse_model_response(response, task):
    if response is None:
        print(f"Warning: response is None for task '{task}'.")
        return None
    if task == "task1_shortest_path_length":
        # Search "Length: X, Path: [A, B, C]"
        match = re.search(r"Length:\s*(\d+),\s*Path:\s*\[([A-Z,\s]+)\]", response)
        if match:
            length = int(match.group(1))
            path = match.group(2).replace(" ", "").split(",")
            return {"prediction": length, "path": path}
        else:
            print(f"Warning: Unable to parse response for task '{task}'.")
            return None

    elif task == "task2_min_nodes_removal":
        # Search "Nodes to remove: [A, B], Cut Set: [C, D]" (it considers the case where the cut set is empty)
        match = re.search(
            r"Nodes to remove:\s*(\d+),\s*Cut Set:\s*\[([\w,\s]*)\]", response
        )
        if match:
            nodes_to_remove = int(match.group(1))

            cut_set_raw = match.group(2).strip()
            # Handle the case where the cut set is empty
            if not cut_set_raw:
                cut_set = []
            else:
                cut_set = cut_set_raw.replace(" ", "").split(",")

            return {"prediction": nodes_to_remove, "cut_set": cut_set}
        else:
            print(f"Warning: Unable to parse response for task '{task}'.")
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

            return {"prediction": edges_to_remove, "cut_set": cut_set}
        else:
            print(f"Warning: Unable to parse response for task '{task}'.")
            return None
    else:
        print(f"Error: Unsupported task '{task}' in parse_model_response.")
        return None


def is_path_correct(predicted_path, ground_truth_paths):
    for gt_path in ground_truth_paths:
        if predicted_path == gt_path or predicted_path == gt_path[::-1]:
            return True
    return False


# 7 Calculate the accuracy
def calculate_accuracy(task, parsed_response, ground_truth):
    ##For now the accuracy only checks whether the number is correct, not if the path/cut set itself is correct
    if task == "task1_shortest_path_length":
        is_correct_length = parsed_response["prediction"] == ground_truth["length"]
        # Decomment the following lines if we want to consider the accuracy of the path as well in the future
        # is_correct_path = (
        #     parsed_response["path"] == ground_truth["path"] or
        #     parsed_response["path"] == ground_truth["path"][::-1]  # To consider the reverse path
        # )
        return 1.0 if is_correct_length else 0.0

    elif task == "task2_min_nodes_removal":
        # Verify that the nodes are the same regardless of the order
        is_correct_nodes = parsed_response["prediction"] == ground_truth["length"]
        return 1.0 if is_correct_nodes else 0.0

    elif task == "task3_min_edges_removal":
        # Verify that the edges are the same regardless of the order and inversion
        is_correct_edges = parsed_response["prediction"] == ground_truth["length"]
        return 1.0 if is_correct_edges else 0.0
    return 0.0


def load_ground_truth(ground_truth_data, image_name):
    try:
        return ground_truth_data[image_name]
    except KeyError as e:
        raise KeyError(
            f"Key error: {e}. Please check the ground truth JSON for image '{image_name}'."
        )


# 8. Compute all metrics
def compute_metrics(task, response, ground_truth, base_metrics=None):
    """
    Compute all metrics, including accuracy, and return them as a dictionary.
    """
    # Initialize the metrics dictionary
    metrics = base_metrics if base_metrics else {}

    # Compare the model response with the ground truth
    parsed_response = parse_model_response(response, task)

    if not parsed_response:
        print(f"Error: Unable to parse the model response for task '{task}'.")
    else:
        accuracy = calculate_accuracy(task, parsed_response, ground_truth)
        metrics["Accuracy"] = accuracy

    return metrics


# 9. Save the metrics to a CSV file
def save_results_to_csv(results, output_file="results.csv"):
    # Check if the output file already exists
    if os.path.exists(output_file):
        # Add new results to the existing file
        existing_results = pd.read_csv(output_file)
        # Filter empty rows
        existing_results = existing_results.dropna(how="all", axis=1)
        results_df = pd.DataFrame(results).dropna(how="all", axis=1)
        results = pd.concat([existing_results, results_df], ignore_index=True)
    else:
        results = pd.DataFrame(results).dropna(how="all", axis=1)

    results.to_csv(output_file, index=False)


# 10. Convert local image to data URL (as required for langchain)
def local_image_to_data_url(image_path):
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = "image/png"  # Default MIME type
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_encoded_data}"


# 11. Get processed images from the CSV file so we can avoid reprocessing them while selecting a random image
def get_processed_images(
    csv_file="results.csv", mode=None, cot_mode=None, attempt=None, model_name=None
):
    """
    Return a set of processed image names for the given configuration.
    """
    if not os.path.exists(csv_file):
        return set()
    df = pd.read_csv(csv_file)
    if "Attempt" in df.columns:
        df["Attempt"] = df["Attempt"].astype(int)
    filters = []
    if mode:
        filters.append(
            df["LLM Mode"] == ("Few-Shot" if mode == "few_shot" else "Zero-Shot")
        )
    if cot_mode:
        filters.append(df["COT Mode"] == ("COT" if cot_mode == "cot" else "No COT"))
    if attempt is not None:
        filters.append(df["Attempt"] == int(attempt))
    if model_name:
        filters.append(df["Model Name"] == model_name)
    if filters:
        mask = filters[0]
        for f in filters[1:]:
            mask &= f
        df = df[mask]
    processed = set(df["Layout"].astype(str))
    return processed


# 12. Pick a random image from the dataset
def pick_random_image_and_task(test_images_dir, processed_images):
    """
    Pick a random image from the test set that has not been processed yet.
    """
    images = [f for f in os.listdir(test_images_dir) if f.endswith(".png")]
    image_names = [os.path.splitext(f)[0] for f in images]
    unprocessed = [f for f in image_names if f not in processed_images]
    if not unprocessed:
        raise ValueError(
            "All images have already been processed for this configuration!"
        )
    chosen_image_name = random.choice(unprocessed)
    chosen_image = chosen_image_name + ".png"
    image_path = os.path.join(test_images_dir, chosen_image)

    # Deduce the task from the file name
    if "_task1_" in chosen_image_name:
        task = "task1_shortest_path_length"
    elif "_task2_" in chosen_image_name:
        task = "task2_min_nodes_removal"
    elif "_task3_" in chosen_image_name:
        task = "task3_min_edges_removal"
    else:
        raise ValueError(f"Cannot deduce task from image name: {chosen_image_name}")

    return image_path, chosen_image_name, task, len(unprocessed)


### NEW FUNCTION ###
def generate_and_create_paths(model_name, mode, cot_mode, attempt):
    """
    Generate paths for results and logs based on parameters,
    and create the destination directory if it doesn't exist.
    """
    # Create the base directory path
    base_dir = os.path.join("results", model_name, mode, cot_mode)

    # Create the directory (does nothing if it already exists)
    os.makedirs(base_dir, exist_ok=True)

    # Define the filenames
    csv_filename = f"results_attempt_{attempt}.csv"
    log_filename = f"log_attempt_{attempt}.txt"

    # Return the full paths
    csv_path = os.path.join(base_dir, csv_filename)
    log_path = os.path.join(base_dir, log_filename)

    return csv_path, log_path

### MODIFIED ###
def main(
    task, mode, cot_mode, model_name, image_path, attempt, output_file_path, log_file_path,
    images_done=None, total_images=None
):
    # Map the task to the corresponding JSON file
    task_files = {
        "task1_shortest_path_length": "tasks/T1_shortest_path_length/task1_shortest_path_length.json",
        "task2_min_nodes_removal": "tasks/T2_nodes_remove/task2_min_nodes_removal.json",
        "task3_min_edges_removal": "tasks/T3_edges_remove/task3_min_edges_removal.json",
    }

    # Load the task data
    task_file = task_files.get(task)
    if not task_file:
        raise ValueError(f"Unsupported task: {task}")
    data = load_task_data(task_file)

    # Load the ground truth file for the current task
    gt_files = {
        "task1_shortest_path_length": "tasks/T1_shortest_path_length/task1_shortest_path_length_gt.json",
        "task2_min_nodes_removal": "tasks/T2_nodes_remove/task2_min_nodes_removal_gt.json",
        "task3_min_edges_removal": "tasks/T3_edges_remove/task3_min_edges_removal_gt.json",
    }

    gt_file = gt_files.get(task)
    if not gt_file:
        raise ValueError(f"Unsupported task: {task}")
    with open(gt_file, "r", encoding="utf-8") as f:
        ground_truth_data = json.load(f)

    # Extract system and user messages based on input mode and cot_mode
    try:
        system_msg = data[task]["prompts"][mode][cot_mode]["system_message"]
        user_msg = data[task]["prompts"][mode][cot_mode]["user_message"]
        examples = data[task]["prompts"][mode][cot_mode].get("examples", [])
    except KeyError as e:
        raise KeyError(
            f"Key error: {e}. Please check the JSON structure for task '{task}', mode '{mode}', and cot_mode '{cot_mode}'."
        )

    # Initialize the model
    model = initialize_model(model_name)

    # Load the desired image
    image_url = local_image_to_data_url(image_path)
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    print(f"Image name: {image_name}")

    config = configure_model(model_name, system_msg)

    # Prepare the examples for "few_shot" mode
    few_shot_prompts = []

    if mode == "few_shot":
        examples_text = (
            "## Examples\n\n"
            "Carefully review the following examples of graph visualizations. "
            "You will receive image-answer pairs. "
            "They demonstrate how you are expected to reason through the task and format your answers. "
            "The real test image will come afterwards.\n\n"
        )

        few_shot_prompts.append({"type": "text", "text": examples_text})

        for example in examples:
            example_image_url = local_image_to_data_url(example["image_path"])

            few_shot_prompts.append({"type": "text", "text": "Example:\nImage:"})
            few_shot_prompts.append({"type": "image_url", "image_url": {"url": example_image_url}})
            few_shot_prompts.append({"type": "text", "text": f"\nAnswer: {example["output"]}\n\n"})

    prompt = create_prompt(model_name, system_msg, user_msg, image_url, few_shot_prompts)

    # Load the ground truth for the current image
    ground_truth = load_ground_truth(ground_truth_data, image_name)
    # Invoke the model and get the response
    try:
        response, base_metrics = invoke_model(model_name, model, prompt, config=config)
        print("\n--- Model Response ---")
        print(response)
        
        ### MODIFIED ###
        # Save the full response to the correct log file
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write("\n" + "="*60 + "\n")
            log_file.write(f"Image name: {image_name}\n")
            log_file.write(f"Task: {task}\n")
            log_file.write(f"Model: {model_name}\n")
            log_file.write(f"Mode: {mode}, COT: {cot_mode}, Attempt: {attempt}\n")
            log_file.write("--- Model Response ---\n")
            log_file.write(f"{response}\n")
            log_file.write("--- Ground Truth ---\n")
            log_file.write(f"{ground_truth}\n")
            if images_done is not None and total_images is not None:
                log_file.write(f"Progress: {images_done}/{total_images} images processed.\n")
            log_file.write("="*60 + "\n")
            
    except Exception as e:
        print(f"Error during model invocation: {e}")
        response = None
        base_metrics = None

    # Evaluate the response by comparing it with the ground truth
    print("\n--- Ground Truth ---")
    print(ground_truth)

    # compute all metrics
    metrics = compute_metrics(task, response, ground_truth, base_metrics)
    
    # Parse the response
    parsed_response = parse_model_response(response, task)

    # Check correctness
    if parsed_response:
        if task == "task1_shortest_path_length":
            correct = (
                parsed_response
                and parsed_response.get("prediction", None) == ground_truth["length"]
            )

        elif task == "task2_min_nodes_removal":
            correct = (
                parsed_response
                and parsed_response.get("prediction", None) == ground_truth["length"]
            )

        elif task == "task3_min_edges_removal":
            correct = (
                parsed_response
                and parsed_response.get("prediction", None) == ground_truth["length"]
            )

        else:
            correct = False  # Default to False for unsupported tasks

        # Collect results
        results = [
            {
                "Task": task,
                "Attempt": attempt,
                "LLM Mode": "Few-Shot" if mode == "few_shot" else "Zero-Shot",
                "COT Mode": "COT" if cot_mode == "cot" else "No COT",
                "Layout": image_name,
                "Model Name": model_name,
                "Temperature": config.temperature
                if hasattr(config, "temperature")
                else None,
                "Prediction": parsed_response.get("prediction", None)
                if parsed_response
                else None,
                "Output": (
                    parsed_response.get("path", None)
                    if (parsed_response and task == "task1_shortest_path_length")
                    else parsed_response.get("cut_set", None)
                    if (
                        parsed_response
                        and task
                        in ["task2_min_nodes_removal", "task3_min_edges_removal"]
                    )
                    else None
                ),
                "True Value": ground_truth["length"],
                "Correct Prediction (True/False)": correct,
                "Time (sec)": base_metrics.get("Response Time", None)
                if base_metrics
                else None,
                "Input Tokens": base_metrics.get("Input Tokens", None)
                if base_metrics
                else None,
                "Output Tokens": base_metrics.get("Output Tokens", None)
                if base_metrics
                else None,
                "Total Tokens": base_metrics.get("Total Tokens", None)
                if base_metrics
                else None,
            }
        ]
    
        save_results_to_csv(results, output_file=output_file_path)


if __name__ == "__main__":
    # Parameters
    test_images_dir = "dataset/test"
    mode = "zero_shot"  # "zero_shot" or "few_shot"
    cot_mode = "cot"  # "no_cot" or "cot"
    model_name = "mistral-small-3.1-24b"
    attempt = 14
    max_images_per_run = 280

    ### MODIFIED ###
    # Dynamically generate paths for the results and log files
    csv_output_file, log_file_path = generate_and_create_paths(
        model_name, mode, cot_mode, attempt
    )
    
    print(f"CSV results will be saved to: {csv_output_file}")
    print(f"Logs will be saved to: {log_file_path}")

    for i in range(max_images_per_run):
        # Use the dynamic CSV path to get the already processed images
        processed_images = get_processed_images(
            csv_file=csv_output_file,
            mode=mode,
            cot_mode=cot_mode,
            attempt=attempt,
            model_name=model_name,
        )
        total_images = len(
            [f for f in os.listdir(test_images_dir) if f.endswith(".png")]
        )
        if len(processed_images) >= total_images:
            print("All images have been processed for this configuration!")
            break
        image_path, image_name, task, remaining = pick_random_image_and_task(
            test_images_dir, processed_images
        )
        images_done = len(processed_images) + 1
        
        # Pass the dynamic paths to the main function
        main(
            task,
            mode,
            cot_mode,
            model_name,
            image_path,
            attempt,
            output_file_path=csv_output_file,
            log_file_path=log_file_path,
            images_done=images_done,
            total_images=total_images,
        )
        print(
            f"\nProgress: {images_done}/{total_images} images processed for mode='{mode}', cot_mode='{cot_mode}', attempt={attempt}, model='{model_name}'."
        )
        print(
            f"\n{total_images - images_done} images remaining for this configuration.\n"
        )