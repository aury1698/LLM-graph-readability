import pandas as pd
import glob
import os
import math

# --- CONFIGURATION ---

BASE_SEARCH_PATH = '../layout_algorithms_performance/results/mistral-small-3.1-24b'
TASKS_PER_CONFIGURATION = 280   # Tasks per configuration
NUM_CONFIGURATIONS = 4          # Configurations tested (e.g., cot/no_cot * zero/few_shot)
TARGET_COMPUTE_DAYS = 7         # Total compute budget in days
# ---------------------

# --- COLORS (ANSI escape codes) ---
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def analyze_experiment_progress():
    """
    Recursively analyzes CSV files to calculate compute time usage,
    average time per task, and estimate feasible reruns within a target budget.
    """
    
    all_time_values = []
    search_pattern = os.path.join(BASE_SEARCH_PATH, '**', '*.csv')
    
    print(f"{Colors.HEADER}{Colors.BOLD}>>> Starting experiment progress analysis...{Colors.RESET}\n")
    print(f"Searching recursively in: {Colors.CYAN}{os.path.abspath(BASE_SEARCH_PATH)}{Colors.RESET}\n")
    
    csv_file_paths = glob.glob(search_pattern, recursive=True)
    csv_file_paths = [path for path in csv_file_paths if 'venv' not in path and '.venv' not in path]

    if not csv_file_paths:
        print(f"{Colors.RED}Error: No CSV files found in the specified path.{Colors.RESET}")
        return

    print(f"Discovered {Colors.GREEN}{len(csv_file_paths)}{Colors.RESET} CSV file(s). Processing...\n")

    for file_path in csv_file_paths:
        try:
            df = pd.read_csv(file_path)
            
            # Do not consider attempt 20 to not surpass the 7 days budget
            if 'Attempt' in df.columns:
                df = df[df['Attempt'] != 20]

            if 'Time (sec)' in df.columns:
                numeric_strings = df['Time (sec)'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
                numeric_times = pd.to_numeric(numeric_strings, errors='coerce')
                valid_times = numeric_times.dropna()
                all_time_values.extend(valid_times.tolist())
            else:
                print(f"{Colors.YELLOW}Warning: Column 'Time (sec)' not found in {file_path}{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.RED}Error processing {os.path.basename(file_path)}: {e}{Colors.RESET}")

    if all_time_values:
        # --- CALCULATIONS ---
        average_time_sec = sum(all_time_values) / len(all_time_values)
        total_time_spent_sec = sum(all_time_values)
        target_total_time_sec = TARGET_COMPUTE_DAYS * 24 * 60 * 60
        remaining_time_sec = target_total_time_sec - total_time_spent_sec

        total_tasks_per_rerun = TASKS_PER_CONFIGURATION * NUM_CONFIGURATIONS
        estimated_time_per_rerun_sec = average_time_sec * total_tasks_per_rerun
        total_achievable_attempts = target_total_time_sec / estimated_time_per_rerun_sec

        # --- OUTPUT ---
        print(f"\n{Colors.BOLD}{Colors.HEADER}--- Compute Time Analysis Complete ---{Colors.RESET}\n")
        
        print(f"{Colors.BOLD}[ Current Status ]{Colors.RESET}")
        print(f" • Files analyzed: {Colors.GREEN}{len(csv_file_paths)}{Colors.RESET}")
        print(f" • Total tasks executed: {Colors.GREEN}{len(all_time_values)}{Colors.RESET}")
        print(f" • Compute time used: {Colors.CYAN}{total_time_spent_sec:,.2f} sec{Colors.RESET} "
              f"({total_time_spent_sec/3600:.2f} hours)")

        print(f"\n{Colors.BOLD}[ Target and Remaining Budget ]{Colors.RESET}")
        print(f" • Target budget: {Colors.BLUE}{target_total_time_sec:,.0f} sec{Colors.RESET} "
              f"({TARGET_COMPUTE_DAYS} days)")
        if remaining_time_sec > 0:
            print(f" • Remaining: {Colors.GREEN}{remaining_time_sec:,.2f} sec{Colors.RESET} "
                  f"({remaining_time_sec/3600:.2f} hours)")
        else:
            print(f" • Budget exceeded by: {Colors.RED}{-remaining_time_sec:,.2f}sec ({-remaining_time_sec/3600:.2f} hours){Colors.RESET}") 
    
        print(f"\n{Colors.BOLD}[ Rerun Estimation ]{Colors.RESET}")
        print(f" • Average time per task: {Colors.CYAN}{average_time_sec:.2f} sec{Colors.RESET}")
        print(f" • Estimated time per full rerun ({total_tasks_per_rerun} tasks): "
              f"{Colors.CYAN}{estimated_time_per_rerun_sec:,.2f} sec{Colors.RESET} "
              f"({estimated_time_per_rerun_sec/3600:.2f} hours)")
        print("-" * 60)
        print(f"{Colors.BOLD}>>> Achievable full reruns within {TARGET_COMPUTE_DAYS} days: "
              f"{Colors.GREEN}{math.floor(total_achievable_attempts)}{Colors.RESET}")
        print("-" * 60)

    else:
        print(f"\n{Colors.YELLOW}--- Analysis finished: No valid 'Time (sec)' data found ---{Colors.RESET}")


if __name__ == "__main__":
    analyze_experiment_progress()
