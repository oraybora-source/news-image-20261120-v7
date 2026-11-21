#!/usr/bin/env python3
"""SKETSA v4-1r4 news-image-20261120 — revisi sketsa 1r3 dari koreksi Kevin.

Koreksi Kevin 19:09 WIB (sambil melihat sketsa 1r3): "Masih belum di hapus
ya win footer setiap gambar" — yang dimaksud BUKAN footer halaman (DATE
CHECK tipis + Sources sudah dihapus di 1r3), melainkan strip/band di
BAWAH tiap gambar hero/kartu, dan itu MASIH ADA di 1r3:
- Hero 1-3: strip navy 16px di bawah gambar berisi caption emas
  ("LANDFALL 07:30 IST · 300,000 EVACUATED", "STRIKES FROM 01:25 ·
  BLASTS HEARD", "FINAL TEXT DUE MIDNIGHT") — dicek parent di 2x.
- Kartu 4: band sage di bawah gambar kriket (lapangan sage 45% bawah
  tile; konten gambar hanya di 55% atas tile) — dicek parent di 2x.

Perbaikan 1r4:
- Hero: strip caption DIHAPUS (blok caption di draw_panel_1r). Info
  strip SUDAH ADA di ringkasan tiap hero (dicek satu per satu di bawah),
  jadi tidak ada yang hilang dan tidak dipindahkan ke mana-mana. Gambar
  hero mengisi penuh tile (scene 77px penuh, bukan 61px + strip 16px).
- Kartu: audit 10 tile kartu — HANYA kartu 4 (kriket) yang punya band
  bawah berupa bidang warna kosong (konten hanya di 55% atas tile).
  Tile lain kontennya sudah memenuhi penuh tile dan bagian bawahnya
  adalah ISI cerita, bukan footer: Florida (air banjir + ombak),
  F1 (aspal + garis start + garis kecepatan), GTA (sunset = seluruh
  gambar), SCO/flags (meja = alas bendera), chart/gold (garis/batang
  memenuhi tile), Kyiv (skyline), COP31 (termometer). Kriket digambar
  ulang: tanpa lapangan sage; bat + bola + stumps diperbesar mengisi
  penuh tile + garis tanah tipis 2px di 0.90h (GARIS, bukan band — sama
  seperti ground line SCO / baseline Gold yang sudah ada).
- Bar aksen 8px di ATAS tiap tile TETAP ADA (aturan warna-atas Kevin).
- Yang TIDAK berubah: masthead hitam seragam 72pt satu baris; DATE
  CHECK tipis 2 baris; TANPA baris Sources; chip "WHERE IT HAPPENED"
  menyatu dengan border peta; peta navy + pin merah 13; MORE STORIES
  bertitle + berborder; layout 3 hero + 10 kartu 2x5; slot 34-36
  placeholder; anggaran vertikal sama dengan 1r3 (hero 166, kartu 130,
  gap 12, band 240).

Info caption hero vs ringkasan (tidak ada yang hilang):
- Hero 1 "LANDFALL 07:30 IST · 300,000 EVACUATED" -> ringkasan
  "Landfall 07:30 IST, gusts to 90 km/h. 300,000 evacuated to shelters."
- Hero 2 "STRIKES FROM 01:25 · BLASTS HEARD" -> ringkasan "Missiles
  strike the capital from 01:25. Blasts heard across the city."
- Hero 3 "FINAL TEXT DUE MIDNIGHT" -> ringkasan "Draft omits phase-out
  wording; final text due midnight."

Dasar: render_v4_1r3.py (masthead, peta, datecheck, strip region,
brief dipakai ulang apa adanya; isi cerita TIDAK diubah; slot 34-36
tetap placeholder).
Analisis + catatan revisi: sketches-v4/analisis-improve-sketsa1.md (§6 Revisi 1r4)
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
import render_v4_1r as r1
import render_v4_1r3 as r3

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


# ------------------------------------------------------------------ tile kriket 1r4
def p_cricket_1r4(w, h):
    """Kriket 1r4: TANPA lapangan sage (band bawah dihapus — koreksi Kevin
    19:09 WIB). Dulu: lapangan sage 45% bawah tile, konten (bat/bola/
    stumps) hanya di 55% atas — terbaca sebagai footer. Sekarang: latar
    krem penuh; bat + bola + stumps diperbesar mengisi penuh tile; garis
    tanah tipis 2px di 0.90h (GARIS, bukan band — sama seperti ground line
    SCO / baseline Gold). Bar aksen 8px di atas tile ditambahkan oleh
    tile_1r4, jadi gambar mulai di bawah 8px (bat atas di 0.16h)."""
    im = r1._base(w, h)
    d = ImageDraw.Draw(im)
    # garis tanah tipis (2px) — stumps + bat berdiri di atasnya
    gy = int(h * 0.90)
    d.line([(0, gy), (w, gy)], fill=NAVY, width=2)
    # bat coklat diagonal, diperbesar: dari 0.16h sampai 0.88h
    d.polygon([(int(w * 0.30), int(h * 0.16)), (int(w * 0.36), int(h * 0.20)),
               (int(w * 0.58), int(h * 0.88)), (int(w * 0.52), int(h * 0.90))],
              fill=(150, 110, 70), outline=NAVY)
    # bola merah, diperbesar
    d.ellipse([int(w * 0.64), int(h * 0.22), int(w * 0.74), int(h * 0.38)],
              fill=r1.RED_M, outline=NAVY, width=1)
    # stumps emas, diperpanjang sampai garis tanah
    for i in range(3):
        sx = int(w * (0.80 + i * 0.05))
        d.rectangle([sx, int(h * 0.32), sx + 4, int(h * 0.90)],
                    fill=r1.GOLD_M, outline=NAVY, width=1)
    # bails di atas stumps
    d.rectangle([int(w * 0.80), int(h * 0.295), int(w * 0.90) + 4,
                 int(h * 0.32)], fill=r1.GOLD_M, outline=NAVY, width=1)
    return im


TILE_1R4 = dict(r1.TILE_1R)
TILE_1R4["cricket"] = p_cricket_1r4


def tile_1r4(story, w, h):
    """Tile 1r4 + bar aksen 8px di atas (aturan warna atas Kevin) — sama
    seperti r1.tile_1r, hanya painter kriket yang diganti (tanpa band
    sage bawah)."""
    pic = TILE_1R4[story["key"]](w, h)
    d = ImageDraw.Draw(pic)
    d.rectangle([0, 0, w, 8], fill=r1.ACCENTS[story["key"]])
    return pic


# ------------------------------------------------------------------ panel 1r4
def draw_panel_1r4(im, x, y, w, h, story, cfg, is_hero):
    """Sama persis dengan r1.draw_panel_1r, KECUALI: blok strip caption
    hero DIHAPUS (koreksi Kevin 19:09 WIB — strip navy 16px di bawah
    gambar hero adalah footer; info caption sudah ada di ringkasan).
    Gambar mengisi penuh tile (hero: scene 77px penuh; kartu: 50px).
    Registrasi kotak + sampling warna atas identik dengan 1r."""
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
    pic = tile_1r4(story, w, img_h)
    # 1r4: TIDAK ADA strip caption hero di bawah gambar — dihapus.
    # (Dulu di sini: rectangle navy 16px + teks caption emas.)
    im.paste(pic, (x, y))
    r1.reg("image", (x, y, x + w, y + img_h), f"img-{story['num']}")
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=1)  # frame panel
    yy = y + img_h + 3
    b = d.textbbox((x + 5, yy), kicker, font=f_kick, anchor="la")
    d.text((x + 5, yy), kicker, font=f_kick, fill=RED)
    r1.reg("text", b, f"kicker-{story['num']}")
    yy += kick_h
    for ln in tw:
        b = d.textbbox((x + 5, yy), ln, font=f_title, anchor="la")
        d.text((x + 5, yy), ln, font=f_title, fill=INK)
        r1.reg("text", b, f"title-{story['num']}")
        yy += (cfg["hero_tpt"] if is_hero else cfg["card_tpt"]) + 3
    for ln in s_lines:
        b = d.textbbox((x + 5, yy), ln, font=f_sum, anchor="la")
        d.text((x + 5, yy), ln, font=f_sum, fill=INK)
        r1.reg("text", b, f"sum-{story['num']}")
        yy += (cfg["hero_spt"] if is_hero else cfg["card_spt"]) + 3
    px = pic.crop((w // 2 - 10, 2, w // 2 + 10, 8))
    cols = list(px.getdata())
    avg = tuple(sum(c[i] for c in cols) // len(cols) for i in range(3))
    return avg


# ------------------------------------------------------------------ layout 1r4
def build_1r4(path):
    """Sama dengan r3.build_1r3, hanya draw_panel_1r -> draw_panel_1r4
    (tanpa strip caption hero + kriket tanpa band sage). Anggaran
    vertikal, masthead, peta, brief, DATE CHECK tipis: identik 1r3."""
    r1.BOXREG = []
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
    gaps = r3.GAPS_1R3
    CFG = r1.CFG_1R

    y = 12  # margin atas 1r3
    y = r3.draw_masthead_1r3(d, W, y, total)
    y += gaps[0]
    y = r1.draw_numbers_strip_1r(d, W, y)
    y += gaps[1]
    y = r3.draw_region_tints_1r3(d, W, y, counts)
    y += gaps[2]
    tops = {}
    hero_w = (W - 24 - 2 * r1.PANEL_GAP) // 3
    for i, st in enumerate(panels[:3]):
        xx = 12 + i * (hero_w + r1.PANEL_GAP)
        tops[(0, i)] = draw_panel_1r4(im, xx, y, hero_w, r3.HERO_H_1R3, st,
                                      CFG, True)
    y += r3.HERO_H_1R3 + gaps[3]
    card_w = (W - 24 - 4 * r1.PANEL_GAP) // 5
    for rr in range(2):
        for c in range(5):
            st = panels[3 + rr * 5 + c]
            xx = 12 + c * (card_w + r1.PANEL_GAP)
            tops[(1 + rr, c)] = draw_panel_1r4(im, xx, y, card_w,
                                              r3.CARD_H_1R3, st, CFG, False)
        y += r3.CARD_H_1R3 + (r1.ROW_GAP if rr == 0 else 0)
    y += gaps[4]
    band_y = y
    band_h = 1024 - band_y - gaps[5] - 32 - 12
    assert band_h >= 239, f"band terlalu pendek: {band_h} (briefs butuh >=239)"
    map_w = 400
    map_legend_h = 12
    map_h = band_h - map_legend_h
    assert map_h >= 150, f"peta terlalu pendek: {map_h}"
    skipped = r3.draw_map_1r3(im, 12, band_y, map_w, map_h, panels, "Gopalpur")
    bx = 12 + map_w + 12
    bw = W - 12 - bx
    f_bh = F(BOLD, 12)
    btitle = "ALSO ON FRIDAY 20 NOVEMBER — 23 MORE STORIES"
    b = d.textbbox((bx + 8, band_y + 4), btitle, font=f_bh, anchor="la")
    d.text((bx + 8, band_y + 4), btitle, font=f_bh, fill=RED, anchor="la")
    r1.reg("text", b, "more-title")
    d.rectangle([bx, band_y, W - 12, band_y + band_h], outline=NAVY, width=1)
    r1.draw_briefs_1r(im, bx + 8, band_y + 22, bw - 8, band_h - 22, briefs,
                      font_pt=CFG["brief_pt"])
    y = band_y + band_h + gaps[5]
    y = r3.draw_datecheck_thin_1r3(d, W, y)
    # Baris Sources tetap DIHAPUS (keputusan Kevin 19:03 WIB).
    im.save(path)
    top_bad = rs.check_top_colors(tops)
    ink_bottom, margin = v4.audit_footer(path)
    nreg = r3.check_no_overlap_1r3()
    return {"total": total, "counts": counts, "band_h": band_h,
            "map_h": map_h, "map_skipped": skipped, "top_bad": top_bad,
            "ink_bottom": ink_bottom, "bottom_margin": margin,
            "registered_boxes": nreg, "gaps": gaps}


if __name__ == "__main__":
    out = "/home/hatch/workspace/makefun/news-image-20261120/sketches-v4"
    path = f"{out}/sketch-v4-1r4-koran-serif-revised.png"
    res = build_1r4(path)
    assert not res["top_bad"], f"pelanggaran warna atas: {res['top_bad']}"
    assert res["ink_bottom"] <= 1012, f"tinta sampai y={res['ink_bottom']}"
    assert res["bottom_margin"] >= 10, f"margin bawah cuma {res['bottom_margin']}px"
    h1 = hashlib.sha256(open(path, "rb").read()).hexdigest()
    build_1r4("/tmp/v4-1r4-determinism-check.png")
    h2 = hashlib.sha256(open("/tmp/v4-1r4-determinism-check.png", "rb").read()).hexdigest()
    assert h1 == h2, "tidak deterministik"
    res["sha256"] = h1
    res["measure_1r4"] = r3.measure(path)
    res["measure_1r3"] = r3.measure(f"{out}/sketch-v4-1r3-koran-serif-revised.png")
    print("1r4", json.dumps(res, default=str))
    print("OK")
