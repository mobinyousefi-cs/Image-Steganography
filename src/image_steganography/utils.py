#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Python Image Steganography 
File: utils.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Utility helpers: validations, file checks, simple conversions.

Usage: 
python -c "from image_steganography.utils import ensure_png; print(ensure_png('a.jpg'))"

Notes: 
- Lossless formats are recommended. This module nudges users to use PNG.

===================================================================
"""
from __future__ import annotations

from pathlib import Path


LOSSLESS_EXTS = {".png", ".bmp", ".tiff", ".tif"}


def ensure_png(path: str | Path) -> Path:
    """Ensure the output path ends with .png (recommended for LSB).

    If a different extension is provided, replace it with `.png`.
    """
    p = Path(path)
    if p.suffix.lower() != ".png":
        return p.with_suffix(".png")
    return p


def is_lossless_image(path: str | Path) -> bool:
    """Return True if the file extension indicates a lossless image format."""
    return Path(path).suffix.lower() in LOSSLESS_EXTS
