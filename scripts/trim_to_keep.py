"""Trim images + breeds.json (+ breeds-data.js) to keep_ids.txt. Always keeps hero.*"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEEP = set(p.strip() for p in (ROOT / "keep_ids.txt").read_text(encoding="utf-8").splitlines() if p.strip())
KEEP_FILES = KEEP | {"hero"}

img_dir = ROOT / "images"
removed = []
for f in list(img_dir.iterdir()):
    if not f.is_file():
        continue
    if f.stem not in KEEP_FILES:
        f.unlink()
        removed.append(f.name)

breeds_path = ROOT / "data" / "breeds.json"
breeds = json.loads(breeds_path.read_text(encoding="utf-8"))
filtered = [b for b in breeds if Path(b["image"]).stem in KEEP]
breeds_path.write_text(json.dumps(filtered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

data_js = ROOT / "js" / "breeds-data.js"
if data_js.exists():
    data_js.write_text(
        "window.BREEDS_DATA = " + json.dumps(filtered, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )

# size report
total = sum(f.stat().st_size for f in img_dir.iterdir() if f.is_file())
print(f"kept_breeds={len(filtered)} images={len(list(img_dir.iterdir()))} removed={len(removed)} MB={total/1024/1024:.2f}")
