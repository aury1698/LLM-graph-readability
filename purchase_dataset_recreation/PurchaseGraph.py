import networkx as nx
import json
from networkx.readwrite import json_graph

DRAW_OPTIONS = {
    # node styling
    "node_color": "white",
    "edgecolors": "black",
    "node_size": 1300,
    "linewidths": 2.7,
    "with_labels": True,
    "font_size": 13,
    "font_weight": "bold",
    "font_family": "monospace",
    # edge styling
    "edge_color": "black",
    # general line styling
    "width": 2.7,
}

DRAW_WIDTH = 1024
DRAW_HEIGHT = 1024
DRAW_DPI = 170
DRAW_FIGSIZE = (DRAW_WIDTH / DRAW_DPI, DRAW_HEIGHT / DRAW_DPI)


class PurchaseGraph(nx.Graph):
    """
    PurchaseGraph is a subclass of networkx.Graph that adds
    an additional method to draw the graph with edges, which
    can be bent at specified coordinates.

    This is used to draw the graphs in the purchase dataset.

    Additionally, it adds a method to convert the graph to
    json format, which is used to save the graph to a file.
    """

    def __init__(self, purchase_name: str):
        super().__init__()
        self.purchase_name = purchase_name

    def draw(self, ax=None, color_map: dict[str, str] = {}, with_labels: bool = True):
        pos = nx.get_node_attributes(self, "pos")

        # filter out invisible nodes, additionally the invisible labels must be manually excluded.
        filtered_nodes = {
            node
            for node in self.nodes()
            if not self.nodes[node].get("invisible", False)
        }
        # if the node is invisible, we replace the label with a dot
        filtered_labels = {
            label: label if label in filtered_nodes else "" for label in self.nodes()
        }

        DRAW_OPTIONS_COPY = DRAW_OPTIONS.copy()

        # if the color_map is non-empty, we use it to color the nodes
        if color_map:
            color_list = [
                color_map.get(node) if node in color_map else DRAW_OPTIONS["node_color"] for node in filtered_nodes
            ]
            DRAW_OPTIONS_COPY["node_color"] = color_list

        DRAW_OPTIONS_COPY["with_labels"] = with_labels

        nx.draw(
            self,
            pos,
            ax,
            nodelist=filtered_nodes,
            labels=filtered_labels,
            **DRAW_OPTIONS_COPY,
        )

    def to_json(self) -> dict:
        return json.dumps(json_graph.node_link_data(self, edges="edges"), indent=2)

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
                node2 = f"{u_of_edge}_{v_of_edge}_via{i}"
                self.add_node(node2, pos=coords[i], invisible=True)
                # add edge between the two nodes, purposfully not adding the **attr
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
