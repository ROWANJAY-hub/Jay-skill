#!/usr/bin/env python3
"""Validate deterministic file properties for accepted product-image outputs."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:  # pragma: no cover - environment-dependent failure message
    Image = None
    ImageOps = None
    UnidentifiedImageError = OSError


RATIO_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*:\s*([0-9]+(?:\.[0-9]+)?)\s*$")
FORMAT_ALIASES = {"JPG": "JPEG", "TIF": "TIFF"}


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def parse_ratio(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    match = RATIO_RE.fullmatch(value)
    if not match:
        return None
    left, right = float(match.group(1)), float(match.group(2))
    if left <= 0 or right <= 0:
        return None
    return left / right


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def decoded_pixel_hash(image: Any) -> str:
    normalized = ImageOps.exif_transpose(image).convert("RGBA")
    digest = hashlib.sha256()
    digest.update(f"{normalized.width}x{normalized.height}:RGBA".encode("ascii"))
    digest.update(normalized.tobytes())
    return digest.hexdigest()


def load_plan(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"plan file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(data, dict):
        raise ValueError("plan root must be a JSON object")
    return data


def normalized_expected_format(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    name = value.strip().lstrip(".").upper()
    return FORMAT_ALIASES.get(name, name)


def validate(plan_path: Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if Image is None:
        return ["Pillow is required to inspect image files but is not installed"]

    outputs = data.get("final_outputs")
    if not isinstance(outputs, list) or not outputs or not all(
        nonempty_string(item) for item in outputs
    ):
        return ["final_outputs must be a non-empty array of slot ids"]

    output_files = data.get("output_files")
    if not isinstance(output_files, dict):
        return ["output_files must map every accepted slot id to a local image path"]

    missing_keys = set(outputs) - set(output_files)
    extra_keys = set(output_files) - set(outputs)
    if missing_keys:
        errors.append("output_files is missing: " + ", ".join(sorted(missing_keys)))
    if extra_keys:
        errors.append("output_files has non-final slots: " + ", ".join(sorted(extra_keys)))

    output_spec = data.get("output_spec")
    if not isinstance(output_spec, dict):
        errors.append("output_spec must be an object")
        output_spec = {}
    expected_ratio = parse_ratio(output_spec.get("aspect_ratio"))
    if expected_ratio is None:
        errors.append("output_spec.aspect_ratio must look like 1:1 or 4:5")
    target_width = output_spec.get("target_width")
    target_height = output_spec.get("target_height")
    min_width = output_spec.get("min_width")
    min_height = output_spec.get("min_height")
    max_bytes = output_spec.get("max_bytes")
    expected_format = normalized_expected_format(output_spec.get("format"))

    hashes: dict[str, list[str]] = {}
    pixel_hashes: dict[str, list[str]] = {}
    seen_paths: dict[Path, str] = {}
    for slot_id in outputs:
        raw_path = output_files.get(slot_id)
        if not nonempty_string(raw_path):
            continue
        image_path = Path(raw_path)
        if not image_path.is_absolute():
            image_path = (plan_path.parent / image_path).resolve()
        else:
            image_path = image_path.resolve()

        if image_path in seen_paths:
            errors.append(
                f"{slot_id} and {seen_paths[image_path]} point to the same output file"
            )
            continue
        seen_paths[image_path] = slot_id

        if not image_path.is_file():
            errors.append(f"{slot_id} output file not found: {image_path}")
            continue

        byte_size = image_path.stat().st_size
        if positive_int(max_bytes) and byte_size > max_bytes:
            errors.append(
                f"{slot_id} file size {byte_size} exceeds max_bytes {max_bytes}"
            )

        try:
            with Image.open(image_path) as image:
                actual_format = (image.format or "").upper()
                normalized = ImageOps.exif_transpose(image)
                width, height = normalized.size
                image.load()
                pixel_digest = decoded_pixel_hash(image)
        except (UnidentifiedImageError, OSError) as exc:
            errors.append(f"{slot_id} is not a readable image: {exc}")
            continue

        if positive_int(target_width) and width != target_width:
            errors.append(f"{slot_id} width {width} != target_width {target_width}")
        if positive_int(target_height) and height != target_height:
            errors.append(f"{slot_id} height {height} != target_height {target_height}")
        if positive_int(min_width) and width < min_width:
            errors.append(f"{slot_id} width {width} < min_width {min_width}")
        if positive_int(min_height) and height < min_height:
            errors.append(f"{slot_id} height {height} < min_height {min_height}")
        if expected_ratio is not None and abs((width / height) - expected_ratio) > 0.005:
            errors.append(
                f"{slot_id} ratio {width}:{height} does not match "
                f"{output_spec.get('aspect_ratio')}"
            )
        if expected_format and actual_format != expected_format:
            errors.append(
                f"{slot_id} format {actual_format or 'unknown'} != {expected_format}"
            )

        digest = file_hash(image_path)
        hashes.setdefault(digest, []).append(slot_id)
        pixel_hashes.setdefault(pixel_digest, []).append(slot_id)

    for slots in hashes.values():
        if len(slots) > 1:
            errors.append("exact duplicate output files: " + ", ".join(sorted(slots)))
    for slots in pixel_hashes.values():
        if len(slots) > 1 and not any(
            set(slots).issubset(set(binary_slots))
            for binary_slots in hashes.values()
            if len(binary_slots) > 1
        ):
            errors.append("pixel-identical output images: " + ", ".join(sorted(slots)))

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_outputs.py /absolute/path/to/plan.json", file=sys.stderr)
        return 2
    plan_path = Path(sys.argv[1]).resolve()
    try:
        data = load_plan(plan_path)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors = validate(plan_path, data)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: validated {len(data['final_outputs'])} accepted image files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
