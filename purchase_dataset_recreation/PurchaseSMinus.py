from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

SMinus = PurchaseGraph("s-")
"""
The s- graph has very wide distances between nodes.

As the graph is so wide, the labels are illegible on the scan of the paper.
Thus we have chosen the labels ourselves.
"""

SMinus.add_node("A", pos=(1.0, 14.0))
SMinus.add_node("B", pos=(1.0, 10.0))

SMinus.add_node("C", pos=(6.0, 8.0))

SMinus.add_node("D", pos=(7.0, 11.0))

SMinus.add_node("E", pos=(10.0, 1.0))
SMinus.add_node("F", pos=(10.0, 8.0))

SMinus.add_node("G", pos=(11.0, 4.0))
SMinus.add_node("H", pos=(11.0, 10.0))

SMinus.add_node("I", pos=(12.0, 15.0))

SMinus.add_node("J", pos=(15.0, 6.0))
SMinus.add_node("K", pos=(15.0, 13.0))

SMinus.add_node("L", pos=(16.0, 13.0))

SMinus.add_node("M", pos=(17.0, 7.0))

SMinus.add_node("N", pos=(19.0, 17.0))

SMinus.add_node("O", pos=(20.0, 10.0))

SMinus.add_node("P", pos=(21.0, 18.0))

SMinus.add_edge("A", "N")
SMinus.add_edge_via("A", "P", [(9.5, 16.5)])

SMinus.add_edge("B", "I")
SMinus.add_edge("B", "D")
SMinus.add_edge("B", "H")
SMinus.add_edge("B", "F")
SMinus.add_edge("B", "E")

SMinus.add_edge("C", "H")
SMinus.add_edge("C", "G")
SMinus.add_edge("C", "J")
SMinus.add_edge("C", "E")

SMinus.add_edge("D", "I")
SMinus.add_edge_via("D", "K", [(11.0, 13.0)])
SMinus.add_edge("D", "H")

SMinus.add_edge("E", "M")
SMinus.add_edge("E", "F")

SMinus.add_edge("F", "H")

SMinus.add_edge("G", "J")

SMinus.add_edge("H", "K")
SMinus.add_edge("H", "M")
SMinus.add_edge("H", "J")

SMinus.add_edge("I", "K")

# we cant see whether those are connected or not
SMinus.add_edge("K", "L")

SMinus.add_edge("L", "N")
SMinus.add_edge("L", "O")

SMinus.add_edge("M", "O")

SMinus.add_edge("N", "P")
SMinus.add_edge("N", "O")

SMinus.add_edge_via("O", "P", [(21.0, 11.0)])


if __name__ == "__main__":
    SMinus.draw()
    plt.axis("scaled")
    plt.show()
