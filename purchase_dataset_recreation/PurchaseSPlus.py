from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

SPlus = PurchaseGraph("s+")
"""
The s+ graph has very wide distances between nodes.
We have determined the distance between the main nodes to be 5.0 units in the x direction,
and 2.5 units in the y direction.

As the graph is so wide, the labels are illegible on the online obtainable scan of the paper.
Thanks to Niko's high resolution scans of the paper, we were able to determine the labels of the nodes afterall.
"""

SPlus.add_node("A", pos=(0.0, 4.0))
SPlus.add_node("E", pos=(5.0, 4.0))
SPlus.add_node("F", pos=(10.0, 4.0))
SPlus.add_node("T", pos=(15.0, 4.0))

SPlus.add_node("S", pos=(7.5, 1.5))
SPlus.add_node("K", pos=(7.5, 6.5))
# Node "G" is completely illegible in the paper and all existing scans.
# We will assume it is a "G".
SPlus.add_node("G", pos=(15.0, 6.5))

SPlus.add_node("N", pos=(5.0, 9.0))
SPlus.add_node("C", pos=(10.0, 9.0))
SPlus.add_node("M", pos=(15.0, 9.0))

SPlus.add_node("O", pos=(7.5, 11.5))

SPlus.add_node("I", pos=(17.5, 9.0))
SPlus.add_node("J", pos=(17.5, 4.0))

SPlus.add_node("P", pos=(22.5, 9.0))
SPlus.add_node("R", pos=(22.5, 4.0))
SPlus.add_node("Q", pos=(25.0, 6.5))

SPlus.add_edge("A", "E")
SPlus.add_edge("A", "S")
SPlus.add_edge("A", "K")

SPlus.add_edge("E", "F")
SPlus.add_edge("E", "S")
SPlus.add_edge("E", "K")

SPlus.add_edge("F", "T")
SPlus.add_edge("F", "S")
SPlus.add_edge("F", "K")
SPlus.add_edge("F", "G")

SPlus.add_edge("T", "G")

SPlus.add_edge("K", "N")
SPlus.add_edge("K", "C")

SPlus.add_edge_via("K", "T", [(11.0, 5.25), (13.75, 5.25)])
SPlus.add_edge_via("K", "M", [(11.0, 7.75), (13.75, 7.75)])

SPlus.add_edge("G", "M")

SPlus.add_edge("N", "O")
SPlus.add_edge("N", "C")

SPlus.add_edge("C", "O")
SPlus.add_edge("C", "G")

SPlus.add_edge("M", "I")

SPlus.add_edge("I", "J")
SPlus.add_edge("J", "R")
SPlus.add_edge("R", "Q")
SPlus.add_edge("Q", "P")
SPlus.add_edge("P", "I")

SPlus.add_edge_via("I", "Q", [(18.75, 7.75), (21.5, 7.75)])
SPlus.add_edge_via("J", "Q", [(18.75, 5.25), (21.5, 5.25)])


if __name__ == "__main__":
    # needs overriding for different scale
    DRAW_WIDTH = 1024
    DRAW_HEIGHT = 1024
    DRAW_DPI = 90
    DRAW_FIGSIZE = (DRAW_WIDTH / DRAW_DPI, DRAW_HEIGHT / DRAW_DPI)

    fig = plt.figure(figsize=(DRAW_FIGSIZE), dpi=DRAW_DPI)
    SPlus.draw()
    plt.axis("scaled")
    plt.savefig(
        f"dataset_png/{SPlus.purchase_name}.png",
        dpi=DRAW_DPI,
    )
