import pandas as pd
import glob
import os
import math

# Path to the CSV results. This is critical for accuracy.
BASE_SEARCH_PATH = 'results/mistral-small-3.1-24b'

# Which attempt number to analyze.
TARGET_ATTEMPT = 1 

# OpenAI Model Pricing (Source: https://platform.openai.com/docs/pricing): need to check better
TARGET_MODEL_NAME = "GPT-4o"
MODEL_TEXT_PRICING = {
    "input_cost_per_million": 2.50,
    "output_cost_per_million": 10.00
}

# Image Token Calculation Rules (based on official OpenAI documentation)
# Formula: Total Tokens = BASE_TOKENS + (TOKENS_PER_TILE * num_tiles)
BASE_TOKENS_PER_IMAGE = 85
TOKENS_PER_512PX_TILE = 170

# Currency Conversion (optional)
USD_TO_EUR_RATE = 0.86

# Dimensions of your specific images to calculate costs accurately.
TASK_IMAGE_DIMS = {
    "FD-FR": (1024, 1044), "FD-K": (1024, 957), "PG": (1024, 1160),
    "PGS": (1024, 576), "POGBa": (1024, 685), "POGBb": (1024, 1089),
    "SEIS": (1024, 1132), "Tu": (1024, 657)
}
PRACTICE_IMAGE_DIMS = {
    "Practice_1": (1024, 625), "Practice_2": (1024, 1181), "Practice_3": (1024, 1014),
    "Practice_4": (1024, 946), "Practice_5": (1024, 674), "Practice_6": (1024, 1478)
}
# ---------------------

def calculate_image_cost(width, height):
    """
    Calculates the precise cost of a single image based on OpenAI's full formula.
    """
    # Calculate the number of 512x512 tiles needed to cover the image.
    tiles_wide = math.ceil(width / 512)
    tiles_high = math.ceil(height / 512)
    total_tiles = tiles_wide * tiles_high
    
    # Calculate total tokens for the image using the official formula.
    total_image_tokens = BASE_TOKENS_PER_IMAGE + (total_tiles * TOKENS_PER_512PX_TILE)
    
    # Calculate the final cost in USD based on the input token price.
    cost_per_input_token = MODEL_TEXT_PRICING["input_cost_per_million"] / 1_000_000
    return total_image_tokens * cost_per_input_token

def estimate_openai_multimodal_cost():
    """Analyzes text and image usage to provide the most accurate cost estimate."""

    print("--- Pre-calculating Image Costs Based on Official OpenAI Formula ---")
    task_image_costs = {name: calculate_image_cost(w, h) for name, (w, h) in TASK_IMAGE_DIMS.items()}
    practice_image_costs = {name: calculate_image_cost(w, h) for name, (w, h) in PRACTICE_IMAGE_DIMS.items()}
    
    average_task_image_cost = sum(task_image_costs.values()) / len(task_image_costs)
    total_practice_images_cost = sum(practice_image_costs.values())
    
    print(f"Average cost per single task image: ${average_task_image_cost:.6f}")
    print(f"Total cost for all 6 practice images (used in each few-shot task): ${total_practice_images_cost:.6f}\n")

    # --- Data Loading and Processing ---
    try:
        master_df = pd.concat((pd.read_csv(f) for f in glob.glob(os.path.join(BASE_SEARCH_PATH, '**', '*.csv'), recursive=True)), ignore_index=True)
    except ValueError:
        print(f"Error: No CSV files found in '{BASE_SEARCH_PATH}'. Please check the path.")
        return
        
    attempt_df = master_df[master_df['Attempt'] == TARGET_ATTEMPT].copy()

    if attempt_df.empty:
        print(f"Error: No data found for Attempt #{TARGET_ATTEMPT}.")
        return

    attempt_df['Input Tokens'] = pd.to_numeric(attempt_df['Input Tokens'], errors='coerce').fillna(0)
    attempt_df['Output Tokens'] = pd.to_numeric(attempt_df['Output Tokens'], errors='coerce').fillna(0)
    
    grouped_data = attempt_df.groupby(['LLM Mode', 'COT Mode']).agg(
        TotalInputTokens=('Input Tokens', 'sum'),
        TotalOutputTokens=('Output Tokens', 'sum'),
        TaskCount=('Task', 'count')
    ).reset_index()

    # --- Cost Calculation and Reporting ---
    grand_total_cost = 0.0
    print("--- Cost Estimation Breakdown per Configuration (Text + Vision) ---")

    for _, row in grouped_data.iterrows():
        llm_mode, config_name, task_count = row['LLM Mode'], f"{row['LLM Mode']} / {row['COT Mode']}", row['TaskCount']
        
        text_input_cost = (row['TotalInputTokens'] / 1_000_000) * MODEL_TEXT_PRICING["input_cost_per_million"]
        text_output_cost = (row['TotalOutputTokens'] / 1_000_000) * MODEL_TEXT_PRICING["output_cost_per_million"]
        total_text_cost = text_input_cost + text_output_cost
        
        total_task_images_cost = task_count * average_task_image_cost
        total_few_shot_images_cost = task_count * total_practice_images_cost if llm_mode == 'Few-Shot' else 0
            
        total_image_cost = total_task_images_cost + total_few_shot_images_cost
        total_config_cost = total_text_cost + total_image_cost
        grand_total_cost += total_config_cost
        
        print(f"\nConfiguration: {config_name}")
        print(f"  - Tasks to run: {task_count}")
        print(f"  - Text Cost:      ${total_text_cost:,.4f} (Input: ${text_input_cost:,.4f}, Output: ${text_output_cost:,.4f})")
        print(f"  - Image Cost:     ${total_image_cost:,.4f}")
        if llm_mode == 'Few-Shot':
            print(f"     (Breakdown: ${total_task_images_cost:,.4f} for task images + ${total_few_shot_images_cost:,.4f} for practice images)")
        print(f"  - Estimated Total for Config: ${total_config_cost:,.4f}")

    print("\n" + "="*60)
    print(f"ESTIMATED GRAND TOTAL for one full attempt ({attempt_df.shape[0]} tasks):")
    print(f"${grand_total_cost:.2f} (USD)")
    print(f"≈ €{grand_total_cost * USD_TO_EUR_RATE:.2f} (EUR)")
    print("="*60)

if __name__ == "__main__":
    estimate_openai_multimodal_cost()