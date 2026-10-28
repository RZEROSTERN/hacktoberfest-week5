"""Export selected original art as WebP and create review previews.

Run with a repository-local environment containing Pillow 13.0.0. Originals stay
under .dev/art-sources; the committed manifest records their SHA-256 hashes.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, cast

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets/manifest.json"
ART = ROOT / "assets/art"
SOURCES = ROOT / ".dev/art-sources"
REVISIONS = {
    "title",
    "memory-radio",
    "memory-letter",
    "ending-peace",
    "ending-bittersweet",
    "ending-forgotten",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export_assets() -> list[dict[str, Any]]:
    manifest: dict[str, Any] = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries: list[dict[str, Any]] = manifest["images"]
    ART.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    total = 0
    for entry in entries:
        identifier = entry["id"]
        if identifier in seen or entry["filename"] != f"{identifier}.webp":
            raise ValueError("Duplicate or invalid asset filename")
        if not identifier or any(
            c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in identifier
        ):
            raise ValueError("Unsafe asset identifier")
        seen.add(identifier)
        version = 2 if identifier in REVISIONS else 1
        source = SOURCES / f"{identifier}-v{version}.png"
        output = ART / entry["filename"]
        with Image.open(source) as image:
            if image.format != "PNG":
                raise ValueError(f"Expected PNG original: {source}")
            if entry["transparent"]:
                if image.mode != "RGBA":
                    raise ValueError(f"Missing alpha channel: {source}")
                low, high = cast(tuple[int, int], image.getchannel("A").getextrema())
                if low != 0 or high < 250:
                    raise ValueError(f"Invalid transparency range: {source}")
            elif image.mode == "RGBA" and image.getchannel("A").getextrema()[0] != 255:
                raise ValueError(f"Opaque scene unexpectedly has transparency: {source}")
            expected_ratio = entry["width"] / entry["height"]
            if abs(image.width / image.height - expected_ratio) > 0.02:
                raise ValueError(f"Unexpected aspect ratio: {source}")
            image.thumbnail((entry["width"], entry["height"]), Image.Resampling.LANCZOS)
            image.save(output, "WEBP", quality=82, method=6)
        with Image.open(output) as exported:
            exported.load()
            if exported.format != "WEBP":
                raise ValueError(f"Invalid WebP export: {output}")
            if entry["transparent"] and exported.getchannel("A").getextrema()[0] != 0:
                raise ValueError(f"WebP lost its transparent background: {output}")
            entry["export_width"], entry["export_height"] = exported.size
        entry.update(
            status="exported",
            source_filename=source.name,
            source_sha256=digest(source),
            sha256=digest(output),
            bytes=output.stat().st_size,
        )
        total += output.stat().st_size
    if total > manifest["art_budget_bytes"]:
        raise ValueError(f"Art budget exceeded: {total} bytes")
    manifest["export_bytes"] = total
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return entries


def contact_sheet(entries: list[dict[str, Any]]) -> None:
    width, height, cols = 360, 260, 4
    rows = (len(entries) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * width, rows * height), "#10172e")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(ROOT / "assets/fonts/AtkinsonHyperlegible-Regular.ttf"), 20)
    for index, entry in enumerate(entries):
        x, y = (index % cols) * width, (index // cols) * height
        draw.rounded_rectangle(
            (x + 6, y + 6, x + width - 6, y + height - 6),
            radius=8,
            fill="#241e36",
            outline="#806139",
            width=1,
        )
        with Image.open(ART / str(entry["filename"])) as source:
            thumbnail = ImageOps.contain(source.convert("RGBA"), (width - 22, height - 42))
        sheet.paste(thumbnail, (x + (width - thumbnail.width) // 2, y + 10), thumbnail)
        draw.text((x + 14, y + height - 27), str(entry["id"]), fill="#fff1d2", font=font)
    sheet.save(ROOT / "docs/ART_CONTACT_SHEET.webp", "WEBP", quality=82, method=6)


def scene_preview() -> None:
    with Image.open(ART / "ofrenda-wall.webp") as background:
        scene = background.convert("RGBA")
    for layer_name, offset in [("ofrenda-altar", 0), ("ofrenda-papel", -180)]:
        with Image.open(ART / f"{layer_name}.webp") as source:
            scene.alpha_composite(source.convert("RGBA"), (0, offset))
    # Preview-only placement; game core will implement accessible, interactive hotspots.
    placement = {
        "photograph": (360, 150, 220),
        "bowl": (930, 160, 220),
        "radio": (365, 350, 235),
        "screwdriver": (845, 405, 165),
        "letter": (665, 555, 220),
        "scarf": (1070, 535, 220),
    }
    for name, (x, y, size) in placement.items():
        with Image.open(ART / f"object-{name}.webp") as source:
            image_layer = ImageOps.contain(source.convert("RGBA"), (size, size))
            scene.alpha_composite(image_layer, (x, y))
    with Image.open(ART / "ofrenda-foreground.webp") as foreground:
        scene.alpha_composite(foreground.convert("RGBA"), (0, 180))
    path = ROOT / ".dev/art-composite.webp"
    path.parent.mkdir(parents=True, exist_ok=True)
    scene.convert("RGB").save(path, "WEBP", quality=85, method=6)


def main() -> None:
    entries = export_assets()
    contact_sheet(entries)
    scene_preview()
    print(f"Exported {len(entries)} images; art bytes: {sum(int(x['bytes']) for x in entries)}")
    print("Contact sheet: docs/ART_CONTACT_SHEET.webp")
    print("Scene review: .dev/art-composite.webp")


if __name__ == "__main__":
    main()
