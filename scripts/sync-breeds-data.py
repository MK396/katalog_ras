#!/usr/bin/env python3
"""Kopiuje data/breeds.json do js/breeds-data.js (fallback przy file://)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
breeds = json.loads((ROOT / "data" / "breeds.json").read_text(encoding="utf-8"))
out = ROOT / "js" / "breeds-data.js"
out.write_text(
    "window.BREEDS_DATA = " + json.dumps(breeds, ensure_ascii=False, separators=(",", ": ")) + ";\n",
    encoding="utf-8",
)
print("Zapisano", out)
