#!/usr/bin/env python3
"""SKETSA v4-1r3 news-image-20261120 — revisi sketsa 1r2 dari feedback Kevin.

Perintah Kevin 19:01 WIB (sambil melihat sketsa 1r2): "Malah nambah jelek
Win, coba kamu cek deh rank 1-3. Seolah olah ketika buka itu tertuju pada
title nya" — "Friday" MERAH di 1r2 DITOLAK. Pelajaran yang mengikat: mata
tertuju ke title harus terjadi SECARA NATURAL — lewat UKURAN + BOBOT +
RUANG, bukan warna. Ketiga rank teratas (dicek parent di 3x) judulnya
HITAM seragam, satu baris, elemen terbesar di halaman, dikelilingi ruang
kosong: rank 1 hitam tengah besar + ruang; rank 2 hitam rata kiri
RAKSASA selebar halaman; rank 3 hitam bold rata kiri besar + garis
berjarak. Warna merah pada judul = berteriak = JELEK. Jangan pernah lagi
membuat judul berwarna.

Perbaikan 1r3 (HANYA masthead + footer yang berubah; sisanya dari 1r2
dipertahankan): judul "Friday 20 November 2026" HITAM, SERAGAM satu
ukuran + satu bobot (Display Bold), SATU BARIS, RATA KIRI (arah rank 3),
72pt — ukuran terbesar dalam rentang tugas (~64-72pt) yang muat satu
baris (910px dari 1000px; 76pt = 961px sempat dicoba tapi anggaran
vertikal tidak muat bersama hero 166 + gap 12 + band_h 239). Ruang
kosong jelas di atas judul (10px di bawah garis kicker) dan di bawah
judul (12px di atas deck). Deck jadi 1 BARIS merah italic 13pt (seperti
rank 1; 132 karakter = 800px, muat) — membebaskan ~16px untuk hero
yang lebih tinggi. Aksen merah HANYA di kicker/deck, seperti rank 1-3.
Keputusan footer Kevin 19:03 WIB: DATE CHECK TIPIS (kotak 32px, 2
baris, padding ketat; daftar buangan lengkap dipertahankan) + baris
Sources DIHAPUS sepenuhnya. Anggaran vertikal: hero 166 (gambar 77px),
kartu 130 (gambar 50px), gap 12px, strip region 16px, margin atas 12px
— semuanya ukuran 1r, PLUS hero lebih tinggi dari 1r.

Dipertahankan dari 1r2 (sudah disetujui arahnya): chip "WHERE IT
HAPPENED" menyatu dengan border peta, peta navy + pin merah 13, MORE
STORIES bertitle + berborder, palet kalem, layout 3 hero + 10 kartu 2x5,
slot 34-36 placeholder. Chip peta SATU-SATUNYA pasangan yang sengaja
dibiarkan bersinggungan dengan kotak peta (whitelist eksplisit di
check_no_overlap_1r3 — perintah Kevin, bukan kecelakaan).

Dasar: render_v4_1r2.py (panel, strip, brief, datecheck, tile, peta
dipakai ulang apa adanya; isi cerita TIDAK diubah; slot 34-36 tetap
placeholder).
Analisis + catatan revisi: sketches-v4/analisis-improve-sketsa1.md (§5 Revisi 1r3)
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

# Pasangan yang SENGAJA bersinggungan (perintah Kevin 18:54 WIB):
# chip judul peta menembus border atas peta — judul + peta satu kesatuan.
ALLOW_OVERLAP = {frozenset(("map-title", "map"))}


def check_no_overlap_1r3():
    """Sama seperti r1.check_no_overlap + whitelist eksplisit 1 pasangan.

    Whitelist HANYA berlaku untuk (map-title, map): chip judul yang
    menembus border atas peta. Pasangan lain tetap dilarang keras."""
    bad = []
    for i, (k1, b1, l1) in enumerate(r1.BOXREG):
        for k2, b2, l2 in r1.BOXREG[i + 1:]:
            if not r1._overlap(b1, b2):
                continue
            pair = {k1, k2}
            if pair <= {"text", "rule"} or pair == {"text"} or pair == {"text", "image"}:
                if frozenset((l1, l2)) in ALLOW_OVERLAP:
                    continue
                bad.append((l1, l2, k1, k2))
    assert not bad, f"OVERLAP (aturan keras Kevin): {bad}"
    return len(r1.BOXREG)


# ------------------------------------------------------------------ masthead 1r3
def draw_masthead_1r3(d, W, y0, total):
    """Kicker + garis + judul HITAM SERAGAM satu baris + deck + garis.

    Pelajaran Kevin 19:01 WIB (menolak 1r2): "Friday" MERAH malah nambah
    jelek — mata tertuju ke title harus terjadi SECARA NATURAL lewat
    UKURAN + BOBOT + RUANG, bukan warna. Ketiga rank teratas judulnya
    HITAM seragam, satu baris, elemen terbesar di halaman, dikelilingi
    ruang kosong. Warna merah pada judul = berteriak = JELEK. Jangan
    pernah lagi membuat judul berwarna.

    Judul 1r3: "Friday 20 November 2026" HITAM, SERAGAM satu ukuran +
    satu bobot (Display Bold), SATU BARIS, RATA KIRI (arah rank 3),
    76pt — ukuran terbesar yang muat satu baris (961px dari 1000px yang
    tersedia, hampir selebar halaman seperti rank 2). Ruang kosong jelas
    di atas judul (di bawah garis kicker) dan di bawah judul (di atas
    deck) — judul "bernapas" seperti rank 1. Aksen merah HANYA di
    kicker/deck, seperti rank 1-3. Tidak ada garis di dekat judul.
    Mengembalikan y bawah garis deck."""
    f_kick = F(BOLD, 10)
    kl = "THE WORLD IN ONE DAY"
    b = d.textbbox((12, y0), kl, font=f_kick, anchor="la")
    d.text((12, y0), kl, font=f_kick, fill=RED)
    r1.reg("text", b, "kicker-left")
    right = f"FRIDAY'S NEWS · ONE PAGE · {total} STORIES · 6 CONTINENTS"
    b = d.textbbox((W - 12, y0), right, font=f_kick, anchor="ra")
    d.text((W - 12, y0), right, font=f_kick, fill=NAVY, anchor="ra")
    r1.reg("text", b, "kicker-right")
    y = y0 + 13
    rule_y = y + 3
    d.line([(12, rule_y), (W - 12, rule_y)], fill=INK, width=2)
    r1.reg("rule", (12, rule_y - 1, W - 12, rule_y + 1), "kicker-rule")
    assert rule_y - 1 - b[3] >= 3, "garis kicker terlalu dekat ke teks kicker"

    # --- Judul HITAM seragam, satu baris, rata kiri, 72pt ---
    # Ukuran dipilih terukur (rentang tugas ~64-72pt): 72pt = 910px
    # (maks 1000px); 76pt = 961px sempat dicoba tapi anggaran vertikal
    # tidak muat bersama hero 166 + gap 12 + band_h 239 — 72pt tetap
    # elemen terbesar di halaman dan hampir selebar halaman. Satu ukuran
    # + satu bobot + satu warna (INK) untuk seluruh baris — tidak ada
    # kata yang dibedakan. Baseline dihitung dari metrik font, bukan tebak.
    f_title = F(DISPLAY_B, 72)
    title = "Friday 20 November 2026"
    title_w = d.textlength(title, font=f_title)
    assert title_w <= W - 24, f"judul 1r3 kepanjangan: {title_w}"
    assert title_w >= 850, f"judul 1r3 kurang selebar halaman: {title_w}"
    asc, _desc = f_title.getmetrics()
    baseline = rule_y + 1 + 10 + asc  # 10px ruang kosong di atas judul
    tb = d.textbbox((12, baseline), title, font=f_title, anchor="ls")
    d.text((12, baseline), title, font=f_title, fill=INK, anchor="ls")
    r1.reg("text", tb, "masthead-title")
    assert tb[1] - (rule_y + 1) >= 10, "judul terlalu dekat garis kicker"
    title_bottom = tb[3]

    y = title_bottom + 12  # ruang kosong di bawah judul (termasuk "y")
    # Deck 1 BARIS (bukan 2 seperti 1r/1r2) — seperti rank 1: 5 berita
    # terbesar dalam satu baris merah italic. Diukur: 132 karakter =
    # 800px pada 13pt (maks 1000px), jadi font tetap 13pt. Satu baris
    # membebaskan ~16px untuk hero yang lebih tinggi (keputusan footer
    # Kevin 19:03 WIB: ruang bebas dipakai untuk gambar lebih tinggi).
    f_deck = F(SERIF_IT, 13)
    deck_line = " · ".join(v4.DECK_LINES)
    dbx = d.textbbox((12, y), deck_line, font=f_deck, anchor="la")
    d.text((12, y), deck_line, font=f_deck, fill=RED, anchor="la")
    r1.reg("text", dbx, "deck")
    assert dbx[1] - title_bottom >= 12, "deck terlalu dekat judul"
    last_bottom = dbx[3]
    rule2_y = last_bottom + 6
    d.line([(12, rule2_y), (W - 12, rule2_y)], fill=INK, width=2)
    r1.reg("rule", (12, rule2_y - 1, W - 12, rule2_y + 1), "deck-rule")
    return rule2_y + 2


# ------------------------------------------------------------------ peta 1r3
def draw_map_1r3(im, x, y, mw, mh, panels, hero_city):
    """Peta: laut navy + daratan krem pucat + pin merah 1-13.

    Judul "WHERE IT HAPPENED" MENYATU dengan peta: chip PAPER berteks
    merah tebal + outline navy yang MENEMBUS garis border atas (gaya
    legend) — judul + frame satu kesatuan (perintah Kevin 18:54 WIB).
    Legenda pin tetap di bawah peta."""
    d = ImageDraw.Draw(im)
    d.rectangle([x, y, x + mw, y + mh], fill=r1.SEA_1R, outline=NAVY, width=1)
    mtmp = Image.new("RGB", (mw - 2, mh - 2), r1.SEA_1R)
    md = ImageDraw.Draw(mtmp)
    for poly in rv.CONTINENTS:
        pts = [rv.project(lon, lat, 0, 0, mw - 2, mh - 2)
               for lon, lat in poly]
        md.polygon(pts, fill=r1.LAND_1R, outline=r1.LAND_OUT)
    im.paste(mtmp, (x + 1, y + 1))
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
        px, py = rv.project(lon, lat, x + 1, y + 1, mw - 2, mh - 2)
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
    r1.reg("image", (x, y, x + mw, y + mh), "map")
    d.rectangle([x, y, x + mw, y + mh], outline=NAVY, width=1)

    # --- Chip judul menembus border atas (perintah Kevin) ---
    f_t = F(BOLD, 11)
    title = "WHERE IT HAPPENED"
    tw = d.textlength(title, font=f_t)
    chip_w = int(tw) + 16
    chip_h = 16
    cx0, cy0 = x + 10, y - chip_h // 2
    cx1, cy1 = cx0 + chip_w, y + chip_h // 2
    d.rectangle([cx0, cy0, cx1, cy1], fill=PAPER, outline=NAVY, width=1)
    tb = d.textbbox(((cx0 + cx1) // 2, (cy0 + cy1) // 2), title, font=f_t,
                    anchor="mm")
    d.text(((cx0 + cx1) // 2, (cy0 + cy1) // 2), title, font=f_t, fill=RED,
           anchor="mm")
    r1.reg("text", tb, "map-title")
    # Chip menembus border atas: teksnya bersinggungan dengan kotak peta
    # — SATU-SATUNYA pasangan yang di-whitelist (lihat ALLOW_OVERLAP).

    f_lg = F(REG, 9)
    legend = "Pins 1–13 · positions approximate"
    b = d.textbbox((x + mw // 2, y + mh + 3), legend, font=f_lg, anchor="ma")
    d.text((x + mw // 2, y + mh + 3), legend, font=f_lg, fill=NAVY,
           anchor="ma")
    r1.reg("text", b, "map-legend")
    return skipped


# ------------------------------------------------------------------ layout 1r3
GAPS_1R3 = [12, 12, 12, 12, 12, 12]  # 1r: kembali dari 10 (masthead 1r3 hanya +6px vs 1r2)
HERO_H_1R3 = 166  # 1r 160 -> 166: LEBIH TINGGI (keputusan footer Kevin 19:03 WIB; gambar hero 77px vs 71px di 1r, 56px di 1r2)
CARD_H_1R3 = 130  # 1r: kembali dari 128


def draw_region_tints_1r3(d, W, y, counts):
    """Strip region 16px (1r) — dikembalikan dari 14px (1r3)."""
    h = 16  # 1r: kembali dari 14
    disp = {"ASIA": "ASIA-PAC"}
    seg_w = (W - 24) // 7
    for i, r in enumerate(rs.REGION_ORDER):
        x0 = 12 + i * seg_w
        x1 = x0 + seg_w if i < 6 else W - 12
        d.rectangle([x0, y, x1, y + h], fill=r1.TINTS[r], outline=NAVY, width=1)
        f = F(BOLD, 10)
        txt = f"{disp.get(r, r)} {counts[r]}"
        b = d.textbbox(((x0 + x1) // 2, y + h // 2), txt, font=f, anchor="mm")
        d.text(((x0 + x1) // 2, y + h // 2), txt, font=f, fill=NAVY,
               anchor="mm")
        r1.reg("text", b, f"region-{r}")
    return y + h


def draw_datecheck_thin_1r3(d, W, y):
    """DATE CHECK TIPIS (keputusan footer Kevin 19:03 WIB).

    Kotak border merah seperti 1r, tapi TIPIS: 2 baris teks 9pt bold
    dengan padding ketat (3px atas + 3px bawah) -> box_h = 32px
    (lama: 8 + 26 + 6 = 40px). Daftar buangan dipertahankan LENGKAP
    (tidak dipersingkat — muat 2 baris) + kalimat penutup "Every story
    here happened, or was first reported, on Friday 20 November 2026."
    Assert: maksimal 2 baris. Mengembalikan y bawah kotak."""
    f = F(BOLD, 9)
    pref = "DATE CHECK — "
    pref_w = d.textlength(pref, font=f)
    lines = rs.wrap(d, v4.DATECHECK_REST, f, W - 48 - pref_w)
    assert len(lines) <= 2, f"datecheck pecah >2 baris: {lines}"
    box_h = 3 + len(lines) * 13 + 3
    d.rectangle([12, y, W - 12, y + box_h], fill=CARD_BG,
                outline=RED, width=2)
    yy = y + 3
    for j, ln in enumerate(lines):
        if j == 0:
            total_w = pref_w + d.textlength(ln, font=f)
            x0 = (W - total_w) // 2
            b = d.textbbox((x0, yy), pref, font=f, anchor="la")
            d.text((x0, yy), pref, font=f, fill=RED)
            r1.reg("text", b, "datecheck-pref")
            b = d.textbbox((x0 + pref_w, yy), ln, font=f, anchor="la")
            d.text((x0 + pref_w, yy), ln, font=f, fill=NAVY)
            r1.reg("text", b, "datecheck-l1")
        else:
            b = d.textbbox((W // 2, yy), ln, font=f, anchor="ma")
            d.text((W // 2, yy), ln, font=f, fill=NAVY, anchor="ma")
            r1.reg("text", b, f"datecheck-l{j + 1}")
        yy += 13
    return y + box_h


def build_1r3(path):
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
    gaps = GAPS_1R3
    CFG = r1.CFG_1R

    y = 12  # margin atas 1r: kembali dari 10
    y = draw_masthead_1r3(d, W, y, total)
    y += gaps[0]
    y = r1.draw_numbers_strip_1r(d, W, y)
    y += gaps[1]
    y = draw_region_tints_1r3(d, W, y, counts)
    y += gaps[2]
    tops = {}
    hero_w = (W - 24 - 2 * r1.PANEL_GAP) // 3
    for i, st in enumerate(panels[:3]):
        xx = 12 + i * (hero_w + r1.PANEL_GAP)
        tops[(0, i)] = r1.draw_panel_1r(im, xx, y, hero_w, HERO_H_1R3, st,
                                        CFG, True)
    y += HERO_H_1R3 + gaps[3]
    card_w = (W - 24 - 4 * r1.PANEL_GAP) // 5
    for rr in range(2):
        for c in range(5):
            st = panels[3 + rr * 5 + c]
            xx = 12 + c * (card_w + r1.PANEL_GAP)
            tops[(1 + rr, c)] = r1.draw_panel_1r(im, xx, y, card_w,
                                                CARD_H_1R3, st, CFG, False)
        y += CARD_H_1R3 + (r1.ROW_GAP if rr == 0 else 0)
    y += gaps[4]
    band_y = y
    # Footer baru (keputusan Kevin 19:03 WIB): DATE CHECK TIPIS 32px
    # (2 baris, padding ketat) + baris Sources DIHAPUS sepenuhnya.
    # Footer lama: 40 (datecheck) + 15 (sources) = 55px; baru: 32px.
    # Ruang bebas + deck 1 baris dipakai untuk hero 166 + kartu 130.
    # band_h >= 239 supaya briefs gap_each >= 1 (seperti 1r2); di bawah
    # itu briefs menumpuk tanpa napas.
    band_h = 1024 - band_y - gaps[5] - 32 - 12
    assert band_h >= 239, f"band terlalu pendek: {band_h} (briefs butuh >=239)"
    map_w = 400
    map_legend_h = 12
    # Judul peta TIDAK lagi makan 16px di atas peta (chip menembus border)
    map_h = band_h - map_legend_h
    assert map_h >= 150, f"peta terlalu pendek: {map_h}"
    skipped = draw_map_1r3(im, 12, band_y, map_w, map_h, panels, "Gopalpur")
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
    y = draw_datecheck_thin_1r3(d, W, y)
    # Baris Sources DIHAPUS (keputusan Kevin 19:03 WIB) — tidak ada lagi
    # baris "Sources: Reuters · AP · ..." di bawah DATE CHECK.
    im.save(path)
    top_bad = rs.check_top_colors(tops)
    ink_bottom, margin = v4.audit_footer(path)
    nreg = check_no_overlap_1r3()
    return {"total": total, "counts": counts, "band_h": band_h,
            "map_h": map_h, "map_skipped": skipped, "top_bad": top_bad,
            "ink_bottom": ink_bottom, "bottom_margin": margin,
            "registered_boxes": nreg, "gaps": gaps}


def measure(path):
    """Ink coverage + piksel jenuh, metode §0 analisis-improve-sketsa1.md:
    HSV S>0,30 (PIL); ink = JUMLAH selisih 3 kanal >40 dari kertas
    (246,241,231) — diverifikasi: metode ini menghasilkan 34,2% untuk 1r,
    sama dengan tabel §3 analisis (max-kanal memberi 26,8%, salah metode)."""
    import numpy as np
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    ink = (np.abs(a - np.array([246, 241, 231])).sum(axis=2) > 40).mean()
    hsv = np.asarray(im.convert("HSV")).astype(int)
    sat = (hsv[:, :, 1] > int(0.30 * 255)).mean()
    return {"ink_pct": round(float(ink) * 100, 1),
            "saturated_pct": round(float(sat) * 100, 1)}


if __name__ == "__main__":
    out = "/home/hatch/workspace/makefun/news-image-20261120/sketches-v4"
    path = f"{out}/sketch-v4-1r3-koran-serif-revised.png"
    res = build_1r3(path)
    assert not res["top_bad"], f"pelanggaran warna atas: {res['top_bad']}"
    assert res["ink_bottom"] <= 1012, f"tinta sampai y={res['ink_bottom']}"
    assert res["bottom_margin"] >= 10, f"margin bawah cuma {res['bottom_margin']}px"
    h1 = hashlib.sha256(open(path, "rb").read()).hexdigest()
    build_1r3("/tmp/v4-1r3-determinism-check.png")
    h2 = hashlib.sha256(open("/tmp/v4-1r3-determinism-check.png", "rb").read()).hexdigest()
    assert h1 == h2, "tidak deterministik"
    res["sha256"] = h1
    res["measure_1r3"] = measure(path)
    res["measure_1r"] = measure(f"{out}/sketch-v4-1r-koran-serif-improved.png")
    print("1r3", json.dumps(res, default=str))
    print("OK")
