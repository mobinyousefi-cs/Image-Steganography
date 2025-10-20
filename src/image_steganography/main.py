#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=================================================================== 
Project: Python Image Steganography 
File: main.py 
Author: Mobin Yousefi (GitHub: github.com/mobinyousefi) 
Created: 2025-10-20 
Updated: 2025-10-20 
License: MIT License (see LICENSE file for details)
=================================================================== 

Description: 
Application entrypoint. Launches the Tkinter GUI.

Usage: 
python -m image_steganography
# or
stegano-gui

Notes: 
- GUI wraps the core API and provides file dialogs and status messages.

===================================================================
"""
from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from .core import (
    SteganographyError,
    decode_message_from_image,
    encode_message_to_image,
)
from .utils import ensure_png


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Image Steganography — LSB (Mobin Yousefi)")
        self.geometry("720x520")
        self._build_ui()

    # ---------------- UI -----------------
    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        nb = ttk.Notebook(self)
        nb.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        # Encode tab
        self.encode_tab = ttk.Frame(nb)
        nb.add(self.encode_tab, text="Encode")
        self._build_encode_tab(self.encode_tab)

        # Decode tab
        self.decode_tab = ttk.Frame(nb)
        nb.add(self.decode_tab, text="Decode")
        self._build_decode_tab(self.decode_tab)

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

    def _build_encode_tab(self, frame: ttk.Frame) -> None:
        frame.columnconfigure(1, weight=1)

        # Cover image
        ttk.Label(frame, text="Cover Image (PNG recommended):").grid(row=0, column=0, sticky="w", pady=6)
        self.cover_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.cover_path).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(frame, text="Browse...", command=self._browse_cover).grid(row=0, column=2, padx=4)

        # Message
        ttk.Label(frame, text="Secret Message:").grid(row=1, column=0, sticky="nw", pady=6)
        self.message_txt = tk.Text(frame, height=10, wrap="word")
        self.message_txt.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=8)
        frame.rowconfigure(1, weight=1)

        # Output
        ttk.Label(frame, text="Output Image (PNG):").grid(row=2, column=0, sticky="w", pady=6)
        self.output_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.output_path).grid(row=2, column=1, sticky="ew", padx=8)
        ttk.Button(frame, text="Save As...", command=self._browse_output).grid(row=2, column=2, padx=4)

        # Action
        ttk.Button(frame, text="Encode", command=self._on_encode).grid(row=3, column=2, sticky="e", pady=10)

    def _build_decode_tab(self, frame: ttk.Frame) -> None:
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Stego Image:").grid(row=0, column=0, sticky="w", pady=6)
        self.stego_path = tk.StringVar()
        ttk.Entry(frame, textvariable=self.stego_path).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(frame, text="Browse...", command=self._browse_stego).grid(row=0, column=2, padx=4)

        ttk.Label(frame, text="Decoded Message:").grid(row=1, column=0, sticky="nw", pady=6)
        self.decoded_txt = tk.Text(frame, height=12, wrap="word", state="disabled")
        self.decoded_txt.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=8)
        frame.rowconfigure(1, weight=1)

        ttk.Button(frame, text="Decode", command=self._on_decode).grid(row=2, column=2, sticky="e", pady=10)

    # ------------- Callbacks -------------
    def _browse_cover(self) -> None:
        path = filedialog.askopenfilename(
            title="Select cover image",
            filetypes=[("Image files", "*.png;*.bmp;*.tif;*.tiff;*.jpg;*.jpeg;*.webp"), ("All files", "*.*")],
        )
        if path:
            self.cover_path.set(path)

    def _browse_output(self) -> None:
        initial = Path(self.cover_path.get()).with_name("stego.png") if self.cover_path.get() else Path("stego.png")
        path = filedialog.asksaveasfilename(
            title="Save stego image as",
            defaultextension=".png",
            initialfile=str(initial.name),
            filetypes=[("PNG", "*.png")],
        )
        if path:
            self.output_path.set(ensure_png(path).as_posix())

    def _browse_stego(self) -> None:
        path = filedialog.askopenfilename(
            title="Select stego image",
            filetypes=[("Image files", "*.png;*.bmp;*.tif;*.tiff;*.jpg;*.jpeg;*.webp"), ("All files", "*.*")],
        )
        if path:
            self.stego_path.set(path)

    def _on_encode(self) -> None:
        try:
            out = encode_message_to_image(self.cover_path.get(), self.message_txt.get("1.0", "end").strip(), self.output_path.get() or "stego.png")
        except SteganographyError as e:
            messagebox.showerror("Encode failed", str(e))
            self.status_var.set("Encode failed.")
            return
        except Exception as e:  # unexpected
            messagebox.showerror("Unexpected error", str(e))
            self.status_var.set("Unexpected error.")
            return
        messagebox.showinfo("Success", f"Stego image saved to:\n{out}")
        self.status_var.set(f"Encoded -> {out}")

    def _on_decode(self) -> None:
        try:
            msg = decode_message_from_image(self.stego_path.get())
        except SteganographyError as e:
            messagebox.showwarning("No message", str(e))
            self.status_var.set("Decode failed.")
            return
        except Exception as e:
            messagebox.showerror("Unexpected error", str(e))
            self.status_var.set("Unexpected error.")
            return

        self.decoded_txt.configure(state="normal")
        self.decoded_txt.delete("1.0", "end")
        self.decoded_txt.insert("1.0", msg)
        self.decoded_txt.configure(state="disabled")
        self.status_var.set("Decoded message displayed.")


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
