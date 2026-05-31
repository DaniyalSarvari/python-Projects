markdown
# 🎨 ASCII Art Converter

Professional command-line tool to turn any image into stunning ASCII art.  
Supports multiple character sets, brightness inversion, colored terminal preview, and flexible output options.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## Features

- 🖼️ **Image to Text**: Convert JPEG, PNG, BMP, and more to ASCII art
- 🎭 **5 Character Sets**: `standard`, `detailed`, `blocks`, `minimal`, `binary`
- ↔️ **Adjustable Width**: Control output width while preserving aspect ratio
- 🌓 **Invert Brightness**: Dark backgrounds become light, and vice versa
- 🌈 **Terminal Colors**: Preview your art in red, green, blue, cyan, and more
- 💾 **Automatic Saving**: Output saved as a `.txt` file next to the source image
- ⚡ **Fast & Lightweight**: Only requires Pillow, processes images instantly

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Install Pillow
```bash
pip install Pillow
```

##Usage
### Basic conversion
```bash
python converter.py image.jpg
```
This will print the ASCII art in your terminal and save it as image_ascii.txt.

##Full options
```bash
python converter.py photo.jpg -w 150 -c detailed --invert --color green -o art.txt
```
##Skip terminal preview (save only)
```bash
python converter.py poster.png --no-preview -o poster_ascii.txt
```
##Help
```bash
python converter.py --help
```

## Command-line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `image`  |       | Path to the image file (required) | – |
| `--width` | `-w` | Output width in characters | 100 |
| `--invert` | `-i` | Invert brightness | `False` |
| `--charset` | `-c` | Character set: `standard`, `detailed`, `blocks`, `minimal`, `binary` | `standard` |
| `--color` | | Terminal color: `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`, `white`, and bright variants | `None` |
| `--output` | `-o` | Save to a specific file (default: `<image>_ascii.txt`) | auto-generated |
| `--no-preview` | | Do not print to terminal | `False` |

## Character Sets

- **standard** `@%#*+=-:. ` – classic look, works everywhere
- **detailed** `$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^'. ` – rich detail, good for high-resolution images
- **blocks** `█▓▒░ ` – solid block characters for a modern terminal style
- **minimal** `@. ` – high-contrast, sharp edges
- **binary** `10` – pure 1-bit black and white

## Examples

### 1. Standard conversion
```bash
python converter.py cat.jpg
```

```text
Saved ASCII art to cat_ascii.txt
@@@@@@@@@@@@@@@@@@%#*+++=-:..   
@@@@@@@@@@@@@@@%#*+=--::.....   
...
```
##2. Detailed, inverted, colored
```bash
python converter.py mountain.jpg -w 200 -c detailed --invert --color cyan
``

##3. Binary art for a retro feel
```bash
python converter.py face.png -c binary -w 80 -o face_binary.txt --no-preview
```

##How It Works
Load the image and handle errors gracefully.

- Resize preserving aspect ratio (corrected for monospace font dimensions).

- Convert to grayscale (luminance values 0–255).

- Map each pixel to a character from the chosen set based on brightness.

- Colorize with ANSI escape codes if a color is selected.

- Output to terminal and/or file.

##File Structure
```text
ascii-art/
├── converter.py   ← Main application (single-file, no dependencies beyond Pillow)
└── README.md      ← This file
```


##License
MIT — do whatever you want, just don't sue me.
