from PurchaseGraph import PurchaseGraph, DRAW_FIGSIZE, DRAW_DPI
import matplotlib.pyplot as plt

BPlus = PurchaseGraph("b+")

BPlus.add_node("A", pos=(2.0, 9.5))
BPlus.add_node("E", pos=(3.0, 7.5))
BPlus.add_node("F", pos=(3.5, 4.5))

BPlus.add_edge("A", "E")
BPlus.add_edge("E", "F")

BPlus.add_node("S", pos=(5.0, 8.5))
BPlus.add_node("B", pos=(5.5, 6.5))
BPlus.add_node("T", pos=(5.0, 4.5))

BPlus.add_edge("A", "S")
BPlus.add_edge("A", "B")
BPlus.add_edge("E", "S")
BPlus.add_edge("E", "B")
BPlus.add_edge("F", "S")
BPlus.add_edge("F", "B")
BPlus.add_edge("F", "T")
BPlus.add_edge("T", "B")

BPlus.add_node("N", pos=(7.5, 9.0))
BPlus.add_node("C", pos=(7.5, 7.5))
BPlus.add_node("G", pos=(8.0, 6.0))
BPlus.add_node("H", pos=(7.5, 4.0))

BPlus.add_edge("N", "C")
BPlus.add_edge("C", "G")
BPlus.add_edge("G", "H")
BPlus.add_edge("B", "N")
BPlus.add_edge("B", "C")
BPlus.add_edge("B", "H")
BPlus.add_edge("T", "G")

BPlus.add_edge_via("F", "G", [(5.0, 3.5)])

BPlus.add_node("J", pos=(9, 5.5))
BPlus.add_node("I", pos=(9, 4.0))

BPlus.add_edge("J", "I")
BPlus.add_edge("H", "I")

BPlus.add_node("R", pos=(9.5, 8.0))
BPlus.add_node("O", pos=(10.0, 6.0))

BPlus.add_edge("N", "O")
BPlus.add_edge("C", "O")
BPlus.add_edge("R", "J")

BPlus.add_node("Q", pos=(11.5, 5.0))
BPlus.add_node("P", pos=(11.0, 3.0))

BPlus.add_edge("R", "Q")
BPlus.add_edge("J", "Q")
BPlus.add_edge("I", "Q")
BPlus.add_edge("Q", "P")
BPlus.add_edge("I", "P")


if __name__ == "__main__":
    fig = plt.figure(figsize=(DRAW_FIGSIZE), dpi=DRAW_DPI)
    BPlus.draw()
    plt.axis("scaled")
    plt.savefig(
        f"dataset_png/{BPlus.purchase_name}.png",
        dpi=DRAW_DPI,
    )
