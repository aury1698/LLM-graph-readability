from PurchaseBPlus import BPlus
from PurchaseBMinus import BMinus


if __name__ == "__main__":
    with open("BPlus.json", "w") as f:
        f.write(BPlus.to_json())

    with open("BMinus.json", "w") as f:
        f.write(BMinus.to_json())
