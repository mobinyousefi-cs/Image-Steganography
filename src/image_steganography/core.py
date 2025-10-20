#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Python Image Steganography 
File: core.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Core API wrapping the `stegano` LSB functionality with basic validation. 
Also includes a minimal fallback LSB encoder/decoder (educational only).

Usage: 
python -c "from image_steganography.core import encode_message_to_image, decode_message_from_image; \
encode_message_to_image('cover.png','secret','out.png'); print(decode_message_from_image('out.png'))"

Notes: 
- Use PNG or another lossless format to avoid data loss. 
- Fallback implementation is for small ASCII payloads and demos.

===================================================================
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image

from .utils import ensure_png, is_lossless_image

# Third-party LSB from stegano
try:
    from stegano import lsb
except Exception:  # pragma: no cover - library may be unavailable in some envs
    lsb = None  # type: ignore


class SteganographyError(RuntimeError):
    """Domain error for steganography operations."""


def encode_message_to_image(cover_image: str | Path, message: str, output_path: str | Path) -> Path:
    """Encode `message` inside `cover_image` and write to `output_path`.

    Returns the output path.
    """
    cover = Path(cover_image)
    if not cover.exists():
        raise SteganographyError(f"Cover image not found: {cover}")
    if not message:
        raise SteganographyError("Message must not be empty")

    out = ensure_png(output_path)

    if lsb is None:
        _fallback_encode(cover, message, out)
    else:
        if not is_lossless_image(cover):
            # We can still try, but warn users in documentation. Here we proceed.
            pass
        secret = lsb.hide(str(cover), message)
        # Always save as PNG for safety
        secret.save(str(out))
    return out


def decode_message_from_image(stego_image: str | Path) -> str:
    """Decode and return the hidden message from `stego_image`.

    Raises `SteganographyError` if decoding fails or no message was found.
    """
    img = Path(stego_image)
    if not img.exists():
        raise SteganographyError(f"Image not found: {img}")

    if lsb is None:
        msg = _fallback_decode(img)
    else:
        msg: Optional[str] = lsb.reveal(str(img))
    if not msg:
        raise SteganographyError("No hidden message found or unable to decode.")
    return msg


# ------------------------------
# Fallback LSB (educational)
# ------------------------------

_HEADER = b"IMSG\x00"  # magic header to identify payload


def _to_bits(data: bytes):
    for byte in data:
        for i in range(8):
            yield (byte >> (7 - i)) & 1


def _from_bits(bits):
    b = 0
    out = bytearray()
    for i, bit in enumerate(bits, start=1):
        b = (b << 1) | bit
        if i % 8 == 0:
            out.append(b)
            b = 0
    return bytes(out)


def _fallback_encode(cover: Path, message: str, out: Path) -> None:
    img = Image.open(cover).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    payload = _HEADER + len(message.encode("utf-8")).to_bytes(4, "big") + message.encode("utf-8")
    bits = list(_to_bits(payload))
    capacity = width * height * 3  # 3 channels used (RGB)
    if len(bits) > capacity:
        raise SteganographyError("Message is too large for this image in fallback mode.")

    it = iter(bits)
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            try:
                r = (r & ~1) | next(it)
                g = (g & ~1) | next(it)
                b = (b & ~1) | next(it)
            except StopIteration:
                pixels[x, y] = (r, g, b, a)
                img.save(out)
                return
            pixels[x, y] = (r, g, b, a)

    img.save(out)


def _fallback_decode(stego: Path) -> str:
    img = Image.open(stego).convert("RGBA")
    pixels = img.load()
    width, height = img.size

    bits = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            bits.extend([r & 1, g & 1, b & 1])

    # Reconstruct bytes until header and length are parsed
    # First bytes: magic (5) + length (4) => 9 bytes => 72 bits
    header_len_bits = (len(_HEADER) + 4) * 8
    header_bytes = _from_bits(bits[:header_len_bits])
    if not header_bytes.startswith(_HEADER):
        return ""
    msg_len = int.from_bytes(header_bytes[len(_HEADER): len(_HEADER) + 4], "big")

    msg_bits = bits[header_len_bits: header_len_bits + msg_len * 8]
    msg_bytes = _from_bits(msg_bits)
    try:
        return msg_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return ""
