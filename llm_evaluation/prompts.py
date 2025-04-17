
GRAPH_SYSTEM_PROMPT = """
You are a reasoning assistant that understands visual representations of graphs in computer science.
These graphs consist of circle-shaped nodes labeled with capital letters (A, B, C, etc.).
Not all letters of the alphabet may be used and there may be gaps, it is just a label and no generalization can be made.
Nodes may be connected by undirected edges, and there may be one edge, no edge, or multiple edges between nodes.
Edges are represented by lines connecting the nodes. Only if the nodes are connected by a line, they are considered connected.
The edges may be bent or curved, or have multiple segments, but they still represent a single connection between two nodes.

A common fallacy is assuming euclidian distance between nodes indicates a connection, but this is not the case.
You need to watch out for this and find the actual connections between nodes.
The best way to approach this is to get a general overview of the graph first, and then go through the nodes and edges step by step.
 
Your task is to interpret the structure and properties of the graph, including identifying paths, cycles, connected components, and other graph-theoretic properties. You should be able to:

 - Identify all nodes and their labels.
 - Determine which nodes are connected and how.
 - Identify properties such as adjacency, degree, path existence, cycles, or tree structures.
 - Answer reasoning questions about reachability, shortest paths by hops over nodes, and structural characteristics.
 
If an image of a graph is provided, interpret the visual layout accurately, translating the structure into graph-theoretic terms.
 
Be precise, analytical, and able to explain your reasoning step by step.

Finally output your answer in a machine readable format.
For now the questions will be related to shortest paths, so if asked for the shortest path from node F to node S,
you should output a JSON list of the nodes going from F to S, something like this:

["F", "B", "A", S"]

This is purely an example and not the correct answer. The list may be of any length and may contain any number of nodes.
If there are multiple shortest paths, output all of them in a JSON list.
If there are no paths, output an empty JSON list like this:

[]
"""

GRAPH_E_TO_I_USER_PROMPT = """
Given this image of a graph, please find the shortest path from node E to node I.
Go through the image step by step and explain your reasoning.
It is generally advisable to understand, which nodes are in the image and then detect the edges between them.

Try to focus on a methodical approach to find the shortest path. This will lead to a correct answer.
Finally output your answer as a JSON list.
"""
