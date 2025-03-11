import networkx as nx
import json
from networkx.readwrite import json_graph

DRAW_OPTIONS = {
    # node styling
    "node_color": "white",
    "edgecolors": "black",
    "node_size": 1000,
    "linewidths": 3,
    "with_labels": True,
    "font_size": 11,
    "font_weight": "bold",
    "font_family": "monospace",
    # edge styling
    "edge_color": "black",
    # general line styling
    "width": 3,
}


class PurchaseGraph(nx.Graph):
    def __init__(self, purchase_name: str):
        super().__init__()
        self.purchase_name = purchase_name

    def draw(self):
        pos = nx.get_node_attributes(self, "pos")

        # filter out invisible nodes, additionally the invisible labels must be manually excluded.
        filtered_nodes = {
            node
            for node in self.nodes()
            if not self.nodes[node].get("invisible", False)
        }
        labels = {node: node for node in filtered_nodes}

        nx.draw(self, pos, nodelist=filtered_nodes, labels=labels, **DRAW_OPTIONS)

    def to_json(self) -> dict:
        return json_graph.node_link_data(self, edges="edges")

    def add_edge_via(self, u_of_edge, v_of_edge, coords: list, **attr):
        """
        add_edge_via allows to draw edges with bends at the specified coordinates.

        The coordinates are a list of tuples, where each tuple is a point in the edge.

        As networkx does not support edges with bends, we add invisible nodes to the graph
        and connect them with edges.
        """

        if len(coords) == 0:
            self.add_edge(u_of_edge, v_of_edge, **attr)
        else:
            node1 = f"{u_of_edge}_{v_of_edge}_via0"
            self.add_node(node1, pos=coords[0], invisible=True)
            self.add_edge(u_of_edge, node1, **attr)

            for i in range(1, len(coords)):
                node2 = f"{u_of_edge}_{v_of_edge}_via{i + 1}"
                self.add_node(
                    f"{u_of_edge}_{v_of_edge}_via{i + 1}", pos=coords[i], invisible=True
                )
                # add edge between the two nodes, purposedly not adding the **attr
                self.add_edge(node1, node2)
                node1 = node2
            self.add_edge(node1, v_of_edge)


def load_graph_json(json_file: str) -> PurchaseGraph:
    """
    Load a graph from a json file.
    Uses the networkx json graph format and loads using the node_link_graph function.
    It then simply changes the class to PurchaseGraph so we have access to our custom methods.
    """
    with open(json_file, "r") as f:
        data = json.load(f)

    g = json_graph.node_link_graph(data, edges="edges")
    # hack the class to be PurchaseGraph
    g.__class__ = PurchaseGraph
    return g
