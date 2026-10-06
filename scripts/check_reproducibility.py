#!/usr/bin/env python3
"""Verify deterministic regeneration of all committed synthetic CSV files."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

TRACKED = [
    ROOT / "data" / "sample_products.csv",
    ROOT / "data" / "sample_sales_90_days.csv",
    ROOT / "data" / "sample_stock_batches.csv",
    ROOT / "data" / "sample_inventory_snapshot.csv",
]


def main() -> None:
    before = {path: path.read_bytes() for path in TRACKED}

    try:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "generate_sample_data.py")],
            cwd=ROOT,
            check=True,
        )

        changed = [
            str(path.relative_to(ROOT))
            for path, original in before.items()
            if path.read_bytes() != original
        ]
    finally:
        for path, original in before.items():
            path.write_bytes(original)

    if changed:
        print("REPRODUCIBILITY FAILED")
        for rel in changed:
            print(f" - regenerated file differs: {rel}")
        raise SystemExit(1)

    print("REPRODUCIBILITY PASS")
    print("PASS | fixed seed 20260826")
    print("PASS | all four committed CSV files regenerate byte-for-byte")


if __name__ == "__main__":
    main()
