#!/usr/bin/env python3
"""render.py -- draw THE WORLD IN ONE DAY, a newspaper front-page poster
summing up world news of Monday 23 November 2026, as a 1024x1024 PNG.

Pure Python 3.13 standard library only (zlib, struct, binascii). No network,
no files read, no randomness, no clock: every run writes identical bytes.
All drawing is hand-built in this file: a 5x7 bitmap font, a small vector
rasteriser (rects, lines, circles, polygons) and a hand-rolled PNG encoder.
"""
import binascii
import struct
import zlib

W = H = 1024

# ---------------------------------------------------------------- font ----
# A 5-wide, 7-tall bitmap font. Each glyph is 7 rows of 5 cells, '#' = ink.
FONT = {
"A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
"B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
"C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
"D": ("###..", "#..#.", "#...#", "#...#", "#...#", "#..#.", "###.."),
"E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
"F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
"G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
"H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
"I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
"J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
"K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
"L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
"M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
"N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
"O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
"P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
"Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
"R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
"S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
"T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
"U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
"V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
"W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
"X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
"Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
"Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
"0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
"1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
"2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
"3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
"4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
"5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
"6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
"7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
"8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
"9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
"a": (".....", ".....", ".####", "....#", ".####", "#...#", ".####"),
"b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
"c": (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
"d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
"e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
"f": ("..##.", ".#..#", ".#...", "####.", ".#...", ".#...", ".#..."),
"g": (".....", ".....", ".####", "#...#", "#...#", ".####", "....#"),
"h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
"i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
"j": ("...#.", ".....", "..##.", "...#.", "...#.", "...#.", "...#.", "##..."),
"k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
"l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
"m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
"n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
"o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
"p": (".....", ".....", "####.", "#...#", "#...#", "####.", "#...."),
"q": (".....", ".....", ".####", "#...#", "#...#", ".####", "....#"),
"r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
"s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
"t": (".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."),
"u": (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
"v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
"w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
"x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
"y": (".....", ".....", "#...#", "#...#", "#...#", ".####", "....#"),
"z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
" ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
"!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
"?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
"'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
'"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
"-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
"–": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
"—": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
"(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
"/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
"&": (".###.", "#...#", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
"%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
"+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
"=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
"$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
"·": (".....", ".....", ".....", ".##..", ".##..", ".....", "....."),
"•": (".....", ".###.", "#####", "#####", ".###.", ".....", "....."),
"°": (".###.", "#...#", ".###.", ".....", ".....", ".....", "....."),
"#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
"@": (".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."),
"[": (".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."),
"]": (".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."),
"_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
"*": (".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."),
"<": ("...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."),
">": (".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."),
}
# The descender glyphs j, g and y get their hook on the 7th row so every
# glyph stays exactly 7 rows tall.
FONT["j"] = ("...#.", ".....", "..##.", "...#.", "...#.", "...#.", ".##..")
FONT["g"] = (".....", ".....", ".####", "#...#", "#...#", ".####", "....#")
FONT["y"] = (".....", ".....", "#...#", "#...#", "#...#", ".####", "....#")

# ---------------------------------------------------------------- canvas ---
PAPER = (247, 243, 232)   # warm newsprint
INK = (17, 17, 17)
RED = (176, 32, 32)
BLUE = (31, 78, 121)
NAVY = (23, 43, 77)
GREEN = (46, 110, 58)
TEAL = (14, 110, 110)
PURPLE = (96, 54, 130)
ORANGE = (196, 94, 10)
BROWN = (122, 74, 32)
PINK = (168, 54, 96)
GOLD = (158, 118, 20)
GREY = (110, 106, 96)
LIGHT = (226, 220, 205)
SKY = (183, 211, 230)
SEA = (38, 84, 124)
DARKSEA = (22, 52, 82)

buf = bytearray(W * H * 3)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = c


def fill_rect(x0, y0, x1, y1, c):
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(W, x1); y1 = min(H, y1)
    for y in range(y0, y1):
        base = (y * W + x0) * 3
        for x in range(x0, x1):
            i = base + (x - x0) * 3
            buf[i], buf[i + 1], buf[i + 2] = c


def hline(x0, x1, y, c):
    for x in range(max(0, x0), min(W, x1)):
        px(x, y, c)


def vline(x, y0, y1, c):
    for y in range(max(0, y0), min(H, y1)):
        px(x, y, c)


def line(x0, y0, x1, y1, c):
    dx = abs(x1 - x0); dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        px(x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy; x0 += sx
        if e2 <= dx:
            err += dx; y0 += sy


def disc(cx, cy, r, c):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r:
                px(x, y, c)


def ring(cx, cy, r, t, c):
    for y in range(cy - r - t, cy + r + t + 1):
        for x in range(cx - r - t, cx + r + t + 1):
            d2 = (x - cx) * (x - cx) + (y - cy) * (y - cy)
            if (r - t) * (r - t) <= d2 <= (r + t) * (r + t):
                px(x, y, c)


def poly(points, c):
    # Scanline fill for a simple polygon given as [(x, y), ...].
    ys = [p[1] for p in points]
    for y in range(min(ys), max(ys) + 1):
        xs = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(xs[i]), int(xs[i + 1]) + 1):
                px(x, y, c)


# ------------------------------------------------------------------- text ---
def glyph(ch):
    return FONT.get(ch, FONT["?"])


def text_w(s, scale, bold=False):
    return len(s) * 6 * scale + (len(s) * scale if bold else 0)


def draw_char(x, y, scale, ch, c, bold=False):
    g = glyph(ch)
    for r in range(7):
        row = g[r]
        for col in range(5):
            if row[col] == "#":
                fill_rect(x + col * scale, y + r * scale,
                          x + col * scale + scale, y + r * scale + scale, c)
                if bold:
                    fill_rect(x + col * scale + scale, y + r * scale,
                              x + col * scale + 2 * scale,
                              y + r * scale + scale, c)
    return 6 * scale


def draw_text(x, y, scale, s, c, bold=False, align="l"):
    if align == "c":
        x -= text_w(s, scale, bold) // 2
    elif align == "r":
        x -= text_w(s, scale, bold)
    cx = x
    for ch in s:
        cx += draw_char(cx, y, scale, ch, c, bold)
    return cx


def wrap(s, scale, max_w):
    """Word-wrap to lines of at most max_w pixels; returns list of lines."""
    words = s.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# -------------------------------------------------------------------- png ---
def chunk(typ, data):
    return (struct.pack(">I", len(data)) + typ + data +
            struct.pack(">I", binascii.crc32(typ + data) & 0xFFFFFFFF))


def encode_png():
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
           chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))
    return png

# ------------------------------------------------------------------ scenes ---
def chord(cx, cy, r, dy, c):
    half = int((r * r - dy * dy) ** 0.5)
    line(cx - half, cy + dy, cx + half, cy + dy, c)


def draw_lead_scene(x0, y0, x1, y1):
    """COP31: a globe over cracked ground, factories smoking behind it."""
    fill_rect(x0, y0, x1, y1, SKY)
    # sun
    disc(x1 - 52, y0 + 34, 20, GOLD)
    for a in range(8):
        import math
        ang = a * 3.14159 / 4
        line(int(x1 - 52 + 26 * math.cos(ang)), int(y0 + 34 + 26 * math.sin(ang)),
             int(x1 - 52 + 34 * math.cos(ang)), int(y0 + 34 + 34 * math.sin(ang)), GOLD)
    # globe
    cx, cy, r = x0 + 118, y0 + 104, 74
    disc(cx, cy, r, SEA)
    ring(cx, cy, r, 2, NAVY)
    for dy in (-38, 0, 38):
        chord(cx, cy, r, dy, (96, 148, 190))
    chord(cx - 30, cy, r, 0, (96, 148, 190))
    poly([(cx - 52, cy - 30), (cx - 18, cy - 52), (cx + 6, cy - 34),
          (cx - 6, cy - 8), (cx - 40, cy - 6)], GREEN)
    poly([(cx + 12, cy + 6), (cx + 48, cy - 6), (cx + 58, cy + 26),
          (cx + 30, cy + 44), (cx + 8, cy + 30)], GREEN)
    poly([(cx - 46, cy + 34), (cx - 20, cy + 26), (cx - 8, cy + 52),
          (cx - 34, cy + 58)], GREEN)
    # factory silhouettes, right side
    fill_rect(x1 - 128, y1 - 96, x1 - 100, y1 - 34, (74, 74, 78))
    fill_rect(x1 - 92, y1 - 78, x1 - 52, y1 - 34, (74, 74, 78))
    fill_rect(x1 - 44, y1 - 64, x1 - 16, y1 - 34, (74, 74, 78))
    for dx, dy in ((-116, -104), (-108, -116), (-72, -88), (-64, -100), (-30, -74)):
        disc(x1 + dx, y1 + dy, 7, (200, 198, 190))
    # cracked ground
    fill_rect(x0, y1 - 34, x1, y1, (86, 96, 58))
    line(x0 + 8, y1 - 20, x0 + 70, y1 - 12, INK)
    line(x0 + 70, y1 - 12, x0 + 120, y1 - 24, INK)
    line(x0 + 120, y1 - 24, x0 + 190, y1 - 10, INK)
    line(x0 + 190, y1 - 10, x0 + 250, y1 - 22, INK)
    line(x0 + 250, y1 - 22, x0 + 330, y1 - 12, INK)
    line(x0 + 330, y1 - 12, x1 - 8, y1 - 20, INK)
    # three small flags on poles, top left
    for i, fc in enumerate((BLUE, RED, GREEN)):
        fx = x0 + 22 + i * 34
        vline(fx, y0 + 12, y0 + 44, INK)
        fill_rect(fx, y0 + 12, fx + 24, y0 + 26, fc)


def draw_merkury_scene(x0, y0, x1, y1):
    """A warship listing and sinking at night, sea drones overhead."""
    fill_rect(x0, y0, x1, y1, DARKSEA)
    for wy in (y1 - 26, y1 - 44, y1 - 62):
        for wx in range(x0 + 6, x1 - 20, 26):
            line(wx, wy, wx + 14, wy + 3, (120, 170, 205))
    # listing hull
    poly([(x0 + 18, y1 - 58), (x0 + 128, y1 - 84), (x0 + 138, y1 - 66),
          (x0 + 40, y1 - 40)], (40, 40, 44))
    line(x0 + 30, y1 - 62, x0 + 118, y1 - 82, (200, 200, 200))
    # mast and funnel
    line(x0 + 66, y1 - 74, x0 + 66, y1 - 104, (40, 40, 44))
    fill_rect(x0 + 84, y1 - 96, x0 + 96, y1 - 76, (40, 40, 44))
    # explosion star at the bow
    ex, ey = x0 + 128, y1 - 92
    poly([(ex, ey - 18), (ex + 5, ey - 5), (ex + 18, ey - 4), (ex + 8, ey + 5),
          (ex + 12, ey + 16), (ex, ey + 9), (ex - 12, ey + 16), (ex - 8, ey + 5),
          (ex - 18, ey - 4), (ex - 5, ey - 5)], ORANGE)
    disc(ex, ey, 5, GOLD)
    # smoke
    disc(x0 + 90, y1 - 108, 8, (150, 150, 150))
    disc(x0 + 100, y1 - 118, 6, (170, 170, 170))
    # three sea drones
    for dx, dy in ((x0 + 26, y0 + 22), (x0 + 66, y0 + 12), (x0 + 108, y0 + 24)):
        disc(dx, dy, 4, INK)
        line(dx - 10, dy + 6, dx - 2, dy + 2, (220, 220, 220))
        line(dx + 2, dy + 2, dx + 10, dy + 6, (220, 220, 220))


def draw_dymer_scene(x0, y0, x1, y1):
    """A block of flats with one corner collapsed, ladder and rescuers."""
    fill_rect(x0, y0, x1, y1, (214, 208, 192))
    # standing part of the block
    fill_rect(x0 + 18, y0 + 16, x0 + 92, y1 - 26, (120, 118, 112))
    for wy in range(y0 + 28, y1 - 40, 22):
        for wx in (x0 + 30, x0 + 52, x0 + 74):
            fill_rect(wx, wy, wx + 10, wy + 12, (52, 52, 56))
    # collapsed corner, tilted
    poly([(x0 + 92, y0 + 60), (x0 + 132, y0 + 78), (x0 + 138, y1 - 26),
          (x0 + 92, y1 - 26)], (96, 94, 88))
    poly([(x0 + 100, y0 + 96), (x0 + 130, y0 + 106), (x0 + 134, y1 - 26),
          (x0 + 100, y1 - 26)], (70, 68, 64))
    # rubble
    poly([(x0 + 96, y1 - 26), (x0 + 118, y1 - 52), (x0 + 140, y1 - 26)], BROWN)
    poly([(x0 + 118, y1 - 26), (x0 + 136, y1 - 46), (x0 + 148, y1 - 26)], (96, 94, 88))
    # dust
    disc(x0 + 116, y1 - 56, 9, (200, 196, 186))
    disc(x0 + 130, y1 - 66, 6, (210, 206, 196))
    # ladder against the standing block
    line(x0 + 34, y1 - 26, x0 + 52, y0 + 44, ORANGE)
    line(x0 + 42, y1 - 26, x0 + 60, y0 + 44, ORANGE)
    for i in range(5):
        t = i / 4
        rx = int(x0 + 34 + (52 - 34) * t)
        ry = int(y1 - 26 + (y0 + 44 - (y1 - 26)) * t)
        line(rx, ry, rx + 8, ry, ORANGE)
    # rescuer figure
    disc(x0 + 118, y1 - 74, 5, INK)
    line(x0 + 118, y1 - 69, x0 + 118, y1 - 48, ORANGE)
    line(x0 + 118, y1 - 62, x0 + 108, y1 - 54, ORANGE)
    line(x0 + 118, y1 - 48, x0 + 110, y1 - 26, INK)
    line(x0 + 118, y1 - 48, x0 + 126, y1 - 26, INK)


# ----------------------------------------------------------------- stories ---
# (headline, fact, category colour) -- every fact verified against reporting
# of 23 November 2026 (see README.md for the source of each story).
GRID = [
    ("MARKETS TUMBLE", "Nikkei -5.1%; S&P 500 -3.7% in AI sell-off.", BLUE),
    ("DEMOCRATS WIN 258", "Largest House majority since 1992, AP says.", NAVY),
    ("TRUMP WARNS IRAN", "Trump: war if Iran deal fails by New Year.", RED),
    ("THE PENNY IS DEAD", "Trump signs Common Cents Act; 232-year run ends.", GOLD),
    ("DELTA FLIGHTS DELAYED", "System failure snarls Atlanta at holiday start.", BLUE),
    ("NVIDIA CHIEF QUITS", "Nvidia chief quits amid US probe of China chip sales.", PURPLE),
    ("CARTEL KINGPIN CAUGHT", "FBI most-wanted Fausto Isidro Meza Flores seized.", RED),
    ("BALTIC FREIGHTER HIT", "Russian ship Sparta II hit by drone off Finland.", NAVY),
    ("PROBE REACHES MERCURY", "ESA-JAXA craft enters orbit after eight years.", TEAL),
    ("FACTORY FIRE KILLS 24", "Banten factory blaze; dozens still missing.", BROWN),
    ("SEATTLE ICE PROTESTS", "Masked officers detain a family; video goes viral.", RED),
    ("US DEPORTED A CITIZEN", "Justice Dept: a US citizen was sent to Mexico.", NAVY),
    ("BELGIUM AIRPORTS SHUT", "Controllers join national anti-austerity strike.", BLUE),
    ("EUROPE GAS JUMPS 8.6%", "Cold forecasts lift futures to about 96 euros.", GREEN),
    ("ALCARAZ WINS ATP TITLE", "Beats world No. 1 Zverev 6-2, 7-6 in Turin.", ORANGE),
    ("LIVERPOOL 4, UNITED 0", "Pochettino's first game as boss ends in a rout.", ORANGE),
    ("MARQUEZ WINS 8TH TITLE", "Equals Agostini's record in Portugal.", ORANGE),
    ("BOCA END 18-YEAR WAIT", "Beat Atletico Mineiro 2-0 to win Copa Sudamericana.", ORANGE),
    ("RIEMANN PROOF CLAIMED", "Mathematician posts proof; years to verify it.", PURPLE),
    ("A YEAR ON A PIG KIDNEY", "Molly Falco, 58, marks a transplant record.", PINK),
    ("24 KILLED IN S. SUDAN", "Paramilitary attack kills seven children.", RED),
    ("DRONES HIT KHARTOUM", "Strikes hit homes and a UN office in Khartoum.", RED),
    ("HOUTHIS HIT SAUDI OIL", "Saudi strike on Hodeida kills four, wounds 18.", RED),
    ("GAZA: TOXIC WASTELAND", "Study finds contamination across 99% of Gaza.", BROWN),
    ("NEPAL PM VISITS INDIA", "First foreign trip brings 15,000-crore aid.", GREEN),
    ("MONGOLIA LEADER QUITS", "Parliament approves the president's resignation.", NAVY),
    ("KOREA MINISTER RESIGNS", "Education chief quits over AI-cheating exam chaos.", NAVY),
]


# ------------------------------------------------------------------ layout ---
def draw():
    fill_rect(0, 0, W, H, PAPER)
    # outer frame
    fill_rect(0, 0, W, 5, INK)
    fill_rect(0, H - 5, W, H, INK)
    fill_rect(0, 0, 5, H, INK)
    fill_rect(W - 5, 0, W, H, INK)

    # ---- masthead
    draw_text(512, 14, 3, "THE WORLD IN ONE DAY", INK, bold=True, align="c")
    draw_text(512, 42, 5, "MONDAY 23 NOVEMBER 2026", INK, bold=True, align="c")
    draw_text(512, 86, 2, "ONE DAY · 30 STORIES · EVERY REGION · THE NEWS THAT MADE MONDAY",
              GREY, align="c")
    fill_rect(16, 108, 1008, 111, INK)
    fill_rect(16, 114, 1008, 115, INK)

    # ---- lead story: COP31 collapse
    draw_lead_scene(16, 122, 460, 332)
    draw_text(476, 128, 2, "CLIMATE · ANTALYA, TURKIYE", RED, bold=True)
    draw_text(476, 152, 4, "CLIMATE TALKS", INK, bold=True)
    draw_text(476, 184, 4, "COLLAPSE", INK, bold=True)
    fill_rect(476, 216, 640, 220, RED)
    ly = 230
    for ln in wrap("COP31 ends with no deal after the EU and about 130 nations "
                   "reject a draft text that says nothing about phasing out "
                   "fossil fuels.", 2, 532):
        draw_text(476, ly, 2, ln, INK)
        ly += 16
    draw_text(476, 286, 2, "200 NATIONS · NO FOSSIL-FUEL DEAL", BLUE, bold=True)
    draw_text(476, 308, 2, "The longest climate talks ever end empty.", GREY)

    # ---- secondary stories
    fill_rect(16, 338, 1008, 339, LIGHT)
    draw_merkury_scene(16, 344, 166, 500)
    draw_text(178, 350, 2, "WAR AT SEA · BENGHAZI", RED, bold=True)
    draw_text(178, 372, 3, "UKRAINE SINKS", INK, bold=True)
    draw_text(178, 395, 3, "RUSSIAN WARSHIP", INK)
    sy = 424
    for ln in wrap("Sea drones sink the corvette Merkury; 10 hurt.", 2, 314):
        draw_text(178, sy, 2, ln, INK)
        sy += 16

    draw_dymer_scene(520, 344, 670, 500)
    draw_text(682, 350, 2, "UKRAINE · KYIV REGION", RED, bold=True)
    draw_text(682, 372, 3, "BOY, 7, PULLED", INK, bold=True)
    draw_text(682, 395, 3, "FROM THE RUBBLE", INK)
    sy = 424
    for ln in wrap("Russian strike flattens a block of flats; 11 dead.", 2, 314):
        draw_text(682, sy, 2, ln, INK)
        sy += 16

    # ---- grid of the day's other stories
    fill_rect(16, 506, 1008, 507, INK)
    gx = [16, 350, 684]
    for r in range(9):
        y = 514 + r * 52
        if r:
            for x in range(16, 1008):
                px(x, y - 4, LIGHT)
        for c in range(3):
            x = gx[c]
            if c:
                vline(x - 6, y, y + 48, LIGHT)
            head, fact, col = GRID[r * 3 + c]
            fill_rect(x, y + 2, x + 4, y + 48, col)
            draw_text(x + 10, y + 2, 2, head, INK, bold=True)
            fy = y + 20
            for ln in wrap(fact, 2, 312)[:2]:
                draw_text(x + 10, fy, 2, ln, INK)
                fy += 15

    # ---- footer
    fill_rect(16, 986, 1008, 987, INK)
    draw_text(512, 996, 2, "MONDAY 23 NOVEMBER 2026 · 30 STORIES · DRAWN FROM THE DAY'S REPORTING",
              GREY, align="c")


def main():
    import os
    draw()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")
    with open(out, "wb") as f:
        f.write(encode_png())
    print("wrote", out)


if __name__ == "__main__":
    main()
