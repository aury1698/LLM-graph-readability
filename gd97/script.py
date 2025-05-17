import re
import networkx as nx

def parse_graphed_file(file_path):
    """
    Parses a GraphEd-style graph description file and extracts nodes and edges.

    :param file_path: Path to the GraphEd file.
    :return: Tuple of (nodes_dict, edges_list)
    """
    nodes = {}
    edges = []

    with open(file_path, 'r') as f:
        content = f.read()

    # Match nodes: format -> ID {$ ... NP x y $}"label"
    node_pattern = re.compile(r'(\d+)\s+\{\$\s+NS.*?NP\s+(\d+)\s+(\d+)\s+\$\}"([^"]+)"', re.DOTALL)
    for match in node_pattern.finditer(content):
        node_id = int(match.group(1))
        x = int(match.group(2))
        y = int(match.group(3))
        label = match.group(4)
        nodes[node_id] = {'label': label, 'pos': (x, y)}

    # Match edges: format -> ID {$ ... EL x1 y1 x2 y2 ... $}""
    edge_pattern = re.compile(r'(\d+)\s+\{\$\s+ETI.*?EL\s+([\d\s]+)\s+\$\}"[^"]*"', re.DOTALL)
    for match in edge_pattern.finditer(content):
        edge_id = int(match.group(1))
        coords = list(map(int, match.group(2).strip().split()))
        if len(coords) >= 4:
            # Extract start and end coordinates of the polyline
            x_start, y_start = coords[0], coords[1]
            x_end, y_end = coords[-2], coords[-1]

            # Find the closest node to each endpoint (approximation)
            from_node = min(nodes, key=lambda n: (nodes[n]['pos'][0] - x_start)**2 + (nodes[n]['pos'][1] - y_start)**2)
            to_node = min(nodes, key=lambda n: (nodes[n]['pos'][0] - x_end)**2 + (nodes[n]['pos'][1] - y_end)**2)

            edges.append((from_node, to_node))

    return nodes, edges

def build_graph(nodes, edges):
    """
    Builds a NetworkX graph from node and edge data.

    :param nodes: Dictionary of node_id -> {'label': str, 'pos': (x, y)}
    :param edges: List of tuples (from_node_id, to_node_id)
    :return: A NetworkX Graph object
    """
    G = nx.Graph()
    for node_id, data in nodes.items():
        G.add_node(node_id, label=data['label'], pos=data['pos'])
    for from_node, to_node in edges:
        G.add_edge(from_node, to_node)
    return G

def export_graph(G, filename, format="graphml"):
    """
    Exports the NetworkX graph to a file in the desired format.

    :param G: NetworkX graph
    :param filename: Output file name
    :param format: Format: 'graphml', 'dot', 'gexf', or 'edgelist'
    """
    if format == "graphml":
        nx.write_graphml(G, filename)
    elif format == "dot":
        nx.nx_pydot.write_dot(G, filename)
    elif format == "gexf":
        nx.write_gexf(G, filename)
    elif format == "edgelist":
        nx.write_edgelist(G, filename)
    else:
        raise ValueError(f"Unsupported format: {format}")

# Example usage
if __name__ == "__main__":
    input_path = "graph_input.txt"  # Replace with your actual file path
    output_path = "graph_output.graphml"

    node_data, edge_data = parse_graphed_file(input_path)
    G = build_graph(node_data, edge_data)
    export_graph(G, output_path, format="graphml")