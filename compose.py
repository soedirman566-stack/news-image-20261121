#!/usr/bin/env python3
"""
compose.py -- builds entry.png, the one-image front page for
news-image-20261121 ("The Daily Globe", Saturday 21 November 2026).

The page is drawn with Pillow at 1024x1024 from four real photographs
in assets/ (Wikimedia Commons, freely licensed -- see credits.txt).
Every text block is sized with a shrink-to-fit ladder instead of fixed
metrics, so the layout adapts to whatever Pillow/FreeType build runs
it and never dies on a hard layout assertion.

Run it twice and the sha256 of entry.png is identical: the drawing is
fully deterministic (fixed fonts, fixed geometry, fixed crop anchors,
no timestamps or randomness anywhere).

    python3 compose.py        # writes ./entry.png
"""

import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAGE = 1024
MARGIN = 28
WIDTH = PAGE - 2 * MARGIN  # 968

PAPER = (247, 243, 234)
INK = (18, 18, 18)
GREY = (70, 66, 60)
RED = (163, 22, 33)
WHITE = (250, 248, 242)


def font(path, size):
    return ImageFont.truetype(path, int(size))


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def fit_size(draw, s, path, max_w, start, minimum=10):
    """Largest integer font size (<= start) at which s fits max_w."""
    size = start
    while size > minimum and text_w(draw, s, font(path, size)) > max_w:
        size -= 1
    return size


def wrap(draw, s, f, max_w):
    """Greedy word wrap; a single over-long word still gets its own line."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if cur and text_w(draw, trial, f) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def fit_block(draw, s, path, max_w, max_h, start, minimum=10, leading=1.12):
    """Shrink s (font ladder) until its wrapped block fits max_w x max_h.

    Returns (font, lines, block_height). Never raises: at the minimum
    size the block is returned as-is and the caller simply draws it.
    """
    size = start
    while size > minimum:
        f = font(path, size)
        lines = wrap(draw, s, f, max_w)
        h = len(lines) * size * leading
        if h <= max_h:
            return f, lines, h
        size -= 1
    f = font(path, minimum)
    lines = wrap(draw, s, f, max_w)
    return f, lines, len(lines) * minimum * leading


def draw_lines(draw, x, y, lines, f, fill, leading=1.12, centre_w=None):
    for line in lines:
        if centre_w is not None:
            x0 = x + (centre_w - text_w(draw, line, f)) / 2
        else:
            x0 = x
        draw.text((x0, y), line, font=f, fill=fill)
        y += f.size * leading
    return y


def photo_crop(name, w, h, focus_y=0.5):
    """Crop an asset to exactly w x h with a mild print punch-up.

    focus_y anchors the crop window vertically (0 = top, 1 = bottom)
    so the subject of each photo lands in frame deterministically.
    """
    img = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    scale = max(w / img.width, h / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = int((nh - h) * focus_y)
    img = img.crop((left, top, left + w, top + h))
    img = ImageEnhance.Color(img).enhance(1.06)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Sharpness(img).enhance(1.15)
    return img


def rule(draw, y, weight=2, fill=INK):
    draw.rectangle([MARGIN, y, MARGIN + WIDTH, y + weight - 1], fill=fill)


def main():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(page)
    y = 20

    # ---- masthead ------------------------------------------------------
    rule(d, y, 5)
    y += 12
    name = "The Daily Globe"
    size = fit_size(d, name, SERIF_BOLD, WIDTH - 40, 84)
    draw_lines(d, MARGIN, y, [name], font(SERIF_BOLD, size), INK, centre_w=WIDTH)
    y += int(size * 1.08)
    rule(d, y, 2)
    y += 6
    f_info = font(SANS, 15)
    d.text((MARGIN, y), "WORLD EDITION", font=f_info, fill=GREY)
    right = "ONE PAGE - THE DAY'S WORLD"
    d.text((MARGIN + WIDTH - text_w(d, right, f_info), y), right, font=f_info, fill=GREY)
    y += 23
    rule(d, y, 1, GREY)
    y += 9

    # ---- date bar ------------------------------------------------------
    bar_h = 48
    d.rectangle([MARGIN, y, MARGIN + WIDTH, y + bar_h], fill=INK)
    date = "SATURDAY, 21 NOVEMBER 2026"
    size = fit_size(d, date, SANS_BOLD, WIDTH - 60, 38)
    f_date = font(SANS_BOLD, size)
    d.text((MARGIN + (WIDTH - text_w(d, date, f_date)) / 2, y + (bar_h - size) / 2 - 2),
           date, font=f_date, fill=WHITE)
    y += bar_h + 13

    # ---- lead story ----------------------------------------------------
    f_kick = font(SANS_BOLD, 19)
    d.text((MARGIN, y), "WAR IN EUROPE  -  POLAND / NATO", font=f_kick, fill=RED)
    y += 28

    for line in ("RUSSIAN MISSILES", "FALL ON POLAND"):
        size = fit_size(d, line, SERIF_BOLD, WIDTH, 66)
        draw_lines(d, MARGIN, y, [line], font(SERIF_BOLD, size), INK,
                   leading=1.0, centre_w=WIDTH)
        y += int(size * 1.02)
    y += 6

    photo_h = 224
    page.paste(photo_crop("kyiv-bridge.jpg", WIDTH, photo_h, focus_y=0.32), (MARGIN, y))
    y += photo_h + 5

    caption = ("The Paton Bridge over the Dnipro in Kyiv - three of the capital's "
               "bridges were hit in the same overnight barrage. "
               "(Photo: V. Vlasenko, CC BY 4.0)")
    f_cap, lines, h = fit_block(d, caption, SANS, WIDTH, 36, 15, minimum=11)
    draw_lines(d, MARGIN, y, lines, f_cap, GREY, leading=1.15)
    y += int(h) + 5

    blurb = ("Two Russian missiles and a suspected drone came down on Polish soil "
             "in the early hours of Saturday, an incursion Warsaw called a deliberate "
             "provocation and NATO a grave violation of allied airspace. The same "
             "barrage struck three bridges in Kyiv as Moscow pressed its assault "
             "on Ukraine.")
    f_bl, lines, h = fit_block(d, blurb, SERIF, WIDTH, 68, 18, minimum=13)
    draw_lines(d, MARGIN, y, lines, f_bl, INK, leading=1.18)
    y += int(h) + 10

    rule(d, y, 3)
    y += 11

    # ---- three secondary stories --------------------------------------
    stories = [
        {
            "img": "peace-palace.jpg",
            "focus": 0.5,
            "kick": "THE HAGUE - WORLD COURT",
            "head": "World Court: Myanmar Committed Genocide",
            "body": ("Judges ruled 9-6 that Myanmar's forces committed genocide "
                     "against the Rohingya in northern Rakhine, a landmark "
                     "finding of state responsibility."),
        },
        {
            "img": "shenzhen.jpg",
            "focus": 0.29,
            "kick": "SHENZHEN - SUMMIT",
            "head": "Trump, Xi, Putin Hold First Summit",
            "body": ("Trump, Xi and Putin met in Shenzhen for a first trilateral "
                     "summit, with Trump urging closer security cooperation. "
                     "It ended with few concrete results."),
        },
        {
            "img": "wall-street.jpg",
            "focus": 0.5,
            "kick": "NEW YORK - MARKETS",
            "head": "Wall Street Slides Into Correction",
            "body": ("The S&P 500 and Dow entered correction territory on Friday "
                     "as plunging AI and chip shares dragged US stocks down "
                     "about 3.7 percent."),
        },
    ]
    col_w = (WIDTH - 2 * 19) // 3  # 310
    col_bottom = PAGE - 44
    for i, st in enumerate(stories):
        x = MARGIN + i * (col_w + 19)
        cy = y
        ph = 102
        page.paste(photo_crop(st["img"], col_w, ph, focus_y=st["focus"]), (x, cy))
        cy += ph + 6
        f_k = font(SANS_BOLD, fit_size(d, st["kick"], SANS_BOLD, col_w, 12, minimum=9))
        d.text((x, cy), st["kick"], font=f_k, fill=RED)
        cy += 17
        f_h, lines, h = fit_block(d, st["head"], SERIF_BOLD, col_w, 52, 24, minimum=15,
                                  leading=1.05)
        draw_lines(d, x, cy, lines, f_h, INK, leading=1.05)
        cy += int(h) + 4
        f_b, lines, h = fit_block(d, st["body"], SANS, col_w, col_bottom - cy, 14,
                                  minimum=11, leading=1.16)
        draw_lines(d, x, cy, lines, f_b, INK, leading=1.16)
        if i:
            d.line([x - 10, y, x - 10, col_bottom], fill=(190, 184, 170), width=1)

    # ---- footer ---------------------------------------------------------
    rule(d, PAGE - 36, 1, GREY)
    credits = ("Photos via Wikimedia Commons: V. Vlasenko (CC BY 4.0) - Txllxt TxllxT "
               "(CC BY-SA 4.0) - W. de Silva (CC BY-SA 4.0) - C. Delgado (CC BY-SA 3.0)")
    f_f = font(SANS, fit_size(d, credits, SANS, WIDTH, 13, minimum=9))
    d.text((MARGIN + (WIDTH - text_w(d, credits, f_f)) / 2, PAGE - 28),
           credits, font=f_f, fill=GREY)

    page.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
