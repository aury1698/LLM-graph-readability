# calculate_average_time_recursive.py

# Step 1: Import necessary libraries
# We need 'pandas' to read and manipulate CSV files.
# We need 'glob' to find all files matching a pattern recursively.
# We need 'os' to work with file paths correctly.
import pandas as pd
import glob
import os

# --- CONFIGURATION ---
# Step 2: Define the BASE path where your project folders are located.
# This is the ONLY path you need to change.
# It should point to the directory that CONTAINS 'layout_algorithms_performance'
# and 'aesthetic_effect_human_performance'.
# Let's assume you run this script from a 'scripts' folder, so '../' goes one level up.
BASE_SEARCH_PATH = '../layout_algorithms_performance/results' 
# ---------------------

def calculate_average_time_recursively():
    """
    Recursively finds all CSV files in a base directory, extracts 
    time values from them, and calculates the overall average.
    """
    
    # Step 3: Create a list to store all the numerical time values found.
    # This list will aggregate values from every single CSV file found.
    all_time_values = []
    
    # Step 4: Define the search pattern for finding the files.
    # os.path.join(BASE_SEARCH_PATH, '**', '*.csv') builds a pattern.
    # - '**' is a special wildcard that tells glob to search in the current directory
    #   AND all subdirectories, no matter how deep.
    # - '*.csv' matches any file that ends with .csv.
    search_pattern = os.path.join(BASE_SEARCH_PATH, '**', '*.csv')
    
    print(f"Searching for all .csv files recursively inside: {os.path.abspath(BASE_SEARCH_PATH)}\n")
    
    # Step 5: Execute the search.
    # The 'recursive=True' argument enables the '**' wildcard functionality.
    # This will return a list of all matching file paths.
    csv_file_paths = glob.glob(search_pattern, recursive=True)
    
    # Filter out any potential results from a virtual environment folder if it exists
    csv_file_paths = [path for path in csv_file_paths if 'venv' not in path and '.venv' not in path]

    # Check if any CSV files were found.
    if not csv_file_paths:
        print(f"Error: No .csv files were found in the search path.")
        return # Exit the function if there's nothing to process.

    print(f"Found {len(csv_file_paths)} CSV file(s). Starting processing...")

    # Step 6: Loop through each file path that was found.
    for file_path in csv_file_paths:
        try:
            # For clarity, print the file being processed.
            print(f"  -> Processing: {file_path}")
            
            # Read the current CSV file into a pandas DataFrame.
            df = pd.read_csv(file_path)
            
            # Check if the 'Time (sec)' column exists in this DataFrame.
            if 'Time (sec)' in df.columns:
                
                # Step 7: Extract, clean, and convert the 'Time (sec)' column.
                # This is the same logic as before, but applied to each file found.
                
                # Use .str.extract() with a regular expression to robustly find the number.
                # '(\d+\.?\d*)' looks for one or more digits, optionally followed by a dot and more digits.
                # This is more robust than just replacing ' seconds'.
                numeric_strings = df['Time (sec)'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
                
                # Convert the extracted strings to numeric values. 'coerce' handles any failures.
                numeric_times = pd.to_numeric(numeric_strings, errors='coerce')
                
                # Remove any NaN (Not a Number) values that might result from failed conversions.
                valid_times = numeric_times.dropna()
                
                # Add the valid numbers from this file to our master list.
                all_time_values.extend(valid_times.tolist())
                
            else:
                # If the column is missing, print a warning but continue with the other files.
                print(f"     Warning: Column 'Time (sec)' not found in this file.")

        except Exception as e:
            # If any other error happens (e.g., file is empty or corrupt), report it and move on.
            print(f"     Error processing file {os.path.basename(file_path)}: {e}")

    # Step 8: Calculate the final average from all collected data.
    if all_time_values:
        # Calculate the sum divided by the count.
        average_time = sum(all_time_values) / len(all_time_values)
        
        # Step 9: Print the final, consolidated result.
        print("\n--- Calculation Complete ---")
        print(f"Total valid time entries found across {len(csv_file_paths)} file(s): {len(all_time_values)}")
        print(f"The average time is: {average_time:.2f} seconds")
    else:
        # This message appears if no files contained valid time data.
        print("\n--- Calculation Complete ---")
        print("No valid 'Time (sec)' data was found in any of the processed files.")

# Standard entry point to run the function when the script is executed.
if __name__ == "__main__":
    calculate_average_time_recursively()