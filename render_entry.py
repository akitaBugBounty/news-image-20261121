#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261121.

Front-page newspaper style, 1024x1024, drawn from scratch with PIL:
masthead + date bar, lead story (Russia's barrage / Poland), then
S&P 500 correction, COP31 overtime, UK-EU deal, and an ALSO footer.

All text is the verified wording from the build brief; nothing else is
added. Motifs are simple shapes drawn here (sky + missile streaks,
falling chart, globe, flag blocks) -- no photos, logos or copied art.

Run:  python3 render_entry.py   (writes entry.png next to this script)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

PAPER = (247, 244, 235)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (24, 48, 84)
BLUE = (30, 90, 160)
SKY = (16, 32, 64)
GREY = (96, 92, 84)
PANEL = (233, 229, 217)
WHITE = (255, 255, 255)
ORANGE = (224, 122, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

M = 48  # side margin


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit_font(draw, text, path, start, max_w):
    """Largest size (<= start) at which text fits max_w on one line."""
    size = start
    while size > 10 and text_w(draw, text, font(path, size)) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; returns y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, text):
    fnt = font(SANS_B, 21)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + 30


def headline(draw, x, y, text, max_w, size, max_lines=3):
    """Serif-bold headline, wrapped, shrinking until it fits max_lines."""
    while size > 24:
        fnt = font(SERIF_B, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            break
        size -= 2
    fnt = font(SERIF_B, size)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += int(size * 1.12)
    return y


def body(draw, x, y, text, max_w, size=24):
    fnt = font(SANS, size)
    return draw_wrapped(draw, x, y, text, fnt, max_w, int(size * 1.38))


# ---------------------------------------------------------------- lead art
def draw_sky_panel(draw, x0, y0, x1, y1):
    """Night sky: drone dots, missile streaks, one burst. All drawn here."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # stars / drone dots
    dots = [(30, 26), (90, 14), (150, 34), (210, 18), (260, 40),
            (60, 60), (130, 74), (200, 62), (290, 70), (170, 100)]
    for dx, dy in dots:
        draw.ellipse([x0 + dx - 2, y0 + dy - 2, x0 + dx + 2, y0 + dy + 2],
                     fill=WHITE)
    # missile streaks (orange lines with a bright head)
    streaks = [(20, 104, 150, 76), (55, 118, 200, 88), (125, 126, 285, 96)]
    for sx, sy, ex, ey in streaks:
        draw.line([(x0 + sx, y0 + sy), (x0 + ex, y0 + ey)],
                  fill=ORANGE, width=4)
        draw.ellipse([x0 + ex - 5, y0 + ey - 5, x0 + ex + 5, y0 + ey + 5],
                     fill=(255, 200, 90))
    # burst where a missile lands
    bx, by = x0 + 300, y0 + 60
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 10, 26
        a = math.radians(ang)
        draw.line([(bx + r1 * math.cos(a), by + r1 * math.sin(a)),
                   (bx + r2 * math.cos(a), by + r2 * math.sin(a))],
                  fill=(255, 200, 90), width=3)
    draw.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED,
                 outline=(255, 200, 90), width=2)


def draw_chart_panel(draw, x0, y0, x1, y1):
    """Falling market line with candlesticks on a white panel."""
    draw.rectangle([x0, y0, x1, y1], fill=WHITE)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # axes
    draw.line([(x0 + 14, y1 - 34), (x1 - 14, y1 - 34)], fill=GREY, width=2)
    # descending line: S&P into correction (kept clear of the label)
    pts = [(x0 + 24, y0 + 18), (x0 + 90, y0 + 30), (x0 + 150, y0 + 26),
           (x0 + 210, y0 + 46), (x0 + 260, y0 + 58), (x0 + 292, y1 - 52)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    # small red candlesticks on the right side only, clear of the label
    for cx, top, bot in [(196, 52, 70), (238, 66, 84), (272, 78, 98)]:
        draw.rectangle([x0 + cx, y0 + top, x0 + cx + 14, y0 + bot], fill=RED)
    # big fall label, bottom-left under the line's start
    fnt = font(SANS_B, 44)
    draw.text((x0 + 24, y1 - 96), "-3.7%", font=fnt, fill=RED)


def draw_globe_panel(draw, x0, y0, x1, y1):
    """Simple globe: blue disc, meridians, red clock hands for overtime."""
    draw.rectangle([x0, y0, x1, y1], fill=PANEL)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 14
    r = 44
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE,
                 outline=NAVY, width=3)
    for rx in (18, 38):
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=WHITE,
                     width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=WHITE, width=2)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=WHITE, width=2)
    # clock hands: talks running past the deadline
    import math
    hx = cx + int(30 * math.cos(math.radians(-50)))
    hy = cy + int(30 * math.sin(math.radians(-50)))
    draw.line([(cx, cy), (hx, hy)], fill=RED, width=4)
    draw.line([(cx, cy), (cx, cy - 34)], fill=RED, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    fnt = font(SANS_B, 24)
    label = "200 NATIONS"
    tw = text_w(draw, label, fnt)
    draw.text(((x0 + x1 - tw) / 2, y1 - 30), label, font=fnt, fill=NAVY)


def draw_deal_panel(draw, x0, y0, x1, y1):
    """Two flag blocks (UK / EU) over a signature line: three agreements.

    All geometry is relative to the panel box, so the contents always
    fit whatever row height the page flow gives this panel.
    """
    draw.rectangle([x0, y0, x1, y1], fill=PANEL)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # red count label at the top of the panel
    f2 = font(SANS_B, 22)
    label = "3 AGREEMENTS"
    tw = text_w(draw, label, f2)
    draw.text(((x0 + x1 - tw) / 2, y0 + 6), label, font=f2, fill=RED)
    bw, bh = 104, 52
    by = y0 + 34
    # UK block: navy with a white cross
    ux = x0 + 34
    draw.rectangle([ux, by, ux + bw, by + bh], fill=NAVY)
    draw.rectangle([ux + bw // 2 - 7, by, ux + bw // 2 + 7, by + bh],
                   fill=WHITE)
    draw.rectangle([ux, by + bh // 2 - 7, ux + bw, by + bh // 2 + 7],
                   fill=WHITE)
    # EU block: blue with a ring of stars
    ex = x0 + 170
    draw.rectangle([ex, by, ex + bw, by + bh], fill=BLUE)
    import math
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = ex + bw // 2 + int(24 * math.cos(a))
        sy = by + bh // 2 + int(18 * math.sin(a))
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 215, 0))
    fnt = font(SANS_B, 22)
    draw.text((ux + 34, by + bh + 4), "UK", font=fnt, fill=INK)
    draw.text((ex + 34, by + bh + 4), "EU", font=fnt, fill=INK)
    # signature squiggle along the panel's bottom edge
    pts = [(x0 + 24, y1 - 12), (x0 + 70, y1 - 22), (x0 + 110, y1 - 12),
           (x0 + 160, y1 - 22), (x0 + 210, y1 - 12), (x0 + 260, y1 - 20)]
    draw.line(pts, fill=INK, width=3, joint="curve")


def divider(draw, y):
    rule(draw, M, W - M, y + 4, w=2)
    return y + 12


def story_row(draw, y, kicker_text, head_text, body_text, panel_fn,
              head_size=33, body_size=20, min_panel_h=130):
    """One story row: kicker + headline + body on the left, art panel
    on the right. The panel stretches to the text height. Returns the
    y just below the row."""
    top = kicker(draw, M, y, kicker_text)
    head_end = headline(draw, M, top, head_text, 590, head_size,
                        max_lines=2)
    body_end = body(draw, M, head_end + 4, body_text, 590, size=body_size)
    row_h = max(body_end - y, min_panel_h)
    panel_fn(draw, 668, y, W - M, y + row_h)
    return y + row_h


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top red rule
    d.rectangle([0, 0, W, 10], fill=RED)

    # masthead
    mast = fit_font(d, "WORLD NEWS IN ONE IMAGE", SERIF_B, 62, W - 2 * M)
    tw = text_w(d, "WORLD NEWS IN ONE IMAGE", mast)
    d.text(((W - tw) / 2, 22), "WORLD NEWS IN ONE IMAGE", font=mast, fill=INK)

    # date bar (the day this page sums up -- judge criterion 1)
    d.rectangle([M, 104, W - M, 148], fill=INK)
    date_fnt = font(SANS_B, 32)
    date = "SATURDAY 21 NOVEMBER 2026"
    tw = text_w(d, date, date_fnt)
    d.text(((W - tw) / 2, 110), date, font=date_fnt, fill=WHITE)
    rule(d, M, W - M, 158, w=3)

    # ---------------------------------------------------------- lead story
    y = 172
    y = kicker(d, M, y, "LEAD STORY  —  EUROPE")
    y = headline(d, M, y, "RUSSIA'S BARRAGE HITS UKRAINE — "
                 "MISSILES LAND IN POLAND", W - 2 * M, 46, max_lines=2)
    y += 4
    stat = fit_font(d, "400+ DRONES  •  110 MISSILES  •  AT LEAST 8 KILLED IN KYIV",
                    SANS_B, 27, W - 2 * M)
    d.text((M, y), "400+ DRONES  •  110 MISSILES  •  AT LEAST 8 KILLED IN KYIV",
           font=stat, fill=RED)
    y += 32
    lead_body_end = body(d, M, y, "400+ drones and 110 missiles strike "
                         "Ukraine; two missiles and a suspected drone come "
                         "down in Poland. NATO calls it a 'grave violation'; "
                         "PM Tusk calls it a deliberate provocation.",
                         540, size=22)
    panel_h = max(lead_body_end - y, 130)
    draw_sky_panel(d, 620, y, W - M, y + panel_h)
    y = max(lead_body_end, y + panel_h)
    y = divider(d, y)

    # ---------------------------------------------------------- story 2
    y = story_row(d, y, "MARKETS  —  WALL STREET",
                  "AI SELL-OFF PUSHES S&P 500 INTO CORRECTION",
                  "US stocks fall 3.7% as an AI and chip sell-off drags "
                  "Wall Street into correction territory.",
                  draw_chart_panel)
    y = divider(d, y)

    # ---------------------------------------------------------- story 3
    y = story_row(d, y, "CLIMATE  —  ANTALYA",
                  "COP31 TALKS RUN PAST DEADLINE",
                  "Climate summit in Antalya goes into overtime as nearly "
                  "200 nations fail to agree on fossil fuels.",
                  draw_globe_panel)
    y = divider(d, y)

    # ---------------------------------------------------------- story 4
    y = story_row(d, y, "BRITAIN & EUROPE",
                  "UK AND EU SIGN BIGGEST POST-BREXIT DEAL",
                  "PM Burnham and EU leaders sign three agreements on food "
                  "exports, carbon markets and youth mobility.",
                  draw_deal_panel)
    y = divider(d, y)

    # footer: one more verified item, small (drawn only if it fits)
    if y + 24 <= H:
        foot = font(SANS, 18)
        also = ("ALSO: Trial pill makes pancreatic tumours undetectable "
                "in 1 in 12 patients")
        tw = text_w(d, also, foot)
        d.text(((W - tw) / 2, y), also, font=foot, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
