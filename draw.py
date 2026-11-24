#!/usr/bin/env python3
"""Draw the front page of THE WORLD IN ONE DAY — 24 November 2026.

Pure stdlib + Pillow, no network. Writes /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png), 1024x1024, deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (163, 22, 33)
GREY = (90, 90, 90)
SKY = (191, 211, 230)
SEA = (127, 163, 196)
ISLAND = (90, 125, 79)
STEEL = (60, 60, 60)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, f, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y just below it."""
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def rule(d, x0, x1, y, w=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=w)


def draw_jet(d, x, y, s, color):
    """Side-view delta jet silhouette, nose to the right, scale s."""
    body = [(x, y + 6 * s), (x + 34 * s, y + 2 * s), (x + 62 * s, y + 6 * s),
            (x + 66 * s, y + 9 * s), (x + 34 * s, y + 12 * s), (x, y + 9 * s)]
    d.polygon(body, fill=color)
    d.polygon([(x + 26 * s, y + 2 * s), (x + 40 * s, y - 12 * s),
               (x + 48 * s, y - 12 * s), (x + 40 * s, y + 2 * s)], fill=color)
    d.polygon([(x + 30 * s, y + 12 * s), (x + 40 * s, y + 20 * s),
               (x + 46 * s, y + 20 * s), (x + 40 * s, y + 12 * s)], fill=color)
    d.polygon([(x + 4 * s, y + 2 * s), (x + 10 * s, y - 8 * s),
               (x + 16 * s, y - 8 * s), (x + 12 * s, y + 2 * s)], fill=color)


def draw_lead_art(d, x0, y0, x1, y1):
    """Sky, sea, island, two jets, radar arcs, alert triangle."""
    d.rectangle([x0, y0, x1, y0 + (y1 - y0) * 0.62], fill=SKY)
    d.rectangle([x0, y0 + (y1 - y0) * 0.62, x1, y1], fill=SEA)
    # radar arcs from the island
    cx, cy = x0 + 90, y0 + (y1 - y0) * 0.62
    for r in (46, 78, 110):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340,
              fill=(255, 255, 255), width=2)
    # island
    d.polygon([(x0 + 30, y0 + (y1 - y0) * 0.62), (x0 + 70, y0 + (y1 - y0) * 0.42),
               (x0 + 130, y0 + (y1 - y0) * 0.46), (x0 + 165, y0 + (y1 - y0) * 0.62)],
              fill=ISLAND)
    d.rectangle([x0 + 88, y0 + (y1 - y0) * 0.30, x0 + 96, y0 + (y1 - y0) * 0.44],
                fill=(120, 40, 40))
    # jets
    draw_jet(d, x0 + 150, y0 + 34, 1, (30, 30, 30))
    draw_jet(d, x0 + 210, y0 + 96, 1, (70, 70, 70))
    # alert triangle
    tx, ty = x1 - 78, y0 + 22
    d.polygon([(tx, ty + 52), (tx + 30, ty), (tx + 60, ty + 52)], fill=RED)
    d.text((tx + 24, ty + 14), "!", font=SANS_B(30), fill=(255, 255, 255))
    # wave lines
    for wy in (y1 - 34, y1 - 18):
        d.line([(x0 + 14, wy), (x0 + 60, wy)], fill=(255, 255, 255), width=2)
        d.line([(x0 + 90, wy), (x0 + 150, wy)], fill=(255, 255, 255), width=2)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_rubble(d, x, y, w, h):
    """Broken apartment blocks with smoke."""
    d.rectangle([x, y + h * 0.45, x + w * 0.42, y + h], fill=(120, 118, 112))
    d.rectangle([x + w * 0.52, y + h * 0.25, x + w, y + h], fill=(96, 94, 88))
    d.polygon([(x, y + h * 0.45), (x + w * 0.14, y + h * 0.28),
               (x + w * 0.28, y + h * 0.45)], fill=(120, 118, 112))
    for wx in (6, 30, 58):
        d.rectangle([x + wx, y + h * 0.58, x + wx + 12, y + h * 0.74],
                    fill=(60, 58, 54))
    for sx, sy, sr in ((x + w * 0.30, y + 8, 10), (x + w * 0.48, y + 2, 13),
                       (x + w * 0.68, y + 10, 9)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(170, 168, 160))
    d.polygon([(x + w * 0.80, y + h * 0.25), (x + w * 0.88, y + h * 0.05),
               (x + w * 0.96, y + h * 0.25)], fill=(220, 110, 30))


def draw_tanker(d, x, y, w, h):
    """Oil tanker, spiked mine and flames on a dark sea."""
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(36, 68, 96))
    d.rectangle([x + w * 0.08, y + h * 0.34, x + w * 0.88, y + h * 0.58],
                fill=(25, 25, 25))
    d.rectangle([x + w * 0.70, y + h * 0.14, x + w * 0.82, y + h * 0.36],
                fill=(25, 25, 25))
    d.rectangle([x + w * 0.10, y + h * 0.40, x + w * 0.86, y + h * 0.46],
                fill=(200, 60, 30))
    mx, my, mr = x + w * 0.16, y + h * 0.20, 11
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([(mx + int(mr * 0.7 * math.cos(a)), my + int(mr * 0.7 * math.sin(a))),
                (mx + int(mr * 1.6 * math.cos(a)), my + int(mr * 1.6 * math.sin(a)))],
               fill=(20, 20, 20), width=3)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(20, 20, 20))
    d.polygon([(x + w * 0.42, y + h * 0.34), (x + w * 0.50, y + h * 0.08),
               (x + w * 0.58, y + h * 0.34)], fill=(235, 130, 30))
    d.polygon([(x + w * 0.56, y + h * 0.34), (x + w * 0.64, y + h * 0.14),
               (x + w * 0.72, y + h * 0.34)], fill=(240, 180, 40))


def draw_plane(d, x, y, w, h):
    """Airliner climbing away, with a runway line below."""
    d.line([(x, y + h - 6), (x + w, y + h - 6)], fill=STEEL, width=3)
    draw_jet(d, x + w * 0.18, y + h * 0.30, 1, (40, 40, 40))
    d.polygon([(x + w * 0.72, y + h * 0.30), (x + w * 0.80, y + h * 0.18),
               (x + w * 0.86, y + h * 0.30)], fill=RED)


def draw_rocket_car(d, x, y, w, h):
    """A rocket lifting off beside a low car silhouette."""
    rx, ry = x + w * 0.20, y + 4
    d.polygon([(rx, ry + 44), (rx + 8, ry + 20), (rx + 16, ry + 20),
               (rx + 24, ry + 44)], fill=(230, 230, 230), outline=INK)
    d.polygon([(rx, ry + 20), (rx + 12, ry), (rx + 24, ry + 20)], fill=RED)
    d.polygon([(rx, ry + 44), (rx - 8, ry + 56), (rx, ry + 44)], fill=RED)
    d.polygon([(rx + 24, ry + 44), (rx + 32, ry + 56), (rx + 24, ry + 44)],
              fill=RED)
    d.polygon([(rx + 8, ry + 56), (rx + 12, ry + 70), (rx + 16, ry + 56)],
              fill=(240, 160, 30))
    cx, cy = x + w * 0.55, y + h - 26
    d.rounded_rectangle([cx, cy, cx + w * 0.42, cy + 16], radius=7, fill=INK)
    d.polygon([(cx + 8, cy), (cx + 18, cy - 10), (cx + w * 0.30, cy - 10),
               (cx + w * 0.36, cy)], fill=INK)
    for wx in (cx + 10, cx + w * 0.30):
        d.ellipse([wx, cy + 12, wx + 12, cy + 24], fill=(20, 20, 20),
                  outline=(255, 255, 255))


def draw_chip(d, x, y, w, h):
    """A chip crossed by a red ban circle."""
    d.rectangle([x + w * 0.22, y + 6, x + w * 0.78, y + h - 6], fill=(30, 30, 30))
    for i in range(4):
        px = x + w * (0.30 + i * 0.14)
        d.line([(px, y), (px, y + 6)], fill=STEEL, width=3)
        d.line([(px, y + h - 6), (px, y + h)], fill=STEEL, width=3)
    d.rectangle([x + w * 0.36, y + h * 0.30, x + w * 0.64, y + h * 0.70],
                outline=(200, 200, 200), width=2)
    cx, cy, r = x + w * 0.50, y + h * 0.50, h * 0.46
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=5)
    d.line([(cx - r * 0.7, cy + r * 0.7), (cx + r * 0.7, cy - r * 0.7)],
           fill=RED, width=5)


def draw_satellite(d, x, y, s):
    """Small satellite: body, two panels, dish."""
    d.rectangle([x, y + 8 * s, x + 26 * s, y + 26 * s], fill=STEEL)
    d.rectangle([x - 26 * s, y + 12 * s, x, y + 22 * s], fill=(70, 110, 160))
    d.rectangle([x + 26 * s, y + 12 * s, x + 52 * s, y + 22 * s],
                fill=(70, 110, 160))
    d.line([(x + 13 * s, y + 8 * s), (x + 20 * s, y)], fill=STEEL, width=2)
    d.ellipse([x + 16 * s, y - 4 * s, x + 24 * s, y + 4 * s], outline=STEEL,
              width=2)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    R = W - M  # right edge

    # ---- Masthead ----
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(60)
    d.text(((W - d.textlength(title, font=tf)) / 2, 26), title, font=tf,
           fill=INK)
    rule(d, M, R, 106, 3)
    rule(d, M, R, 112, 1)
    d.text((M, 122), "TUESDAY, 24 NOVEMBER 2026", font=SANS_B(20), fill=INK)
    tag = "SIX STORIES · ONE DAY"
    d.text((R - d.textlength(tag, font=SANS_B(20)), 122), tag,
           font=SANS_B(20), fill=INK)
    rule(d, M, R, 152, 2)

    # ---- Lead story: Russian jets / Ulleung ----
    draw_lead_art(d, 680, 168, R, 400)
    d.text((M, 168), "LEAD", font=SANS_B(18), fill=RED)
    hy = 192
    for line in ["RUSSIAN JETS SPARK", "KOREA AIR ALERT"]:
        d.text((M, hy), line, font=SERIF_B(46), fill=INK)
        hy += 54
    deck = ("Seoul scrambles F-15K fighters as Russian warplanes enter the "
            "air-defence zone near Ulleung Island. Islanders are told to "
            "shelter — the warning is lifted five minutes later.")
    para(d, M, 306, deck, SANS(23), 620, 30)
    d.text((M, 434), "NO VIOLATION OF AIRSPACE, SEOUL SAYS",
           font=SANS_B(17), fill=RED)
    rule(d, M, R, 460, 2)

    # ---- Middle row: two stories ----
    mid_y = 476
    col_w = 462
    # Zaporizhzhia (left)
    x = M
    draw_rubble(d, x, mid_y, 120, 64)
    d.text((x + 132, mid_y + 6), "UKRAINE", font=SANS_B(17), fill=RED)
    d.text((x + 132, mid_y + 28), "OVERNIGHT ATTACK", font=SANS(15), fill=GREY)
    hy = mid_y + 76
    for line in ["Strike on Zaporizhzhia", "kills 2, wounds 22"]:
        d.text((x, hy), line, font=SERIF_B(30), fill=INK)
        hy += 34
    para(d, x, hy + 4,
         "A Russian overnight attack hits homes in Zaporizhzhia; 22 wounded, "
         "two children.",
         SANS(19), col_w, 24)
    # Hormuz tankers (right)
    x = 526
    draw_tanker(d, x, mid_y, 120, 64)
    d.text((x + 132, mid_y + 6), "THE GULF", font=SANS_B(17), fill=RED)
    d.text((x + 132, mid_y + 28), "STRAIT OF HORMUZ", font=SANS(15), fill=GREY)
    hy = mid_y + 76
    for line in ["Iran says three tankers", "hit mines in Hormuz"]:
        d.text((x, hy), line, font=SERIF_B(30), fill=INK)
        hy += 34
    para(d, x, hy + 4,
         "Tehran's Revolutionary Guards say three oil tankers caught fire "
         "after striking naval mines.",
         SANS(19), col_w, 24)
    rule(d, M, R, 690, 2)

    # ---- Bottom row: three stories ----
    bot_y = 706
    bw = 304
    cols = [
        (M, "BANGLADESH", ["Hasina plans return", "on 16 December"],
         "In exile since 2024, she says she will fly home on Victory Day.",
         draw_plane),
        (M + 312, "BUSINESS", ["Five directors named", "for Musk merger talks"],
         "Five directors will steer talks on combining the two companies.",
         draw_rocket_car),
        (M + 624, "CHIPS & SPYING", ["US blacklists Megaspeed", "in Nvidia scandal"],
         "Washington bars the chip firm and Alibaba's Apex from US tech.",
         draw_chip),
    ]
    for x, kick, head_lines, deck, art in cols:
        art(d, x, bot_y, 120, 54)
        d.text((x + 132, bot_y + 8), kick, font=SANS_B(15), fill=RED)
        d.text((x + 132, bot_y + 30), "24 NOV", font=SANS(14), fill=GREY)
        hy = bot_y + 66
        for line in head_lines:
            d.text((x, hy), line, font=SERIF_B(24), fill=INK)
            hy += 30
        para(d, x, hy + 2, deck, SANS(18), bw, 23)
    rule(d, M, R, 900, 2)

    # ---- Box strip: NATO / satellite ----
    d.text((M, 914), "ALSO TODAY", font=SANS_B(18), fill=RED)
    para(d, M, 940,
         "NATO vows to defend space after reports Russia is ready to launch a "
         "nuclear-armed satellite, 'Sputnik-S'.",
         SANS(20), 830, 26)
    draw_satellite(d, 920, 920, 1)

    img.save(os.path.join(outdir, "entry.png"))
    print("wrote", os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    main()
