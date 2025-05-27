# Visual Graph Reasoning with Multimodal Large Language Models

This project investigates whether multimodal Large Language Models (LLMs) can act as **human proxies** in user studies on graph visualization. Specifically, it explores if LLMs are able to replicate human reasoning and performance on visual graph tasks, potentially replacing human participants in experimental settings.

The project **replicates the user study "Performance of Layout Algorithms" by Helen Purchase**, faithfully reproducing its three core tasks. The original study evaluated how different graph layouts affect human performance on combinatorial reasoning tasks. Here, the same tasks and layouts are presented to LLMs, using images manually recreated in yED Live to match the original study (since the original images were of insufficient quality).

Given a graph image and a textual prompt, the model must solve specific combinatorial problems using both visual and textual understanding. The results are then compared to the original human data to assess the viability of LLMs as substitutes for human participants in graph visualization research.

## 📁 Project Structure

```
layout_algorithms_performance/
├── dataset/
│   └── test/                        # Folder containing test PNG images (graph layouts)
│   └── template_graphml/            # Folder containing the templates in graphml format for each graph layout
│   └── practice/                    # Folder containing practice PNG images (for Few Shot prompting)
├── tasks/
│   ├── T1_shortest_path_lenght/
│   │   ├── task1_shortest_path_length.json
│   │   └── task1_shortest_path_length_gt.json
│   ├── T2_nodes_remove/
│   │   ├── task2_min_nodes_removal.json
│   │   └── task2_min_nodes_removal_gt.json
│   └── T3_edges_remove/
│       ├── task3_min_edges_removal.json
│       └── task3_min_edges_removal_gt.json
├── results.csv                      # File storing predictions, metrics, and performance data
├── main.py                          # Main script to run experiments
└── find_missing_predictions.py      # Utility script to check for missing predictions in results.csv
```

## 🧠 Tasks Overview

Each graph image encodes one of the following tasks:

1. **Task 1 – Shortest Path Length**  
   Predict the length of the shortest path between two nodes.
2. **Task 2 – Node Removal (Cut Set)**  
   Predict the minimum number of nodes to remove in order to disconnect a pair of nodes and identify the cut set.
3. **Task 3 – Edge Removal (Cut Set)**  
   Predict the minimum number of edges to remove in order to disconnect a pair of nodes and identify the cut set.

Ground truth answers are stored in corresponding `*_gt.json` files under each task directory.

## ⚙️ How It Works

The script:

1. Loads the prompts and ground truth.
2. Randomly selects a task-specific image not yet processed.
3. Converts the image into base64 (data URL) to make it compatible with the LLM API.
4. Sends a multimodal prompt (system + user + image) to the chosen model (OpenAI GPT-4o or Google Gemini).
5. Parses the model response and evaluates accuracy.
6. Stores the results and metrics (latency, token usage, prediction correctness) in `results.csv`.

The system supports both:
- **Zero-Shot** and **Few-Shot** prompting
- **Chain-of-Thought (CoT)** and **No-CoT** prompting

## ✅ Requirements

- Python ≥ 3.8
- `openai`
- `google-generativeai`
- `langchain`
- `langchain-openai`
- `langchain-google-genai`
- `google-generativeai`
- `openai`
- `pandas`

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## 🚀 Running the Script

Modify the parameters at the bottom of `main.py`:

```python
mode = "zero_shot"           # or "few_shot"
cot_mode = "cot"             # or "no_cot"
model_name = "gpt-4o"        # or "gemini-2.5-flash-preview-05-20"
attempt = 1
```

Then run:

```bash
python main.py
```

The script will process up to `max_images_per_run` images for the current configuration and append the results to `results.csv`.

## 📊 Output

Each row in `results.csv` includes:

* Task type
* Model used
* Image name (graph layout)
* Ground truth and predicted values
* Prediction correctness
* Response time
* Token usage metrics

## 📌 Notes

* Ground truth data must be consistent with image filenames.
* Image filenames must contain a task identifier, such as `_task1_`, `_task2_`, `_task3_`.

## 📝 Example File Naming

The naming scheme for each image is:

```{graph_name}-{#task}_{ground_truth}_{node_pair}```

So, for instance, you may find:
```
FD-FR_task3_gt3_PAIR2.png  → Belongs to Task 3
SEIS_task1_gt4_PAIR1.png   → Belongs to Task 1
```


---

