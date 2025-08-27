# Visual Graph Reasoning with Multimodal Large Language Models

This project investigates whether multimodal Large Language Models (LLMs) can act as **human proxies** in user studies on graph visualization. Specifically, it explores if LLMs are able to replicate human reasoning and performance on visual graph tasks, potentially replacing human participants in experimental settings.

The project replicates the user study *"Performance of Layout Algorithms"* by Helen Purchase, faithfully reproducing its three core tasks. The original study evaluated how different graph layouts affect human performance on reasoning tasks. Here, the same tasks and layouts are presented to LLMs, using images manually recreated in yED Live to match the original study (since the original images were of insufficient quality).

Given a graph image and a textual prompt, the model must solve a reasoning problem using visual understanding. The results are then compared to the original human data to assess the viability of LLMs as substitutes for human participants in graph visualization research.

## 🧠 Tasks Overview

Each graph image encodes one of the following tasks:

1. **Task 1 – Shortest Path Length**  
   Predict the length of the shortest path between two nodes.
2. **Task 2 – Node Removal (Cut Set)**  
   Predict the minimum number of nodes to remove in order to disconnect a pair of nodes and identify the cut set.
3. **Task 3 – Edge Removal (Cut Set)**  
   Predict the minimum number of edges to remove in order to disconnect a pair of nodes and identify the cut set.

Ground truth answers are stored in corresponding `*_gt.json` files under each task directory.


## 📁 Project Structure

```
project/
├── dataset/
│   └── test/                        # Folder containing test PNG images (graph layouts)
│   └── template_graphml/            # Folder containing the templates in graphml format for each graph layout
│   └── practice/                    # Folder containing practice PNG images (for Few Shot prompting)
├── tasks/
│   ├── T1_shortest_path_length/
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

## 🧩 Experimental Design Details

- **Predefined Answer Sets:**  
  Each task had a fixed set of possible answers:
  - **Task 1 (Shortest Path Length):** possible answers were 2, 3, or 4.
  - **Task 2 (Minimum Node Removal):** possible answers were 2 or 3.
  - **Task 3 (Minimum Edge Removal):** possible answers were 2 or 3.

- **Target Node Pairs:**  
  For each possible answer in every task, **5 different pairs** of target nodes were selected, ensuring that for each answer value, there are 5 node pairs that yield that answer.

- **Input Graphs and Layouts:**  
  The experiment uses 8 different input graphs, each rendered in a specific layout.

- **Prompting Styles:**  
  Four prompting styles are tested:
  1. Zero-shot without CoT (Chain-of-Thought)
  2. Zero-shot with CoT
  3. Few-shot without CoT 
  4. Few-shot with CoT

- **Repetitions (Attempts):**  
  Each experiment is repeated **3 times** (3 attempts) to increase the reliability of the results.

- **Models Tested:**  
  Four different models are evaluated: *Gemini*, *ChatGPT*, *DeepSeek*, and *Llama*.

- **Differences from the Original User Study:**  
  In the original user study, graph drawings were also *rotated* and node labels were *omitted* during testing to prevent **learning effects** in human participants. In this LLM-based replication, both graph rotations and label omission were not applied, since LLMs do not exhibit human-like learning effects across trials.

## ⚙️ How It Works

The `main.py` script:

1. Loads a task-specific prompt and ground truth.
2. Randomly selects a task-specific unprocessed test image.
3. Encodes the image and constructs a multimodal prompt (system context + user msg + image) to the chosen model.
4. Parses the model response and evaluates accuracy.
5. Stores the results and metrics (latency, token usage, prediction correctness) in `results.csv`.

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


## 📝 Example File Naming

The naming scheme for each image is:

```{graph_name}-{#task}_{ground_truth}_{node_pair}```

So:
* Ground truth data must be consistent with image filenames.
* Image filenames must contain a task identifier, such as `_task1_`, `_task2_`, `_task3_`.

Examples: 
```
FD-FR_task3_gt3_PAIR2.png  → Task 3, GT = 3
SEIS_task1_gt4_PAIR1.png   → Task 1, GT = 4
```
---

## How many attempts are needed to achieve statistical significance?
### Data

-   **Real Average Time per Task:** 26.25 sec
    
-   **Number of Tasks:** 280
    
-   **Number of Configurations:** 4
    
-   **Available Calculation Time:** 7 days
    

### Final Calculation

1. **Time for a single complete repetition:**
    
    - 280 tasks \* 4 configurations \* **26.25** (CHECK IT EACH TIME WITH THE SCRIPT) seconds/task = 29,400 seconds
        
    - This should be equivalent to about **8.17 hours** to complete all my experiments once.
        
2.  **Total computing time available in seconds:**
    
    - 7 days \ 24 hours/day \ 3600 seconds/hour = 604,800 seconds
        
3.  **Total number of possible repetitions:**
    
    - 604,800 total seconds / 29,400 seconds per repetition = 20.57
        

### The Concrete Answer.

Since I can only perform full repetitions, the final number is **20** or a little higher.

So, to the question “How many attempts should I do?” --> **approximately 20 repetitions.**

