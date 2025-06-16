import pandas as pd
from colorama import Fore, Style, init
from tabulate import tabulate

# This script checks the CSV "results" file for rows where the "Prediction" column is missing 
# in order to delete them manually and re-run the script to get a proper response from the model.

csv_file = "results.csv"

# Load the CSV
df = pd.read_csv(csv_file)

# Find rows where Prediction is missing (NaN or empty string)
missing_pred = df[df["Prediction"].isnull() | (df["Prediction"].astype(str).str.strip() == "")]

if not missing_pred.empty:
    # Add a column for the real CSV line number
    missing_pred = missing_pred.copy()
    missing_pred["CSV row"] = missing_pred.index + 2  # +2: header + 1-based index
    print("⚠️ Rows with missing Prediction:")
    print(tabulate(missing_pred[["CSV row", "Task", "Layout", "Prediction"]], headers="keys", tablefmt="fancy_grid"))
    print(f"\nFound {len(missing_pred)} rows with missing Prediction.\n")
else:
    print("✅ No rows with missing Prediction found.")

# --- Bonus check: Check for each configuration if True+False == 280 ---
group_cols = ["LLM Mode", "COT Mode", "Attempt", "Model Name"]
df_valid = df[df["Prediction"].notnull() & (df["Prediction"].astype(str).str.strip() != "")]
df_valid = df_valid[df_valid["Correct Prediction (True/False)"].isin([True, False, "True", "False"])]

# Normalize values to string for grouping
df_valid["Correct Prediction (True/False)"] = df_valid["Correct Prediction (True/False)"].astype(str)

grouped = df_valid.groupby(group_cols)["Correct Prediction (True/False)"].value_counts().unstack(fill_value=0).reset_index()

table = []
for _, row in grouped.iterrows():
    config = [row[col] for col in group_cols]
    n_true = row.get("True", 0)
    n_false = row.get("False", 0)
    total = n_true + n_false
    status = f"{Fore.GREEN}OK!{Style.RESET_ALL}" if total == 280 else f"{Fore.RED}NOT OK! ({total}/280){Style.RESET_ALL}"
    table.append(config + [n_true, n_false, total, status])

headers = group_cols + ["True", "False", "Total", "Status"]
print(tabulate(table, headers=headers, tablefmt="grid"))
