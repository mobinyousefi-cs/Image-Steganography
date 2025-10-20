#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Python Image Steganography 
File: test_core.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Unit tests for the core encode/decode API. Uses a generated image.

Usage: 
pytest -q

Notes: 
- Tests exercise both stegano-based and fallback paths implicitly depending on env.

===================================================================
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from image_steganography.core import (
    SteganographyError,
    decode_message_from_image,
    encode_message_to_image,
)


def _make_cover(tmp_path: Path) -> Path:
    img = Image.new("RGBA", (128, 128), (20, 40, 60, 255))
    p = tmp_path / "cover.png"
    img.save(p)
    return p


def test_encode_decode_roundtrip(tmp_path: Path):
    cover = _make_cover(tmp_path)
    out = tmp_path / "stego.png"
    secret = "The quick brown fox jumps over 13 lazy dogs. 🦊"

    stego_path = encode_message_to_image(cover, secret, out)
    assert stego_path.exists()

    revealed = decode_message_from_image(stego_path)
    assert revealed == secret


def test_decode_missing(tmp_path: Path):
    # Image without payload should raise
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 255))
    p = tmp_path / "blank.png"
    img.save(p)

    try:
        decode_message_from_image(p)
    except SteganographyError:
        pass
    else:
        raise AssertionError("Expected SteganographyError for image without message")
