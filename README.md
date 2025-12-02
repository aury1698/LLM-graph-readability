# Do Graph Drawing Aesthetics Matter for AI? A Replication of Foundational Studies in Graph Readability

## Overview
This repository contains the source code, experimental data, and analysis scripts for the paper **"Do Graph Drawing Aesthetics Matter for AI? A Replication of Foundational Studies in Graph Readability"**.

We replicated two foundational user studies on graph layouts written by Helen Purchase—originally designed for humans—substituting human participants with Multimodal Large Language Models (LLMs). This repository provides the tools to reproduce our experiments and the statistical analysis of the results.

---

## Repository Structure

The repository is organized into three main components: the two core experiments, the statistical analysis, and the visualization tools.

### 1. Core Experiments
The folders **`aesthetic_effect_human_performance`** and **`layout_algorithms_performance`** correspond respectively to **Experiment 1** (Aesthetic Criteria) and **Experiment 2** (Layout Algorithms). Both directories share the same internal structure:

* **`dataset/`**: Contains the graph stimuli used for the experiment (images and GraphML templates).
* **`tasks/`**: Defines the three reasoning tasks: *Shortest Path*, *Node Removal*, and *Edge Removal*.
* **`results/`**: Stores raw model outputs, organized by model name (e.g., `gemini-2.5-flash`, `gpt-5`, `mistral`, `glm`).
* **`main.py`**: The primary script to execute a specific experiment.
* **`run.sh`**: Shell script for batch execution.

### 2. Analysis
* These are the R and Python scripts for performing the statistical tests that were used:
    * `exp1_anova.py` / `exp2_anova.py`: Specific analysis scripts, one for each experiment.
    * `wsd.r`: R script for post-hoc analysis. It performs Tukey's WSD tests.
    * `calculate_averages.py`: Utility to process raw results into CSV files.

### 3. Visualization
* **`visualization/`**: Contains instructions on how to view our interactive charts and visualizations presented in the paper.


