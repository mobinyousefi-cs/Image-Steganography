#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Python Image Steganography 
File: gui.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Optional module if you want to import the Tkinter App class directly.

Usage: 
from image_steganography.gui import App

Notes: 
- `main.py` imports and uses the same App class; this module simply re-exports it
  for users who want to embed or customize the GUI.

===================================================================
"""
from .main import App  # re-export for convenience

__all__ = ["App"]
