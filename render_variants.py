#!/usr/bin/env python3
"""Sketch B-rev4 VARIANTS for news-image-20261119 (Kevin's request,
11:50 WIB): two layouts to compare against rev4 (20 cards) — 15 cards
(3 rows x 5 cols) and 12 cards (3 rows x 4 cols).

WHY (parent's verification): in rev4 the card image is only 28px tall
(strip 10px + image 28px + title + 2-line summary in an 82px card) —
the picture is barely visible. Fewer cards = taller cards = the picture
actually shows. That is what the three-way comparison is about.

WHAT CHANGES vs rev4 (and ONLY this):
  * Cards: the FIRST 15 (variant A) / FIRST 12 (variant B) cards of
    rev4's card order, in the same order. Card height 82 -> 112px
    (image 28 -> 58px, more than double), 3 rows instead of 4.
  * The remaining rev4 cards become briefs, in the same order, prefixed
    with their strip city (rev4 convention: trim the city name out of
    the title when it repeats, e.g. "Coalition of the Willing meets in
    Berlin" -> "Berlin: Coalition of the Willing meets"). Two brief
    prefixes are non-city labels, exactly as in rev4: "MAIB" (report
    author, card 23) — noted in NOTE.md.
  * Brief columns: A = 29 briefs 10/10/9; B = 32 briefs 11/11/10.
    Brief type is smaller to fit the denser columns (A: 9pt/10px lines;
    B: 8pt/9px lines) — the only typography change, forced by the
    column density; brief TEXTS are identical to rev4 (same wording).
  * Grid heading count: "15 STORIES" / "12 STORIES".

WHAT DOES NOT CHANGE: global numbering 1-47 is INVARIANT — every story
keeps its rev4 global number (heroes 1-3, cards 4-18 / 4-15, briefs
19-47 / 16-47), so map pins, the "CITY - N" list, the region bar, the
big-numbers bar, DATE CHECK, masthead and footer are byte-identical in
spirit to rev4. Heroes, map, DATE CHECK, masthead, region bar and big
numbers are rendered by the SAME code as rev4, untouched.
Jeffries stays flagged "(18 Nov?)"; 3 tankers + NIA + Bangladesh flagged.
Layout: 1024x1024, deterministic, no network, no clock, no randomness.

FIXES 11:55 WIB (Kevin, after seeing rev4 — apply to BOTH variants):
  1. "19" BASELINE: in rev4 the red 60pt "19" shared its TOP edge with
     the 52pt neighbours, so its baseline sat ~6px lower and it looked
     like it was floating. Now all three segments are drawn with
     anchor "ls" (baseline) at the same y — baselines aligned, the "19"
     extends higher instead. Verified by masthead zoom crop.
  2. BIGGER PICTURES (priority #1): hero image 58 -> 70px (heroes
     start 6px higher, hero cards 144 -> 150px tall); card image
     58 -> 60px (visible picture 48 -> 50px). Rev4's card image was
     28px (18px visible); the variants now show 50px of picture per
     card (2.8x). The canvas budget caps it here without cutting
     required content (2-line summaries, strips, briefs, map, DATE
     CHECK) — recorded in NOTE.md.
  3. OWN WORDS (not rank 1's): the deck under the date is rewritten
     in our own phrasing (see the deck comment in main()); the 6 big
     numbers are KEPT — they are our stories' verified numbers, and
     only $81.3bn coincides with rank 1's bar (same fact of the day);
     the other five differ from rank 1's (whose 15.9m / 200,000 /
     730,000 / $120bn / 13 yrs are NOT verified from our sources and
     are deliberately NOT used). Region bar still counted from our 47.

ROUND 12:08-12:12 WIB (Kevin + parent) — map + briefs + flexible total
(same round as rev4; see render_rev4.py docstring for the full list):
  1. MAP: the long "CITY - N" list is DELETED; rank-1 pattern instead
     (numbered pins = cards, dots = briefs, short region-count legend
     below the map, key "NUMBERED PINS = CARDS · DOTS = BRIEFS · ★ =
     SUMMIT"); map 122 -> 156px; colliding pins offset with leader
     lines, colliding dots skipped (logged, NOTE.md).
  2. BRIEFS: city BOLD; red number dot replaced by a vertical
     region-colour strip at the left edge; 2 sentences where 2 verified
     facts exist (1 sentence for thin briefs); 8pt throughout.
  3. FLEXIBLE TOTAL: no longer forced to 47. Borderline deleted in both
     variants (35, 38, 43, 47); weakest thin briefs deleted too — A
     also deletes 27, 33, 36, 37 (total 39); B also deletes 27, 33, 36,
     37, 34, 42, 29 (total 36; B keeps 28 + 32 so the New Delhi map pin
     survives). Masthead count, region bar, highest number, DATE CHECK
     and map legend are recomputed per variant from the final lists.
  4. GRID HEADING DELETED ("THE DAY, IN PICTURES — N STORIES"); the
     freed ~20px go to the 3 HERO images (correction 12:12 — NOT to the
     card images): hero image 70 -> 88px, hero card 150 -> 170px.
"""
import hashlib
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

PAPER = (246, 241, 231)
INK = (24, 28, 36)
NAVY = (15, 36, 64)
RED = (178, 44, 36)
GOLD = (217, 164, 65)
MUTED = (92, 96, 104)
WHITE = (255, 255, 255)
LIGHT = (226, 231, 238)
SEA = (198, 220, 236)
LAND = (210, 188, 140)
LAND_LINE = (168, 148, 108)
DARK = (20, 24, 32)
CARD_BG = (250, 247, 240)
CARD_LINE = (205, 200, 185)

# Region system (rank-3 edisi 17 legend): one colour per region, used by
# the card/hero strips AND the map pins AND the map city-count dots.
REGION_COLORS = {
    "AMERICAS": (178, 44, 36),
    "EUROPE": (40, 90, 160),
    "MIDEAST": (200, 120, 40),
    "ASIA": (130, 80, 160),
    "AFRICA": (40, 130, 70),
    "OCEANIA": (30, 140, 140),
    "WORLD": (110, 110, 110),
}
# Rule: region = the story's place, EXCEPT 28/29 WORLD (global tech:
# senators' AI-cyber warning, Microsoft x ByteDance) and 31 EUROPE
# (newsmaker Putin/Russia) — the classification that reproduces the bar
# Kevin already saw for the full 47 (EUROPE 13, AMERICAS 4, ASIA-PACIFIC
# 13, MIDEAST 6, AFRICA 0, OCEANIA 2, WORLD 9); the per-story table is in
# NOTE.md "Total cerita fleksibel". The map legend and the bar above the
# heroes are drawn from the SAME computed list, so they always agree.
REGION_ORDER = [("EUROPE", "EUROPE"), ("THE AMERICAS", "AMERICAS"),
                ("ASIA-PACIFIC", "ASIA"), ("MIDEAST", "MIDEAST"),
                ("AFRICA", "AFRICA"), ("OCEANIA", "OCEANIA"),
                ("WORLD", "WORLD")]
# 6 key numbers for the big-numbers bar — all verified (STORIES.md /
# NOTE.md). Numbers from rank-1 edisi 19's bar that are NOT verified for
# our stories are deliberately NOT used (see docstring point 5).
BIG_NUMBERS = [
    ("$81.3bn", "Anthropic IPO — largest ever"),
    ("$190.4m", "Van Gogh sells — artist record"),
    ("$1.6bn", "US aid package for Ukraine"),
    ("53", "soldiers killed in Yemen strike"),
    ("4.9%", "Australia jobless — highest since 2021"),
    ("$63,000", "Bitcoin slips below, down 2.7%"),
]
# Region per big number (from the same story's strip region in CARDS /
# HEROES — Kevin 13:11 WIB: soft coloured box per number, tint of its
# region colour, number stays bold NAVY): $81.3bn IPO = hero 3 AMERICAS;
# $190.4m Van Gogh = card 15 WORLD; $1.6bn Ukraine aid = card 5 AMERICAS;
# 53 Yemen = card 14 MIDEAST; 4.9% Australia jobless = OCEANIA;
# $63,000 Bitcoin = WORLD.
BIG_NUMBER_REGIONS = ["AMERICAS", "WORLD", "AMERICAS",
                      "MIDEAST", "OCEANIA", "WORLD"]
# Map places, keyed by the city label in a card strip or a brief.
# Country labels resolve to their capital (Spain = Madrid, Estonia =
# Tallinn, UK = London, US = Washington, China = Beijing, Australia =
# Canberra). "Global" stories have no place and get no marker. Rank-1
# pattern: NUMBERED pins = card stories, small dots = brief stories.
# The map is only 300px wide, so Europe is crowded: pins whose true
# positions collide are drawn at a hand-tuned offset with a thin leader
# line (PIN_OFFSETS); dots that would collide are SKIPPED (logged by the
# render, listed in NOTE.md) instead of drawn on top of each other.
# (The old "CITY - N" list that filled the map box was DELETED 12:08
# WIB — it cancelled Kevin's 11:28 request for that list; see NOTE.md.)
PLACES = {
    "Gaza": (34.4, 31.4), "Washington": (-77.0, 38.9),
    "Kyiv": (30.5, 50.4), "Estonia": (24.7, 59.4),
    "Prague": (14.4, 50.1), "Spain": (-3.7, 40.4),
    "Kerch": (36.5, 45.3), "The Hague": (4.3, 52.1),
    "Puri": (85.8, 19.8), "Taiwan": (121.0, 25.0),
    "Yemen": (44.2, 15.3), "Saudi Arabia": (46.7, 24.6),
    "Finland": (24.9, 60.2), "Wellington": (174.8, -41.3),
    "Berlin": (13.4, 52.5), "Saada": (43.8, 16.9),
    "Tokyo": (139.7, 35.7), "Hormuz": (56.3, 26.6),
    "Shenzhen": (114.1, 22.5), "New Delhi": (77.2, 28.6),
    "London": (-0.1, 51.5), "UK": (-0.1, 51.5),
    "US": (-77.0, 38.9), "China": (116.4, 39.9),
    "Australia": (149.1, -35.3), "Kuala Lumpur": (101.7, 3.1),
    "Beijing": (116.4, 39.9), "Brussels": (4.4, 50.8),
}
# Hand-tuned offsets (dx, dy in px) for pins whose true positions
# collide on this 300px map. A leader line joins the pin to its place.
PIN_OFFSETS = {
    "Finland": (0, -12), "Prague": (0, 14), "The Hague": (-14, 0),
    "Kerch": (12, 0), "Saada": (0, 14), "Hormuz": (0, -12),
    "Taiwan": (12, 0),
}
# Pins keep their city label only where the label cannot collide with
# another marker (isolated places). Rank 1 labels NO pins; we label the
# four that were labelled before and are isolated. New Delhi's label
# was DROPPED (its pin 32 stays) — the label crowded pins 32/12.
PIN_LABELS = {"Gaza": "l", "Wellington": "l", "Tokyo": "a",
              "Shenzhen": "b"}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover_crop(img, tw, th):
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def vgrad(d, x, y, w, h, c1, c2):
    for i in range(h):
        t = i / max(h - 1, 1)
        col = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w - 1, y + i)], fill=col)


# ---------------------------------------------------------------- scenes
# Each motif draws a small ILLUSTRATION (a scene with sky, ground and a
# recognisable subject) inside box (x, y, w, h). No pictogram icons.

def m_capitol(d, x, y, w, h):
    vgrad(d, x, y, w, h, (36, 58, 100), (130, 150, 185))
    d.polygon([(x, y + h), (x, y + h - 12), (x + w, y + h - 12),
               (x + w, y + h)], fill=(52, 66, 52))
    cx = x + w // 2
    d.rectangle([cx - 34, y + h - 26, cx + 34, y + h - 12], fill=(228, 226, 218))
    d.pieslice([cx - 20, y + h - 44, cx + 20, y + h - 18], 180, 360,
               fill=(228, 226, 218))
    d.rectangle([cx - 2, y + h - 50, cx + 2, y + h - 42], fill=(228, 226, 218))
    d.rectangle([cx + 2, y + h - 50, cx + 12, y + h - 46], fill=(178, 44, 36))
    for dx in (-26, -13, 0, 13, 26):
        d.rectangle([cx + dx - 2, y + h - 24, cx + dx + 2, y + h - 13],
                    fill=(180, 180, 172))


def m_kyiv(d, x, y, w, h):
    vgrad(d, x, y, w, h, (205, 125, 80), (95, 65, 115))
    d.ellipse([x + w - 34, y + 4, x + w - 18, y + 20], fill=(245, 210, 130))
    for bx, bw, bh in ((0, 46, 30), (48, 60, 22), (112, 44, 34), (158, 35, 26)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(38, 34, 52))
    for dx, dy, r in ((28, 8, 7), (78, 14, 6), (134, 6, 7)):
        d.rectangle([x + dx - 1, y + h - 30 - dy, x + dx + 1, y + h - 30],
                    fill=(38, 34, 52))
        d.ellipse([x + dx - r, y + h - 38 - dy, x + dx + r, y + h - 26 - dy],
                  fill=(217, 164, 65))
    for wx in range(8, w - 6, 14):
        d.rectangle([x + wx, y + h - 12, x + wx + 3, y + h - 8],
                    fill=(245, 210, 130))


def m_forest(d, x, y, w, h):
    vgrad(d, x, y, w, h, (205, 215, 205), (155, 175, 155))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 120, 118))
    for tx in (6, 34, 62, 90, 118, 146, 170):
        th = 26 + (tx % 3) * 4
        d.polygon([(x + tx, y + h - 12), (x + tx + 9, y + h - 12 - th),
                   (x + tx + 18, y + h - 12)], fill=(34, 80, 48))
    d.rectangle([x + 20, y + h - 26, x + w - 20, y + h - 18], fill=(240, 240, 235))
    for sx in range(24, w - 24, 16):
        d.line([(x + sx, y + h - 26), (x + sx + 8, y + h - 18)],
               fill=(178, 44, 36), width=3)


def m_prague(d, x, y, w, h):
    vgrad(d, x, y, w, h, (225, 175, 125), (125, 95, 135))
    d.polygon([(x, y + h - 14), (x + w // 2, y + h - 34),
               (x + w, y + h - 14), (x + w, y + h), (x, y + h)],
              fill=(52, 46, 60))
    for tx, tw, th in ((30, 16, 26), (70, 20, 34), (120, 16, 28), (155, 14, 22)):
        d.rectangle([x + tx, y + h - 14 - th, x + tx + tw, y + h - 14],
                    fill=(52, 46, 60))
        d.polygon([(x + tx - 2, y + h - 14 - th), (x + tx + tw // 2, y + h - 26 - th),
                   (x + tx + tw + 2, y + h - 14 - th)], fill=(52, 46, 60))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(70, 110, 150))
    d.line([(x + 10, y + h - 8), (x + w - 30, y + h - 8)], fill=(200, 220, 235),
           width=1)
    d.line([(x + 40, y + h - 4), (x + w - 10, y + h - 4)], fill=(200, 220, 235),
           width=1)


def m_port(d, x, y, w, h):
    vgrad(d, x, y, w, h, (185, 205, 225), (145, 165, 195))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(70, 110, 150))
    for cx in (18, 96):
        d.rectangle([x + cx, y + 6, x + cx + 6, y + h - 14], fill=(50, 55, 70))
        d.rectangle([x + cx, y + 6, x + cx + 52, y + 12], fill=(50, 55, 70))
        d.line([(x + cx + 44, y + 12), (x + cx + 44, y + 26)],
               fill=(50, 55, 70), width=2)
        d.rectangle([x + cx + 38, y + 26, x + cx + 50, y + 32], fill=(178, 44, 36))
    for bx, bc in ((60, (200, 90, 60)), (78, (60, 120, 90)), (140, (200, 160, 60))):
        d.rectangle([x + bx, y + h - 26, x + bx + 22, y + h - 14], fill=bc)


def m_bridge(d, x, y, w, h):
    vgrad(d, x, y, w, h, (205, 215, 230), (165, 185, 210))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 110, 150))
    d.rectangle([x, y + h - 26, x + w, y + h - 20], fill=(70, 75, 85))
    for ax in (20, 90):
        d.arc([x + ax, y + h - 44, x + ax + 46, y + h - 8], 180, 360,
              fill=(70, 75, 85), width=3)
    d.rectangle([x + 150, y + 8, x + 154, max(y + h - 26, y + 9)],
                fill=(70, 75, 85))
    for i, r in enumerate((5, 7, 9)):
        d.ellipse([x + 148 - r, y + 6 - i * 9, x + 148 + r, y + 6 - i * 9 + r * 2],
                  fill=(150, 150, 150))


def m_court(d, x, y, w, h):
    vgrad(d, x, y, w, h, (205, 210, 220), (175, 180, 195))
    cx = x + w // 2
    d.polygon([(cx - 62, y + 20), (cx + 62, y + 20), (cx, y + 6)],
              fill=(235, 230, 215))
    d.rectangle([x + 28, y + 20, x + w - 28, y + 26], fill=(235, 230, 215))
    for i in range(4):
        px = x + 40 + i * 38
        d.rectangle([px, y + 26, px + 10, max(y + h - 12, y + 27)],
                    fill=(235, 230, 215))
    d.rectangle([x + 28, y + h - 12, x + w - 28, y + h - 6], fill=(225, 220, 205))
    d.ellipse([cx - 7, y + 11, cx + 7, y + 19], fill=(190, 160, 90))


def m_cyclone(d, x, y, w, h):
    vgrad(d, x, y, w, h, (22, 62, 72), (42, 92, 102))
    cx, cy = x + w // 2, y + h // 2 - 4
    for r, col in ((34, (220, 235, 240)), (26, (190, 210, 220)),
                   (18, (220, 235, 240)), (10, (245, 245, 240))):
        d.arc([cx - r, cy - r, cx + r, cy + r], -60, 210, fill=col, width=3)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(40, 95, 130))
    for wx in range(6, w - 10, 26):
        d.arc([x + wx, y + h - 10, x + wx + 18, y + h - 2], 180, 360,
              fill=(220, 235, 240), width=2)


def m_island(d, x, y, w, h):
    vgrad(d, x, y, w, h, (195, 215, 235), (155, 185, 210))
    d.ellipse([x + w - 36, y + 4, x + w - 18, y + 22], fill=(245, 215, 130))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(60, 120, 165))
    d.polygon([(x + 30, y + h - 20), (x + 70, y + h - 38), (x + 130, y + h - 38),
               (x + 165, y + h - 20)], fill=(60, 130, 80))
    d.rectangle([x + 92, y + h - 52, x + 108, y + h - 38], fill=(235, 235, 225))
    d.polygon([(x + 88, y + h - 52), (x + 100, y + h - 60), (x + 112, y + h - 52)],
              fill=(178, 44, 36))
    d.line([(x + 8, y + h - 12), (x + w - 8, y + h - 12)], fill=(220, 235, 240),
           width=1)


def m_desert_smoke(d, x, y, w, h):
    vgrad(d, x, y, w, h, (238, 222, 192), (212, 182, 142))
    d.ellipse([x + 12, y + 5, x + 30, y + 23], fill=(245, 225, 170))
    d.polygon([(x, y + h - 16), (x + w // 2, y + h - 28), (x + w, y + h - 16),
               (x + w, y + h), (x, y + h)], fill=(198, 164, 118))
    d.polygon([(x, y + h - 8), (x + w // 2, y + h - 16), (x + w, y + h - 8),
               (x + w, y + h), (x, y + h)], fill=(182, 148, 104))
    sx = x + w - 42
    for i, r in enumerate((6, 8, 10, 12)):
        d.ellipse([sx - r, y + 30 - i * 8, sx + r, y + 30 - i * 8 + r],
                  fill=(120, 118, 112))


def m_vangogh(d, x, y, w, h):
    vgrad(d, x, y, w, h, (28, 48, 112), (52, 72, 142))
    d.ellipse([x + w - 38, y + 5, x + w - 16, y + 27], fill=(245, 210, 90))
    for cx, cy, r in ((30, 14, 26), (70, 26, 32), (120, 16, 28), (160, 28, 24)):
        d.arc([x + cx - r, y + cy - r, x + cx + r, y + cy + r], 200, 80,
              fill=(245, 210, 90), width=3)
    for sx, sy in ((14, 34), (52, 8), (96, 40), (140, 8), (176, 36)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(245, 235, 180))
    d.polygon([(x + 8, y + h), (x + 16, y + h - 26), (x + 24, y + h)],
              fill=(18, 28, 60))
    d.ellipse([x + w - 52, y + h - 16, x + w - 30, y + h + 6], fill=(245, 190, 60))
    for px in range(-50, -30, 4):
        d.line([(x + w + px, y + h - 6), (x + w + px + 8, y + h - 6)],
               fill=(220, 160, 40), width=2)


def m_saudi_dawn(d, x, y, w, h):
    vgrad(d, x, y, w, h, (242, 202, 152), (202, 152, 112))
    d.ellipse([x + w // 2 - 12, y + 6, x + w // 2 + 12, y + 30],
              fill=(245, 220, 160))
    for bx, bw, bh in ((0, 30, 22), (34, 22, 32), (60, 34, 18), (98, 26, 28),
                       (128, 30, 20), (162, 31, 26)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(74, 58, 52))


def m_finland(d, x, y, w, h):
    vgrad(d, x, y, w, h, (192, 207, 222), (162, 182, 202))
    for tx in (4, 28, 52, 76, 100, 124, 148, 170):
        th = 22 + (tx % 3) * 5
        d.polygon([(x + tx, y + h - 16), (x + tx + 8, y + h - 16 - th),
                   (x + tx + 16, y + h - 16)], fill=(28, 74, 52))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 125, 165))
    d.line([(x + 12, y + h - 9), (x + w - 12, y + h - 9)], fill=(220, 235, 245),
           width=2)


def m_cricket(d, x, y, w, h):
    vgrad(d, x, y, w, h, (202, 222, 236), (172, 202, 222))
    d.ellipse([x + 6, y + h - 26, x + w - 6, y + h + 8], fill=(52, 130, 70))
    d.rectangle([x + w // 2 - 9, y + h - 30, x + w // 2 + 9, y + h - 4],
                fill=(205, 180, 130))
    for dx in (-4, 0, 4):
        d.rectangle([x + w // 2 + dx - 1, y + h - 34, x + w // 2 + dx + 1,
                     y + h - 24], fill=(245, 245, 240))
    d.ellipse([x + w - 26, y + h - 22, x + w - 20, y + h - 16],
              fill=(178, 44, 36))


def m_berlin(d, x, y, w, h):
    vgrad(d, x, y, w, h, (188, 198, 212), (152, 162, 188))
    tx = x + 26
    d.rectangle([tx - 2, y + 14, tx + 2, y + h - 8], fill=(60, 62, 70))
    d.ellipse([tx - 7, y + 6, tx + 7, y + 20], fill=(60, 62, 70))
    d.line([(tx, y + 2), (tx, y + 6)], fill=(60, 62, 70), width=2)
    gx = x + 78
    for i in range(6):
        px = gx + i * 16
        d.rectangle([px, y + h - 30, px + 6, y + h - 8], fill=(60, 62, 70))
    d.rectangle([gx - 6, y + h - 38, gx + 92, y + h - 30], fill=(60, 62, 70))
    d.rectangle([gx + 34, y + h - 46, gx + 52, y + h - 38], fill=(60, 62, 70))


def m_intercept(d, x, y, w, h):
    vgrad(d, x, y, w, h, (16, 22, 48), (42, 52, 92))
    for sx, sy in ((20, 10), (60, 22), (110, 8), (150, 18), (180, 30)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(220, 225, 240))
    d.line([(x + 20, y + h - 12), (x + w - 30, y + 10)], fill=(245, 210, 90),
           width=3)
    d.ellipse([x + w - 38, y + 4, x + w - 26, y + 16], fill=(255, 240, 180))
    d.polygon([(x, y + h - 12), (x + w // 2, y + h - 22), (x + w, y + h - 12),
               (x + w, y + h), (x, y + h)], fill=(120, 100, 74))


def m_tokyo_pagoda(d, x, y, w, h):
    vgrad(d, x, y, w, h, (222, 152, 112), (142, 92, 112))
    tx = x + 34
    d.polygon([(tx - 16, y + h - 8), (tx, y + 8), (tx + 16, y + h - 8)],
              fill=(178, 60, 44))
    d.line([(tx - 10, y + h - 26), (tx + 10, y + h - 26)], fill=(120, 40, 30),
           width=2)
    d.line([(tx - 7, y + h - 38), (tx + 7, y + h - 38)], fill=(120, 40, 30),
           width=2)
    px = x + 118
    for i, rw in enumerate((46, 38, 30)):
        ry = y + h - 12 - i * 13
        d.polygon([(px - rw // 2, ry), (px + rw // 2, ry), (px + rw // 2 - 6, ry - 6),
                   (px - rw // 2 + 6, ry - 6)], fill=(52, 44, 52))
        d.rectangle([px - 4, ry - 10, px + 4, ry - 6], fill=(52, 44, 52))


def m_tanker(d, x, y, w, h):
    vgrad(d, x, y, w, h, (192, 207, 222), (152, 177, 202))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(60, 110, 150))
    d.polygon([(x + 12, y + h - 26), (x + w - 30, y + h - 26),
               (x + w - 12, y + h - 18), (x + 12, y + h - 18)],
              fill=(52, 52, 58))
    d.rectangle([x + w - 52, y + h - 40, x + w - 34, y + h - 26],
                fill=(235, 235, 228))
    for i, r in enumerate((4, 6)):
        d.ellipse([x + w - 46 - r, y + h - 52 - i * 8,
                   x + w - 46 + r, y + h - 52 - i * 8 + r],
                  fill=(150, 150, 150))
    d.line([(x + 8, y + h - 8), (x + w - 8, y + h - 8)], fill=(200, 220, 235),
           width=1)


def m_yacht(d, x, y, w, h):
    vgrad(d, x, y, w, h, (190, 210, 230), (150, 180, 205))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(50, 100, 140))
    d.polygon([(x + 40, y + h - 26), (x + 150, y + h - 26),
               (x + 140, y + h - 14), (x + 50, y + h - 14)],
              fill=(235, 235, 228))
    d.rectangle([x + 92, y + 6, x + 95, max(y + h - 26, y + 7)],
                fill=(60, 60, 66))
    d.polygon([(x + 97, y + 8), (x + 97, y + h - 28), (x + 140, y + h - 28)],
              fill=(250, 250, 245))
    d.polygon([(x + 90, y + 10), (x + 90, y + h - 28), (x + 55, y + h - 28)],
              fill=(225, 225, 215))
    for wx in range(6, w - 10, 26):
        d.arc([x + wx, y + h - 10, x + wx + 18, y + h - 2], 180, 360,
              fill=(220, 235, 240), width=2)


def motif_image(kind, w, h):
    """Draw a motif onto its own image of exactly (w, h) and return it.

    Pillow clips drawing to the image bounds, so a motif can NEVER bleed
    past its box into a title — the rev bug (m_vangogh / m_cricket drew
    below y+h) is impossible by construction.
    """
    im = Image.new("RGB", (w, h), CARD_BG)
    dd = ImageDraw.Draw(im)
    MOTIFS[kind](dd, 0, 0, w, h)
    return im


def wrap_max(draw, text, fnt, max_w, max_lines):
    """wrap() capped at max_lines; the last line gets an ellipsis if cut."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=fnt) > max_w:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = last + "…" if last else "…"
    return lines



def draw_strip(d, x, y, w, h, text, bg, size):
    """A coloured band on the TOP edge of an image: "N · CITY · TOPIC".

    Rank-1 edisi 19 pattern. The band is drawn ON the canvas after the
    image is pasted, so it sits on top of the image and can never bleed
    into text below it. Text auto-fits: the font shrinks until it fits.
    """
    d.rectangle([x, y, x + w, y + h], fill=bg)
    fnt = None
    for s in (size, size - 1, size - 2):
        f_try = font(BOLD, s)
        if d.textlength(text, font=f_try) <= w - 8:
            fnt = f_try
            break
    if fnt is None:
        fnt = font(BOLD, max(size - 2, 6))
    d.text((x + 4, y + h // 2), text, font=fnt, fill=WHITE, anchor="lm")
def fit_one_line(draw, text, fnt, max_w):
    """Truncate to a single line with an ellipsis if it does not fit."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    out = ""
    for wd in text.split():
        trial = (out + " " + wd).strip()
        if draw.textlength(trial + "…", font=fnt) <= max_w:
            out = trial
        else:
            break
    return out + "…" if out else "…"


MOTIFS = {
    "capitol": m_capitol, "kyiv": m_kyiv, "forest": m_forest,
    "prague": m_prague, "port": m_port, "bridge": m_bridge,
    "court": m_court, "cyclone": m_cyclone, "island": m_island,
    "desert_smoke": m_desert_smoke, "vangogh": m_vangogh,
    "saudi_dawn": m_saudi_dawn, "finland": m_finland, "cricket": m_cricket,
    "berlin": m_berlin, "intercept": m_intercept,
    "tokyo_pagoda": m_tokyo_pagoda, "tanker": m_tanker, "yacht": m_yacht,
}

AI_ASSETS = {
    "ipo": "media-generation-hero-ipo-0-8cbb9db1-f691-408f-ab20-746c58a7d930.png",
    "gaza": "media-generation-hero-gaza-0-d883abe3-a658-4e15-8940-7187b06791d4.png",
    # Ilustrasi AI per kartu 2x5 (keputusan Kevin 21:54 WIB — ganti motif
    # Pillow; brief di illustration-brief-2x5.md). Nama file = output
    # media.generate_image (name card-<kartu>).
    "card_gaza": "media-generation-card-gaza-0-f096b08f-9edf-4908-b025-7a2ac5ab476f.png",
    "card_ukraine": "media-generation-card-ukraine-0-1bb1ae8f-f27e-4ca3-81ce-65f60fefa8a5.png",
    "card_icj": "media-generation-card-icj-0-011a1eeb-2b66-41b8-a944-1d5ddf9a0fda.png",
    "card_cyclone": "media-generation-card-cyclone-0-d9f8d73c-ef93-4c67-b3e4-31660ea6557b.png",
    "card_sarb": "media-generation-card-sarb-0-1ae3bf5f-15dd-42cd-9cf8-09688ab8d5fa.png",
    "card_berlin": "media-generation-card-berlin-0-bf1abbaa-3f07-4a81-bf3c-09cc2250243e.png",
    "card_uganda": "media-generation-card-uganda-0-0d4c990a-2283-406e-b539-5e1a6a8324fc.png",
    "card_cop31": "media-generation-card-cop31-0-b3cba7ef-38d6-43dc-b5ed-902701778d89.png",
    "card_prague": "media-generation-card-prague-0-85b675a9-6723-4533-ac21-802291588bd5.png",
    "card_kyiv": "media-generation-card-kyiv-0-bd53f931-1191-476d-9dd6-cafd2dc91fdd.png",
}

# "strip" = the band on the TOP edge of the hero image, rank-1 edisi 19
# pattern: "NUMBER · CITY · TOPIC". Strip colour = the story's region.
# 1 Shenzhen: APEC summit (STORIES.md). 2 New York: Rockstar Games, the
# GTA VI maker, is headquartered in New York City (Wikipedia, verified
# 19 Nov 11:35 WIB) — same choice as rank 1 edisi 19 ("2 · NEW YORK ·
# GAMES"). 3 Nasdaq: Anthropic shares trade on the Nasdaq Global Select
# Market as ANT at $83 (SEC filing / Reuters, verified 19 Nov 11:35 WIB).
# The old red "19 NOV" chip is GONE — the strip is the one system now.
HEROES = [
    {
        "file": "media-generation-hero-summit-0-2facf046-c366-4c54-811a-378f151baf31.png",
        "headline": "Trump, Xi and Putin meet in Shenzhen",
        "deck": "Trade truce and nuclear arms top the agenda as the three leaders meet in Shenzhen",
        "strip": "1 · SHENZHEN · SUMMIT",
        "region": "ASIA",
    },
    {
        "file": "media-generation-hero-gtavi-0-2ba192a8-4751-42fd-bb85-541410d0920c.png",
        "headline": "GTA VI launches worldwide",
        "deck": "Gamers enter Vice City as the launch begins on PlayStation 5 and Xbox",
        "strip": "2 · NEW YORK · GAMES",
        "region": "AMERICAS",
    },
    {
        "file": "media-generation-hero-ipo-0-8cbb9db1-f691-408f-ab20-746c58a7d930.png",
        "headline": "Anthropic's $81.3bn IPO — a record",
        "deck": "Priced at $83 a share, the biggest IPO ever; markets rise ahead of the debut",
        "strip": "3 · NASDAQ · MARKETS",
        "region": "AMERICAS",
    },
]

# 20 cards, row-major (5 cols x 4 rows): (title, kind, summary line 1,
# summary line 2, strip, region). Numbers are the GLOBAL story numbers
# (heroes 1-3, cards 4-23, briefs 24-47). Summaries are verified facts
# only (STORIES.md / NOTE.md). "asset" = reuse a v1.1 AI asset; anything
# else = Pillow mini-illustration. Strip = "N · CITY · TOPIC" on the
# image top; strip colour = the story's region. Two strips use a
# non-city label because no city is verified for the story: 15 AUCTION
# (the sale's city is not in our sources) and 23 MAIB (the report's
# author, UK Marine Accident Investigation Branch).
CARDS = [
    ("Israeli push past Gaza ceasefire line", "asset:gaza",
     "Rare ground op beyond Yellow Line",
     "Israeli troops cross the ceasefire line",
     "4 · GAZA · CEASEFIRE LINE", "MIDEAST"),
    ("US approves $1.6bn Ukraine aid package", "capitol",
     "Package approved on Thursday",
     "$1.6bn for Ukraine's defence",
     "5 · WASHINGTON · UKRAINE AID", "AMERICAS"),
    ("Zelensky: US blocking missile deliveries", "kyiv",
     "Kyiv accuses Washington",
     "Missile deliveries held back",
     "6 · KYIV · MISSILE DELIVERIES", "EUROPE"),
    ("Estonia to shut Russia border", "forest",
     "Crossings close from December",
     "Border with Russia to shut",
     "7 · ESTONIA · RUSSIA BORDER", "EUROPE"),
    ("Prague mass protest for media independence", "prague",
     "Crowds demand a free press",
     "Hundreds of thousands protest",
     "8 · PRAGUE · MEDIA PROTEST", "EUROPE"),
    ("Spain hit by nationwide general strike", "port",
     "Ports and factories disrupted",
     "General strike hits the country",
     "9 · SPAIN · GENERAL STRIKE", "EUROPE"),
    ("Crimean Bridge attacked again", "bridge",
     "Traffic suspended, says official",
     "Russian official confirms the attack",
     "10 · KERCH · BRIDGE ATTACK", "EUROPE"),
    ("ICJ rules on Myanmar genocide case", "court",
     "Verdict due today in The Hague",
     "Rohingya case at the UN court",
     "11 · THE HAGUE · GENOCIDE CASE", "EUROPE"),
    ("Cyclone Akvan nears India's coast", "cyclone",
     "Red alerts out; schools shut",
     "Machilipatnam to Puri in its path",
     "12 · PURI · CYCLONE AKVAN", "ASIA"),
    ("Taiwan drafts transnational repression law", "island",
     "Draft bill targets coercion abroad",
     "Transnational repression crime",
     "13 · TAIWAN · REPRESSION LAW", "ASIA"),
    ("Houthi rocket kills 53 soldiers in Yemen", "desert_smoke",
     "Strike reported on Thursday",
     "53 soldiers killed in Yemen",
     "14 · YEMEN · ROCKET STRIKE", "MIDEAST"),
    ("Van Gogh sells for record $190.4m", "vangogh",
     "Auction record for the artist",
     "Painting sells for $190.4m",
     "15 · AUCTION · VAN GOGH RECORD", "WORLD"),
    ("Saudi: danger has passed in south", "saudi_dawn",
     "Danger passed, civil defence says",
     "Alerts lifted in three southern cities",
     "16 · SAUDI ARABIA · ALL CLEAR", "MIDEAST"),
    ("Finland approves first nuclear waste store", "finland",
     "World-first permanent repository",
     "Nuclear waste store approved",
     "17 · FINLAND · WASTE STORE", "EUROPE"),
    ("India v NZ: 1st Test begins", "cricket",
     "Bumrah strikes twice at lunch",
     "1st Test at Basin Reserve, Wellington",
     "18 · WELLINGTON · 1ST TEST", "OCEANIA"),
    ("Coalition of the Willing meets in Berlin", "berlin",
     "Witkoff and Kushner attend",
     "Coalition meets in the capital",
     "19 · BERLIN · COALITION TALKS", "EUROPE"),
    ("Saudi coalition intercepts Houthi missile", "intercept",
     "Launcher destroyed in Saada",
     "Houthi missile intercepted",
     "20 · SAADA · MISSILE INTERCEPT", "MIDEAST"),
    ("India, Japan hold 2+2 defence talks", "tokyo_pagoda",
     "Ministers meet in Tokyo",
     "Defence talks in the capital",
     "21 · TOKYO · DEFENCE TALKS", "ASIA"),
    ("Tanker hit by projectile in Strait of Hormuz", "tanker",
     "Oil steadies after the strike",
     "ADNOC tanker struck overnight",
     "22 · HORMUZ · TANKER STRUCK", "MIDEAST"),
    ("Bayesian had hidden wind weakness", "yacht",
     "Crew unaware of risk, report finds",
     "80 mph winds capsized her in seconds",
     "23 · MAIB · WIND WEAKNESS", "WORLD"),
]

# Final briefs (20): rev4's briefs 24-47 MINUS the 4 borderline stories
# deleted 12:10 WIB — 35 Hormuz tankers, 38 NIA, 43 Jeffries, 47
# Bangladesh (see NOTE.md "Total cerita fleksibel"). Total 43 stories.
# Each brief: (city, region, text). Region = the story's place, EXCEPT
# 28/29 WORLD (global tech) and 31 EUROPE (newsmaker Putin) — the
# classification that reproduces the bar Kevin already saw (NOTE.md).
# Text: 2 sentences where 2 verified facts exist; 1 sentence where only
# 1 fact is in the files (thin — kept here, rev4's columns fit them).
# The city is NOT repeated inside the text (rev4 convention).
# Old rev4 numbers of the 20 briefs below (the 4 borderline are already
# gone from this list, so the numbers are NOT 24 + index).
OLD_NUMS = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 39, 40,
            41, 42, 44, 45, 46]
BRIEFS = [
    ("Shenzhen", "ASIA", "Trump mentions ex-Nvidia boss Huang 'briefly' in Xi talks. The talks are at the APEC summit."),
    ("Australia", "OCEANIA", "The jobless rate jumps to 4.9%. It is the highest since 2021."),
    ("London", "EUROPE", "The UK leasehold Bill enters Parliament. Rents are capped at £250."),
    ("UK", "EUROPE", "450 McDonald's discrimination claims can proceed."),
    ("Washington", "WORLD", "US senators warn AI cyber threats are outpacing defences."),
    ("US", "WORLD", "Microsoft is in talks to sell AI services to ByteDance."),
    ("Global", "WORLD", "Gold sinks below $3,700. It is the lowest since Sept 2025."),
    ("Shenzhen", "EUROPE", "Japan PM Takaichi holds talks with Putin. Both leaders are at the APEC summit."),
    ("New Delhi", "ASIA", "Congress targets the Modi government over inflation."),
    ("China", "ASIA", "Trump plays down US tech outages."),
    ("Kuala Lumpur", "ASIA", "UNHCR halts refugee registration in Malaysia."),
    ("London", "EUROPE", "Google rejects a UK bid to remove a Brand video."),
    ("Beijing", "ASIA", "China moves to ease curbs on Korean content."),
    ("Global", "WORLD", "Bitcoin slips below $63,000. It is down 2.7%."),
    ("Tokyo", "ASIA", "Japan machinery orders dip 0.3%. The figures are for September."),
    ("Global", "WORLD", "Silver slides 5%. It is near $45 an ounce."),
    ("Brussels", "EUROPE", "The EU delays methane rules by two years."),
    ("Global", "WORLD", "The dollar hovers near a 19-month high. It follows Fed signals."),
    ("Tokyo", "ASIA", "Stocks rise. The Anthropic IPO lifts the AI mood."),
    ("Global", "WORLD", "Oil heads for a third weekly fall. Surplus fears weigh on prices."),
]
VARIANTS = {
    "15cards": {
        "n_cards": 15, "n_cols": 5, "col_w": 193,
        "first_brief": 19, "total": 39,
        "expected": [("EUROPE", 11), ("THE AMERICAS", 3),
                     ("ASIA-PACIFIC", 9), ("MIDEAST", 5), ("AFRICA", 0),
                     ("OCEANIA", 2), ("WORLD", 9)],
        "out": "sketch-v2b-rev4-15cards.png",
        "tag": "rev4-15cards",
    },
    "12cards": {
        "n_cards": 12, "n_cols": 4, "col_w": 243,
        "first_brief": 16, "total": 36,
        "expected": [("EUROPE", 10), ("THE AMERICAS", 3),
                     ("ASIA-PACIFIC", 8), ("MIDEAST", 5), ("AFRICA", 0),
                     ("OCEANIA", 2), ("WORLD", 8)],
        "out": "sketch-v2b-rev4-12cards.png",
        "tag": "rev4-12cards",
    },
}

# Brief texts for demoted cards (rev4 convention: the city name is trimmed
# out of the title when it repeats, so "Berlin: ..." does not say Berlin
# twice). Keys are the GLOBAL story numbers; city comes from the card's
# own strip ("N · CITY · TOPIC"). "MAIB" is a non-city label, exactly as
# in rev4's strip 23 (report author, not a city). Each entry is
# (city, region, text) — 2 sentences where 2 verified facts exist.
DEMOTED_BRIEFS = {
    16: ("Saudi Arabia", "MIDEAST", "Danger has passed in the south. Civil defence lifts alerts in three southern cities."),
    17: ("Finland", "EUROPE", "The first nuclear waste store is approved. It is the world's first permanent repository."),
    18: ("Wellington", "OCEANIA", "Bumrah strikes twice at lunch. The 1st Test is at Basin Reserve."),
    19: ("Berlin", "EUROPE", "The Coalition of the Willing meets. Witkoff and Kushner attend."),
    20: ("Saada", "MIDEAST", "The Saudi coalition intercepts a Houthi missile. The launcher is destroyed."),
    21: ("Tokyo", "ASIA", "India and Japan hold 2+2 defence talks. The ministers meet in the capital."),
    22: ("Hormuz", "MIDEAST", "A tanker is hit by a projectile. Oil steadies after the strike."),
    23: ("MAIB", "WORLD", "The Bayesian had a hidden wind weakness. Winds of 80 mph capsized her in seconds."),
}

# Stories deleted 12:10 WIB (NOTE.md "Total cerita fleksibel"): borderline
# in BOTH variants {35, 38, 43, 47} + weakest thin briefs. A also deletes
# {27, 33, 36, 37} (total 39). B also deletes {27, 33, 36, 37, 34, 42, 29}
# (total 36) — B keeps 28 + 32, so the New Delhi map pin survives in B.
DELETE_A = {35, 38, 43, 47, 27, 33, 36, 37}
DELETE_B = {35, 38, 43, 47, 27, 33, 36, 37, 34, 42, 29}


def build_variant(cfg):
    """Split rev4's CARDS/BRIEFS into this variant's cards + briefs.

    Cards = the FIRST n_cards of rev4's order. The rest become briefs
    (DEMOTED_BRIEFS table), in the same order, ahead of rev4's briefs.
    Then the per-variant deletion set removes borderline + weakest thin
    briefs (12:10 WIB flexible total). Every story keeps its rev4
    global number, so the map pins / region bar / DATE CHECK are
    recomputed from the final lists, not from 47. Returns
    (cards, briefs, first_brief) with briefs as (city, region, text).
    """
    n = cfg["n_cards"]
    cards = CARDS[:n]
    briefs = []
    for title, kind, sum1, sum2, strip, region in CARDS[n:]:
        gnum = int(strip.split(" · ")[0])
        city, bregion, text = DEMOTED_BRIEFS[gnum]
        briefs.append((city, bregion, text))
    delete = DELETE_A if cfg["tag"] == "rev4-15cards" else DELETE_B
    # BRIEFS below are rev4's FINAL 20 (the 4 borderline already gone),
    # so the old rev4 number is NOT 24 + index — it is OLD_NUMS[i].
    for i, (city, region, text) in enumerate(BRIEFS):
        if OLD_NUMS[i] in delete:
            continue
        briefs.append((city, region, text))
    assert int(CARDS[n][4].split(" · ")[0]) == cfg["first_brief"], \
        (CARDS[n][4], cfg["first_brief"])
    total = 3 + len(cards) + len(briefs)
    assert total == cfg["total"], (total, cfg["total"])
    return cards, briefs, cfg["first_brief"]



def brief_lines(d, city, text, width):
    """Wrap one brief's full text to the brief width (8pt). The first
    line starts with "CITY: " in bold; wrap() counts the whole line
    INCLUDING the bold prefix, so the first line is measured honestly.
    Returns the wrapped lines (prefix included in line 0)."""
    f = font(REG, 8)
    pref = f"{city}: "
    w_pref = d.textlength(pref, font=font(BOLD, 8))
    words, lines, cur, cur_w = text.split(), [], "", w_pref
    for w in words:
        ww = d.textlength((" " if cur else "") + w, font=f)
        if cur and cur_w + ww > width:
            lines.append(pref + cur if not lines else cur)
            cur, cur_w = w, d.textlength(w, font=f)
        else:
            cur = (cur + " " + w) if cur else w
            cur_w += ww
    if cur:
        lines.append(pref + cur if not lines else cur)
    return lines


def split_cols(items, n):
    """Split a list into n columns as EVENLY as possible (sizes differ
    by at most 1; the first columns get the extra item)."""
    base, extra = divmod(len(items), n)
    cols, i = [], 0
    for c in range(n):
        k = base + (1 if c < extra else 0)
        cols.append(items[i:i + k])
        i += k
    return cols


# ---------------------------------------------------------------- map
# Simplified continents as (lon, lat) polygons, equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80), (-80, 73),
     (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-76, 35), (-81, 26),
     (-84, 30), (-90, 21), (-97, 16), (-102, 18), (-110, 24), (-117, 33),
     (-124, 40), (-124, 49), (-135, 58), (-150, 60), (-168, 66)],
    [(-45, 60), (-32, 68), (-22, 70), (-20, 76), (-40, 80), (-58, 76),
     (-55, 70), (-45, 60)],
    [(-79, 9), (-72, 11), (-62, 9), (-52, 5), (-50, -2), (-42, -5),
     (-35, -9), (-39, -18), (-48, -28), (-55, -35), (-62, -41), (-68, -50),
     (-73, -54), (-74, -44), (-72, -30), (-80, -18), (-81, -5), (-79, 9)],
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (5, 57), (8, 57), (12, 55),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70), (22, 70),
     (15, 68), (10, 64), (5, 60), (-2, 57), (-6, 53), (-10, 50), (-10, 44),
     (-10, 36)],
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (3, 37), (10, 37), (15, 32),
     (22, 33), (30, 31), (34, 28), (37, 22), (43, 12), (48, 11), (51, 12),
     (46, 2), (41, -8), (38, -18), (33, -26), (28, -33), (20, -35),
     (16, -29), (14, -22), (12, -17), (9, -2), (9, 4), (0, 6), (-8, 5),
     (-13, 8), (-17, 15)],
    [(30, 70), (60, 70), (90, 75), (120, 73), (150, 70), (178, 66),
     (170, 60), (158, 52), (142, 40), (130, 33), (122, 38), (118, 25),
     (108, 18), (103, 7), (97, 15), (91, 22), (85, 19), (77, 8), (72, 20),
     (63, 25), (54, 27), (48, 30), (40, 32), (36, 36), (30, 42), (30, 70)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -11), (137, -12), (132, -12), (126, -14),
     (122, -17), (118, -20), (113, -22)],
    [(-5, 50), (-3, 53), (-1, 55), (0, 53), (1, 51), (-2, 50), (-5, 50)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 37), (141, 39),
     (143, 42), (144, 44), (142, 42), (140, 38), (137, 35), (134, 34),
     (131, 32), (130, 31)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (175, -41),
     (172, -43), (169, -46), (167, -45)],
]

REG_KEY = {"EUROPE": "EUROPE", "THE AMERICAS": "AMERICAS",
           "ASIA-PACIFIC": "ASIA", "MIDEAST": "MIDEAST",
           "AFRICA": "AFRICA", "OCEANIA": "OCEANIA", "WORLD": "WORLD"}


def region_counts_for(heroes, cards, briefs):
    """Count stories per region from the final lists (heroes + cards +
    briefs). Each entry carries its region; the bar above the heroes and
    the map legend are both drawn from this list, so they always agree.
    Returns [(display name, count)] in REGION_ORDER and the total."""
    counts = {k: 0 for _n, k in REGION_ORDER}
    for h in heroes:
        counts[h["region"]] += 1
    for c in cards:
        counts[c[5]] += 1
    for b in briefs:
        counts[b[1]] += 1
    total = sum(counts.values())
    assert total == len(heroes) + len(cards) + len(briefs), total
    return [(name, counts[key]) for name, key in REGION_ORDER], total


def build_markers(cards, briefs, first_brief):
    """Pins + dots for the map, derived from the final story lists.

    Pins: every CARD story with a place in PLACES (mark = its global
    story number from the strip, colour = its region) + the gold star
    for the Shenzhen summit (hero 1) + a numbered pin for the surviving
    New Delhi brief (it was pinned before; the NIA brief was deleted,
    so the pin now points at the Congress/Modi brief). Dots: one per
    DISTINCT brief place (a place already pinned gets no dot).
    Returns (pins, dots): pins are (city, mark, region), dots are
    (city, region). Pixel placement + collision handling live in
    map_box, which logs what got skipped.
    """
    pins = []
    for _t, _k, _s1, _s2, strip, region in cards:
        num = strip.split(" · ")[0]
        # strip cities are ALL-CAPS ("GAZA"); PLACES keys are title case
        city = strip.split(" · ")[1].title()
        if city in PLACES:
            pins.append((city, num, region))
    pins.append(("Shenzhen", "star", "ASIA"))
    for i, (city, region, _text) in enumerate(briefs):
        if city == "New Delhi":
            pins.append((city, str(first_brief + i), region))
            break
    # dots: one per DISTINCT place (dedup by coordinates — "China" and
    # "Beijing" are the same dot, "UK" and "London" are the same dot).
    # A place already pinned gets no dot.
    seen_coords = {PLACES[city] for city, _m, _r in pins}
    dots = []
    for city, region, _text in briefs:
        if city in ("Global", "New Delhi") or city not in PLACES:
            continue
        if PLACES[city] in seen_coords:
            continue
        seen_coords.add(PLACES[city])
        dots.append((city, region))
    return pins, dots


def project(lon, lat, mx, my, mw, mh):
    # 8px horizontal padding inside the box, so pins near the edge
    # (Wellington, lon 174.8) stay fully inside instead of being clipped.
    x = mx + 8 + (lon + 180.0) / 360.0 * (mw - 16)
    y = my + (75.0 - lat) / 130.0 * mh
    return (x, y)


def star_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def map_box(mw, mh, cards, briefs, first_brief, region_counts,
            legend_size=8, map_h=156, legend_counts=True, key_line=True):
    """The whole map box: bigger map (top) + one key line + region counts.

    Everything is drawn inside the box's own image, so nothing can bleed
    past the box border — the rev2 bleed is impossible by construction.
    Layout inside the 300x202 box: map 156px (was 122 — the freed space
    from the deleted city-count list), key line "NUMBERED PINS = CARDS ·
    DOTS = BRIEFS · ★ = SUMMIT", then the region counts in 2 lines
    (the SAME numbers as the bar above the heroes).
    legend_size: ukuran font hitungan region di legenda (default 8;
    9 aman — probe: tetap 2 baris di mw 300/330/380; 10 pecah jadi
    3 baris di mw 300 dan baris ke-3 dibuang). Returns (image, log):
    log lists placed pins/dots and skipped dots.
    map_h: tinggi gambar laut/peta di dalam box (default 156; revisi
    2x5 21:41 WIB butuh 140 untuk B supaya legenda tetap muat saat
    box menyusut — pin/titik dihitung dari map_h, jadi tetap benar).
    legend_counts: False = legenda HANYA key line, tanpa hitungan
    region (revisi 2x5 21:48 WIB — hitungan pindah ke section
    'N STORIES FROM 7 REGIONS'; default True supaya sketsa fewer
    tidak berubah).
    key_line: False = HAPUS baris legenda "NUMBERED PINS = CARDS ·
    DOTS = BRIEFS · ★ = SUMMIT" (revisi 2x5 22:23 WIB, Kevin:
    "HAPUS kata-kata di bawah peta"); pin/titik/★ tetap digambar.
    Default True supaya sketsa fewer tidak berubah. Bila map_h == mh
    (laut setinggi kotak penuh) + key_line=False, peta mengisi penuh
    kotak sampai tepi bawah tanpa pita kosong (revisi 22:23 WIB,
    Kevin: "PETA DIBUAT FULL").
    """
    pins, dots = build_markers(cards, briefs, first_brief)
    im = Image.new("RGB", (mw, mh), CARD_BG)
    d = ImageDraw.Draw(im)
    mtmp = Image.new("RGB", (mw, map_h), SEA)
    md = ImageDraw.Draw(mtmp)
    for poly in CONTINENTS:
        pts = [project(lon, lat, 0, 0, mw, map_h) for lon, lat in poly]
        md.polygon(pts, fill=LAND, outline=LAND_LINE)
    fl = font(BOLD, 10)
    fp = font(BOLD, 7)
    placed = []  # (x, y, radius) of everything drawn, for collision checks
    # --- pins (numbered) + star; leader lines for offset pins
    for city, mark, region in pins:
        lon, lat = PLACES[city]
        px, py = project(lon, lat, 0, 0, mw, map_h)
        dx, dy = PIN_OFFSETS.get(city, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            md.line([(px, py), (qx, qy)], fill=NAVY, width=1)
        if mark == "star":
            md.polygon(star_points(qx, qy, 8, 3.5), fill=GOLD, outline=NAVY)
            placed.append((qx, qy, 8))
        else:
            col = REGION_COLORS[region]
            md.ellipse([qx - 5.5, qy - 5.5, qx + 5.5, qy + 5.5], fill=col,
                       outline=WHITE, width=1)
            tw = md.textlength(mark, font=fp)
            md.text((qx - tw / 2, qy - 4), mark, font=fp, fill=WHITE)
            placed.append((qx, qy, 5.5))
        if city in PIN_LABELS:
            side = PIN_LABELS[city]
            tw = md.textlength(city, font=fl)
            if side == "r":
                tx, ty = qx + 8, qy - 5
            elif side == "l":
                tx, ty = qx - 8 - tw, qy - 5
            elif side == "a":
                tx, ty = qx - tw / 2, qy - 16
            elif side == "b":
                tx, ty = qx - tw / 2, qy + 9
            md.text((tx, ty), city, font=fl, fill=NAVY,
                    stroke_width=2, stroke_fill=(246, 241, 231))
    # pins must not overlap each other (offsets are hand-tuned for this)
    for i, (x1, y1, _r1) in enumerate(placed):
        for x2, y2, _r2 in placed[i + 1:]:
            assert ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 >= 10, \
                f"map pins collide: {(x1, y1)} vs {(x2, y2)}"
    # --- dots (brief places): skip any that would collide with a pin/dot
    placed_dots, skipped_dots = [], []
    for city, region in dots:
        lon, lat = PLACES[city]
        px, py = project(lon, lat, 0, 0, mw, map_h)
        if any(((px - x) ** 2 + (py - y) ** 2) ** 0.5 < 8
               for x, y, _r in placed):
            skipped_dots.append(city)
            continue
        md.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                   fill=REGION_COLORS[region], outline=WHITE, width=1)
        placed.append((px, py, 2.5))
        placed_dots.append(city)
    im.paste(mtmp, (0, 0))
    # --- key line + region counts (same numbers as the bar above heroes)
    # REVISI 22:23 WIB (Kevin: "HAPUS kata-kata di bawah peta"): bila
    # key_line=False, baris legenda tidak digambar sama sekali.
    f_key = font(BOLD, 8)
    ky = map_h + 4
    if key_line:
        d.text((6, ky), "NUMBERED PINS = CARDS · DOTS = BRIEFS · ★ = SUMMIT",
               font=f_key, fill=NAVY)
    # region counts in 2 lines, greedy by width (dot + "NAME N" each).
    # legend_counts=False (revisi 2x5 21:48 WIB): hitungan region pindah
    # ke section 'N STORIES FROM 7 REGIONS', legenda tinggal key line.
    if legend_counts:
        f_rc = font(BOLD, legend_size)
        lines, cur, cur_w = [], [], 0.0
        for name, n in region_counts:
            w = 8 + d.textlength(f"{name} {n}", font=f_rc) + 8
            if cur and cur_w + w > mw - 12:
                lines.append(cur)
                cur, cur_w = [(name, n)], w
            else:
                cur.append((name, n))
                cur_w += w
        if cur:
            lines.append(cur)
        assert len(lines) <= 2, f"legenda region jadi {len(lines)} baris di mw {mw}"
        ly = ky + 13
        for line in lines[:2]:
            x = 6
            for name, n in line:
                d.ellipse([x, ly + 2, x + 6, ly + 8],
                          fill=REGION_COLORS[REG_KEY[name]])
                d.text((x + 8, ly), f"{name} {n}", font=f_rc, fill=NAVY)
                x += 8 + int(d.textlength(f"{name} {n}", font=f_rc)) + 8
            ly += legend_size + 4
    log = {"pins": [m for _c, m, _r in pins],
           "dots": placed_dots, "skipped_dots": skipped_dots}
    return im, log


def main(cfg):
    cards, briefs, first_brief = build_variant(cfg)
    REGION_COUNTS, TOTAL = region_counts_for(HEROES, cards, briefs)
    assert TOTAL == cfg["total"], (TOTAL, cfg["total"])
    assert REGION_COUNTS == cfg["expected"], REGION_COUNTS
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ---- top strip (16px inset so the corner texts are never clipped)
    f_top = font(BOLD, 13)
    f_top_c = font(BOLD, 15)
    d.text((16, 8), "ALL DATED 19 NOV", font=f_top, fill=RED)
    # kicker (rev4, feedback Kevin 11:47 WIB): wider tracking (a space
    # between every letter) so the masthead area feels richer; already
    # navy, so the colour stays.
    kick = "  ".join(" ".join(w) for w in "THE WORLD IN ONE DAY".split())
    d.text((W // 2, 7), kick, font=f_top_c, fill=NAVY, anchor="ma")
    d.text((W - 16, 8), f"{TOTAL} STORIES", font=f_top, fill=RED,
           anchor="ra")

    # ---- masthead (auto-fit so the date never overflows the page)
    # rev4, feedback Kevin 11:47 WIB: the "19" is bigger (+8pt) and red,
    # so the date pops like rank 1's masthead — while the date stays the
    # largest text on the page (criterion 1). FIX 11:55 WIB: in rev4 all
    # three segments shared their TOP edge (anchor "la"), so the bigger
    # "19" sat ~6px lower than its neighbours and looked like it was
    # floating. Now all three are drawn with anchor "ls" (baseline) at
    # the SAME y — baselines aligned; the "19" extends ~6px HIGHER
    # instead (deliberate emphasis). Baseline = neighbours' top (y=26)
    # + their ascent (49px at 52pt) = 75. The "19" glyph top is then
    # ~y=30, clear of the kicker (bottom ~y=21) — verified by zoom crop.
    # (SERIF is already DejaVu Serif Bold, so no separate bold font is
    # needed.)
    f_size = 52
    while f_size > 30:
        f_date = font(SERIF, f_size)
        f_19 = font(SERIF, f_size + 8)
        w = (d.textlength("THURSDAY ", font=f_date)
             + d.textlength("19", font=f_19)
             + d.textlength(" NOVEMBER 2026", font=f_date))
        if w <= 1000:
            break
        f_size -= 2
    w1 = d.textlength("THURSDAY ", font=f_date)
    w2 = d.textlength("19", font=f_19)
    w3 = d.textlength(" NOVEMBER 2026", font=f_date)
    x0 = (W - (w1 + w2 + w3)) // 2
    baseline = 26 + f_date.getmetrics()[0]
    d.text((x0, baseline), "THURSDAY ", font=f_date, fill=INK, anchor="ls")
    d.text((x0 + w1, baseline), "19", font=f_19, fill=RED, anchor="ls")
    d.text((x0 + w1 + w2, baseline), " NOVEMBER 2026", font=f_date,
           fill=INK, anchor="ls")
    # deck (rewritten 11:55 WIB — OWN WORDS, not rank 1's): rev4's deck
    # ("a three-way summit, GTA VI's release day, the biggest IPO ever,
    # a genocide verdict, a cyclone") copied rank 1's deck almost word
    # for word. The new deck names the same five verified main stories
    # with our own phrasing: "three-president summit" (not "three-way
    # summit"), "GTA VI on sale" (not "release day"), "an $81.3bn IPO"
    # (the number, not "the biggest IPO ever"), "the ICJ verdict" (not
    # "a genocide judgment"), "a storm off India" (not "a cyclone").
    # Auto-fit: 14pt, shrinking to 12pt if the line ever exceeds the
    # page (measured 930px at 14pt — fits).
    deck_txt = (f"{TOTAL} stories from one day — a three-president summit, "
                "GTA VI on sale, an $81.3bn IPO, the ICJ verdict, "
                "a storm off India")
    f_deck = None
    for dsize in (14, 13, 12):
        f_try = font(BOLD, dsize)
        if d.textlength(deck_txt, font=f_try) <= 1000:
            f_deck = f_try
            break
    if f_deck is None:
        f_deck = font(BOLD, 12)
    d.text((W // 2, 80), deck_txt, font=f_deck, fill=RED, anchor="ma")
    d.line([12, 100, W - 12, 100], fill=GOLD, width=2)

    # ---- (a) STORIES BY REGION bar — computed from this variant's
    # final story lists (region_counts_for); the parts sum to TOTAL.
    reg_txt = " · ".join(f"{name} {n}" for name, n in REGION_COUNTS)
    f_reg = None
    for size in (13, 12, 11, 10):
        f_try = font(BOLD, size)
        if (d.textlength("STORIES BY REGION — ", font=f_try)
                + d.textlength(reg_txt, font=f_try)) <= 1000:
            f_reg = f_try
            break
    if f_reg is None:
        f_reg = font(BOLD, 10)
    lw = d.textlength("STORIES BY REGION — ", font=f_reg)
    total_w = lw + d.textlength(reg_txt, font=f_reg)
    rx = (W - total_w) // 2
    d.text((rx, 104), "STORIES BY REGION — ", font=f_reg, fill=RED)
    d.text((rx + lw, 104), reg_txt, font=f_reg, fill=NAVY)

    # ---- (b) big-numbers bar — 6 verified key numbers of the day.
    # MERGED (Kevin 13:28 WIB): one continuous strip, segmented by region
    # tint, NAVY outer frame, thin region-colour dividers between segments.
    f_nb = font(BOLD, 17)
    f_nc = font(REG, 9)
    nb_w, nb_gap = 160, 8
    strip_l, strip_t, strip_b = 7, 119, 168
    seg_w = 167  # 6 * 167 = 1002 = strip width (x 7..1009)
    for i, (num, cap) in enumerate(BIG_NUMBERS):
        nx = 12 + i * (nb_w + nb_gap)
        rc = REGION_COLORS[BIG_NUMBER_REGIONS[i]]
        tint = tuple(round(0.12 * a + 0.88 * b)
                     for a, b in zip(rc, PAPER))
        sx0 = strip_l + i * seg_w
        d.rectangle([sx0, strip_t, sx0 + seg_w - 1, strip_b], fill=tint)
        if i:
            d.line([sx0, strip_t, sx0, strip_b], fill=rc, width=1)
        d.text((nx, 124), num, font=f_nb, fill=NAVY)
        for j, ln in enumerate(wrap_max(d, cap, f_nc, nb_w - 4, 2)):
            d.text((nx, 146 + j * 11), ln, font=f_nc, fill=MUTED)
    d.rectangle([strip_l, strip_t, strip_l + 6 * seg_w - 1, strip_b],
                outline=NAVY, width=2)

    # ---- 3 heroes as CARDS (Kevin 11:33): each hero is wrapped in a 3px
    # border (grid cards: 2px) around image + headline + 2-line deck,
    # with its "N · CITY · TOPIC" strip on the image top — same structure
    # as the grid cards, bigger. FIX 11:55 WIB: hero image 58 -> 70px
    # (heroes start 6px higher, cards 144 -> 150px tall) — the pictures
    # must actually show. CORRECTION 12:12 WIB: the freed ~20px from
    # the deleted grid heading go to the HERO images (not the card
    # images): hero image 70 -> 88px, hero card 150 -> 170px. Deck
    # offset stays 47 (deck ends hy+167, card ends hy+170).
    hw, img_h, hero_h = 328, 88, 170
    hy = 170
    f_hh = font(BOLD, 16)
    f_hd = font(REG, 13)
    for i, hero in enumerate(HEROES):
        x = 12 + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hero_h], fill=CARD_BG,
                    outline=CARD_LINE, width=3)
        img = Image.open(os.path.join(ASSETS, hero["file"])).convert("RGB")
        canvas.paste(cover_crop(img, hw - 6, img_h), (x + 3, hy + 3))
        draw_strip(d, x + 3, hy + 3, hw - 6, 16, hero["strip"],
                   REGION_COLORS[hero["region"]], 9)
        lines = wrap_max(d, hero["headline"], f_hh, hw - 10, 2)
        ly = hy + img_h + 7
        for ln in lines:
            d.text((x + 5, ly), ln, font=f_hh, fill=INK)
            ly += 19
        deck_lines = wrap_max(d, hero["deck"], f_hd, hw - 10, 2)
        ly = hy + img_h + 47
        for ln in deck_lines:
            d.text((x + 5, ly), ln, font=f_hd, fill=MUTED)
            ly += 16
    # ---- grid (no heading above it any more — DELETED 12:12 WIB, rank
    # 1/2 have no heading above the cards; the cards flow straight after
    # the heroes. The freed ~20px went to the hero images above.)
    # 3 rows (not rev4's 4): cards 82 -> 112px tall, image 28 -> 60px,
    # so the picture actually shows (FIX 11:55 WIB: 58 -> 60px — the
    # extra 2px come from the title/summary geometry, which already
    # left 2px slack at the card bottom). Same 5-col (A) / 4-col (B)
    # widths as the variant config; the grid fills the same slot
    # (gy0 346, sec_y 696) rev4's 4-row grid filled, so nothing below
    # moves. Strip / title / summary geometry is rev4's, only img_h2
    # grew (title and summary sit at y+img_h2+4 / +31 / +41 as in rev4).
    col_w, card_h, gap_x, gap_y = cfg["col_w"], 112, 8, 5
    gx0, gy0 = 12, 346
    img_h2 = 60
    f_ct = font(BOLD, 11)
    f_cs = font(REG, 9)
    for idx, (title, kind, sum1, sum2, strip, region) in enumerate(cards):
        r, c = divmod(idx, cfg["n_cols"])
        x = gx0 + c * (col_w + gap_x)
        y = gy0 + r * (card_h + gap_y)
        d.rectangle([x, y, x + col_w, y + card_h], fill=CARD_BG,
                    outline=CARD_LINE, width=2)
        if kind.startswith("asset:"):
            img = Image.open(os.path.join(ASSETS, AI_ASSETS[kind[6:]]))
            img = img.convert("RGB")
            canvas.paste(cover_crop(img, col_w - 4, img_h2), (x + 2, y + 2))
        else:
            canvas.paste(motif_image(kind, col_w - 4, img_h2), (x + 2, y + 2))
        draw_strip(d, x + 2, y + 2, col_w - 4, 10, strip,
                   REGION_COLORS[region], 7)
        lines = wrap_max(d, title, f_ct, col_w - 12, 2)
        ly = y + img_h2 + 4
        for ln in lines:
            d.text((x + 6, ly), ln, font=f_ct, fill=INK)
            ly += 13
        d.text((x + 6, y + img_h2 + 31),
               fit_one_line(d, sum1, f_cs, col_w - 12),
               font=f_cs, fill=MUTED)
        d.text((x + 6, y + img_h2 + 41),
               fit_one_line(d, sum2, f_cs, col_w - 12),
               font=f_cs, fill=MUTED)
    # ---- map (300x202 box: bigger map + key line + region counts, all
    # clipped inside the border) + 3 brief columns, 21 briefs (7/7/7).
    # Briefs are numbered first_brief-TOTAL, CONTINUING from heroes 1-3
    # + cards (no "MORE", no restart at 1). Each brief starts with its
    # city.
    sec_y = 696
    f_sh = font(BOLD, 16)
    d.text((12, sec_y), "WHERE IT HAPPENED", font=f_sh, fill=NAVY)
    d.text((324, sec_y), "MORE STORIES FROM 19 NOVEMBER",
           font=font(BOLD, 15), fill=NAVY)
    d.line([324, sec_y + 22, W - 12, sec_y + 22], fill=GOLD, width=2)
    map_im, map_log = map_box(300, 202, cards, briefs, first_brief,
                              REGION_COUNTS)
    canvas.paste(map_im, (12, sec_y + 22))
    d.rectangle([12, sec_y + 22, 12 + 300, sec_y + 22 + 202],
                outline=CARD_LINE, width=2)
    print(cfg["tag"], "map pins:", map_log["pins"], "| dots:",
          map_log["dots"], "| skipped dots:", map_log["skipped_dots"])
    # ---- briefs (12:10 WIB format): a vertical REGION-COLOUR strip at
    # the left edge of each brief (replacing the red number dot), the
    # story number in small red bold, the CITY IN BOLD at the start of
    # the text, 2 sentences where 2 verified facts exist. 8pt throughout.
    # Layout is STACKED with measured heights (not even-spread slots):
    # total = sum(lines x 10px) + gaps; the slack is spread evenly as
    # extra gap. The script FAILS loudly if a column overflows, so a
    # too-long brief is never silently clipped.
    bw, bgap = 221, 12
    bx0, by0 = 324, sec_y + 24
    col_h = 200  # all columns end at by0 + 200
    f_bn = font(BOLD, 8)
    f_city = font(BOLD, 8)
    f_bt = font(REG, 8)
    LH, GAP = 10, 5
    cols = split_cols(briefs, 3)
    for ci, col in enumerate(cols):
        cx = bx0 + ci * (bw + bgap)
        measured = []
        for bi, (city, region, b) in enumerate(col):
            n = first_brief + sum(len(c) for c in cols[:ci]) + bi
            lines = brief_lines(d, city, b, bw - 25)
            measured.append((n, city, region, lines))
        total_h = sum(len(lns) * LH for _n, _c, _r, lns in measured) \
            + (len(measured) - 1) * GAP
        assert total_h <= col_h, \
            f"brief column {ci} overflows by {total_h - col_h}px"
        extra = (col_h - total_h) / max(len(measured) - 1, 1)
        cy = by0
        for n, city, region, lines in measured:
            # vertical strip, region colour, spanning the text block
            d.rectangle([cx, cy, cx + 5, cy + len(lines) * LH - 1],
                        fill=REGION_COLORS[region])
            d.text((cx + 9, cy), f"{n}.", font=f_bn, fill=RED)
            ly = cy
            for li, ln in enumerate(lines):
                if li == 0:
                    pref = f"{city}: "
                    d.text((cx + 25, ly), pref, font=f_city, fill=INK)
                    d.text((cx + 25 + d.textlength(pref, font=f_city), ly),
                           ln[len(pref):], font=f_bt, fill=INK)
                else:
                    d.text((cx + 25, ly), ln, font=f_bt, fill=INK)
                ly += LH
            cy = ly + GAP + extra
    # ---- DATE CHECK strip — PROMINENT: dark navy band, 2px gold frame,
    #   gold badge + white bold message, so the eye goes straight to it.
    dy, dh = 923, 46
    d.rectangle([12, dy, W - 12, dy + dh], fill=NAVY)
    d.rectangle([12, dy, W - 12, dy + dh], outline=GOLD, width=2)
    badge = "DATE CHECK"
    f_badge = font(BOLD, 13)
    bw_b = int(d.textlength(badge, font=f_badge)) + 20
    d.rectangle([22, dy + 8, 22 + bw_b, dy + dh - 8], fill=GOLD)
    d.text((22 + bw_b // 2, dy + dh // 2), badge, font=f_badge, fill=NAVY,
           anchor="mm")
    msg = (f"All {TOTAL} stories are 19 November 2026 — Fed minutes, "
           "Voyager 1, Nvidia H200 halt, EU loan are 18 Nov: left out.")
    f_msg = 14
    while f_msg > 10:
        f_dc = font(BOLD, f_msg)
        if d.textlength(msg, font=f_dc) <= (W - 12) - (22 + bw_b + 12) - 10:
            break
        f_msg -= 1
    d.text((22 + bw_b + 12, dy + dh // 2), msg, font=f_dc, fill=WHITE,
           anchor="lm")

    # ---- footer (auto-fit: both lines shrink until they fit the page —
    # the rev3 first render clipped both lines past the edges)
    src = ("Sources: Reuters · BBC · The Guardian · Fox News · ABS · "
           "CoinGecko · Al Jazeera · gov.uk · TBS · Daily Star · ANI")
    f_size = 11
    while f_size > 8:
        f_ft = font(REG, f_size)
        if d.textlength(src, font=f_ft) <= 1000:
            break
        f_size -= 1
    d.text((W // 2, 975), src, font=f_ft, fill=MUTED, anchor="ma")
    deleted = DELETE_A if cfg["tag"] == "rev4-15cards" else DELETE_B
    note = (f"Sketch {cfg['tag']} of B — 3 AI hero pictures from v1.1; "
            "cards are "
            "Pillow mini-illustrations (final: small AI pictures). "
            f"Numbering 1–{TOTAL}. {len(deleted)} stories removed: "
            "Jeffries, 3 tankers, NIA, Bangladesh + weakest thin briefs.")
    f_size = 10
    while f_size > 7:
        f_nt = font(REG, f_size)
        if d.textlength(note, font=f_nt) <= 1000:
            break
        f_size -= 1
    d.text((W // 2, 991), note, font=f_nt, fill=MUTED, anchor="ma")

    out = os.path.join(HERE, cfg["out"])
    canvas.save(out, format="PNG", optimize=True)
    data = open(out, "rb").read()
    print("wrote", out, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])
    assert canvas.size == (1024, 1024), canvas.size
    assert len(data) <= 1048576, len(data)


if __name__ == "__main__":
    for name in ("15cards", "12cards"):
        main(VARIANTS[name])
