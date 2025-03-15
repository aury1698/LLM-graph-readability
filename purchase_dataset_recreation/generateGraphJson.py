from PurchaseBPlus import BPlus


if __name__ == "__main__":
    with open("BPlus.json", "w") as f:
        f.write(BPlus.to_json())
