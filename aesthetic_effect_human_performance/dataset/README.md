# Dataset

Our experiment configuration space was calculated to be the following

| number of experiments          | #n      | description                                                        |
| ------------------------------ | ------- | ------------------------------------------------------------------ |
|                                |         |                                                                    |
| **Tasks x path lengths**       | **9**   | **T1: 2,3,4,5 T2: 1,2 T3: 1,2,3**                                  |
| **different node pairs**       | **5**   | **For each Task x numerical answer we can select different nodes** |
| **input graphs**               | **18**  | **That is 10 + 8 graphs**                                          |
| prompting styles               | 4       | zero-/few-”shot” (examples), reasoning on/off                      |
| reruns                         | 3       | To gain confidence in results                                      |
| models                         | 4       | Gemini, ChatGPT, DeepSeek, LLAMA                                   |
|                                |         |                                                                    |
|                                |         |                                                                    |
| **Number of graphs to create** | **810** |                                                                    |


The rows marked with **bold** are the ones we manually need to create.

As this `aesthetic_effect_human_performance` subdirectory only references the Helen Purchase paper
"Which aesthetic has the greatest effect on human understanding?" 1997, we only need to create the 10 graphs
mentioned in the paper. The other 8 graphs are handled in the `layout_algorithms_performance` subdirectory.

## Graphs

All 10 graphs, albeit in different layouts, all share the same adjacency.

| Node Name | Connected To        |
| --------- | ------------------- |
| A         | B, E, S             |
| B         | A, C, E, F, H, N, T |
| C         | B, G, N, O          |
| E         | A, B, F, S          |
| F         | B, E, G, S, T       |
| G         | C, F, H, T          |
| H         | B, G, I             |
| I         | H, J, P, Q          |
| J         | I, Q, R             |
| N         | B, C, O             |
| O         | C, N                |
| P         | I, Q                |
| Q         | I, J, P, R          |
| R         | J, Q                |
| S         | A, E, F             |
| T         | B, F, G             |

This allows us to create one global randomization on the questions for each task and use the same answer for all graphs.

## Tasks

1. How long is the shortest path between two given nodes?
2. What is the minimum number of nodes that must be removed in order to disconnect two given nodes such that there is no path between them?
3. What is the minimum number of edges that must be removed in order to disconnect two given nodes such that there is no path between them?

### Task 1

