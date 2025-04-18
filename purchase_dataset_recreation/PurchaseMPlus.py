from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

MPlus = PurchaseGraph("m+")

MPlus.add_node("S", pos=(4.0, 7.25))
MPlus.add_node("A", pos=(5.0, 10.25))

MPlus.add_node("R", pos=(5.25, 2.0))

MPlus.add_node("E", pos=(5.75, 7.75))
MPlus.add_node("F", pos=(6.5, 5.25))

MPlus.add_node("N", pos=(8.5, 10.5))
MPlus.add_node("B", pos=(7.5, 8.25))
MPlus.add_node("T", pos=(8.0, 6.25))
MPlus.add_node("J", pos=(7.75, 4.25))

MPlus.add_node("C", pos=(9.25, 9.0))
MPlus.add_node("Q", pos=(9.25, 2.5))

MPlus.add_node("O", pos=(11.0, 10.0))
MPlus.add_node("H", pos=(10.0, 6.5))

MPlus.add_node("K", pos=(12.0, 6.25))
MPlus.add_node("I", pos=(11.0, 5.0))
MPlus.add_node("L", pos=(13.0, 4.25))


MPlus.add_edge("S", "E")
MPlus.add_edge_via("S", "F", [(3.0, 3.0)])

MPlus.add_edge("A", "E")
MPlus.add_edge("A", "B")
MPlus.add_edge_via("A", "S", [(1.0, 10.0)])

MPlus.add_edge("B", "T")
MPlus.add_edge("B", "E")
MPlus.add_edge("B", "N")
MPlus.add_edge("B", "C")
MPlus.add_edge("B", "K")

MPlus.add_edge("C", "O")
MPlus.add_edge("C", "H")
MPlus.add_edge("C", "N")
MPlus.add_edge_via("N", "O", [(11.0, 12.0), (12.0, 10.5)])

MPlus.add_edge("E", "F")
MPlus.add_edge("F", "B")
MPlus.add_edge("F", "T")
MPlus.add_edge_via("F", "H", [(7.25, 2.5), (9.5, 1.5), (10.5, 2.75)])

MPlus.add_edge("T", "H")
MPlus.add_edge("H", "K")
MPlus.add_edge("K", "I")

MPlus.add_edge("I", "L")
MPlus.add_edge("I", "Q")

MPlus.add_edge("J", "Q")
MPlus.add_edge_via("J", "R", [(6.0, 4.0)])
MPlus.add_edge_via("J", "I", [(9.0, 5.5)])

MPlus.add_edge_via("R", "Q", [(7.5, 0.5)])
MPlus.add_edge_via("Q", "L", [(11.0, 0.5)])


if __name__ == "__main__":
    # needs overriding for different scale
    DRAW_WIDTH = 1024
    DRAW_HEIGHT = 1024
    DRAW_DPI = 120
    DRAW_FIGSIZE = (DRAW_WIDTH / DRAW_DPI, DRAW_HEIGHT / DRAW_DPI)

    fig = plt.figure(figsize=(DRAW_FIGSIZE), dpi=DRAW_DPI)
    MPlus.draw()
    plt.axis("scaled")
    plt.savefig(
        f"dataset_png/{MPlus.purchase_name}.png",
        dpi=DRAW_DPI,
    )
