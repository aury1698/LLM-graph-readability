from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

OPlus = PurchaseGraph("o+")

OPlus.add_node("A", pos=(2.0, 10.0))
OPlus.add_node("E", pos=(2.0, 8.0))
OPlus.add_node("F", pos=(2.0, 4.0))

OPlus.add_node("S", pos=(4.0, 8.0))
OPlus.add_node("B", pos=(4.0, 6.0))
OPlus.add_node("T", pos=(4.0, 4.0))

OPlus.add_node("N", pos=(6.0, 10.0))
OPlus.add_node("C", pos=(6.0, 8.0))
OPlus.add_node("G", pos=(6.0, 6.0))
OPlus.add_node("H", pos=(6.0, 4.0))

OPlus.add_node("R", pos=(8.0, 8.0))
OPlus.add_node("J", pos=(8.0, 6.0))
OPlus.add_node("I", pos=(8.0, 4.0))

OPlus.add_node("O", pos=(10.0, 6.0))
OPlus.add_node("Q", pos=(10.0, 4.0))
OPlus.add_node("P", pos=(10.0, 2.0))

OPlus.add_edge("A", "E")
OPlus.add_edge("A", "B")
OPlus.add_edge_via("A", "S", [(4.0, 10.0)])

OPlus.add_edge("E", "S")
OPlus.add_edge("E", "B")
OPlus.add_edge("E", "F")

OPlus.add_edge("F", "S")
OPlus.add_edge("F", "B")
OPlus.add_edge("F", "T")
OPlus.add_edge_via("F", "G", [(2.0, 2.0), (4.0, 2.0)])

OPlus.add_edge("B", "N")
OPlus.add_edge("B", "C")
OPlus.add_edge("B", "T")
OPlus.add_edge_via("B", "H", [(5.0, 6.0)])

OPlus.add_edge("T", "G")

OPlus.add_edge("N", "C")
OPlus.add_edge_via("N", "O", [(10.0, 10.0)])

OPlus.add_edge("C", "G")
OPlus.add_edge("C", "O")

OPlus.add_edge("G", "H")

OPlus.add_edge("H", "I")

OPlus.add_edge("R", "J")
OPlus.add_edge("R", "Q")

OPlus.add_edge("J", "I")
OPlus.add_edge("J", "Q")

OPlus.add_edge_via("I", "P", [(8.0,2.0)])

OPlus.add_edge("Q", "P")


if __name__ == "__main__":
    OPlus.draw()
    plt.axis("scaled")
    plt.show()
