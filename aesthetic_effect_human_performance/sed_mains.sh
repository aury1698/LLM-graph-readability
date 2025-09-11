#!/bin/bash

set -euo pipefail

# Set your desired modes here
mode="zero_shot"      # "zero_shot" or "few_shot"
cot_mode="no_cot"     # "no_cot" or "cot"
model_name="gpt-5"  # Set your desired model name

# Loop through main1.py to main20.py
for i in {1..20}; do
    cp main.py "main${i}.py"
    file="main${i}.py"
    if [[ -f "$file" ]]; then
        # Replace mode line
        sed -i -E "s/^([[:space:]]*)mode = \".*\"  # \"zero_shot\" or \"few_shot\"/\1mode = \"$mode\"  # \"zero_shot\" or \"few_shot\"/" "$file"
        sed -i -E "s/^([[:space:]]*)cot_mode = \".*\"  # \"no_cot\" or \"cot\"/\1cot_mode = \"$cot_mode\"  # \"no_cot\" or \"cot\"/" "$file"
        # Replace model_name line
        sed -i -E "s/^([[:space:]]*)model_name = \".*\"/\1model_name = \"$model_name\"/" "$file"
        # replace attempt line and insert i value
        sed -i -E "s/^([[:space:]]*)attempt = [0-9]+/\1attempt = $i/" "$file"
    fi
done