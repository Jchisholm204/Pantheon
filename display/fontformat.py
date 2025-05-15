# WARNING
# This script was generated using ChatGPT
from PIL import Image, ImageFont, ImageDraw
import sys

FONT_PATH = "myFont.otf"
OUTPUT_PATH = "font8x16.hex"
CHAR_WIDTH = 8
CHAR_HEIGHT = 16

# Choose the ASCII range you want
CHAR_START = 0x20  # Space
CHAR_END   = 0x7F  # DEL (printable characters)

def reverse_bits(byte):
    return int('{:08b}'.format(byte)[::-1], 2)

def render_char_to_bitmap(font, char):
    img = Image.new("L", (CHAR_WIDTH, CHAR_HEIGHT), 0)
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), char, fill=255, font=font)
    img = img.point(lambda x: 255 if x > 128 else 0, mode='1')  # Threshold to black/white
    return img

def main():
    try:
        font = ImageFont.truetype(FONT_PATH, CHAR_HEIGHT)
    except IOError:
        print(f"Failed to load font: {FONT_PATH}")
        sys.exit(1)

    hex_lines = []

    for code in range(256):  # Full ASCII range
        char = chr(code) if CHAR_START <= code <= CHAR_END else " "
        img = render_char_to_bitmap(font, char)
        cropped = img.crop((0, 0, CHAR_WIDTH, CHAR_HEIGHT))

        for y in range(CHAR_HEIGHT):
            row_bits = 0
            for x in range(CHAR_WIDTH):
                pixel = cropped.getpixel((x, y))
                if pixel:
                    row_bits |= (1 << (7 - x))  # Original MSB-left layout
            reversed_row = reverse_bits(row_bits)  # <-- Add this
            hex_lines.append(f"{reversed_row:02X}")

    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join(hex_lines))

    print(f"Wrote {len(hex_lines)} lines to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

