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
    with open("BPlus.json", "w") as f:
        f.write(BPlus.to_json())

    with open("BMinus.json", "w") as f:
        f.write(BMinus.to_json())

    with open("CPlus.json", "w") as f:
        f.write(CPlus.to_json())

    with open("CMinus.json", "w") as f:
        f.write(CMinus.to_json())

    with open("OPlus.json", "w") as f:
        f.write(OPlus.to_json())

    with open("OMinus.json", "w") as f:
        f.write(OMinus.to_json())

    with open("MPlus.json", "w") as f:
        f.write(MPlus.to_json())

    with open("SPlus.json", "w") as f:
        f.write(SPlus.to_json())

    with open("SMinus.json", "w") as f:
        f.write(SMinus.to_json())
