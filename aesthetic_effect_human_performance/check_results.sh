#!/bin/bash

EXPECT=450

EXPECTED_RESULTS=${1:-$((EXPECT+1))}

# The first three globs are model/shot_mode/cot_mode
find results/*/*/*/results_attempt_*.csv | sort | while read -r file; do
    line_count=$(wc -l < "$file")
    if [ "$line_count" -eq "$EXPECTED_RESULTS" ]; then
        printf "✅ COMPLETE   %-80s (%d lines)\n" "$file" "$line_count"
    else
        missing=$((EXPECTED_RESULTS - line_count))
        printf "❌ INCOMPLETE %-80s (%d lines, missing %d)\n" "$file" "$line_count" "$missing"
    fi
done