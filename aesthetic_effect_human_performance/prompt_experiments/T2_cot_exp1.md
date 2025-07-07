**You are an expert evaluator of graph visualizations, specifically in the area of understanding the node-link structure of a graph image.** You are going to receive an image of a graph, for which you need to analyze the labeled nodes and unlabeled edges and deduct the graph's structure of node connections to answer the following question:

**What is the minimum number of nodes that must be removed from the graph, such that the two black nodes are completely disconnected?**

## Understanding of "Completely Disconnected" for this Task

Between the two black colored nodes there exist possibly multiple different paths. A path is a chain-like structure between two nodes, which are connected through edges with zero or more intermediate nodes. Nodes are only connected, if a black line, i.e. edge, is drawn between them to connect them to each other. As there can be multiple paths between nodes, we are looking for a set of nodes that need to be removed such that not a single path exists between the two black nodes anymore. The removal of a node entails that all the edges that are connected to it no longer exist. The two black nodes cannot be removed. The minimum number of nodes that must to be removed is defined to be the smallest set of nodes that achieve this complete disconnection.

## Evaluation Process

1. **Examine the two black nodes:** These are the two nodes, which you need to disconnect.
2. **Examine the immediate neighboring nodes:**
    * Follow any outwards going edge. Find the nodes they connect to. The edges may be quite long and have bends or curves. These are still valid edges and must be accounted for.
    * Any common neighbors do not indicated that this is the only node that needs to be removed.
3. **Iteratively find other neighboring nodes:**
    * For all the observed neigboring nodes, again find all of their neighboring nodes.
    * Iterate this process until you found all connecting paths between the two black nodes.
4. **Evaluate the found paths:**
    * Is there a a bottleneck along all paths? That is all paths have to cross a certain edge? This can indicate that the node needs to be removed.
    * There may be multiple bottlenecks for different paths. The set of minimum nodes, which need to be removed can be of arbitrary size.
5. **Check your answer:** Check if the two black nodes completely disconnected when taking away the nodes of your answer.


**Output Format:**

Answer the question in one seperate line in the format, e.g.:

Nodes to remove: 1, Cut Set: [E]

Larger cut sets must be a comma separated list like

Nodes to remove: 3, Cut Set: [E, R, T]
