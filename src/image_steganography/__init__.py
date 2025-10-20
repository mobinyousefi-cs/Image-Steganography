#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Python Image Steganography 
File: __init__.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Package init exposing public API for encoding/decoding and GUI entrypoint. 

Usage: 
python -m image_steganography 

Notes: 
- Prefer PNGs or other lossless formats for reliability. 
- Relies on the `stegano` package for robust LSB encoding/decoding.

===================================================================
"""
from .core import encode_message_to_image, decode_message_from_image

__all__ = [
    "encode_message_to_image",
    "decode_message_from_image",
]
