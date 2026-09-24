#!/usr/bin/env python3
"""Finalize one image to exact pixels without stretching its contents."""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

try:
    from PIL import Image, ImageColor, ImageOps, UnidentifiedImageError
except ImportError:  # pragma: no cover - environment-dependent failure message
    Image = None
    ImageColor = None
    ImageOps = None
    UnidentifiedImageError = OSError


FORMAT_ALIASES = {"JPG": "JPEG"}
SUPPORTED_FORMATS = {"PNG", "JPEG", "WEBP"}


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def parse_background(value: str) -> tuple[int, int, int, int]:
    if value.lower() == "transparent":
        return (0, 0, 0, 0)
    try:
        rgb = ImageColor.getrgb(value)
    except ValueError as exc:
        raise ValueError(f"invalid background color: {value}") from exc
    if len(rgb) == 4:
        return rgb
    return (*rgb, 255)


def output_format(path: Path, requested: str | None) -> str:
    if requested:
        name = requested.upper().lstrip(".")
    else:
        name = path.suffix.upper().lstrip(".")
    name = FORMAT_ALIASES.get(name, name)
    if name not in SUPPORTED_FORMATS:
        raise ValueError("output format must be PNG, JPEG/JPG, or WEBP")
    return name


def fitted_image(
    source: Image.Image,
    width: int,
    height: int,
    fit: str,
    background: tuple[int, int, int, int],
    allow_upscale: bool,
) -> Image.Image:
    source = ImageOps.exif_transpose(source).convert("RGBA")
    scale_x = width / source.width
    scale_y = height / source.height
    scale = min(scale_x, scale_y) if fit == "contain" else max(scale_x, scale_y)
    if not allow_upscale:
        scale = min(scale, 1.0)

    resized_width = max(1, round(source.width * scale))
    resized_height = max(1, round(source.height * scale))
    resized = source.resize((resized_width, resized_height), Image.Resampling.LANCZOS)

    if fit == "cover":
        left = max(0, (resized_width - width) // 2)
        top = max(0, (resized_height - height) // 2)
        right = min(resized_width, left + width)
        bottom = min(resized_height, top + height)
        cropped = resized.crop((left, top, right, bottom))
        if cropped.size == (width, height):
            return cropped
        resized = cropped

    canvas = Image.new("RGBA", (width, height), background)
    x = (width - resized.width) // 2
    y = (height - resized.height) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def encoded_bytes(
    image: Image.Image,
    fmt: str,
    quality: int,
) -> bytes:
    buffer = io.BytesIO()
    save_image = image
    options: dict[str, object] = {}
    if fmt == "PNG":
        options.update(optimize=True, compress_level=9)
    elif fmt == "JPEG":
        if image.mode != "RGB":
            flattened = Image.new("RGB", image.size, (255, 255, 255))
            if "A" in image.getbands():
                flattened.paste(image.convert("RGB"), mask=image.getchannel("A"))
            else:
                flattened.paste(image.convert("RGB"))
            save_image = flattened
        options.update(quality=quality, optimize=True, progressive=True)
    elif fmt == "WEBP":
        options.update(quality=quality, method=6)
    save_image.save(buffer, format=fmt, **options)
    return buffer.getvalue()


def fit_file_size(
    image: Image.Image,
    fmt: str,
    preferred_quality: int,
    max_bytes: int | None,
) -> tuple[bytes, int | None]:
    if fmt == "PNG":
        data = encoded_bytes(image, fmt, preferred_quality)
        if max_bytes is not None and len(data) > max_bytes:
            raise ValueError(
                f"optimized PNG is {len(data)} bytes, above max_bytes {max_bytes}; "
                "use JPEG/WEBP or revise the approved delivery format"
            )
        return data, None

    qualities = list(range(preferred_quality, 34, -5))
    if qualities[-1] != 35:
        qualities.append(35)
    last_data = b""
    last_quality = qualities[-1]
    for quality in qualities:
        data = encoded_bytes(image, fmt, quality)
        last_data = data
        last_quality = quality
        if max_bytes is None or len(data) <= max_bytes:
            return data, quality
    raise ValueError(
        f"{fmt} remains {len(last_data)} bytes at quality {last_quality}, "
        f"above max_bytes {max_bytes}"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resize with contain/cover geometry and optional file-size compression"
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", required=True, type=positive_int)
    parser.add_argument("--height", required=True, type=positive_int)
    parser.add_argument("--fit", choices=("contain", "cover"), default="contain")
    parser.add_argument("--background", default="#FFFFFF")
    parser.add_argument("--format", dest="format_name")
    parser.add_argument("--quality", type=int, default=95)
    parser.add_argument("--max-bytes", type=positive_int)
    parser.add_argument("--no-upscale", action="store_true")
    return parser


def main() -> int:
    if Image is None:
        print("FAIL: Pillow is required but is not installed", file=sys.stderr)
        return 1

    parser = build_parser()
    args = parser.parse_args()
    if not 35 <= args.quality <= 100:
        parser.error("--quality must be from 35 to 100")

    input_path = args.input.resolve()
    output_path = args.output.resolve()
    if input_path == output_path:
        print("FAIL: input and output must be different files", file=sys.stderr)
        return 1
    if not input_path.is_file():
        print(f"FAIL: input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        fmt = output_format(output_path, args.format_name)
        background = parse_background(args.background)
        if fmt == "JPEG" and background[3] == 0:
            raise ValueError("JPEG cannot use a transparent background")
        with Image.open(input_path) as source:
            source.load()
            finalized = fitted_image(
                source,
                args.width,
                args.height,
                args.fit,
                background,
                not args.no_upscale,
            )
        data, used_quality = fit_file_size(
            finalized, fmt, args.quality, args.max_bytes
        )
    except (ValueError, UnidentifiedImageError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)
    quality_note = "" if used_quality is None else f" quality={used_quality}"
    print(
        "PASS: "
        f"{output_path} width={args.width} height={args.height} "
        f"format={fmt} bytes={len(data)} fit={args.fit}{quality_note}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
