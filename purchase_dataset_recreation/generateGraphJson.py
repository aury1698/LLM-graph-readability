from PurchaseBPlus import BPlus
from PurchaseBMinus import BMinus
from PurchaseCMinus import CMinus
from PurchaseCPlus import CPlus
from PurchaseOPlus import OPlus
from PurchaseOMinus import OMinus
from PurchaseMPlus import MPlus
from PurchaseSPlus import SPlus
from PurchaseSMinus import SMinus


if __name__ == "__main__":
    graph = BPlus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = BMinus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = CPlus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = CMinus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = MPlus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = OPlus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = OMinus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = SPlus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

    graph = SMinus

    with open(f"dataset_json/{graph.purchase_name}.json", "w") as f:
        f.write(graph.to_json())

