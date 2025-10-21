#!/bin/bash

EXPECT=280

EXPECTED_RESULTS=$((EXPECT+1))

# The first three globs are model/shot_mode/cot_mode
find results/*/*/*/results_attempt_*.csv | sort -V | while read -r file; do
    line_count=$(wc -l < "$file")
    if [ "$line_count" -eq "$EXPECTED_RESULTS" ]; then
        printf "YES $EXPECT/$EXPECT %-80s\n" "$file"
    else
        result_count=$((line_count-1))
        missing=$((EXPECTED_RESULTS - line_count))
        printf "NO  %3d/%3d %-80s (%d missing)\n" "$result_count" "$EXPECT" "$file" "$missing"
    fi
done
