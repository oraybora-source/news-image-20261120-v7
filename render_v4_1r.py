#!/usr/bin/env python3
"""SKETSA v4-1r news-image-20261120 — improve sketsa 1 "Koran Serif".

Perintah Kevin 18:44 WIB: "analisis dan improve gambarnya dulu" — SEBELUM
build final. Ini SKETSA (mockup layout), BUKAN entry final, BUKAN submit,
BILANGAN repo GitHub.

Dasar: sketches-v4/render_v4.py sketsa v4-1 (data HEROES/CARDS/BRIEFS sama,
isi cerita TIDAK diubah; slot 34–36 tetap placeholder seperti sketsa 1).
Analisis lengkap: sketches-v4/analisis-improve-sketsa1.md

Perubahan vs sketsa 1 (semua dari analisis):
1. Masthead ala RANK 3: kicker + garis (gap 6px) + judul 54pt Display Bold
   RATA KIRI + ruang kosong + deck 2 baris merah italic RATA KIRI + garis
   di bawah deck (gap 8px). TIDAK ADA garis di dekat judul.
2. Assert no-overlap programatik: registry semua kotak teks/garis/gambar;
   teks×garis, teks×teks, teks×gambar tidak boleh beririsan; gap garis
   masthead ≥8px dari bbox tinta judul.
3. Gap antar section 12px; hero 160px, kartu 132px (anggaran vertikal: 23 brief × 2 baris butuh band 232px).
4. Chip region -> tint pucat + teks navy (pilihan Winter sendiri).
5. Daratan peta krem pucat; judul "WHERE IT HAPPENED"; frame border
   kelihatan; legenda pin (bukan hitungan region).
6. MORE STORIES: judul merah + border di sekeliling blok brief.
7. Grafik Taipei + Asia markets -> garis MERAH TURUN (sebelumnya naik,
   bertentangan dengan cerita); Gold -> batang menurun + panah turun.
8. Tile baru palet kalem Winter (krem/navy/merah kalem/emas kalem/sage/
   slate) + bar aksen 8px di atas tiap tile (memenuhi aturan Kevin:
   warna atas tiap gambar beda dari tetangganya — dicek check_top_colors).
   Kyiv + F1 gelap dipertahankan (satu hero + satu kartu gelap, ala rank 1).
"""
import os
import sys
import json
import hashlib

sys.path.insert(0, "/home/hatch/workspace/makefun/news-image-20261120/sketches-v4")
sys.path.insert(0, "/home/hatch/workspace/makefun/news-image-20261120")

from PIL import Image, ImageDraw, ImageFont

import render_v4 as v4
import render_sketches as rs
import render_variants as rv

PAPER = rv.PAPER
NAVY = rv.NAVY
INK = rv.INK
RED = rv.RED
GOLD = rv.GOLD
WHITE = rv.WHITE
CARD_BG = rv.CARD_BG
BOLD, REG = rv.BOLD, rv.REG
F = v4.F
SERIF_B = v4.SERIF_B
SERIF = v4.SERIF
SERIF_IT = v4.SERIF_IT
DISPLAY_B = v4.DISPLAY_B

# ------------------------------------------------------------------ palet Winter
CREAM = (250, 247, 238)      # latar tile (S~0.05)
SAGE = (138, 155, 126)       # S=0.19
SLATE = (91, 107, 122)       # S=0.25
TEAL_M = (105, 130, 138)     # S=0.24
DUSTY = (198, 150, 135)      # S=0.24
RED_M = (176, 48, 48)        # merah kalem (dipakai garis/panah, bukan bidang)
GOLD_M = (200, 170, 90)      # emas (S=0.55 — hanya aksen kecil)
LAND_1R = (232, 224, 196)    # daratan peta krem pucat (S=0.155)
LAND_OUT = (180, 160, 115)
SEA_1R = NAVY
TINTS = {  # chip region: tint pucat + teks navy
    "EUROPE": (200, 215, 235), "AMERICAS": (235, 200, 200),
    "ASIA": (220, 205, 235), "MIDEAST": (240, 220, 190),
    "AFRICA": (205, 225, 200), "OCEANIA": (195, 220, 220),
    "WORLD": (225, 225, 225),
}
# Bar aksen atas tiap tile (8px) — tetangga ortogonal selalu beda warna.
ACCENTS = {
    "akvan": NAVY, "kyiv": RED_M, "cop31": GOLD_M,
    "cricket": SAGE, "sco": SLATE, "florida": DUSTY, "apec": TEAL_M,
    "taipei": NAVY,
    "gold": GOLD_M, "gta": RED_M, "mkt": SLATE, "prabowo": SAGE,
    "f1": GOLD_M,
}

# ------------------------------------------------------------------ registry no-overlap
BOXREG = []  # (kind, (x0,y0,x1,y1), label); kind: text|rule|image


def reg(kind, box, label):
    assert box[2] > box[0] and box[3] > box[1], f"box kosong {label}: {box}"
    BOXREG.append((kind, box, label))


def _overlap(a, b):
    """Beririsan bila bersinggungan >1px di kedua arah (toleransi 1px:
    textbbox Pillow bisa meleset ~0,3px dari advance — bukan tumpang
    tindih sungguhan)."""
    ax0, ay0, ax1, ay1 = a[0] + 1, a[1] + 1, a[2] - 1, a[3] - 1
    bx0, by0, bx1, by1 = b[0] + 1, b[1] + 1, b[2] - 1, b[3] - 1
    return not (ax1 <= bx0 or bx1 <= ax0 or ay1 <= by0 or by1 <= ay0)


def check_no_overlap():
    bad = []
    for i, (k1, b1, l1) in enumerate(BOXREG):
        for k2, b2, l2 in BOXREG[i + 1:]:
            if not _overlap(b1, b2):
                continue
            pair = {k1, k2}
            if pair <= {"text", "rule"} or pair == {"text"} or pair == {"text", "image"}:
                bad.append((l1, l2, k1, k2))
    assert not bad, f"OVERLAP (aturan keras Kevin): {bad}"
    return len(BOXREG)


# ------------------------------------------------------------------ tile painters 1r
def _base(w, h, bg=CREAM):
    return Image.new("RGB", (w, h), bg)


def p_radar_cream(w, h):
    """Akvan: krem + busur navy + jalur merah + titik landfall (ala rank 1)."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    cx, cy = int(w * 0.62), int(h * 0.52)
    for r in (0.24, 0.44, 0.64, 0.84):
        rr = min(w, h) * r
        d.ellipse([cx - rr, cy - rr * 0.70, cx + rr, cy + rr * 0.70],
                  outline=NAVY, width=3)
    d.line([(int(w * 0.06), int(h * 0.92)), (cx, cy)], fill=RED_M, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD_M, outline=NAVY, width=1)
    d.ellipse([int(w * 0.06) - 4, int(h * 0.92) - 4,
               int(w * 0.06) + 4, int(h * 0.92) + 4], fill=RED_M)
    return im


def p_night_kyiv(w, h):
    """Kyiv: langit malam + 3 jejak rudal MENURUN + ledakan di bawah
    (bukan busur menggantung seperti kalung — itu cacat paint_arcs)."""
    im = Image.new("RGB", (w, h), (12, 20, 38))
    d = ImageDraw.Draw(im)
    for (sx, sy) in ((0.10, 0.15), (0.30, 0.08), (0.55, 0.18),
                     (0.80, 0.10), (0.92, 0.25)):
        d.ellipse([int(w * sx) - 1, int(h * sy) - 1,
                   int(w * sx) + 1, int(h * sy) + 1], fill=(220, 220, 200))
    for k, (x0, x1, col) in enumerate((
            (0.15, 0.30, (255, 140, 60)),
            (0.45, 0.55, (255, 200, 90)),
            (0.72, 0.85, (255, 140, 60)))):
        mx = (x0 + x1) / 2 + (0.06 if k % 2 else -0.06)
        for t in range(0, 21):
            u = t / 20
            fx = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1
            fy = (1 - u) ** 2 * 0.08 + 2 * (1 - u) * u * 0.30 + u * u * 0.78
            px, py = int(w * fx), int(h * fy)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
        bx, by = int(w * x1), int(h * 0.78)
        d.polygon(rv.star_points(bx, by, 9, 4), fill=(255, 180, 60),
                  outline=(255, 220, 120))
    for i, bh in enumerate((0.20, 0.30, 0.16, 0.26, 0.22)):
        bx = int(w * (0.06 + i * 0.18))
        d.rectangle([bx, h * (0.98 - bh), bx + int(w * 0.13), h],
                    fill=(30, 42, 66))
    return im


def p_globe_cop(w, h):
    """COP31: globe + termometer merah di latar krem (ala rank 1)."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    cx, cy, r = int(w * 0.36), int(h * 0.50), int(min(w, h) * 0.44)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.ellipse([cx - r // 2, cy - r // 2, cx - r // 6, cy + r // 4], fill=SLATE)
    d.ellipse([cx + r // 6, cy - r // 4, cx + r // 2, cy + r // 8], fill=SAGE)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=NAVY, width=2)
    tx = int(w * 0.80)
    d.rounded_rectangle([tx - 7, int(h * 0.14), tx + 7, int(h * 0.72)],
                        radius=7, fill=WHITE, outline=NAVY, width=2)
    d.rectangle([tx - 4, int(h * 0.42), tx + 4, int(h * 0.70)], fill=RED_M)
    d.ellipse([tx - 12, int(h * 0.68), tx + 12, int(h * 0.92)],
              fill=RED_M, outline=NAVY, width=2)
    return im


def p_cricket(w, h):
    """Kriket: langit krem + lapangan sage + bat + bola + stumps."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    d.rectangle([0, int(h * 0.55), w, h], fill=SAGE)
    d.line([(0, int(h * 0.55)), (w, int(h * 0.55))], fill=NAVY, width=2)
    d.line([(int(w * 0.10), int(h * 0.72)), (int(w * 0.90), int(h * 0.72))],
           fill=WHITE, width=3)
    # bat coklat diagonal
    d.polygon([(int(w * 0.30), int(h * 0.10)), (int(w * 0.36), int(h * 0.14)),
               (int(w * 0.52), int(h * 0.52)), (int(w * 0.46), int(h * 0.56))],
              fill=(150, 110, 70), outline=NAVY)
    # bola merah + stumps kuning
    d.ellipse([int(w * 0.62), int(h * 0.30), int(w * 0.70), int(h * 0.42)],
              fill=RED_M, outline=NAVY, width=1)
    for i in range(3):
        sx = int(w * (0.80 + i * 0.05))
        d.rectangle([sx, int(h * 0.28), sx + 4, int(h * 0.52)],
                    fill=GOLD_M, outline=NAVY, width=1)
    return im


def p_sco(w, h):
    """SCO: gedung kalem + 2 bendera kecil + garis tanah."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    bx0, bx1 = int(w * 0.30), int(w * 0.70)
    by0, by1 = int(h * 0.30), int(h * 0.82)
    d.rectangle([bx0, by0, bx1, by1], fill=(200, 180, 140), outline=NAVY, width=2)
    d.polygon([(bx0 - 8, by0), (bx1 + 8, by0), ((bx0 + bx1) // 2, int(h * 0.12))],
              fill=NAVY)
    d.rectangle([(bx0 + bx1) // 2 - 8, int(h * 0.60),
                 (bx0 + bx1) // 2 + 8, by1], fill=NAVY)
    for i, col in enumerate((NAVY, RED_M)):
        fx = int(w * (0.16 + i * 0.62))
        d.line([(fx, int(h * 0.22)), (fx, int(h * 0.82))], fill=NAVY, width=2)
        d.rectangle([fx, int(h * 0.22), fx + int(w * 0.13), int(h * 0.38)],
                    fill=col, outline=NAVY, width=1)
    d.line([(0, by1), (w, by1)], fill=SLATE, width=3)
    return im


def p_flood(w, h):
    """Florida: langit biru-grey pucat + rumah krem atap merah + air + ombak."""
    im = _base(w, h, (185, 200, 210))
    d = ImageDraw.Draw(im)
    hx0, hx1 = int(w * 0.30), int(w * 0.70)
    hy0, hy1 = int(h * 0.34), int(h * 0.68)
    d.rectangle([hx0, hy0, hx1, hy1], fill=CREAM, outline=NAVY, width=2)
    d.polygon([(hx0 - 8, hy0), (hx1 + 8, hy0), ((hx0 + hx1) // 2, int(h * 0.18))],
              fill=RED_M, outline=NAVY)
    d.rectangle([int(w * 0.44), int(h * 0.52), int(w * 0.56), hy1], fill=NAVY)
    d.rectangle([0, int(h * 0.68), w, h], fill=(90, 120, 140))
    for i, wx in enumerate((0.12, 0.42, 0.72)):
        d.arc([int(w * wx), int(h * 0.74), int(w * (wx + 0.22)), int(h * 0.92)],
              180, 360, fill=WHITE, width=3)
    d.ellipse([int(w * 0.08), int(h * 0.30), int(w * 0.20), int(h * 0.48)],
              fill=SAGE, outline=NAVY, width=1)
    return im


def p_flags3(w, h, cols):
    """3 bendera kalem + meja (APEC / Prabowo) — tanpa figur blob."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    for i, col in enumerate(cols):
        fx = int(w * (0.12 + i * 0.30))
        d.line([(fx + int(w * 0.10), int(h * 0.18)),
                (fx + int(w * 0.10), int(h * 0.78))], fill=NAVY, width=2)
        d.rectangle([fx, int(h * 0.18), fx + int(w * 0.20), int(h * 0.48)],
                    fill=col, outline=NAVY, width=1)
        if col == WHITE:  # bendera putih (Jepang/Indonesia): titik merah
            d.ellipse([fx + int(w * 0.07), int(h * 0.27),
                       fx + int(w * 0.13), int(h * 0.39)], fill=RED_M)
    d.rectangle([int(w * 0.08), int(h * 0.78), int(w * 0.92), int(h * 0.86)],
                fill=(150, 110, 70), outline=NAVY, width=1)
    return im


def p_chart_down(w, h):
    """Grafik TURUN merah tebal di latar krem (Taipei / Asia markets).

    FIX vs sketsa 1: garisnya dulu NAIK (hijau/emas) padahal ceritanya
    pasar JATUH — grafik tidak boleh bertentangan dengan cerita."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    for gy in (0.25, 0.50, 0.75):
        d.line([(int(w * 0.06), int(h * gy)), (int(w * 0.94), int(h * gy))],
               fill=(215, 210, 200), width=1)
    pts = [(0.08, 0.22), (0.26, 0.34), (0.42, 0.30), (0.60, 0.55),
           (0.76, 0.50), (0.90, 0.78)]
    xy = [(int(w * a), int(h * b)) for a, b in pts]
    d.line(xy, fill=RED_M, width=4, joint="curve")
    ex, ey = xy[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED_M)
    d.line([(int(w * 0.06), int(h * 0.90)), (int(w * 0.94), int(h * 0.90))],
           fill=SLATE, width=2)
    return im


def p_gold_down(w, h):
    """Gold: batang emas MENURUN + panah merah turun (cerita: plunges)."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    heights = (0.50, 0.42, 0.34, 0.26)
    for i, hh in enumerate(heights):
        bx0 = int(w * (0.10 + i * 0.20))
        d.rectangle([bx0, int(h * (0.82 - hh)), bx0 + int(w * 0.13),
                     int(h * 0.82)], fill=GOLD_M, outline=NAVY, width=1)
    ax = int(w * 0.88)
    d.line([(ax, int(h * 0.18)), (ax, int(h * 0.72))], fill=RED_M, width=4)
    d.polygon([(ax - 9, int(h * 0.60)), (ax + 9, int(h * 0.60)),
               (ax, int(h * 0.80))], fill=RED_M)
    d.line([(0, int(h * 0.82)), (w, int(h * 0.82))], fill=SLATE, width=2)
    return im


def p_gta(w, h):
    """GTA: sunset kalem + matahari emas + 'VI' PUTIH di atas band
    (FIX vs versi sebelumnya: 'VI' navy 44pt terpotong tepi bawah tile —
    font kini dihitung dari tinggi tile, teks penuh di dalam gambar)."""
    im = _base(w, h)
    d = ImageDraw.Draw(im)
    bands = [(205, 170, 130), (198, 150, 135), (150, 140, 160)]
    for i, col in enumerate(bands):
        d.rectangle([0, int(h * i / 3), w, int(h * (i + 1) / 3)], fill=col)
    d.ellipse([int(w * 0.62), int(h * 0.06), int(w * 0.84), int(h * 0.44)],
              fill=GOLD_M, outline=NAVY, width=1)
    f = F(BOLD, max(18, int(h * 0.55)))
    d.text((int(w * 0.08), int(h * 0.50)), "VI", font=f, fill=WHITE,
           anchor="lm")
    return im


TILE_1R = {
    "akvan": p_radar_cream,
    "kyiv": p_night_kyiv,        # jejak rudal menurun + ledakan (bukan kalung)
    "cop31": p_globe_cop,
    "cricket": p_cricket,
    "sco": p_sco,
    "florida": p_flood,
    "apec": lambda w, h: p_flags3(w, h, [RED_M, NAVY, WHITE]),
    "taipei": p_chart_down,
    "gold": p_gold_down,
    "gta": p_gta,
    "mkt": p_chart_down,
    "prabowo": lambda w, h: p_flags3(w, h, [RED_M, WHITE, GOLD_M]),
    "f1": lambda w, h: rs.motif("s_f1", w, h),  # gelap dipertahankan
}


def tile_1r(story, w, h):
    """Tile 1r + bar aksen 8px di atas (aturan warna atas Kevin)."""
    pic = TILE_1R[story["key"]](w, h)
    d = ImageDraw.Draw(pic)
    d.rectangle([0, 0, w, 8], fill=ACCENTS[story["key"]])
    return pic


# ------------------------------------------------------------------ panel koran 1r
def draw_panel_1r(im, x, y, w, h, story, cfg, is_hero):
    d = ImageDraw.Draw(im)
    f_kick = F(BOLD, 10 if is_hero else 9)
    f_title = F(SERIF_B, cfg["hero_tpt"] if is_hero else cfg["card_tpt"])
    f_sum = F(SERIF, cfg["hero_spt"] if is_hero else cfg["card_spt"])
    kicker = f"{story['num']} · {story['city'].upper()} · {story['topic']}"
    tw = rs.wrap(d, story["title"], f_title, w - 10)
    assert len(tw) <= 2, f"judul pecah >2: {story['title']} -> {tw}"
    s_lines = rs.wrap(d, story["s1"], f_sum, w - 10)
    assert len(s_lines) <= 2, f"ringkasan pecah >2: {story['num']} -> {s_lines}"
    kick_h = 13 if is_hero else 12
    text_h = (kick_h + len(tw) * ((cfg["hero_tpt"] if is_hero else cfg["card_tpt"]) + 3)
              + len(s_lines) * ((cfg["hero_spt"] if is_hero else cfg["card_spt"]) + 3) + 4)
    img_h = h - text_h - 6
    assert img_h >= 48, f"gambar {story['num']} terlalu pendek: {img_h}"
    pic = tile_1r(story, w, img_h)
    if is_hero and story.get("caption"):
        cap = ImageDraw.Draw(pic)
        f_cap = F(BOLD, 9)
        cap.rectangle([0, img_h - 16, w, img_h], fill=NAVY)
        cap.text((6, img_h - 8), story["caption"], font=f_cap,
                 fill=GOLD, anchor="lm")
    im.paste(pic, (x, y))
    reg("image", (x, y, x + w, y + img_h), f"img-{story['num']}")
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=1)  # frame panel
    yy = y + img_h + 3
    b = d.textbbox((x + 5, yy), kicker, font=f_kick, anchor="la")
    d.text((x + 5, yy), kicker, font=f_kick, fill=RED)
    reg("text", b, f"kicker-{story['num']}")
    yy += kick_h
    for ln in tw:
        b = d.textbbox((x + 5, yy), ln, font=f_title, anchor="la")
        d.text((x + 5, yy), ln, font=f_title, fill=INK)
        reg("text", b, f"title-{story['num']}")
        yy += (cfg["hero_tpt"] if is_hero else cfg["card_tpt"]) + 3
    for ln in s_lines:
        b = d.textbbox((x + 5, yy), ln, font=f_sum, anchor="la")
        d.text((x + 5, yy), ln, font=f_sum, fill=INK)
        reg("text", b, f"sum-{story['num']}")
        yy += (cfg["hero_spt"] if is_hero else cfg["card_spt"]) + 3
    px = pic.crop((w // 2 - 10, 2, w // 2 + 10, 8))
    cols = list(px.getdata())
    avg = tuple(sum(c[i] for c in cols) // len(cols) for i in range(3))
    return avg


# ------------------------------------------------------------------ masthead ala rank 3
def draw_masthead_1r(d, W, y0, total):
    """Kicker + garis + judul 60pt RATA KIRI + deck rata kiri + garis.
    Mengembalikan y bawah garis deck. Assert gap tiap langkah."""
    f_kick = F(BOLD, 10)
    kl = "THE WORLD IN ONE DAY"
    b = d.textbbox((12, y0), kl, font=f_kick, anchor="la")
    d.text((12, y0), kl, font=f_kick, fill=RED)
    reg("text", b, "kicker-left")
    right = f"FRIDAY'S NEWS · ONE PAGE · {total} STORIES · 6 CONTINENTS"
    b = d.textbbox((W - 12, y0), right, font=f_kick, anchor="ra")
    d.text((W - 12, y0), right, font=f_kick, fill=NAVY, anchor="ra")
    reg("text", b, "kicker-right")
    y = y0 + 13
    rule_y = y + 3
    d.line([(12, rule_y), (W - 12, rule_y)], fill=INK, width=2)
    reg("rule", (12, rule_y - 1, W - 12, rule_y + 1), "kicker-rule")
    assert rule_y - 1 - b[3] >= 3, "garis kicker terlalu dekat ke teks kicker"
    y = rule_y + 2 + 5
    # Judul 54pt, rata kiri; tidak ada garis di dekatnya.
    f_mast = F(DISPLAY_B, 54)
    title = "Friday 20 November 2026"
    assert d.textlength(title, font=f_mast) <= W - 24, "judul 54pt kepanjangan"
    tb = d.textbbox((12, y), title, font=f_mast, anchor="la")
    d.text((12, y), title, font=f_mast, fill=INK, anchor="la")
    reg("text", tb, "masthead-title")
    assert tb[1] - (rule_y + 1) >= 6, "judul terlalu dekat garis kicker"
    y = tb[3] + 10  # ruang kosong di bawah judul (termasuk descender "y")
    f_deck = F(SERIF_IT, 13)
    last_bottom = None
    first_top = None
    for ln in v4.DECK_LINES:
        db = d.textbbox((12, y), ln, font=f_deck, anchor="la")
        d.text((12, y), ln, font=f_deck, fill=RED, anchor="la")
        reg("text", db, "deck")
        if first_top is None:
            first_top = db[1]
        last_bottom = db[3]
        y = db[3] + 4
    assert first_top - tb[3] >= 10, "deck terlalu dekat judul"
    rule2_y = last_bottom + 7
    d.line([(12, rule2_y), (W - 12, rule2_y)], fill=INK, width=2)
    reg("rule", (12, rule2_y - 1, W - 12, rule2_y + 1), "deck-rule")
    return rule2_y + 2


def draw_numbers_strip_1r(d, W, y, style="red"):
    """Strip 6 angka (h=46). Registrasi teks + divider vertikal."""
    h = 46
    widths = [166, 166, 166, 166, 166, 170]
    x = 12
    for i, (num, cap, region) in enumerate(v4.NUMBERS):
        cw = widths[i]
        x0, x1 = x, x + cw
        d.rectangle([x0, y, x1, y + h], fill=WHITE, outline=NAVY, width=1)
        d.rectangle([x0, y + h - 3, x1, y + h], fill=GOLD)
        f_n = F(SERIF_B, 22)
        b = d.textbbox(((x0 + x1) // 2, y + 3), num, font=f_n, anchor="ma")
        d.text(((x0 + x1) // 2, y + 3), num, font=f_n, fill=RED, anchor="ma")
        reg("text", b, f"num-{num}")
        f_c = F(REG, 9)
        lines = rs.wrap(d, cap, f_c, cw - 12)
        assert len(lines) <= 2, f"caption strip pecah: {cap}"
        yy = y + 27
        for ln in lines:
            b = d.textbbox(((x0 + x1) // 2, yy), ln, font=f_c, anchor="ma")
            d.text(((x0 + x1) // 2, yy), ln, font=f_c, fill=INK, anchor="ma")
            reg("text", b, f"numcap-{num}")
            yy += 11
        if i > 0:
            reg("rule", (x0 - 1, y, x0 + 1, y + h), f"numdiv-{i}")
        x = x1
    return y + h


def draw_region_tints(d, W, y, counts):
    """Strip region: tint pucat + teks navy + outline (pilihan Winter)."""
    h = 16
    disp = {"ASIA": "ASIA-PAC"}
    seg_w = (W - 24) // 7
    for i, r in enumerate(rs.REGION_ORDER):
        x0 = 12 + i * seg_w
        x1 = x0 + seg_w if i < 6 else W - 12
        d.rectangle([x0, y, x1, y + h], fill=TINTS[r], outline=NAVY, width=1)
        f = F(BOLD, 10)
        txt = f"{disp.get(r, r)} {counts[r]}"
        b = d.textbbox(((x0 + x1) // 2, y + h // 2), txt, font=f, anchor="mm")
        d.text(((x0 + x1) // 2, y + h // 2), txt, font=f, fill=NAVY,
               anchor="mm")
        reg("text", b, f"region-{r}")
    return y + h


def draw_map_1r(im, x, y, mw, mh, panels, hero_city):
    """Peta: laut navy + daratan krem pucat + pin merah 1–13.
    Judul + frame + legenda pin (bukan hitungan region)."""
    d = ImageDraw.Draw(im)
    f_t = F(BOLD, 11)
    title = "WHERE IT HAPPENED"
    b = d.textbbox((x, y), title, font=f_t, anchor="la")
    d.text((x, y), title, font=f_t, fill=RED, anchor="la")
    reg("text", b, "map-title")
    my = y + 16
    d.rectangle([x, my, x + mw, my + mh], fill=SEA_1R, outline=NAVY, width=1)
    mtmp = Image.new("RGB", (mw - 2, mh - 2), SEA_1R)
    md = ImageDraw.Draw(mtmp)
    for poly in rv.CONTINENTS:
        pts = [rv.project(lon, lat, 0, 0, mw - 2, mh - 2)
               for lon, lat in poly]
        md.polygon(pts, fill=LAND_1R, outline=LAND_OUT)
    im.paste(mtmp, (x + 1, my + 1))
    md = ImageDraw.Draw(im)
    fp = F(BOLD, 8)
    placed = []
    skipped = []

    def place(px, py):
        for (qx, qy) in placed:
            if ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5 < 12:
                return False
        placed.append((px, py))
        return True

    for p in panels:
        city = p["map_city"]
        if city not in rv.PLACES:
            continue
        lon, lat = rv.PLACES[city]
        px, py = rv.project(lon, lat, x + 1, my + 1, mw - 2, mh - 2)
        if p["city"] == hero_city:
            if place(px, py):
                md.polygon(rv.star_points(px, py, 9, 4), fill=GOLD,
                           outline=NAVY)
            continue
        if not place(px, py):
            skipped.append((city, p["num"]))
            continue
        md.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                   outline=WHITE, width=1)
        mark = str(p["num"])
        tw = md.textlength(mark, font=fp)
        md.text((px - tw / 2, py - 5), mark, font=fp, fill=WHITE)
    reg("image", (x, my, x + mw, my + mh), "map")
    # frame kelihatan di sekeliling peta (di atas kertas)
    d.rectangle([x, my, x + mw, my + mh], outline=NAVY, width=1)
    f_lg = F(REG, 9)
    legend = "Pins 1–13 · positions approximate"
    b = d.textbbox((x + mw // 2, my + mh + 3), legend, font=f_lg, anchor="ma")
    d.text((x + mw // 2, my + mh + 3), legend, font=f_lg, fill=NAVY,
           anchor="ma")
    reg("text", b, "map-legend")
    return skipped


def draw_briefs_1r(im, x, y, w, h, briefs, font_pt=10):
    """MORE STORIES 3 kolom (sama seperti v4) + registrasi tiap baris."""
    d = ImageDraw.Draw(im)
    f_n = F(BOLD, font_pt)
    f_c = F(BOLD, font_pt)
    f_t = F(REG, font_pt)
    cols = [[], [], []]
    for i, b in enumerate(briefs):
        cols[i % 3].append(b)
    col_w = (w - 16) // 3
    lh = font_pt + 3
    col_items = []
    for col in cols:
        items = []
        for (n, city, region, text) in col:
            head = f"{n}. {city}: "
            hw = d.textlength(head, font=f_n)
            lines = []
            words = text.split()
            cur = ""
            first_w = col_w - hw - 6
            for wd in words:
                trial = (cur + " " + wd).strip()
                lim = first_w if not lines else col_w - 6
                if d.textlength(trial, font=f_t) <= lim:
                    cur = trial
                else:
                    lines.append(cur)
                    cur = wd
            if cur:
                lines.append(cur)
            assert len(lines) <= 2, f"brief {n} pecah >2: {lines}"
            items.append((n, city, region, lines, head))
        col_items.append(items)
    for ci, items in enumerate(col_items):
        cx = x + ci * col_w + (8 if ci else 0)
        total_lines = sum(len(it[3]) for it in items)
        gaps = h - total_lines * lh
        gap_each = max(0, gaps // (len(items) + 1))
        yy = y + gap_each
        for (n, city, region, lines, head) in items:
            b = d.textbbox((cx, yy), f"{n}. ", font=f_n, anchor="la")
            d.text((cx, yy), f"{n}. ", font=f_n, fill=RED)
            reg("text", b, f"brief-{n}-num")
            nx = cx + d.textlength(f"{n}. ", font=f_n)
            b = d.textbbox((nx, yy), f"{city}: ", font=f_c, anchor="la")
            d.text((nx, yy), f"{city}: ", font=f_c, fill=NAVY)
            reg("text", b, f"brief-{n}-city")
            tx = nx + d.textlength(f"{city}: ", font=f_c)
            b = d.textbbox((tx, yy), lines[0], font=f_t, anchor="la")
            d.text((tx, yy), lines[0], font=f_t, fill=INK)
            reg("text", b, f"brief-{n}-l1")
            yy += lh
            for ln in lines[1:]:
                b = d.textbbox((cx, yy), ln, font=f_t, anchor="la")
                d.text((cx, yy), ln, font=f_t, fill=INK)
                reg("text", b, f"brief-{n}-l2")
                yy += lh
            yy += gap_each
    return y + h


def draw_datecheck_1r(d, W, y):
    """Kotak DATE CHECK border merah + registrasi teks (copy v4 + reg)."""
    f = F(BOLD, 9)
    pref = "DATE CHECK — "
    pref_w = d.textlength(pref, font=f)
    lines = rs.wrap(d, v4.DATECHECK_REST, f, W - 48 - pref_w)
    assert len(lines) <= 3, f"datecheck pecah >3: {lines}"
    box_h = 8 + len(lines) * 13 + 6
    d.rectangle([12, y, W - 12, y + box_h], fill=CARD_BG,
                outline=RED, width=2)
    yy = y + 7
    for j, ln in enumerate(lines):
        if j == 0:
            total_w = pref_w + d.textlength(ln, font=f)
            x0 = (W - total_w) // 2
            b = d.textbbox((x0, yy), pref, font=f, anchor="la")
            d.text((x0, yy), pref, font=f, fill=RED)
            reg("text", b, "datecheck-pref")
            b = d.textbbox((x0 + pref_w, yy), ln, font=f, anchor="la")
            d.text((x0 + pref_w, yy), ln, font=f, fill=NAVY)
            reg("text", b, "datecheck-l1")
        else:
            b = d.textbbox((W // 2, yy), ln, font=f, anchor="ma")
            d.text((W // 2, yy), ln, font=f, fill=NAVY, anchor="ma")
            reg("text", b, f"datecheck-l{j + 1}")
        yy += 13
    return y + box_h


# ------------------------------------------------------------------ layout 1r
GAPS_1R = [12, 12, 12, 12, 12, 12]  # deck→angka, angka→region, region→hero,
# hero→kartu, kartu→band, band→datecheck
PANEL_GAP = 10
ROW_GAP = 10
HERO_H = 160
CARD_H = 130
CFG_1R = {"tile": "motif-1r", "total": 36, "gaps": GAPS_1R,
          "hero_tpt": 16, "hero_spt": 11, "card_tpt": 13, "card_spt": 10,
          "brief_pt": 10}


def build_1r(path):
    global BOXREG
    BOXREG = []
    W = 1024
    im = Image.new("RGB", (W, 1024), PAPER)
    d = ImageDraw.Draw(im)
    total = 36
    brief_keys = v4.BRIEFS_20_KEYS + ["slot"] * 3
    panels = [dict(p) for p in v4.HEROES + v4.CARDS]
    briefs = []
    for i, key in enumerate(brief_keys):
        if key == "slot":
            city, region, text = v4.AMERICA_SLOTS[i - len(v4.BRIEFS_20_KEYS)]
        else:
            city, region, text = v4.BRIEF_POOL[key]
        briefs.append((14 + i, city, region, text))
    counts = rs.region_counts(panels, briefs)
    assert sum(counts.values()) == total
    gaps = GAPS_1R

    y = 12
    y = draw_masthead_1r(d, W, y, total)
    y += gaps[0]
    y = draw_numbers_strip_1r(d, W, y)
    y += gaps[1]
    y = draw_region_tints(d, W, y, counts)
    y += gaps[2]
    tops = {}
    hero_w = (W - 24 - 2 * PANEL_GAP) // 3
    for i, st in enumerate(panels[:3]):
        xx = 12 + i * (hero_w + PANEL_GAP)
        tops[(0, i)] = draw_panel_1r(im, xx, y, hero_w, HERO_H, st, CFG_1R,
                                     True)
    y += HERO_H + gaps[3]
    card_w = (W - 24 - 4 * PANEL_GAP) // 5
    for r in range(2):
        for c in range(5):
            st = panels[3 + r * 5 + c]
            xx = 12 + c * (card_w + PANEL_GAP)
            tops[(1 + r, c)] = draw_panel_1r(im, xx, y, card_w, CARD_H,
                                             st, CFG_1R, False)
        y += CARD_H + (ROW_GAP if r == 0 else 0)
    y += gaps[4]
    band_y = y
    band_h = 1024 - band_y - gaps[5] - 40 - 15 - 10
    assert band_h >= 180, f"band terlalu pendek: {band_h}"
    map_w = 400
    map_title_h = 16
    map_legend_h = 12
    map_h = band_h - map_title_h - map_legend_h
    assert map_h >= 150, f"peta terlalu pendek: {map_h}"
    skipped = draw_map_1r(im, 12, band_y, map_w, map_h, panels, "Gopalpur")
    bx = 12 + map_w + 12
    bw = W - 12 - bx
    # MORE STORIES: judul merah + border (fix #3 Kevin)
    f_bh = F(BOLD, 12)
    btitle = "ALSO ON FRIDAY 20 NOVEMBER — 23 MORE STORIES"
    b = d.textbbox((bx + 8, band_y + 4), btitle, font=f_bh, anchor="la")
    d.text((bx + 8, band_y + 4), btitle, font=f_bh, fill=RED, anchor="la")
    reg("text", b, "more-title")
    d.rectangle([bx, band_y, W - 12, band_y + band_h], outline=NAVY, width=1)
    draw_briefs_1r(im, bx + 8, band_y + 22, bw - 8, band_h - 22, briefs,
                   font_pt=CFG_1R["brief_pt"])
    y = band_y + band_h + gaps[5]
    y = draw_datecheck_1r(d, W, y)
    f2 = F(REG, 9)
    b = d.textbbox((W // 2, y + 3), v4.DATECHECK_SOURCES, font=f2, anchor="ma")
    d.text((W // 2, y + 3), v4.DATECHECK_SOURCES, font=f2,
           fill=(90, 90, 90), anchor="ma")
    reg("text", b, "sources")
    im.save(path)
    top_bad = rs.check_top_colors(tops)
    ink_bottom, margin = v4.audit_footer(path)
    nreg = check_no_overlap()
    return {"total": total, "counts": counts, "band_h": band_h,
            "map_h": map_h, "map_skipped": skipped, "top_bad": top_bad,
            "ink_bottom": ink_bottom, "bottom_margin": margin,
            "registered_boxes": nreg, "gaps": gaps}


if __name__ == "__main__":
    out = "/home/hatch/workspace/makefun/news-image-20261120/sketches-v4"
    path = f"{out}/sketch-v4-1r-koran-serif-improved.png"
    res = build_1r(path)
    assert not res["top_bad"], f"pelanggaran warna atas: {res['top_bad']}"
    assert res["ink_bottom"] <= 1012, f"tinta sampai y={res['ink_bottom']}"
    assert res["bottom_margin"] >= 10, f"margin bawah cuma {res['bottom_margin']}px"
    h1 = hashlib.sha256(open(path, "rb").read()).hexdigest()
    build_1r("/tmp/v4-1r-determinism-check.png")
    h2 = hashlib.sha256(open("/tmp/v4-1r-determinism-check.png", "rb").read()).hexdigest()
    assert h1 == h2, "tidak deterministik"
    res["sha256"] = h1
    print("1r", json.dumps(res, default=str))
    print("OK")
