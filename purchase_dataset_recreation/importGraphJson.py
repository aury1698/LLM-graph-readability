import sys
from PurchaseGraph import load_graph_json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python importGraphJson.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    graph = load_graph_json(input_file)

    graph.draw()
    plt.axis("scaled")
    plt.show()
