import pandas as pd
import os
import glob

#This script should only be used in the extreme case of some errors during the execution of the main scripts, 
#possibily due to parrallel executions of the same configuration, which causes duplicates.
# It checks for duplicate entries in a specified CSV file based on a key column ('Layout').

# # --- INSERT HERE THE PATH OF THE CSV FILES YOU WANT TO CHECK ---
results_folder = 'results/gpt-5/few_shot'

# The column name that should be unique for each experiment
key_column = 'Layout'

# The column to check for empty/missing values
column_to_check_for_empty = 'Prediction'


csv_files = glob.glob(os.path.join(results_folder, '**', '*.csv'), recursive=True)

if not csv_files:
    print(f"ERROR: No CSV files found in '{results_folder}'.")
else:
    for file_to_check in csv_files:
        print(f"\n{'='*100}\nAnalyzing file: {file_to_check}\n{'='*100}")
        try:
            df = pd.read_csv(file_to_check)
            print(f"Loaded {len(df)} rows.")

            # 1. CHECKING FOR DUPLICATE ROWS
            duplicates_df = df[df.duplicated(subset=[key_column], keep=False)]
            if not duplicates_df.empty:
                print(f"⚠️ Found {len(duplicates_df)} duplicate rows for '{key_column}' ({duplicates_df[key_column].nunique()} unique values):")
                print(duplicates_df.sort_values(by=key_column).to_string())
            else:
                print(f"✅ No duplicate rows found based on '{key_column}'.")

            # 2. CHECKING FOR EMPTY PREDICTION VALUES
            missing_values_df = df[df[column_to_check_for_empty].isnull()]
            if not missing_values_df.empty:
                print(f"⚠️ Found {len(missing_values_df)} rows with missing '{column_to_check_for_empty}' values:")
                print(missing_values_df.to_string())
            else:
                print(f"✅ No rows with missing '{column_to_check_for_empty}' values.")

        except Exception as e:
            print(f"An error occurred while reading or analyzing the file: {e}")