# Dataset

Our experiment configuration space was calculated to be the following

| number of experiments          | #n      | description                                                        |
| ------------------------------ | ------- | ------------------------------------------------------------------ |
| **Tasks x path lengths**       | **9**   | **T1: 2,3,4,5 T2: 1,2 T3: 1,2,3**                                  |
| **different node pairs**       | **5**   | **For each Task x numerical answer we can select different nodes** |
| **input graphs**               | **18**  | **That is 10 + 8 graphs**                                          |
| prompting styles               | 4       | zero-/few-”shot” (examples), reasoning on/off                      |
| reruns                         | 3       | To gain confidence in results                                      |
| models                         | 4       | Gemini, ChatGPT, DeepSeek, LLAMA                                   |
|                                |         |                                                                    |
| **Number of graphs to create** | **810** |                                                                    |


The rows marked with **bold** are the ones we manually need to create.

As this `aesthetic_effect_human_performance` subdirectory only references the Helen Purchase paper
"Which aesthetic has the greatest effect on human understanding?" 1997, we only need to create the 10 graphs
mentioned in the paper. The other 8 graphs are handled in the `layout_algorithms_performance` subdirectory.

As such we end up with 450 unique graph-task-answer-variation combinations for this paper.

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

How long is the shortest path between two given nodes?

The answer range is from 2 to 5 inclusive.

Length 2:

| Variation | Node Pair | Answer | Ground Truth         |
| --------- | --------- | ------ | -------------------- |
| 1         | E, H      | 2      | [E, B, H]            |
| 2         | R, P      | 2      | [R, Q, P]            |
| 3         | S, T      | 2      | [S, F, T]            |
| 4         | H, C      | 2      | [H, G, C], [C, B, H] |
| 5         | A, N      | 2      | [A, B, N]            |

Length 3:

| Variation | Node Pair | Answer | Ground Truth               |
| --------- | --------- | ------ | -------------------------- |
| 1         | A, I      | 3      | [A, B, H, I]               |
| 2         | F, I      | 3      | [F, B, H, I], [F, G, H, I] |
| 3         | R, H      | 3      | [R, Q, I, H], [R, J, I, H] |
| 4         | E, O      | 3      | [E, B, N, O], [E, B, C, O] |
| 5         | B, Q      | 3      | [B, H, I, Q]               |

Length 4:

| Variation | Node Pair | Answer | Ground Truth                                      |
| --------- | --------- | ------ | ------------------------------------------------- |
| 1         | A, J      | 4      | [A, B, H, I, J]                                   |
| 2         | C, P      | 4      | [C, B, H, I, P], [C, G, H, I, P]                  |
| 3         | I, O      | 4      | [I, H, B, N, O], [I, H, G, C, O], [I, H, B, C, O] |
| 4         | A, P      | 4      | [A, B, H, I, P]                                   |
| 5         | E, Q      | 4      | [E, B, H, I, Q]                                   |

Length 5:

| Variation | Node Pair | Answer | Ground Truth                           |
| --------- | --------- | ------ | -------------------------------------- |
| 1         | A, R      | 5      | [A, B, H, I, J, R], [A, B, H, I, Q, R] |
| 2         | N, R      | 5      | [N, B, H, I, J, R], [N, B, H, I, Q, R] |
| 3         | S, Q      | 5      | [S, F, B, H, I, Q], [S, F, G, H, I, Q] |
| 4         | O, J      | 5      | [O, C, B, H, I, J], [O, C, G, H, I, J] |
| 5         | E, R      | 5      | [E, B, H, I, J, R], [E, B, H, I, Q, R] |

### Task 2

What is the minimum number of nodes that must be removed in order to disconnect two given nodes such that there is no path between them?

Number of nodes to remove to disconnect the two nodes is either 1 or 2.

Removing 1 node:

| Variation | Node Pair | Answer | Ground Truth |
| --------- | --------- | ------ | ------------ |
| 1         | A, I      | 1      | [H]          |
| 2         | E, J      | 1      | [H], [I]     |
| 3         | Q, N      | 1      | [H], [I]     |
| 4         | S, R      | 1      | [H], [I]     |
| 5         | R, H      | 1      | [I]          |

Removing 2 nodes:

| Variation | Node Pair | Answer | Ground Truth           |
| --------- | --------- | ------ | ---------------------- |
| 1         | S, O      | 2      | [N, C], [B, C], [B, G] |
| 2         | A, H      | 2      | [B, G], [B, F]         |
| 3         | N, G      | 2      | [B, C]                 |
| 4         | P, J      | 2      | [I, Q]                 |
| 5         | E, T      | 2      | [B, F]                 |

### Task 3

What is the minimum number of edges that must be removed in order to disconnect two given nodes such that there is no path between them?

The set of node pairs (edges) to remove is either 1, 2 or 3.

Removing 1 edge:

| Variation | Node Pair | Answer | Ground Truth |
| --------- | --------- | ------ | ------------ |
| 1         | A, I      | 1      | [(H, I)]     |
| 2         | E, J      | 1      | [(H, I)]     |
| 3         | Q, N      | 1      | [(H, I)]     |
| 4         | S, R      | 1      | [(H, I)]     |
| 5         | Q, H      | 1      | [(H, I)]     |

Removing 2 edges:

| Variation | Node Pair | Answer | Ground Truth                       |
| --------- | --------- | ------ | ---------------------------------- |
| 1         | S, O      | 2      | [(N, O), (S, O)]                   |
| 2         | P, R      | 2      | [(J, R), (Q, R)], [(P, I), (P, Q)] |
| 3         | A, H      | 2      | [(B, H), (G, H)]                   |
| 4         | I, R      | 2      | [(J, R), (Q, R)]                   |
| 5         | H, B      | 2      | [(H, B), (H, G)]                   |

Removing 3 edges:

| Variation | Node Pair | Answer | Ground Truth                                                                 |
| --------- | --------- | ------ | ---------------------------------------------------------------------------- |
| 1         | J, R      | 3      | [(J, R), (J, Q), (J, I)]                                                     |
| 2         | E, N      | 3      | [(N, O), (N, C), (N, B)], [(O, C), (N, C), (N, B)], [(N, B), (C, B), (C, G)] |
| 3         | A, T      | 3      | [(A, B), (A, E), (A, S)], [(T, F), (T, B), (T, G)]                           |
| 4         | F, C      | 3      | [(N, B), (C, B), (C, G)]                                                     |
| 5         | I, Q      | 3      | [(I, J), (I, P), (I, Q)], [(I, J), (P, Q), (I, Q)]                           |

