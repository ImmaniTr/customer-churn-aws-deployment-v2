import json
import sys
from pathlib import Path

METRICS_PATH = Path("metrics.json")

MIN_RECALL = 0.70
MIN_ROC_AUC = 0.80


def main() -> None:
    if not METRICS_PATH.exists():
        print("metrics.json file not found.")
        sys.exit(1)

    with METRICS_PATH.open("r", encoding="utf-8") as file:
        metrics = json.load(file)

    recall = metrics.get("recall")
    roc_auc = metrics.get("roc_auc")

    if recall is None or roc_auc is None:
        print("Required metrics are missing: recall and/or roc_auc.")
        sys.exit(1)

    print(f"Recall: {recall}")
    print(f"ROC-AUC: {roc_auc}")

    if recall < MIN_RECALL:
        print(f"Validation failed: recall {recall} is below minimum {MIN_RECALL}.")
        sys.exit(1)

    if roc_auc < MIN_ROC_AUC:
        print(f"Validation failed: ROC-AUC {roc_auc} is below minimum {MIN_ROC_AUC}.")
        sys.exit(1)

    print("Model metrics validation passed.")


if __name__ == "__main__":
    main()
