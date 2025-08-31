#!/bin/bash

# Set your desired modes here
mode="few_shot"      # "zero_shot" or "few_shot"
cot_mode="no_cot"     # "no_cot" or "cot"
model_name="mistral-small-3.1-24b"  # Set your desired model name

# Loop through main1.py to main20.py
for i in {1..20}; do
    file="main${i}.py"
    if [[ -f "$file" ]]; then
        # Replace mode line
        sed -i -E "s/^([[:space:]]*)mode = \".*\"  # \"zero_shot\" or \"few_shot\"/\1mode = \"$mode\"  # \"zero_shot\" or \"few_shot\"/" "$file"
        sed -i -E "s/^([[:space:]]*)cot_mode = \".*\"  # \"no_cot\" or \"cot\"/\1cot_mode = \"$cot_mode\"  # \"no_cot\" or \"cot\"/" "$file"
        # Replace model_name line
        sed -i -E "s/^([[:space:]]*)model_name = \".*\"/\1model_name = \"$model_name\"/" "$file"
    fi
done