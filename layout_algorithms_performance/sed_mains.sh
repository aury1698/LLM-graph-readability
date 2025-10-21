#!/bin/bash

set -euo pipefail

# Set your desired modes here
mode="few_shot"      # "zero_shot" or "few_shot"
cot_mode="no_cot"     # "no_cot" or "cot"
model_name="glm-4.5v-106b"  # Set your desired model name gpt-4o, gpt-5, gpt-5-2025-08-07, gemini-2.5-flash, mistral-small-3.2-24b, glm-4.5v-106b

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
        sed -i -E "s/^([[:space:]]*)attempt = [0-9]+/\1attempt = $((i-0))/" "$file"
    fi
done