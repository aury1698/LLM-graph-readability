from PurchaseGraph import PurchaseGraph, DRAW_FIGSIZE, DRAW_DPI
import matplotlib.pyplot as plt

SMinus = PurchaseGraph("s-")
"""
The s- graph has very wide distances between nodes.

As the graph is so wide, the labels are illegible on the online obtainable scan of the paper.
Thanks to Niko's high resolution scans of the paper, we were able to determine the labels of the nodes afterall.
"""

SMinus.add_node("R", pos=(1.0, 14.0))
SMinus.add_node("F", pos=(1.0, 10.0))

SMinus.add_node("C", pos=(6.0, 8.0))

SMinus.add_node("E", pos=(7.0, 11.0))

SMinus.add_node("G", pos=(10.0, 1.0))
SMinus.add_node("T", pos=(10.0, 8.0))

SMinus.add_node("O", pos=(11.0, 4.0))
SMinus.add_node("H", pos=(11.0, 10.0))

SMinus.add_node("S", pos=(12.0, 15.0))

SMinus.add_node("N", pos=(15.0, 6.0))
SMinus.add_node("A", pos=(15.0, 13.0))

SMinus.add_node("P", pos=(16.0, 13.0))

SMinus.add_node("M", pos=(17.0, 7.0))

SMinus.add_node("Q", pos=(19.0, 17.0))

SMinus.add_node("I", pos=(20.0, 10.0))

SMinus.add_node("J", pos=(21.0, 18.0))

SMinus.add_edge("R", "Q")
SMinus.add_edge_via("R", "J", [(9.5, 16.5)])

SMinus.add_edge("F", "S")
SMinus.add_edge("F", "E")
SMinus.add_edge("F", "H")
SMinus.add_edge("F", "T")
SMinus.add_edge("F", "G")

SMinus.add_edge("C", "H")
SMinus.add_edge("C", "O")
SMinus.add_edge("C", "N")
SMinus.add_edge("C", "G")

SMinus.add_edge("E", "S")
SMinus.add_edge_via("E", "A", [(11.0, 13.0)])
SMinus.add_edge("E", "H")

SMinus.add_edge("G", "M")
SMinus.add_edge("G", "T")

SMinus.add_edge("T", "H")

SMinus.add_edge("O", "N")

SMinus.add_edge("H", "A")
SMinus.add_edge("H", "M")
SMinus.add_edge("H", "N")

SMinus.add_edge("S", "A")

# we cant see whether those are connected or not
SMinus.add_edge("A", "P")

SMinus.add_edge("P", "Q")
SMinus.add_edge("P", "I")

SMinus.add_edge("M", "I")

SMinus.add_edge("Q", "J")
SMinus.add_edge("Q", "I")

SMinus.add_edge_via("I", "J", [(21.0, 11.0)])


if __name__ == "__main__":
    # needs overriding for different scale
    DRAW_WIDTH = 1024
    DRAW_HEIGHT = 1024
    DRAW_DPI = 80
    DRAW_FIGSIZE = (DRAW_WIDTH / DRAW_DPI, DRAW_HEIGHT / DRAW_DPI)

    fig = plt.figure(figsize=(DRAW_FIGSIZE), dpi=DRAW_DPI)
    SMinus.draw()
    plt.axis("scaled")
    plt.savefig(
        f"dataset_png/{SMinus.purchase_name}.png",
        dpi=DRAW_DPI,
    )
