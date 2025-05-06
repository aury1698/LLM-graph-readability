from PurchaseGraph import PurchaseGraph, DRAW_FIGSIZE, DRAW_DPI
import matplotlib.pyplot as plt

CMinus = PurchaseGraph("c-")

CMinus.add_node("A", pos=(2.0, 8.0))
CMinus.add_node("E", pos=(2.5, 6.0))
CMinus.add_node("J", pos=(2.5, 4.0))
CMinus.add_node("H", pos=(3.5, 2.5))

CMinus.add_node("F", pos=(4.0, 9.5))
CMinus.add_node("B", pos=(4.0, 5.0))

CMinus.add_node("S", pos=(6.0, 6.5))
CMinus.add_node("T", pos=(5.5, 5.5))

CMinus.add_node("C", pos=(7.0, 9.5))
CMinus.add_node("N", pos=(7.0, 1.5))

CMinus.add_node("G", pos=(8.0, 5.5))

CMinus.add_node("I", pos=(9.5, 3.0))

CMinus.add_node("R", pos=(10.5, 6.5))
CMinus.add_node("P", pos=(11.0, 7.5))

CMinus.add_node("Q", pos=(11.5, 4.5))
CMinus.add_node("O", pos=(12.0, 6.0))


CMinus.add_edge("A", "E")
CMinus.add_edge("A", "B")
CMinus.add_edge("A", "S")

CMinus.add_edge("E", "F")
CMinus.add_edge("E", "B")
CMinus.add_edge("E", "S")

CMinus.add_edge("F", "B")
CMinus.add_edge("F", "T")
CMinus.add_edge("F", "S")
CMinus.add_edge("F", "G")

CMinus.add_edge("J", "Q")
CMinus.add_edge_via("J", "R", [(3.5, 8.0)])
CMinus.add_edge("J", "I")

CMinus.add_edge("H", "B")
CMinus.add_edge("H", "G")
CMinus.add_edge("H", "I")

CMinus.add_edge("B", "T")
CMinus.add_edge("B", "C")
CMinus.add_edge("B", "N")

CMinus.add_edge("T", "G")

CMinus.add_edge("C", "N")
CMinus.add_edge("C", "G")
CMinus.add_edge_via("C", "O", [(9.0, 5.5)])

CMinus.add_edge_via("N", "O", [(8.5, 5.0)])

CMinus.add_edge("I", "Q")
CMinus.add_edge_via("I", "P", [(9.5, 7.0)])

CMinus.add_edge("Q", "R")
CMinus.add_edge("Q", "P")


if __name__ == "__main__":
    fig = plt.figure(figsize=(DRAW_FIGSIZE), dpi=DRAW_DPI)
    CMinus.draw()
    plt.axis("scaled")
    plt.savefig(
        f"dataset_png/{CMinus.purchase_name}.png",
        dpi=DRAW_DPI,
    )
