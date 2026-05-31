#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from PIL import Image

# ----- Brightness-to-ASCII mappings -----
CHAR_SETS = {
    "standard":  "@%#*+=-:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "blocks":    "█▓▒░ ",
    "minimal":   "@. ",
    "binary":    "10",
}

# ANSI color codes for terminal output (optional)
COLORS = {
    "black":  30, "red":  31, "green": 32, "yellow": 33,
    "blue":   34, "magenta": 35, "cyan": 36, "white": 37,
    "bright_black": 90, "bright_red": 91, "bright_green": 92,
    "bright_yellow": 93, "bright_blue": 94, "bright_magenta": 95,
    "bright_cyan": 96, "bright_white": 97,
}

class AsciiConverter:
    def __init__(self, image_path, width=100, invert=False, charset="standard", color=None):
        self.image_path = image_path
        self.width = width
        self.invert = invert
        self.chars = list(CHAR_SETS.get(charset, CHAR_SETS["standard"]))
        self.color = color
        self.image = None

    def load_image(self):
        try:
            self.image = Image.open(self.image_path)
        except FileNotFoundError:
            sys.exit(f"Error: File not found: {self.image_path}")
        except Exception as e:
            sys.exit(f"Error opening image: {e}")

    def resize_image(self):
        aspect_ratio = self.image.height / self.image.width / 1.65  # font aspect ratio correction
        new_height = int(aspect_ratio * self.width)
        self.image = self.image.resize((self.width, new_height))

    def convert_to_grayscale(self):
        self.image = self.image.convert("L")

    def map_pixels_to_ascii(self):
        pixels = list(self.image.getdata())
        char_range = len(self.chars) - 1

        if self.invert:
            ascii_str = "".join(
                self.chars[(255 - p) * char_range // 255] for p in pixels
            )
        else:
            ascii_str = "".join(
                self.chars[p * char_range // 255] for p in pixels
            )
        return ascii_str

    def generate_art(self):
        self.load_image()
        self.resize_image()
        self.convert_to_grayscale()
        ascii_str = self.map_pixels_to_ascii()
        # Split into lines
        lines = [ascii_str[i:i+self.width] for i in range(0, len(ascii_str), self.width)]
        return "\n".join(lines)

    def colorize(self, text):
        if self.color and self.color in COLORS:
            code = COLORS[self.color]
            return f"\033[{code}m{text}\033[0m"
        return text

    def preview(self):
        art = self.generate_art()
        print(self.colorize(art))
        return art

    def save(self, output_path=None):
        art = self.generate_art()
        if output_path is None:
            output_path = f"{Path(self.image_path).stem}_ascii.txt"
        try:
            with open(output_path, "w") as f:
                f.write(art)
            print(f"Saved ASCII art to {output_path}")
        except Exception as e:
            sys.exit(f"Error saving file: {e}")
        return art


def main():
    parser = argparse.ArgumentParser(
        description="Convert images to professional ASCII art.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python converter.py cat.jpg\n"
               "  python converter.py cat.jpg -w 120 -c detailed --invert\n"
               "  python converter.py cat.jpg --color green -o art.txt"
    )
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("-w", "--width", type=int, default=100, help="Output width in characters (default: 100)")
    parser.add_argument("-i", "--invert", action="store_true", help="Invert brightness (dark becomes light)")
    parser.add_argument("-c", "--charset", choices=CHAR_SETS.keys(), default="standard", help="Character set for brightness mapping")
    parser.add_argument("--color", choices=COLORS.keys(), default=None, help="Colorize terminal output (requires terminal support)")
    parser.add_argument("-o", "--output", default=None, help="Save to a specific file (default: <image>_ascii.txt)")
    parser.add_argument("--no-preview", action="store_true", help="Skip terminal preview, only save to file")

    args = parser.parse_args()

    converter = AsciiConverter(
        image_path=args.image,
        width=args.width,
        invert=args.invert,
        charset=args.charset,
        color=args.color
    )

    if not args.no_preview:
        art = converter.preview()
    else:
        art = converter.generate_art()

    if args.output or not args.no_preview:  # Save always unless explicitly a preview-only run without -o? Let's save if output given or if we want both preview and save.
        converter.save(args.output)


if __name__ == "__main__":
    main()
