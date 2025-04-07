from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

SPlus = PurchaseGraph("s+")
"""
The s+ graph has very wide distances between nodes.
We have determined the distance between the main nodes to be 5.0 units in the x direction,
and 2.5 units in the y direction.

As the graph is so wide, the labels are illegible on the scan of the paper.
Thus we have chosen the labels ourselves.
"""

SPlus.add_node("A", pos=(0.0, 4.0))
SPlus.add_node("B", pos=(5.0, 4.0))
SPlus.add_node("C", pos=(10.0, 4.0))
SPlus.add_node("D", pos=(15.0, 4.0))

SPlus.add_node("E", pos=(7.5, 1.5))
SPlus.add_node("F", pos=(7.5, 6.5))
SPlus.add_node("G", pos=(15.0, 6.5))

SPlus.add_node("H", pos=(5.0, 9.0))
SPlus.add_node("I", pos=(10.0, 9.0))
SPlus.add_node("J", pos=(15.0, 9.0))

SPlus.add_node("K", pos=(7.5, 11.5))

SPlus.add_node("L", pos=(17.5, 9.0))
SPlus.add_node("M", pos=(17.5, 4.0))

SPlus.add_node("N", pos=(22.5, 9.0))
SPlus.add_node("O", pos=(22.5, 4.0))
SPlus.add_node("P", pos=(25.0, 6.5))

SPlus.add_edge("A", "B")
SPlus.add_edge("A", "E")
SPlus.add_edge("A", "F")

SPlus.add_edge("B", "C")
SPlus.add_edge("B", "E")
SPlus.add_edge("B", "F")

SPlus.add_edge("C", "D")
SPlus.add_edge("C", "E")
SPlus.add_edge("C", "F")
SPlus.add_edge("C", "G")

SPlus.add_edge("D", "G")

SPlus.add_edge("F", "H")
SPlus.add_edge("F", "I")

SPlus.add_edge_via("F", "D", [(11.0, 5.0), (14.0, 5.0)])
SPlus.add_edge_via("F", "J", [(11.0, 8.0), (14.0, 8.0)])

SPlus.add_edge("G", "J")

SPlus.add_edge("H", "K")
SPlus.add_edge("H", "I")

SPlus.add_edge("I", "K")
SPlus.add_edge("I", "G")

SPlus.add_edge("J", "L")

SPlus.add_edge("L", "M")
SPlus.add_edge("M", "O")
SPlus.add_edge("O", "P")
SPlus.add_edge("P", "N")
SPlus.add_edge("N", "L")

SPlus.add_edge_via("L", "P", [(18.5, 8.0), (21.5, 8.0)])
SPlus.add_edge_via("M", "P", [(18.5, 5.0), (21.5, 5.0)])


if __name__ == "__main__":
    SPlus.draw()
    plt.axis("scaled")
    plt.show()
