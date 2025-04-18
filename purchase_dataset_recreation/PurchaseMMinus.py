from PurchaseGraph import PurchaseGraph
import matplotlib.pyplot as plt

MMinus = PurchaseGraph("m-")

MMinus.add_node("O", pos=(0.5, 3.0))

MMinus.add_node("N", pos=(1.125, 6.375))
MMinus.add_node("S", pos=(2.0, 6.25))
MMinus.add_node("F", pos=(3.0, 6.375))

MMinus.add_node("A", pos=(2.25, 10.5))
MMinus.add_node("E", pos=(2.5, 7.5))

MMinus.add_node("B", pos=(3.25, 9.25))

MMinus.add_node("T", pos=(3.75, 2.75))
MMinus.add_node("G", pos=(3.25, 0.5))

MMinus.add_node("P", pos=(4.0, 8.25))
MMinus.add_node("C", pos=(4.5, 2.75))
MMinus.add_node("H", pos=(4.75, 1.25))

MMinus.add_node("Q", pos=(5.5, 6.0))
MMinus.add_node("I", pos=(5.75, 3.5))

MMinus.add_node("J", pos=(7.25, 1.5))
MMinus.add_node("R", pos=(8.5, 0.25))

MMinus.add_edge_via("O", "N", [(2.25, 4.5)])
MMinus.add_edge_via("O", "C", [(2.5, 4.5)])

MMinus.add_edge("N", "B")
MMinus.add_edge("N", "C")

MMinus.add_edge("A", "S")
MMinus.add_edge("A", "E")
MMinus.add_edge("A", "B")

MMinus.add_edge("B", "E")
MMinus.add_edge("B", "F")
MMinus.add_edge("B", "T")
MMinus.add_edge("B", "C")
MMinus.add_edge_via("B", "H", [(5.25, 3.0)])

MMinus.add_edge("C", "G")

MMinus.add_edge("E", "S")
MMinus.add_edge_via("E", "F", [(3.0, 8.25)])

MMinus.add_edge("F", "T")
MMinus.add_edge_via("F", "G", [(3.0, 1.25), (3.25, 2.5)])


MMinus.add_edge("G", "T")
MMinus.add_edge("G", "H")

MMinus.add_edge("H", "I")

MMinus.add_edge("I", "J")
MMinus.add_edge("I", "P")
MMinus.add_edge("I", "Q")

MMinus.add_edge("J", "R")
MMinus.add_edge("J", "Q")


MMinus.add_edge("P", "Q")

MMinus.add_edge("R", "Q")





if __name__ == "__main__":
    # needs overriding for different scale
    DRAW_WIDTH = 1024
    DRAW_HEIGHT = 1024
    DRAW_DPI = 160
    DRAW_FIGSIZE = (DRAW_WIDTH / DRAW_DPI, DRAW_HEIGHT / DRAW_DPI)

    fig = plt.figure(figsize=(DRAW_FIGSIZE), dpi=DRAW_DPI)
    MMinus.draw()
    plt.axis("scaled")
    plt.savefig(
        f"dataset_png/{MMinus.purchase_name}.png",
        dpi=DRAW_DPI,
    )
