# Python Image Steganography (Tkinter GUI)

Hide secret text inside images using Least Significant Bit (LSB) steganography. This project provides a clean Python package with a desktop GUI (Tkinter) and a simple API on top of the excellent [`stegano`](https://pypi.org/project/stegano/) library, plus a tiny fallback pure-PIL LSB implementation for learning/testing.

## Features
- Encode text into PNG images (lossless) and save the stego image
- Decode hidden text from a stego image
- Desktop GUI built with Tkinter (drag & drop friendly via file dialogs)
- CLI entrypoint (`stegano-gui`) to launch the app
- Clean `src/` package layout, tests with `pytest`, CI via GitHub Actions, MIT license

## Requirements
- Python 3.9+
- Dependencies: `stegano`, `pillow`

> **Note**: Use **PNG** or other lossless formats. Lossy formats like JPEG can destroy hidden bits.

## Quick Start
```bash
# (recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install package in editable mode with extras for dev\pip install -e .[dev]

# launch the GUI
stegano-gui
```

## Usage (GUI)
1. Click **Encode**
2. Choose a **cover image** (PNG)
3. Type/paste your **secret message**
4. Choose an **output path** (PNG), save
5. Later, click **Decode** and open the saved stego image to reveal the message

## Usage (Library)
```python
from image_steganography.core import encode_message_to_image, decode_message_from_image

encode_message_to_image("cover.png", "hello world", "out.png")
text = decode_message_from_image("out.png")
print(text)  # -> "hello world"
```

## Project Structure
```
.
├── src/
│   └── image_steganography/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── main.py
├── tests/
│   └── test_core.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .editorconfig
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Running Tests
```bash
pytest -q
```

## Security & Ethics
Steganography is a legitimate research/educational topic but can be misused. **Only hide information you own or are authorized to protect** and comply with laws/policies where you operate.

## Credits
- Author: **Mobin Yousefi** (GitHub: [github.com/mobinyousefi](https://github.com/mobinyousefi))
- Library: [`stegano`](https://github.com/cedricbonhomme/Stegano)

## License
This project is licensed under the **MIT License**. See `LICENSE` for details.

