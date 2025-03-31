from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

OMinus = PurchaseGraph("o-")
"""
The o- graph is equivalent to o+, however the node and edge positions are different,
ensuring no nodes are aligned orthogonally.

Therefore it also makes use of 0.25 steps in the x and y axis, which we don't
need or use in the other graphs.
"""

OMinus.add_node("A", pos=(1.75, 9.0))
OMinus.add_node("E", pos=(1.5, 7.0))
OMinus.add_node("F", pos=(0.5, 4.0))

OMinus.add_node("S", pos=(3.25, 7.0))
OMinus.add_node("B", pos=(3.0, 5.0))
OMinus.add_node("T", pos=(3.0, 3.0))

OMinus.add_node("N", pos=(6.0, 8.5))
OMinus.add_node("C", pos=(5.5, 7.0))
OMinus.add_node("G", pos=(5.0, 5.5))
OMinus.add_node("H", pos=(5.75, 3.5))

OMinus.add_node("R", pos=(7.75, 7.0))
OMinus.add_node("J", pos=(6.0, 5.0))
OMinus.add_node("I", pos=(7.0, 2.25))

OMinus.add_node("O", pos=(7.75, 5.0))
OMinus.add_node("Q", pos=(9.75, 3.0))
OMinus.add_node("P", pos=(9.25, 1.25))

OMinus.add_edge("A", "E")
OMinus.add_edge("A", "B")
OMinus.add_edge_via("A", "S", [(3.5, 8.75)])

OMinus.add_edge("E", "S")
OMinus.add_edge("E", "B")
OMinus.add_edge("E", "F")

OMinus.add_edge("F", "S")
OMinus.add_edge("F", "B")
OMinus.add_edge("F", "T")
OMinus.add_edge_via("F", "G", [(2.5, 1.0), (4.0, 2.25)])

OMinus.add_edge("B", "N")
OMinus.add_edge("B", "C")
OMinus.add_edge("B", "T")
OMinus.add_edge_via("B", "H", [(4.25, 5.0)])

OMinus.add_edge("N", "C")
OMinus.add_edge_via("N", "O", [(9.5, 7.0)])

OMinus.add_edge("C", "G")
OMinus.add_edge("C", "O")

OMinus.add_edge("G", "H")

OMinus.add_edge("H", "I")

OMinus.add_edge("R", "J")
OMinus.add_edge("R", "Q")

OMinus.add_edge("J", "I")
OMinus.add_edge("J", "Q")

OMinus.add_edge_via("I", "P", [(8.0, 1.25)])
OMinus.add_edge("I", "Q")

OMinus.add_edge("Q", "P")

OMinus.add_edge("T", "G")

if __name__ == "__main__":
    print(OMinus.to_json())

    OMinus.draw()
    plt.axis("scaled")
    plt.show()
