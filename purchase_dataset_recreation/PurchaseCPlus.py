from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

CPlus = PurchaseGraph("c+")

CPlus.add_node("S", pos=(2.5, 6.0))
CPlus.add_node("E", pos=(4.0, 5.5))
CPlus.add_node("F", pos=(3.5, 2.5))
CPlus.add_node("T", pos=(5.0, 2.5))

CPlus.add_edge("S", "E")
CPlus.add_edge("S", "F")
CPlus.add_edge("F", "T")
CPlus.add_edge_via("F", "E", [(3.5, 4.0)])

CPlus.add_node("A", pos=(5.5, 6.5))
CPlus.add_node("B", pos=(5.5, 4.5))

CPlus.add_edge("S", "A")
CPlus.add_edge("E", "A")
CPlus.add_edge("E", "B")
CPlus.add_edge("F", "B")
CPlus.add_edge("T", "B")
CPlus.add_edge("A", "B")

CPlus.add_node("N", pos=(6.5, 7.0))
CPlus.add_node("C", pos=(7.5, 5.5))
CPlus.add_node("O", pos=(9.5, 7.0))

CPlus.add_edge("N", "C")
CPlus.add_edge("N", "O")
CPlus.add_edge("C", "O")
CPlus.add_edge("B", "N")
CPlus.add_edge("B", "C")
CPlus.add_edge("J", "Q")
CPlus.add_node("H", pos=(8.5, 5.0))
CPlus.add_node("I", pos=(10.0, 4.5))
CPlus.add_node("J", pos=(7.0, 4.0))
CPlus.add_node("R", pos=(6.0, 3.5))
CPlus.add_node("P", pos=(10.0, 3.0))
CPlus.add_node("Q", pos=(8.5, 3.0))

CPlus.add_edge("B", "H")
CPlus.add_edge("H", "I")
CPlus.add_edge("I", "J")
CPlus.add_edge("I", "P")
CPlus.add_edge("I", "Q")
CPlus.add_edge("J", "R")
CPlus.add_edge("J", "Q")
CPlus.add_edge("Q", "P")
CPlus.add_edge("R", "Q")

CPlus.add_node("G", pos=(10.5, 6.0))
CPlus.add_edge("C", "G")
CPlus.add_edge("H", "G")

CPlus.add_edge_via("F", "G", [(5.0, 1.5), (11.5, 1.5)])
CPlus.add_edge_via("T", "G", [(8.0, 2.0), (10.0, 2.0), (10.5, 2.5)])


if __name__ == "__main__":
    CPlus.draw()
    plt.axis("scaled")
    plt.show()
