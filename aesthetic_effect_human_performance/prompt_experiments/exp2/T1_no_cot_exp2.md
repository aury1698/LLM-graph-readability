**You are an expert evaluator of graph visualizations, specifically in the area of understanding the node-link structure of a graph image.** You are participating in a study that analyzes readability of graphs. You are going to receive an image of a graph, for which you need to analyze the labeled nodes and unlabeled edges and deduct the graph's structure of node connections to answer the following question:

**What is the shortest path length between the two black colored nodes in this graph?**

## Reading the Graph Images

1. **Nodes:** The nodes are drawn as circles with a letter inside as a label. The nodes are white circles with a black outline and a alphabetical letter. The only exceptions are the two filled black nodes, which indicate the nodes the question is asked about.
2. **Edges:**
    * Edges are drawn as black lines between the nodes, connecting to the circular outline of the nodes.
    * An edge always connects exclusively two nodes with each other.
    * A node can have an arbitrary number of edges connected with them.
    * Edges can be bent. You need to follow the curve to find the connecting nodes.
    * Edges can visually cross with other edges. This does not indicate an intersection where you can follow any path. The edge must be followed in its apparent direction at the crossing to find the correct connecting node.
3. **Graph:** Emerging from the nodes and edges is the whole graph structure. Use the deducted understanding of the image to answer questions on the graph. 

## Understanding of "Shortest Path" for this Task

Between the two black colored nodes there exist possibly multiple different paths. A path is a chain-like structure between two nodes, which are connected through edges with zero or more intermediate nodes. Nodes are only connected, if a black line, i.e. edge, is drawn between them to connect them to each other. As there can be multiple paths between nodes, we are looking for the shortest path between the black nodes. The path length is the number of edges making up the path. The shortest path is defined as the path with the least number of intermediate nodes, resulting in the smallest path length.

**Output Format:**

Answer the question in one seperate line in the format, e.g.:

Length: 2, Path: [A, B, C]
