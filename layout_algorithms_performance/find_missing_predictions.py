import os
import pandas as pd
from colorama import Fore, Style
from tabulate import tabulate

def load_all_results_from_subdirs(base_path):
    """
    Scans a directory tree, finds all .csv files, and concatenates them into a single DataFrame.
    
    Args:
        base_path (str): The starting directory to scan (e.g., "results").

    Returns:
        pandas.DataFrame: A single DataFrame containing data from all found CSVs,
                          or None if no files were found.
    """
    all_csv_files = []
    # os.walk traverses the directory tree top-down
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".csv"):
                all_csv_files.append(os.path.join(root, file))

    if not all_csv_files:
        print(f"{Fore.RED}No CSV files found in '{base_path}' or its subdirectories.{Style.RESET_ALL}")
        return None

    print(f"Found {len(all_csv_files)} CSV files to analyze. Loading...")

    df_list = []
    for file_path in all_csv_files:
        try:
            df = pd.read_csv(file_path)
            # Add a column to know the origin of each row
            df['Source File'] = file_path
            df_list.append(df)
        except pd.errors.EmptyDataError:
            print(f"{Fore.YELLOW}Warning: Skipping empty CSV file: {file_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error reading {file_path}: {e}{Style.RESET_ALL}")
    
    if not df_list:
        return None

    # Concatenate all dataframes into one
    return pd.concat(df_list, ignore_index=True)


def main():
    """
    Main function to run the analysis on the experiment results.
    """
    base_results_dir = "results"
    
    # Load all data from the new directory structure
    master_df = load_all_results_from_subdirs(base_results_dir)

    if master_df is None:
        print("Analysis stopped because no data could be loaded.")
        return

    print("\n--- 1. Checking for rows with missing 'Prediction' values ---")
    
    # Find rows where Prediction is missing (NaN or empty string)
    missing_pred_df = master_df[master_df["Prediction"].isnull() | (master_df["Prediction"].astype(str).str.strip() == "")]

    if not missing_pred_df.empty:
        print(f"⚠️ {Fore.YELLOW}Found {len(missing_pred_df)} rows with missing Prediction values.{Style.RESET_ALL}")
        print("These experiments likely failed and may need to be re-run.")
        
        # Display the problematic rows, now showing the source file
        display_cols = ["Source File", "Task", "Layout", "Prediction"]
        print(tabulate(missing_pred_df[display_cols], headers="keys", tablefmt="fancy_grid"))
    else:
        print(f"✅ {Fore.GREEN}No rows with missing 'Prediction' values found.{Style.RESET_ALL}")

    
    print("\n--- 2. Checking if each configuration has 280 results ---")
    
    # Filter out rows that are invalid for this check
    df_valid = master_df[master_df["Prediction"].notnull() & (master_df["Prediction"].astype(str).str.strip() != "")]
    df_valid = df_valid[df_valid["Correct Prediction (True/False)"].isin([True, False, "True", "False"])]

    if df_valid.empty:
        print(f"{Fore.YELLOW}No valid rows found to perform the completeness check.{Style.RESET_ALL}")
        return

    # Normalize boolean/string values for grouping
    df_valid["Correct Prediction (True/False)"] = df_valid["Correct Prediction (True/False)"].astype(str)

    group_cols = ["Model Name", "LLM Mode", "COT Mode", "Attempt"]
    grouped = df_valid.groupby(group_cols)["Correct Prediction (True/False)"].value_counts().unstack(fill_value=0).reset_index()

    table_data = []
    for _, row in grouped.iterrows():
        config = [row.get(col, 'N/A') for col in group_cols]
        # Ensure columns 'True' and 'False' exist, otherwise default to 0
        n_true = row.get("True", 0)
        n_false = row.get("False", 0)
        total = n_true + n_false
        
        status = f"{Fore.GREEN}OK!{Style.RESET_ALL}" if total == 280 else f"{Fore.RED}NOT OK! ({total}/280){Style.RESET_ALL}"
        
        table_data.append(config + [n_true, n_false, total, status])

    headers = group_cols + ["True", "False", "Total", "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()