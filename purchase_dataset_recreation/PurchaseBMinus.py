from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

BMinus = PurchaseGraph("b-")
"""
The "b-" graph's node positions are equivalent to b+'s.
Additionally, also the connecting edges are the same as b+.
However, these edges are bent.
"""

BMinus.add_node("A", pos=(2.0, 9.5))
BMinus.add_node("E", pos=(3.0, 7.5))
BMinus.add_node("F", pos=(3.5, 4.5))

BMinus.add_edge_via("A", "E", [(2.0, 8.0)])
BMinus.add_edge_via("E", "F", [(2.5, 7.0), (3.0, 6.0), (2.5, 5.5)])

BMinus.add_node("S", pos=(5.0, 8.5))
BMinus.add_node("B", pos=(5.5, 6.5))
BMinus.add_node("T", pos=(5.0, 4.5))

BMinus.add_edge("A", "S")
BMinus.add_edge_via("A", "B", [(3.5, 8.0), (4.0, 8.5)])
BMinus.add_edge("E", "S")
BMinus.add_edge("E", "B")
BMinus.add_edge_via("F", "S", [(4.0, 7.0), (4.5, 6.5)])
BMinus.add_edge_via("F", "B", [(4.5, 6.0)])
BMinus.add_edge("F", "T")
BMinus.add_edge_via("T", "B", [(5.5, 5.5)])

BMinus.add_node("N", pos=(7.5, 9.0))
BMinus.add_node("C", pos=(7.5, 7.5))
BMinus.add_node("G", pos=(8.0, 6.0))
BMinus.add_node("H", pos=(7.5, 4.0))

BMinus.add_edge("N", "C")
BMinus.add_edge("C", "G")
BMinus.add_edge("G", "H")
BMinus.add_edge_via("B", "N", [(6.0, 8.0), (6.5, 7.5)])
BMinus.add_edge_via("B", "C", [(7.0, 6.5)])
BMinus.add_edge_via("B", "H", [(7.0, 6.0), (6.5, 5.5), (7.5, 5.0)])
BMinus.add_edge_via("T", "G", [(6.5, 5.0), (6.0, 5.5)])
BMinus.add_edge_via("F", "G", [(4.0, 3.5), (5.5, 4.0), (5.5, 3.5)])

BMinus.add_node("J", pos=(9.0, 5.5))
BMinus.add_node("I", pos=(9.0, 4.0))

BMinus.add_edge("J", "I")
BMinus.add_edge("H", "I")

BMinus.add_node("R", pos=(9.5, 8.0))
BMinus.add_node("O", pos=(10.0, 6.0))

BMinus.add_edge_via("N", "O", [(11.0, 9.0), (10.5, 7.5), (11.0, 8.0)])
BMinus.add_edge_via("C", "O", [(8.5, 7.5)])
BMinus.add_edge_via("R", "J", [(9.0, 6.5)])

BMinus.add_node("Q", pos=(11.5, 5.0))
BMinus.add_node("P", pos=(11.0, 3.0))

BMinus.add_edge_via("R", "Q", [(10.5, 6.5), (11.0, 7.0)])
BMinus.add_edge("J", "Q")
BMinus.add_edge("I", "Q")
BMinus.add_edge("Q", "P")
BMinus.add_edge_via("I", "P", [(10.5, 3.5), (10.0, 3.0)])


if __name__ == "__main__":
    BMinus.draw()
    plt.axis("scaled")
    plt.show()
