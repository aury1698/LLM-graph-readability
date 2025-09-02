import pandas as pd
import os

#This script should only be used in the extreme case of some errors during the execution of the main scripts, 
#possibily due to parrallel executions of the same configuration, which causes duplicates.
# It checks for duplicate entries in a specified CSV file based on a key column ('Layout').

# --- INSERT HERE THE PATH OF THE CSV FILE YOU WANT TO CHECK ---
file_checked = 'results/gemini-2.5-flash/zero_shot/cot/results_attempt_7.csv'

# ----------------------------------------------------

# The column we want to check for duplicates
key_column = 'Layout'

if not os.path.exists(file_checked):
    print(f"ERROR: The file '{file_checked}' was not found.")
    print("Please, check that the path and the name of the desired file is correct.")
else:
    try:
        # Carichiamo il file CSV
        df = pd.read_csv(file_checked)

        # Troviamo tutte le righe che hanno un valore duplicato nella colonna 'Layout'
        # Usiamo `keep=False` per marcare TUTTE le occorrenze di un duplicato, non solo la seconda.
        duplicates_df = df[df.duplicated(subset=[key_column], keep=False)]

        # Se il DataFrame dei duplicati non è vuoto, li stampiamo
        if not duplicates_df.empty:
            print(f"ATTENTION: found the following duplicates in the file '{file_checked}':")
            print("="*80)
            
            # Ordiniamo i risultati per 'Layout' per raggruppare visivamente i duplicati
            # Usiamo .to_string() per essere sicuri di stampare tutte le righe senza troncamenti
            print(duplicates_df.sort_values(by=key_column).to_string())
            
            print("="*80)
            num_duplicates_rows = len(duplicates_df)
            num_unique_layouts = duplicates_df[key_column].nunique()
            print(f"\nRecap: Found {num_duplicates_rows} problematic rows which correspond to {num_unique_layouts} unique 'Layout'.")

        else:
            print(f"\nGREAT! No duplicate found in the file '{file_checked}'.")
            print(f"The file contains {len(df)-1} rows, all unique for the column '{key_column}'.")

    except Exception as e:
        print(f"There has been an error during the reading of the file: {e}")