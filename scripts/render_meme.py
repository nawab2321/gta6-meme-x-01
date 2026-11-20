"""Letter the generated Vice City illustration and export the X and judge sizes."""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ARTWORK = ROOT / "artwork/vice-city-getaway.png"
OUTPUT = ROOT / "output"
SIDE = 1536
INK = "#150d25"
PAPER = "#fff9ee"
GOLD = "#ffd468"


def add_caption(canvas, font_path, text, top, size, color):
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(font_path, size)
    while draw.textlength(text, font=font) > SIDE * 0.89:
        font = ImageFont.truetype(font_path, font.size - 1)

    left, upper, right, _ = font.getbbox(text)
    x = (SIDE - right - left) / 2
    y = top - upper
    draw.text((x, y + 6), text, font=font, fill=INK, stroke_width=12, stroke_fill=INK)
    draw.text((x, y), text, font=font, fill=color, stroke_width=6, stroke_fill=INK)


def add_laptop_wordmark(canvas, font_path):
    decal = Image.new("RGBA", (336, 90))
    draw = ImageDraw.Draw(decal)
    font = ImageFont.truetype(font_path, 60)
    draw.text((168, 45), "make.fun", font=font, fill=PAPER, anchor="mm")
    # The laptop lid rises to the right and leans toward the driver.
    decal = decal.transform(
        decal.size,
        Image.Transform.AFFINE,
        (1.0, 0.24, -13, 0.055, 1.0, -9),
        resample=Image.Resampling.BICUBIC,
    )
    canvas.paste(decal, (930, 836), decal)


def render(font_path):
    with Image.open(ARTWORK) as source:
        canvas = source.convert("RGB").resize((SIDE, SIDE), Image.Resampling.LANCZOS)
    add_laptop_wordmark(canvas, font_path)
    add_caption(canvas, font_path, "WAITED 13 YEARS", 71, 113, PAPER)
    add_caption(canvas, font_path, "FOR GTA VI.", 188, 113, GOLD)
    add_caption(canvas, font_path, "MY GETAWAY DRIVER", 1215, 109, PAPER)
    add_caption(canvas, font_path, "HAS A CLIENT CALL.", 1335, 109, GOLD)

    OUTPUT.mkdir(exist_ok=True)
    canvas.save(OUTPUT / "gta6-meme-final.png", optimize=True)
    preview = canvas.resize((480, 480), Image.Resampling.LANCZOS)
    preview.save(OUTPUT / "gta6-meme-preview.png", optimize=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--font", default="DejaVuSans-Bold.ttf", help="DejaVu Sans Bold TTF")
    render(parser.parse_args().font)
