#!/usr/bin/env python3
"""3 sketsa untuk news-image-20261120 (20 Nov 2026) — SKETSA SAJA.

Metode M-C Timeline-first (Kevin GAS 07:21 WIB). Aturan sketch-first:
kirim sketsa dulu ke Kevin sebelum build apa pun. Duel TIDAK jalan
(OpenRouter 402). Build final JANGAN pakai script ini — kompositor
final ditulis fresh di sesi build.

Varian:
- A: port layout v13 ni19 (masthead + deck + strip angka + 3 hero +
  10 kartu 2x5 + peta + MORE STORIES) + BAR TIMELINE horizontal di
  bawah deck (tulang punggung M-C).
- B: 4 hero + 2 baris x 6 kolom (12 kartu) — hero ke-4 = Kyiv;
  menjawab pertanyaan varian Kevin (4 hero dibawa ke ni20 atau tidak).
- C: timeline-first beda jelas — kolom timeline VERTIKAL dominan di
  kiri + 1 hero besar + 4 kartu besar (2x2) di kanan.

Riset: Jum 20 Nov ~10:05 WIB (03:05 UTC) — hari BARU berjalan 3 jam
UTC. Cerita 20 Nov murni masih sedikit; sebagian besar berita besar
hari ini adalah peristiwa 19 Nov yang pertama dilaporkan luas pada
20 Nov (Riyadh, Trump-Iran, ICJ, Shenzhen, Anthropic, Korea) —
ditandai [19 Nov, dilapor 20 Nov] di sketch-NOTE; ATM 21 Nov yang
memutuskan. DATE CHECK di tiap sketsa jujur soal ini.
"""
import sys

sys.path.insert(0, "/home/hatch/workspace/makefun/news-image-20261119")
sys.path.insert(0, "/home/hatch/workspace/makefun/news-image-20261120")

from PIL import Image, ImageDraw, ImageFont

import render_variants as rv
import scenes_2x5 as sc19
import scenes_ni20 as sc20

# ------------------------------------------------------------------ palette
PAPER = rv.PAPER
CARD_BG = rv.CARD_BG
NAVY = rv.NAVY
INK = rv.INK
RED = rv.RED
GOLD = rv.GOLD
WHITE = rv.WHITE
SEA = rv.SEA
LAND = rv.LAND
REGION_COLORS = rv.REGION_COLORS
BOLD, REG = rv.BOLD, rv.REG

# kota baru ni20 untuk peta (lon, lat)
rv.PLACES.update({
    "Riyadh": (46.7, 24.6), "Gopalpur": (85.0, 19.3),
    "Antalya": (30.7, 36.9), "Seoul": (127.0, 37.5),
    "Nairobi": (36.8, -1.3), "Genoa": (8.9, 44.4),
    "Brisbane": (153.0, -27.5), "Dakar": (-17.4, 14.7),
    "Accra": (-0.2, 5.6), "Taipei": (121.6, 25.0),
})

ALL_SCENES = dict(sc19.SCENES)
ALL_SCENES.update(sc20.SCENES_NI20)


def motif(kind, w, h):
    im = Image.new("RGB", (w, h), CARD_BG)
    dd = ImageDraw.Draw(im)
    ALL_SCENES[kind](dd, 0, 0, w, h)
    return im


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    return rv.wrap(d, text, fnt, max_w)


# ------------------------------------------------------------------ data
# story: dict(num, city, topic, region, region_disp, title, s1, s2, scene, map_city)
# region = kunci REGION_COLORS (untuk peta/strip); region_disp = label tampil.
def S(num, city, topic, region, title, s1, s2, scene, map_city=None):
    disp = {"ASIA": "ASIA-PACIFIC"}.get(region, region)
    return {"num": num, "city": city, "topic": topic, "region": region,
            "region_disp": disp, "title": title, "s1": s1, "s2": s2,
            "scene": scene, "map_city": map_city or city}


HEROES_A = [
    S(1, "Riyadh", "MISSILE STRIKE", "MIDEAST",
      "Houthi missile hits Riyadh's tallest tower",
      "PIF Tower damaged on several floors.",
      "No injuries reported, Saudis say.", "s_riyadh"),
    S(2, "Gopalpur", "CYCLONE", "ASIA",
      "Cyclone Akvan hits India's east coast",
      "Landfall near Gopalpur, winds 90 km/h.",
      "300,000 people evacuated to shelters.", "s_cyclone"),
    S(3, "Washington", "IRAN", "AMERICAS",
      "Trump puts Iran decision off to 2027",
      "\u2018We'll see after January 1,\u2019 he says.",
      "Senate rejects a curb on the war.", "s_trump"),
]
CARDS_A = [
    S(4, "Kyiv", "MISSILES", "EUROPE",
      "Russia hits Kyiv with missiles overnight",
      "Blasts at 1 a.m. in 3 districts.",
      "Revenge for Crimea bridge.", "s_kyiv_hit"),
    S(5, "Antalya", "COP31", "MIDEAST",
      "COP31 closes with no fossil-fuel deal",
      "Draft drops all fossil-fuel language.",
      "Final text due by midnight.", "s_cop31"),
    S(6, "Shenzhen", "SUMMIT", "ASIA",
      "Trump, Xi and Putin sign peace declaration",
      "First three-way leaders' summit.",
      "Ukraine tops the agenda.", "s_summit"),
    S(7, "New York", "IPO", "AMERICAS",
      "Anthropic up 17% on debut",
      "$81.3bn IPO, the largest ever.",
      "But the Nasdaq falls 2.3%.", "s_ipo"),
    S(8, "The Hague", "ICJ VERDICT", "EUROPE",
      "World court: Myanmar committed genocide",
      "Rohingya case, ruled 9\u20136.",
      "Gambia brought the case.", "s_icj"),
    S(9, "Seoul", "EXPORTS", "ASIA",
      "Korea joins the $1tn export club",
      "First new member in 19 years.",
      "Chips drive the record.", "s_korea"),
    S(10, "Nairobi", "MINING", "AFRICA",
      "US group wins Kenya's $60bn minerals deal",
      "Mrima Hill holds $60bn of minerals.",
      "Beats Chinese rivals, BBC says.", "s_kenya"),
    S(11, "Hormuz", "OIL", "WORLD",
      "Oil rises as Hormuz tankers burn",
      "Two tankers hit mines, IRGC says.",
      "Brent $92.22 a barrel.", "s_oil"),
    S(12, "Genoa", "DRONES", "EUROPE",
      "Drones close Genoa airport for 4 hours",
      "Flights halted overnight.",
      "No one claims the drones.", "s_genoa"),
    S(13, "Brisbane", "CONCERT", "OCEANIA",
      "Robbie Williams plays Brisbane",
      "BRITPOP tour at Suncorp Stadium.",
      "Auckland next, on 24 November.", "s_brisbane"),
]
BRIEFS_A = [
    (14, "Dakar", "AFRICA", "Pastef confirms Faye has left the party."),
    (15, "Accra", "AFRICA", "Ghana cuts its rate by 3 points to 11%."),
    (16, "Taipei", "ASIA", "Taiwan limits short-selling from today."),
    (17, "Tokyo", "ASIA", "India and Japan hold 2+2 talks in Tokyo."),
    (18, "Washington", "AMERICAS", "Trump to hold a press conference today."),
    (19, "Wellington", "OCEANIA", "Campaigners fault NZ on climate again."),
    (20, "Dakar", "AFRICA", "Dozens missing after a migrant boat sinks."),
    (21, "Berlin", "EUROPE", "Allies meet in Berlin on Ukraine peace."),
    (22, "Global", "WORLD", "JPMorgan and Visa hit by cyber incidents."),
]

HEROES_B = HEROES_A + [
    S(4, "Kyiv", "MISSILES", "EUROPE",
      "Russia hits Kyiv with missiles overnight",
      "Fires in 3 districts.",
      "Revenge for Crimea bridge.", "s_kyiv_hit"),
]
CARDS_B = [
    S(5, "Antalya", "COP31", "MIDEAST",
      "COP31 closes with no fossil-fuel deal",
      "Draft drops fossil-fuel words.",
      "Final text due by midnight.", "s_cop31"),
    S(6, "Shenzhen", "SUMMIT", "ASIA",
      "Trump, Xi and Putin sign peace declaration",
      "First three-way leaders' summit.",
      "Ukraine tops the agenda.", "s_summit"),
    S(7, "New York", "IPO", "AMERICAS",
      "Anthropic up 17% on debut",
      "$81.3bn IPO, the largest ever.",
      "But the Nasdaq falls 2.3%.", "s_ipo"),
    S(8, "The Hague", "ICJ VERDICT", "EUROPE",
      "World court: Myanmar committed genocide",
      "Rohingya case, ruled 9\u20136.",
      "Gambia brought the case.", "s_icj"),
    S(9, "Seoul", "EXPORTS", "ASIA",
      "Korea joins the $1tn export club",
      "First new member in 19 years.",
      "Chips drive the record.", "s_korea"),
    S(10, "Nairobi", "MINING", "AFRICA",
      "US group wins Kenya's $60bn minerals deal",
      "Mrima Hill holds $60bn of minerals.",
      "Beats Chinese rivals.", "s_kenya"),
    S(11, "Hormuz", "OIL", "WORLD",
      "Oil rises as Hormuz tankers burn",
      "Two tankers hit mines, IRGC says.",
      "Brent $92.22 a barrel.", "s_oil"),
    S(12, "Genoa", "DRONES", "EUROPE",
      "Drones close Genoa airport for 4 hours",
      "Flights halted overnight.",
      "No one claims the drones.", "s_genoa"),
    S(13, "Brisbane", "CONCERT", "OCEANIA",
      "Robbie Williams plays Brisbane",
      "BRITPOP tour at Suncorp.",
      "Auckland next, 24 November.", "s_brisbane"),
    S(14, "Dakar", "PARTY SPLIT", "AFRICA",
      "Faye leaves his own party in Senegal",
      "Pastef confirms the split.",
      "Budget row behind the break.", "s_dakar"),
    S(15, "Accra", "RATE CUT", "AFRICA",
      "Ghana cuts its rate to 11%",
      "A 3-point cut.",
      "Rate now 11%, down from 14%.", "s_accra"),
    S(16, "Taipei", "STOCKS", "ASIA",
      "Taiwan steadies its stock market",
      "Short-selling limits from today.",
      "Stocks fell 5,248 points.", "s_taiwan"),
]
BRIEFS_B = [
    (17, "Tokyo", "ASIA", "India and Japan hold 2+2 talks in Tokyo."),
    (18, "Washington", "AMERICAS", "Trump to hold a press conference today."),
    (19, "Wellington", "OCEANIA", "Campaigners fault NZ on climate again."),
    (20, "Dakar", "AFRICA", "Dozens missing after a migrant boat sinks."),
    (21, "Berlin", "EUROPE", "Allies meet in Berlin on Ukraine peace."),
    (22, "Global", "WORLD", "JPMorgan and Visa hit by cyber incidents."),
]

# C: hero Riyadh + 4 kartu besar; briefs 12 (6-17)
HERO_C = HEROES_A[0]
CARDS_C = [
    S(2, "Gopalpur", "CYCLONE", "ASIA",
      "Cyclone Akvan hits India's east coast",
      "Landfall near Gopalpur, winds 90 km/h.",
      "300,000 people evacuated to shelters.", "s_cyclone"),
    S(3, "Washington", "IRAN", "AMERICAS",
      "Trump puts Iran decision off to 2027",
      "\u2018We'll see after January 1,\u2019 he says.",
      "Senate rejects a curb on the war.", "s_trump"),
    S(4, "Kyiv", "MISSILES", "EUROPE",
      "Russia hits Kyiv with missiles overnight",
      "Blasts at 1 a.m. in 3 districts.",
      "Revenge for Crimea bridge.", "s_kyiv_hit"),
    S(5, "Antalya", "COP31", "MIDEAST",
      "COP31 closes with no fossil-fuel deal",
      "Draft drops all fossil-fuel language.",
      "Final text due by midnight.", "s_cop31"),
]
BRIEFS_C = [
    (6, "Shenzhen", "ASIA", "Trump, Xi and Putin sign a peace declaration."),
    (7, "New York", "AMERICAS", "Anthropic up 17% on debut; markets fall 2%."),
    (8, "The Hague", "EUROPE", "World court: Myanmar committed genocide."),
    (9, "Seoul", "ASIA", "Korea joins the $1tn export club."),
    (10, "Nairobi", "AFRICA", "US group wins Kenya's $60bn minerals deal."),
    (11, "Hormuz", "WORLD", "Oil rises as Hormuz tankers burn."),
    (12, "Genoa", "EUROPE", "Drones close Genoa airport for 4 hours."),
    (13, "Brisbane", "OCEANIA", "Robbie Williams plays Brisbane tonight."),
    (14, "Dakar", "AFRICA", "Pastef confirms Faye has left the party."),
    (15, "Accra", "AFRICA", "Ghana cuts its rate by 3 points to 11%."),
    (16, "Taipei", "ASIA", "Taiwan limits short-selling from today."),
    (17, "Tokyo", "ASIA", "India and Japan hold 2+2 talks in Tokyo."),
]

NUMBERS = [
    ("$81.3bn", "Anthropic IPO \u2014 largest ever", "AMERICAS"),
    ("$92.22", "Brent crude a barrel", "WORLD"),
    ("$1tn", "Korea exports, first time", "ASIA"),
    ("300,000", "evacuated for Akvan", "ASIA"),
    ("92,000", "people at COP31", "MIDEAST"),
    ("17%", "Anthropic shares up day one", "AMERICAS"),
]

REGION_ORDER = ["EUROPE", "AMERICAS", "ASIA", "MIDEAST", "AFRICA",
                "OCEANIA", "WORLD"]
REGION_DISP = {"ASIA": "ASIA-PACIFIC"}


def region_counts(panels, briefs):
    c = {r: 0 for r in REGION_ORDER}
    for p in panels:
        c[p["region"]] += 1
    for _n, _city, r, _t in briefs:
        c[r] += 1
    return c


# ------------------------------------------------------------------ chrome
def draw_masthead(d, W, y):
    f_small = F(BOLD, 13)
    f_date = F(BOLD, 30)
    d.text((W // 2, y), "THE WORLD IN ONE IMAGE", font=f_small, fill=NAVY,
           anchor="ma")
    parts = [("FRIDAY ", NAVY), ("20", RED), (" NOVEMBER 2026", NAVY)]
    total = sum(d.textlength(t, font=f_date) for t, _ in parts)
    x = (W - total) // 2
    yy = y + 20
    for t, col in parts:
        d.text((x, yy), t, font=f_date, fill=col)
        x += d.textlength(t, font=f_date)
    d.line([(12, y + 56), (W - 12, y + 56)], fill=NAVY, width=2)
    return y + 62


def draw_deck(d, W, y, text):
    f = F(BOLD, 14)
    lines = wrap(d, text, f, W - 24)
    assert len(lines) == 1, f"deck pecah {len(lines)} baris: {lines}"
    d.text((W // 2, y), lines[0], font=f, fill=RED, anchor="ma")
    return y + 20


def draw_region_section(d, W, y, counts, total):
    h = 36
    x = 12
    f_t = F(BOLD, 12)
    f_s = F(BOLD, 11)
    title = f"{total} STORIES"
    tw = d.textlength(title, font=f_t) + 24
    d.rectangle([x, y, x + tw, y + h], fill=NAVY)
    d.text((x + tw // 2, y + h // 2 - 8), title, font=f_t, fill=WHITE,
           anchor="ma")
    x += tw
    seg_w = (W - 24 - tw) // 7
    for i, r in enumerate(REGION_ORDER):
        col = REGION_COLORS[r]
        tint = tuple(int(255 - (255 - c) * 0.45) for c in col)
        x0 = x + i * seg_w
        x1 = x0 + seg_w if i < 6 else W - 12
        d.rectangle([x0, y, x1, y + h], fill=tint, outline=NAVY, width=1)
        label = f"{REGION_DISP.get(r, r)} {counts[r]}"
        d.text(((x0 + x1) // 2, y + h // 2 - 8), label, font=f_s, fill=NAVY,
               anchor="ma")
    return y + h


def draw_numbers_strip(d, W, y, h=58):
    f_n = F(BOLD, 22)
    f_c = F(BOLD, 10)
    x = 12
    seg_w = (W - 24) // 6
    for i, (num, cap, region) in enumerate(NUMBERS):
        x0 = x + i * seg_w
        x1 = x0 + seg_w if i < 5 else W - 12
        if i > 0:
            col = REGION_COLORS[region]
            d.line([(x0, y + 8), (x0, y + h - 8)], fill=col, width=2)
        d.text(((x0 + x1) // 2, y + 4), num, font=f_n, fill=NAVY, anchor="ma")
        lines = wrap(d, cap, f_c, seg_w - 10)
        assert len(lines) <= 2, f"caption strip pecah: {cap} -> {lines}"
        yy = y + 32
        for ln in lines:
            d.text(((x0 + x1) // 2, yy), ln, font=f_c, fill=INK, anchor="ma")
            yy += 12
    return y + h


def draw_panel(im, x, y, w, h, story, title_pt, sum_pt, strip_h=15):
    """Satu panel: strip 'N · CITY · TOPIC' + gambar + judul + ringkasan.
    Mengembalikan (img_top_color) untuk cek warna tetangga."""
    d = ImageDraw.Draw(im)
    col = REGION_COLORS[story["region"]]
    f_title = F(BOLD, title_pt)
    f_sum = F(REG, sum_pt)
    d.rectangle([x, y, x + w, y + strip_h], fill=col)
    strip = f"{story['num']} \u00b7 {story['city'].upper()} \u00b7 {story['topic']}"
    # STRIP — dua perbaikan (temuan audit R3, 20 Nov 11:05 WIB):
    # (1) font mengecil otomatis sampai muat: di kartu R3 (139 px)
    # "WASHINGTON · SENATE" (+16 px), "BRISBANE · CONCERT" (+12 px)
    # dan "MUMBAI · MARKETS" (+3,5 px) terpotong di 10pt.
    # (2) teks HARUS di tengah strip: anchor "lm" di y+strip_h//2.
    # Kode lama (y+strip_h//2-7) menaruh TENGAH teks di tepi atas strip,
    # sehingga ~40% huruf keluar dari strip, putih di atas krem =
    # tidak terbaca; SEMUA 18 strip R3 (dan A/B/C, R1/R2) kena.
    f_strip = F(BOLD, 10 if strip_h >= 15 else 9)
    while (d.textlength(strip, font=f_strip) > w - 10
           and f_strip.size > 8):
        f_strip = F(BOLD, f_strip.size - 1)
    d.text((x + 6, y + strip_h // 2), strip, font=f_strip, fill=WHITE,
           anchor="lm")
    img_h = h - strip_h - 8
    # ukur judul + ringkasan dulu supaya tinggi gambar pas
    tw = wrap(d, story["title"], f_title, w - 10)
    assert len(tw) <= 2, f"judul pecah >2: {story['title']} -> {tw}"
    s_lines = wrap(d, story["s1"] + " " + story["s2"], f_sum, w - 10)
    assert len(s_lines) <= 2, f"ringkasan pecah >2: {story['num']} -> {s_lines}"
    text_h = len(tw) * (title_pt + 3) + len(s_lines) * (sum_pt + 3) + 4
    img_h = h - strip_h - text_h - 4
    assert img_h >= 48, f"gambar {story['num']} terlalu pendek: {img_h}"
    pic = motif(story["scene"], w, img_h)
    im.paste(pic, (x, y + strip_h))
    yy = y + strip_h + img_h + 2
    for ln in tw:
        d.text((x + 5, yy), ln, font=f_title, fill=INK)
        yy += title_pt + 3
    for ln in s_lines:
        d.text((x + 5, yy), ln, font=f_sum, fill=INK)
        yy += sum_pt + 3
    # warna atas gambar (rata-rata baris 2-8 piksel di tengah)
    px = pic.crop((w // 2 - 10, 2, w // 2 + 10, 8))
    cols = list(px.getdata())
    avg = tuple(sum(c[i] for c in cols) // len(cols) for i in range(3))
    return avg


def draw_briefs(im, x, y, w, h, briefs, first_num, font_pt=13):
    """MORE STORIES 3 kolom, format 'N. Kota: teks…', rata kiri,
    kolom berakhir sejajar (slack dibagi rata)."""
    d = ImageDraw.Draw(im)
    f_n = F(BOLD, font_pt)
    f_c = F(BOLD, font_pt)
    f_t = F(REG, font_pt)
    cols = [[], [], []]
    for i, b in enumerate(briefs):
        cols[i % 3].append(b)
    # hitung baris tiap brief (baris pertama lebih sempit karena kepala)
    col_w = (w - 16) // 3
    lh = font_pt + 3
    col_items = []
    for col in cols:
        items = []
        for (n, city, region, text) in col:
            head = f"{n}. {city}: "
            hw = d.textlength(head, font=f_n)
            # baris 1: kepala + teks; baris lanjut: lebar penuh
            first = wrap(d, text, f_t, col_w - hw - 6)
            rest = []
            # wrap sederhana: gabung dulu, lalu bagi ulang
            full = wrap(d, text, f_t, col_w - 6)
            # hitung dengan kepala: baris pertama menampung lebih sedikit
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
            assert len(lines) <= 3, f"brief {n} pecah >3: {lines}"
            items.append((n, city, region, lines, head))
        col_items.append(items)
    # gambar: slack dibagi rata ke ATAS, ANTAR brief, dan BAWAH kolom
    # (bukan hanya antar brief — sisa di bawah kolom terakhir bikin gap)
    for ci, items in enumerate(col_items):
        cx = x + ci * col_w + (8 if ci else 0)
        total_lines = sum(len(it[3]) for it in items)
        gaps = h - total_lines * lh
        gap_each = max(0, gaps // (len(items) + 1))
        yy = y + gap_each
        for (n, city, region, lines, head) in items:
            # strip warna region di kiri
            d.rectangle([cx - 6, yy + 2, cx - 2, yy + len(lines) * lh - 2],
                        fill=REGION_COLORS[region])
            # baris 1: nomor merah + kota navy + teks
            d.text((cx, yy), f"{n}. ", font=f_n, fill=RED)
            nx = cx + d.textlength(f"{n}. ", font=f_n)
            d.text((nx, yy), f"{city}: ", font=f_c, fill=NAVY)
            tx = nx + d.textlength(f"{city}: ", font=f_c)
            d.text((tx, yy), lines[0], font=f_t, fill=INK)
            yy += lh
            for ln in lines[1:]:
                d.text((cx, yy), ln, font=f_t, fill=INK)
                yy += lh
            yy += gap_each
    return y + h


def draw_map(im, x, y, mw, mh, panels, briefs, hero_city):
    """Peta dunia + pin bernomor (panel) + bintang (hero 1) + dot (brief)."""
    d = ImageDraw.Draw(im)
    d.rectangle([x, y, x + mw, y + mh], fill=CARD_BG, outline=NAVY, width=1)
    mtmp = Image.new("RGB", (mw - 2, mh - 2), SEA)
    md = ImageDraw.Draw(mtmp)
    for poly in rv.CONTINENTS:
        pts = [rv.project(lon, lat, 0, 0, mw - 2, mh - 2) for lon, lat in poly]
        md.polygon(pts, fill=LAND, outline=(180, 160, 115))
    im.paste(mtmp, (x + 1, y + 1))
    md = ImageDraw.Draw(im)
    fl = F(BOLD, 10)
    fp = F(BOLD, 7)
    placed = []
    skipped = []

    def place(px, py, r):
        for (qx, qy, qr) in placed:
            if ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5 < 10:
                return False
        placed.append((px, py, r))
        return True

    for p in panels:
        city = p["map_city"]
        if city not in rv.PLACES:
            continue
        lon, lat = rv.PLACES[city]
        px, py = rv.project(lon, lat, x + 1, y + 1, mw - 2, mh - 2)
        if p["city"] == hero_city:
            if place(px, py, 8):
                md.polygon(rv.star_points(px, py, 8, 3.5), fill=GOLD,
                           outline=NAVY)
            continue
        if not place(px, py, 5.5):
            skipped.append((city, p["num"]))
            continue
        col = REGION_COLORS[p["region"]]
        md.ellipse([px - 5.5, py - 5.5, px + 5.5, py + 5.5], fill=col,
                   outline=WHITE, width=1)
        mark = str(p["num"])
        tw = md.textlength(mark, font=fp)
        md.text((px - tw / 2, py - 4), mark, font=fp, fill=WHITE)
    seen = {rv.PLACES[p["map_city"]] for p in panels
            if p["map_city"] in rv.PLACES}
    for (n, city, region, _t) in briefs:
        if city in ("Global",) or city not in rv.PLACES:
            continue
        if rv.PLACES[city] in seen:
            continue
        seen.add(rv.PLACES[city])
        lon, lat = rv.PLACES[city]
        px, py = rv.project(lon, lat, x + 1, y + 1, mw - 2, mh - 2)
        if not place(px, py, 3):
            skipped.append((city, n))
            continue
        md.ellipse([px - 3, py - 3, px + 3, py + 3],
                   fill=REGION_COLORS[region], outline=WHITE, width=1)
    return skipped


def draw_datecheck_footer(d, W, y, total, note):
    f = F(BOLD, 11)
    d.rectangle([12, y, W - 12, y + 28], fill=(232, 226, 214))
    d.text((W // 2, y + 14), note, font=f, fill=NAVY, anchor="mm")
    f2 = F(REG, 9)
    d.text((W // 2, y + 44),
           "Sources: Reuters \u00b7 AFP \u00b7 IMD \u00b7 ICJ \u00b7 BBC \u00b7 WSJ \u00b7 "
           "SPA \u00b7 ministries. Disputed claims are attributed, not stated as fact.",
           font=f2, fill=(90, 90, 90), anchor="ma")
    return y + 56


def check_top_colors(panels_top):
    """panels_top: dict (row, col) -> warna atas. Laporkan pasangan
    tetangga ortogonal yang warnanya terlalu mirip (<25 jarak RGB)."""
    bad = []
    for (r, c), col in panels_top.items():
        for (dr, dc) in ((0, 1), (1, 0)):
            nb = panels_top.get((r + dr, c + dc))
            if nb is None:
                continue
            dist = sum((a - b) ** 2 for a, b in zip(col, nb)) ** 0.5
            if dist < 25:
                bad.append(((r, c), (r + dr, c + dc), round(dist, 1)))
    return bad


# ------------------------------------------------------------------ layout A
def build_A(path):
    W = 1024
    im = Image.new("RGB", (W, 1024), PAPER)
    d = ImageDraw.Draw(im)
    y = 12
    y = draw_masthead(d, W, y)
    y = draw_deck(d, W, y + 4,
                  "a missile hits Riyadh's tallest tower, a cyclone lands in "
                  "India, Trump delays Iran to 2027")
    # --- bar timeline horizontal (tulang punggung M-C)
    # Tanpa judul baris sendiri (judul lama menabrak label "00:00"):
    # jam di ATAS garis, label di BAWAH garis.
    y += 6
    tl_y = y
    f_tl = F(BOLD, 10)
    f_tm = F(BOLD, 11)
    line_y = tl_y + 18
    d.line([(24, line_y), (W - 24, line_y)], fill=NAVY, width=2)
    nodes = [("00:00", "Kyiv missiles", "EUROPE"),
             ("01:18", "Brent $92.22", "WORLD"),
             ("02:30", "Akvan 110 km off", "ASIA"),
             ("06:00", "Akvan landfall", "ASIA"),
             ("21:00", "COP31 text due", "MIDEAST")]
    seg = (W - 48) // 5
    for i, (tm, label, region) in enumerate(nodes):
        cx = 24 + seg * i + seg // 2
        col = REGION_COLORS[region]
        d.ellipse([cx - 6, line_y - 6, cx + 6, line_y + 6], fill=col,
                  outline=NAVY, width=1)
        d.text((cx, tl_y), tm, font=f_tm, fill=RED, anchor="ma")
        d.text((cx, line_y + 9), label, font=f_tl, fill=INK, anchor="ma")
    y = line_y + 26
    # --- chrome
    counts = region_counts(HEROES_A + CARDS_A, BRIEFS_A)
    total = sum(counts.values())
    y = draw_region_section(d, W, y + 4, counts, total)
    y = draw_numbers_strip(d, W, y + 4)
    # --- heroes
    y += 6
    hero_h = 196
    hero_w = (W - 24 - 8) // 3
    tops = {}
    for i, st in enumerate(HEROES_A):
        xx = 12 + i * (hero_w + 4)
        tops[(0, i)] = draw_panel(im, xx, y, hero_w, hero_h, st, 13, 11)
    y += hero_h + 4
    # --- kartu 2x5
    card_h = 148
    card_w = (W - 24 - 16) // 5
    for r in range(2):
        for c in range(5):
            st = CARDS_A[r * 5 + c]
            xx = 12 + c * (card_w + 4)
            tops[(1 + r, c)] = draw_panel(im, xx, y, card_w, card_h, st, 11, 10)
        y += card_h + 4
    # --- bawah: peta + MORE STORIES
    band_y = y
    band_h = 1024 - 56 - band_y - 4
    map_w = 400
    skipped = draw_map(im, 12, band_y, map_w, band_h,
                       HEROES_A + CARDS_A, BRIEFS_A, "Riyadh")
    bx = 12 + map_w + 12
    bw = W - 12 - bx
    f_bh = F(BOLD, 12)
    d.text((bx, band_y), "MORE STORIES FROM 20 NOVEMBER", font=f_bh, fill=NAVY)
    draw_briefs(im, bx, band_y + 20, bw, band_h - 20, BRIEFS_A, 14, font_pt=13)
    y = band_y + band_h + 4
    note = (f"DATE CHECK \u2014 20 Nov 2026 news as reported on the day; "
            "19 Nov events only where they led 20 Nov coverage. Re-checked 21 Nov.")
    draw_datecheck_footer(d, W, y, total, note)
    im.save(path)
    return {"total": total, "counts": counts, "top_bad": check_top_colors(tops),
            "map_skipped": skipped}


# ------------------------------------------------------------------ layout B
def build_B(path):
    W = 1024
    im = Image.new("RGB", (W, 1024), PAPER)
    d = ImageDraw.Draw(im)
    y = 12
    y = draw_masthead(d, W, y)
    y = draw_deck(d, W, y + 4,
                  "a missile hits Riyadh's tallest tower, a cyclone lands in "
                  "India, Trump delays Iran to 2027")
    y += 6
    panels = HEROES_B + CARDS_B
    counts = region_counts(panels, BRIEFS_B)
    total = sum(counts.values())
    y = draw_region_section(d, W, y, counts, total)
    y = draw_numbers_strip(d, W, y + 4)
    y += 6
    tops = {}
    # 4 hero
    hero_h = 190
    hero_w = (W - 24 - 12) // 4
    for i, st in enumerate(HEROES_B):
        xx = 12 + i * (hero_w + 4)
        tops[(0, i)] = draw_panel(im, xx, y, hero_w, hero_h, st, 12, 10)
    y += hero_h + 4
    # 2x6 kartu
    card_h = 140
    card_w = (W - 24 - 20) // 6
    for r in range(2):
        for c in range(6):
            st = CARDS_B[r * 6 + c]
            xx = 12 + c * (card_w + 4)
            tops[(1 + r, c)] = draw_panel(im, xx, y, card_w, card_h, st, 10, 9)
        y += card_h + 4
    band_y = y
    band_h = 1024 - 56 - band_y - 4
    map_w = 420
    skipped = draw_map(im, 12, band_y, map_w, band_h, panels, BRIEFS_B,
                       "Riyadh")
    bx = 12 + map_w + 12
    bw = W - 12 - bx
    f_bh = F(BOLD, 12)
    d.text((bx, band_y), "MORE STORIES FROM 20 NOVEMBER", font=f_bh, fill=NAVY)
    draw_briefs(im, bx, band_y + 20, bw, band_h - 20, BRIEFS_B, 17, font_pt=13)
    y = band_y + band_h + 4
    note = (f"DATE CHECK \u2014 20 Nov 2026 news as reported on the day; "
            "19 Nov events only where they led 20 Nov coverage. Re-checked 21 Nov.")
    draw_datecheck_footer(d, W, y, total, note)
    im.save(path)
    return {"total": total, "counts": counts, "top_bad": check_top_colors(tops),
            "map_skipped": skipped}


# ------------------------------------------------------------------ layout C
TIMELINE_C = [
    ("00:00", "Missiles strike Kyiv overnight; fires in three districts.",
     "EUROPE"),
    ("01:18", "Oil climbs: Brent $92.22 on Riyadh and Hormuz fears.", "WORLD"),
    ("02:30", "Akvan 110 km off India's coast; landfall hours away.", "ASIA"),
    ("06:00", "Akvan makes landfall near Gopalpur, winds 90 km/h.", "ASIA"),
    ("12:00", "COP31 talks grind on in Antalya; no deal yet.", "MIDEAST"),
    ("21:00", "COP31 final text due at midnight in Antalya.", "MIDEAST"),
    ("LATER", "Trump press conference due at the White House.", "AMERICAS"),
]


def build_C(path):
    W = 1024
    im = Image.new("RGB", (W, 1024), PAPER)
    d = ImageDraw.Draw(im)
    y = 12
    y = draw_masthead(d, W, y)
    y = draw_deck(d, W, y + 4,
                  "hour by hour: missiles over Kyiv, a cyclone lands, "
                  "COP31's last day")
    y += 6
    panels = [HERO_C] + CARDS_C
    counts = region_counts(panels, BRIEFS_C)
    total = sum(counts.values())
    y = draw_region_section(d, W, y, counts, total)
    y = draw_numbers_strip(d, W, y + 4)
    y += 6
    main_y = y
    main_h = 540
    # --- kolom timeline kiri
    tl_x, tl_w = 12, 318
    f_th = F(BOLD, 12)
    f_tt = F(BOLD, 11)
    f_tx = F(REG, 11)
    d.text((tl_x, main_y), "FRIDAY 20 NOVEMBER \u2014 HOUR BY HOUR",
           font=f_th, fill=NAVY)
    d.text((tl_x, main_y + 16), "Times in UTC, as the day unfolded",
           font=F(REG, 10), fill=(90, 90, 90))
    spine_x = tl_x + 52
    top_y = main_y + 44
    bot_y = main_y + main_h - 8
    d.line([(spine_x, top_y), (spine_x, bot_y)], fill=NAVY, width=2)
    slot = (bot_y - top_y) // len(TIMELINE_C)
    for i, (tm, text, region) in enumerate(TIMELINE_C):
        cy = top_y + slot * i + slot // 2
        col = REGION_COLORS[region]
        d.ellipse([spine_x - 6, cy - 6, spine_x + 6, cy + 6], fill=col,
                  outline=NAVY, width=1)
        d.text((spine_x - 10, cy - 7), tm, font=f_tt, fill=RED, anchor="rm")
        lines = wrap(d, text, f_tx, tl_w - 64)
        assert len(lines) <= 3, f"timeline pecah >3: {text} -> {lines}"
        yy = cy - (len(lines) * 14) // 2
        for ln in lines:
            d.text((spine_x + 12, yy), ln, font=f_tx, fill=INK)
            yy += 14
    # --- kanan: 1 hero besar + 2x2 kartu
    rx = tl_x + tl_w + 12
    rw = W - 12 - rx
    tops = {}
    hero_h = 232
    tops[(0, 0)] = draw_panel(im, rx, main_y, rw, hero_h, HERO_C, 14, 12)
    card_h = (main_h - hero_h - 4) // 2
    card_w = (rw - 4) // 2
    cy0 = main_y + hero_h + 4
    for r in range(2):
        for c in range(2):
            st = CARDS_C[r * 2 + c]
            xx = rx + c * (card_w + 4)
            tops[(1 + r, c)] = draw_panel(im, xx, cy0 + r * (card_h + 4),
                                          card_w, card_h, st, 12, 11)
    y = main_y + main_h + 4
    # --- bawah: peta + MORE STORIES
    band_y = y
    band_h = 1024 - 56 - band_y - 4
    map_w = 400
    skipped = draw_map(im, 12, band_y, map_w, band_h, panels, BRIEFS_C,
                       "Riyadh")
    bx = 12 + map_w + 12
    bw = W - 12 - bx
    f_bh = F(BOLD, 12)
    d.text((bx, band_y), "MORE STORIES FROM 20 NOVEMBER", font=f_bh, fill=NAVY)
    draw_briefs(im, bx, band_y + 20, bw, band_h - 20, BRIEFS_C, 6, font_pt=12)
    y = band_y + band_h + 4
    note = (f"DATE CHECK \u2014 20 Nov 2026 news as reported on the day; "
            "19 Nov events only where they led 20 Nov coverage. Re-checked 21 Nov.")
    draw_datecheck_footer(d, W, y, total, note)
    im.save(path)
    return {"total": total, "counts": counts, "top_bad": check_top_colors(tops),
            "map_skipped": skipped}


if __name__ == "__main__":
    import json
    out = "/home/hatch/workspace/makefun/news-image-20261120/sketches"
    import os
    os.makedirs(out, exist_ok=True)
    for name, fn in (("A", build_A), ("B", build_B), ("C", build_C)):
        res = fn(f"{out}/sketch-ni20-{name}.png")
        print(name, json.dumps(res, default=str))
    print("OK")
