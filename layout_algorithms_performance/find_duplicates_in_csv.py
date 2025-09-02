import pandas as pd
import os

#This script should only be used in the extreme case of some errors during the execution of the main scripts, 
#possibily due to parrallel executions of the same configuration, which causes duplicates.
# It checks for duplicate entries in a specified CSV file based on a key column ('Layout').

# --- INSERT HERE THE PATH OF THE CSV FILE YOU WANT TO CHECK ---
file_to_check = 'results/gemini-2.5-flash/zero_shot/cot/results_attempt_7.csv'

# The column name that should be unique for each experiment
key_column = 'Layout'

# The column to check for empty/missing values
column_to_check_for_empty = 'Prediction'


# --- SCRIPT LOGIC ---

# First, check if the file exists to avoid errors
if not os.path.exists(file_to_check):
    print(f"ERROR: The file '{file_to_check}' was not found.")
    print("Please check that the path and filename are correct.")
else:
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_to_check)
        print(f"Successfully loaded '{file_to_check}'. Analyzing {len(df)} rows...")
        print("\n" + "="*80)

        # --- 1. CHECKING FOR DUPLICATE ROWS ---
        print(f"--- 1. Checking for duplicates in the '{key_column}' column ---")

        # Find all rows that have a duplicate value in the key_column
        # We use `keep=False` to mark ALL occurrences of a duplicate, not just the second one.
        duplicates_df = df[df.duplicated(subset=[key_column], keep=False)]

        if not duplicates_df.empty:
            print(f"⚠️ ATTENTION: Found the following duplicate rows:")
            # Sort the results by the key column to visually group the duplicates
            # We use .to_string() to ensure all rows are printed without truncation
            print(duplicates_df.sort_values(by=key_column).to_string())
            
            num_duplicate_rows = len(duplicates_df)
            num_unique_layouts = duplicates_df[key_column].nunique()
            print(f"\nSummary: Found {num_duplicate_rows} problematic rows corresponding to {num_unique_layouts} unique '{key_column}' values.")
        else:
            print(f"✅ OK! No duplicate rows found based on the '{key_column}' column.")

        print("\n" + "="*80)

        # --- 2. CHECKING FOR EMPTY PREDICTION VALUES ---
        print(f"--- 2. Checking for empty values in the '{column_to_check_for_empty}' column ---")
        
        # Find all rows where the specified column is null/empty (NaN)
        # This will catch malformed rows as well, like the one you mentioned
        missing_values_df = df[df[column_to_check_for_empty].isnull()]

        if not missing_values_df.empty:
            print(f" ⚠️ ATTENTION: Found {len(missing_values_df)} rows with missing '{column_to_check_for_empty}' values.")
            print("\nThese experiments may have failed or the rows might be corrupted.")
            print("Here are the complete problematic rows:\n")
            print(missing_values_df.to_string())
        else:
            print(f"✅ OK! No rows with missing '{column_to_check_for_empty}' values found.")
            
        print("\n" + "="*80)

    except Exception as e:
        print(f"An error occurred while reading or analyzing the file: {e}")