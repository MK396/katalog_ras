#!/usr/bin/env python3
"""
Zmniejsza obrazy do maks. ramki bez przycinania (cały pies widoczny w UI z object-fit: contain):
  - images/{id}.jpg  → mieści się w 760×460
  - images/hero.jpg   → mieści się w 1920×840
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "images"
BREED_MAX = (760, 460)
HERO_MAX = (1920, 840)


def fit_inside(src: Path, dst: Path, max_w: int, max_h: int) -> None:
    subprocess.run(
        [
            "convert",
            str(src),
            "-resize",
            f"{max_w}x{max_h}>",
            "-strip",
            "-quality",
            "85",
            str(dst),
        ],
        check=True,
    )


def main() -> None:
    breeds = json.loads((ROOT / "data" / "breeds.json").read_text(encoding="utf-8"))
    hero = SRC / "hero.jpg"
    if hero.is_file():
        fit_inside(hero, hero, *HERO_MAX)

    for breed in breeds:
        breed_id = breed["id"]
        path = SRC / f"{breed_id}.jpg"
        if not path.is_file():
            raise SystemExit(f"Brak pliku: {path}")
        fit_inside(path, path, *BREED_MAX)
        breed.pop("imageModal", None)
        breed["image"] = f"images/{breed_id}.jpg"

    (ROOT / "data" / "breeds.json").write_text(
        json.dumps(breeds, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Rasy: max {BREED_MAX[0]}×{BREED_MAX[1]} (bez kadrowania)")
    print(f"Hero: max {HERO_MAX[0]}×{HERO_MAX[1]} (bez kadrowania)")


if __name__ == "__main__":
    main()
