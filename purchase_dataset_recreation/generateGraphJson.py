from PurchaseBPlus import BPlus
import json


if __name__ == "__main__":
    with open("BPlus.json", "w") as f:
        f.write(json.dumps(BPlus.to_json(), indent=4))
