from __future__ import annotations

from pathlib import Path
from shutil import copyfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "synthetic_support_dataset.json"
TARGET = ROOT / "data" / "synthetic_support_dataset.json"


if __name__ == "__main__":
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    copyfile(SOURCE, TARGET)
    print(f"Seeded dataset to {TARGET}")
