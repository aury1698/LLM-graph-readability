import os
import pandas as pd

CURRENT_MODE = 'exp1' #exp1 or exp2

if CURRENT_MODE == 'exp2':
    BASE_PATH = 'layout_algorithms_performance'
else:
    BASE_PATH = 'aesthetic_effect_human_performance'
    
RESULTS_DIR = os.path.join(BASE_PATH, 'results')
OUTPUT_CSV_FILE = f'average_accuracies_{CURRENT_MODE}_by_difficulty.csv'

MODELS_TO_LOAD = ["gemini-2.5-flash", "mistral-small-3.1-24b", "gpt-5", "glm-4.5v-106b"]
SHOT_TYPES = ["zero_shot", "few_shot"]
COT_TYPES = ["cot", "no_cot"]

def load_and_aggregate_results():
    """
    Scans the results directories, loads all experiment CSV files
    and merges them into a single pandas DataFrame.
    """
    all_data_frames = []
    print(f"[*] Starting scanning and loading files from: {RESULTS_DIR}")

    for model in MODELS_TO_LOAD:
        for shot in SHOT_TYPES:
            for cot in COT_TYPES:
                config_path = os.path.join(RESULTS_DIR, model, shot, cot)
                
                if not os.path.isdir(config_path):
                    continue
                
                for filename in os.listdir(config_path):
                    if filename.startswith('results_attempt_') and filename.endswith('.csv'):
                        file_path = os.path.join(config_path, filename)
                        try:
                            df = pd.read_csv(file_path)
                            all_data_frames.append(df)
                        except Exception as e:
                            print(f"[!] Error reading file {file_path}: {e}")
    
    if not all_data_frames:
        return None

    print(f"[*] Loaded data from {len(all_data_frames)} files. Starting aggregation...")
    master_df = pd.concat(all_data_frames, ignore_index=True)
    return master_df

def calculate_average_accuracy(df):
    """
    Calculates average accuracy by grouping by model, config, task, DIFFICULTY (GT), and layout.
    """
    if df is None or df.empty:
        print("[!] DataFrame is empty. No data to process.")
        return None
        
    df['Task_Group'] = df['Task'].str.split('_').str[0]
    df['Layout_Group'] = df['Layout'].str.split('_').str[0]
    
    df['Ground_Truth'] = df['Layout'].str.extract(r'(_gt\d+)').fillna('_gtN/A')
    df['Ground_Truth'] = df['Ground_Truth'].str.replace('_', '') 
    
    df['Is_Correct'] = df['Correct Prediction (True/False)'].astype(str).apply(lambda x: 1 if x.strip() == 'True' else 0)
    
    grouping_columns = [
        'Model Name', 
        'LLM Mode', 
        'COT Mode', 
        'Task_Group', 
        'Ground_Truth',  
        'Layout_Group'
    ]
    
    aggregated_results = df.groupby(grouping_columns).agg(
        Accuracy=('Is_Correct', 'mean'),
        Sample_Count=('Is_Correct', 'count'),
        Total_Correct=('Is_Correct', 'sum')
    ).reset_index()
    
    aggregated_results['Accuracy'] = aggregated_results['Accuracy'] * 100
    
    print("\nFirst few aggregated results (now with Ground_Truth):")
    print(aggregated_results[['Model Name', 'Task_Group', 'Ground_Truth', 'Accuracy', 'Sample_Count']].head())
    
    return aggregated_results.sort_values(by=grouping_columns).reset_index(drop=True)


if __name__ == "__main__":
    master_data_frame = load_and_aggregate_results()
    
    if master_data_frame is not None:
        average_accuracies = calculate_average_accuracy(master_data_frame)
        
        if average_accuracies is not None:
            print("\n--- Aggregated Results (Grouped by Difficulty) ---")
            print(average_accuracies.to_string())
            
            try:
                average_accuracies.to_csv(OUTPUT_CSV_FILE, index=False, float_format='%.2f')
                print(f"\n[*] Results successfully saved to: {OUTPUT_CSV_FILE}")
            except Exception as e:
                print(f"\n[!] Error saving CSV file: {e}")