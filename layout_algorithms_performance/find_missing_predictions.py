import pandas as pd

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
    print("Rows with missing Prediction:")
    print(missing_pred[["CSV row", "Task", "Layout", "Prediction"]])
    print(f"\nFound {len(missing_pred)} rows with missing Prediction.")

else:
    print("No rows with missing Prediction found.")

# --- Bonus check: Check for each configuration if True+False == 280 ---
group_cols = ["LLM Mode", "COT Mode", "Attempt", "Model Name"]
df_valid = df[df["Prediction"].notnull() & (df["Prediction"].astype(str).str.strip() != "")]
df_valid = df_valid[df_valid["Correct Prediction (True/False)"].isin([True, False, "True", "False"])]

# Normalize values to string for grouping
df_valid["Correct Prediction (True/False)"] = df_valid["Correct Prediction (True/False)"].astype(str)

grouped = df_valid.groupby(group_cols)["Correct Prediction (True/False)"].value_counts().unstack(fill_value=0).reset_index()

print("\nCheck for each configuration if (True + False) == 280:")
for _, row in grouped.iterrows():
    config = ", ".join([f"{col}={row[col]}" for col in group_cols])
    n_true = row.get("True", 0)
    n_false = row.get("False", 0)
    total = n_true + n_false
    status = "OK!" if total == 280 else f"NOT OK! ({total}/280)"
    print(f"Config: {config} | True: {n_true} | False: {n_false} | Total: {total} | Status: {status}")