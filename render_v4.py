#!/usr/bin/env python3
"""3 SKETSA v4 news-image-20261120 — KORAN, bukan poster.

Perintah Kevin 15:52–15:54 WIB (setelah amati rank 1–3):
- Ini KORAN (halaman depan satu halaman), BUKAN poster. v3 terasa poster
  (kartu-kartu ilustrasi rapat) — salah satu penyebab kalah.
- Rank 1 disukai karena ada SPACE di setiap section (prioritas utama,
  terutama sketsa 1). Kartu rank 1 JUGA JELAS: judul besar + terbaca,
  ringkasan terbaca, tiap kartu terpisah jelas (border + spasi).
- Layout KETIGA sketsa: 3 hero + kartu 2x5 (10 kartu, 13 drawn).
  Bukan 2x7 seperti v3.

Metode = sketsa v1r (render_v1r.py): Pillow geometris rapi + motif
render_sketches + data pool v3 yang sudah terverifikasi (STORIES.md v3).
SKETSA SAJA: mockup layout (kotak + judul asli + blok warna/grafis),
bukan entry final, tanpa gambar AI baru. BUKAN build final, BUKAN submit.

Perbedaan dari v1r/v3 (sengaja, meniru rank 1–3):
- Masthead SERIF besar di atas kertas (bukan pita navy), deck merah
  italic serif, strip 6 angka, strip region, 3 hero + 10 kartu,
  peta + brief, kotak DATE CHECK ber-border merah.
- Panel TANPA strip navy di atas gambar (ala koran): gambar di atas,
  lalu kicker "N · KOTA · TOPIK" merah kecil, judul serif tebal,
  ringkasan serif. Border tipis navy di sekeliling tiap panel.
- Gap antar section 10–14 px (v3: 4–6 px) + gap antar kartu 10 px
  (v3: 4 px). Kartu ~192 px lebar (v3: 139 px), judul kartu 13–14pt
  (v3: 11pt), ringkasan 10pt (v3: 9pt).
- Peta HANYA 13 pin cerita drawn (v3: 18 pin + 15 dot = 33 penanda).
  Brief tidak ditandai di peta.
- F1 Las Vegas NAIK jadi kartu #13 (seperti rank 2 #13); konser
  Brisbane TURUN jadi brief (top-3 tidak menggambar konser).
- Sketsa 1 & 3 = 36 cerita (33 pool + 3 slot Amerika baru, ditandai
  jelas sebagai slot riset); sketsa 2 = 33 cerita (13 drawn + 20 brief).

Analisis lengkap: analisis-ulang-top3-vs-v3.md
"""
import os
import sys
import json

sys.path.insert(0, "/home/hatch/workspace/makefun/news-image-20261119")
sys.path.insert(0, "/home/hatch/workspace/makefun/news-image-20261120")

from PIL import Image, ImageDraw, ImageFont

import render_rev2 as r2
assert "news-image-20261120" in r2.__file__, r2.__file__
import render_sketches as rs
import render_variants as rv
import scenes_ni20_rev as rev

rs.ALL_SCENES.update(rev.SCENES_REV)

PAPER = rv.PAPER
NAVY = rv.NAVY
INK = rv.INK
RED = rv.RED
GOLD = rv.GOLD
WHITE = rv.WHITE
CARD_BG = rv.CARD_BG
REGION_COLORS = rv.REGION_COLORS
BOLD, REG = rv.BOLD, rv.REG

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
DISPLAY_B = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"

TEAL_D = (16, 80, 110)
GREEN_D = (35, 90, 55)

rv.PLACES.update({
    "Jakarta": (106.8, -6.2), "Sydney": (151.2, -33.9),
    "Madrid": (-3.7, 40.4), "Pukapuka": (-165.8, -10.9),
    "Loyalty Is.": (167.2, -21.0), "Wellington": (174.8, -41.3),
    "Florida": (-81.5, 28.5), "Taipei": (121.6, 25.0),
    "Brisbane": (153.0, -27.5), "Hong Kong": (114.2, 22.3),
    "Seoul": (127.0, 37.5), "Paris": (2.35, 48.85),
    "Brussels": (4.35, 50.85), "Tokyo": (139.7, 35.7),
    "Antalya": (30.7, 36.9), "Gopalpur": (85.0, 19.3),
    "Kyiv": (30.5, 50.4), "New Delhi": (77.2, 28.6),
    "Shenzhen": (114.1, 22.5), "Riyadh": (46.7, 24.6),
    "Las Vegas": (-115.1, 36.2), "Nairobi": (36.8, -1.3),
    "Johannesburg": (28.0, -26.2),
})


def F(path, size):
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------------ motif baru
def s_f1(d, x, y, w, h):
    """F1 Las Vegas — aspal gelap + garis start kotak-kotak + garis
    kecepatan. Geometris rapi, tanpa teks."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 44))
    sq = max(4, int(w / 16))
    for i in range(0, w // sq + 1):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + i * sq, y + j * sq,
                             x + (i + 1) * sq, y + (j + 1) * sq],
                            fill=WHITE)
    d.rectangle([x, y + int(h * 0.55), x + w, y + int(h * 0.62)],
                fill=(200, 30, 30))
    for k, yy in enumerate((0.72, 0.82, 0.92)):
        d.line([(x + w * 0.08, y + h * yy),
                (x + w * (0.55 + k * 0.12), y + h * yy)],
               fill=(220, 200, 90), width=3)


def s_youtube(d, x, y, w, h):
    """Jakarta/Google — tombol play merah besar + 3 thumb kecil."""
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG)
    bx0, by0 = x + w * 0.16, y + h * 0.22
    bx1, by1 = x + w * 0.84, y + h * 0.62
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=int(h * 0.06),
                        fill=(200, 30, 30))
    cx, cy = x + w * 0.50, y + h * 0.42
    d.polygon([(cx - w * 0.09, cy - h * 0.10), (cx - w * 0.09, cy + h * 0.10),
               (cx + w * 0.11, cy)], fill=WHITE)
    for i, col in enumerate(((90, 130, 170), (200, 170, 90), (70, 140, 120))):
        tx0 = x + w * (0.16 + i * 0.25)
        d.rounded_rectangle([tx0, y + h * 0.72, tx0 + w * 0.20, y + h * 0.88],
                            radius=3, fill=col, outline=NAVY, width=1)


def s_quake(d, x, y, w, h):
    """Loyalty quake — laut teal gelap + cincin seismik + pulau."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 80, 110))
    cx, cy = x + w * 0.50, y + h * 0.52
    rmax = min(w, h) * 0.42
    for i, r in enumerate((0.30, 0.55, 0.80, 1.00)):
        col = (220, 235, 240) if i % 2 == 0 else (60, 140, 160)
        d.ellipse([cx - rmax * r, cy - rmax * r * 0.62,
                   cx + rmax * r, cy + rmax * r * 0.62],
                  outline=col, width=2)
    d.ellipse([x + w * 0.38, y + h * 0.80, x + w * 0.62, y + h * 0.94],
              fill=(210, 185, 130), outline=NAVY, width=1)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(220, 40, 40))


rs.ALL_SCENES["s_f1"] = s_f1
rs.ALL_SCENES["s_youtube"] = s_youtube
rs.ALL_SCENES["s_quake"] = s_quake

S = rs.S


def P(num, city, topic, region, title, summary, scene, key, caption="",
      giant="", giant_color=NAVY):
    d = S(num, city, topic, region, title, summary, "", scene)
    d["key"] = key
    d["caption"] = caption
    d["giant"] = giant
    d["giant_color"] = giant_color
    return d


# ------------------------------------------------------------------ data v3
# 13 drawn: 3 hero + 10 kartu (2x5). Judul + ringkasan = teks v3 persis
# (STORIES.md v3); F1 naik jadi kartu (ringkasan brief v3, dipersingkat
# jadi 2 baris di 10pt — angka 1:47.272 + Gasly tetap).
HEROES = [
    P(1, "Gopalpur", "CYCLONE", "ASIA",
      "Cyclone Akvan hits India's east coast",
      "Landfall 07:30 IST, gusts to 90 km/h. 300,000 evacuated to "
      "shelters. (IMD)", "s_cyclone", "akvan",
      caption="LANDFALL 07:30 IST · 300,000 EVACUATED",
      giant="LANDFALL", giant_color=RED),
    P(2, "Kyiv", "MISSILES", "EUROPE",
      "Missiles hit Kyiv in the early hours",
      "Missiles strike the capital from 01:25. Blasts heard across "
      "the city. (Reuters)", "s_kyiv_hit", "kyiv",
      caption="STRIKES FROM 01:25 · BLASTS HEARD",
      giant="KYIV", giant_color=NAVY),
    P(3, "Antalya", "CLIMATE", "MIDEAST",
      "COP31 draft drops fossil fuels",
      "Draft omits phase-out wording; final text due midnight. "
      "(Reuters)", "s_cop31", "cop31",
      caption="FINAL TEXT DUE MIDNIGHT",
      giant="COP31", giant_color=TEAL_D),
]
CARDS = [
    P(4, "Wellington", "CRICKET", "OCEANIA",
      "Nicholls 175* lifts New Zealand to 368",
      "Nicholls 175*; Phillips adds 118. NZ 368. (ESPNcricinfo)",
      "s_cricket", "cricket",
      giant="175*", giant_color=GREEN_D),
    # NB sketsa: "India 85/0 at stumps" dipangkas di sini supaya ringkasan
    # muat 2 baris di 10pt serif / kartu 192px (fakta tetap di STORIES.md
    # v3; build final boleh kembalikan bila muat).
    P(5, "New Delhi", "SCO", "ASIA",
      "Modi opens SCO civilisations forum",
      "SCO forum opens in Delhi. 20–22 Nov. (Nation Press)", "s_sco",
      "sco", giant="SCO", giant_color=RED),
    P(6, "Florida", "FLOODS", "AMERICAS",
      "Florida river still rising",
      "Crest 18.6 ft Fri; schools shut. (Florida Today)", "s_flood",
      "florida", giant="18.6 FT", giant_color=GREEN_D),
    P(7, "Shenzhen", "APEC", "ASIA",
      "Xi meets Albanese, Prabowo",
      "Bilaterals in Shenzhen after APEC week. (Reuters)", "s_apec",
      "apec", giant="XI–ALBANESE", giant_color=RED),
    P(8, "Taipei", "STOCKS", "ASIA",
      "Taiex slides again Friday",
      "Taiwan stocks fall 6.4%; chips lead losses. (Reuters)",
      "s_taiwan", "taipei", giant="−6.4%", giant_color=NAVY),
    P(9, "Markets", "GOLD", "WORLD",
      "Gold plunges on Friday",
      "Gold falls 2.8% intraday to $3,520. (KuCoin News)", "s_gold",
      "gold", giant="$3,520", giant_color=RED),
    P(10, "Global", "GAMES", "WORLD",
       "GTA VI user scores open at noon",
       "Reviews open 12:00 PT. Metascore 99. (GeekRadar)", "s_gta",
       "gta", giant="99", giant_color=GREEN_D),
    P(11, "Tokyo", "MARKETS", "ASIA",
       "Asia markets plunge",
       "Asia −2.5%; Nikkei −4.1%, Kospi −4.7%. (Reuters)", "s_sensex",
       "mkt", giant="−2.5%", giant_color=NAVY),
    P(12, "Shenzhen", "DEALS", "ASIA",
       "Prabowo, Xi sign $86.8bn deals",
       "Pacts worth about Rp1,600 trillion. (Xinhua)", "s_summit",
       "prabowo", giant="$86.8BN", giant_color=TEAL_D),
    P(13, "Las Vegas", "FORMULA 1", "AMERICAS",
       "Russell fastest in wet Las Vegas FP2",
       "Russell 1:47.272; Gasly +0.071. (Formula1.com)", "s_f1",
       "f1", giant="P1", giant_color=RED),
]

BRIEF_POOL = {  # kunci -> (kota, region, teks) — dipakai build()
    "kyivhit": ("Kyiv", "EUROPE", "Kyiv hit again overnight. Missiles strike the capital."),
    "brisbane": ("Brisbane", "OCEANIA", "Robbie Williams plays Brisbane. BRITPOP tonight."),
    "google": ("Jakarta", "ASIA", "Jakarta asks Google to explain. 19,000 channels removed."),
    "quake": ("Loyalty Is.", "OCEANIA", "M5.6 quake, 00:49 UTC, 10 km deep."),
    "euuk": ("Brussels", "EUROPE", "EU-UK summit opens in Brussels. Second EU–UK summit."),
    "brent": ("Global", "WORLD", "Brent rises to $92.77; WTI $83.40."),
    "cpi": ("Tokyo", "ASIA", "Japan core CPI rises 2.2% in October."),
    "sydney": ("Sydney", "OCEANIA", "Sydney terror raids: several arrested."),
    "pakistan": ("Global", "WORLD", "Pakistan beat Sri Lanka by 8 wickets."),
    "madrid": ("Madrid", "EUROPE", "Spain students strike over education cuts."),
    "samsung": ("Seoul", "ASIA", "Samsung names Choi to head Mobile."),
    "harris": ("Paris", "EUROPE", "Harris meets Macron in Paris."),
    "taiwan_meta": ("Taipei", "ASIA", "Taiwan reports 2,700 accounts to Meta."),
    "houthi": ("Riyadh", "MIDEAST", "Saudi coalition intercepts Houthi missile."),
    "xavier": ("Pukapuka", "OCEANIA", "Cyclone Xavier: Pukapuka on storm alert."),
    "hk_open": ("Hong Kong", "ASIA", "Hong Kong Open quarter-finals decided."),
    "takaichi": ("Tokyo", "ASIA", "Anti-Takaichi protest draws 10,000."),
    "flood_watch": ("Florida", "AMERICAS", "Flood watch holds through Saturday."),
    "kcse": ("Nairobi", "AFRICA", "KCSE ends; record 1.05m candidates."),
    "rand": ("Johannesburg", "AFRICA", "Rand hits one-year low at 17.56 per dollar."),
}
BRIEFS_20_KEYS = ["kyivhit", "brisbane", "google", "quake", "euuk",
                  "brent", "cpi", "sydney", "pakistan", "madrid",
                  "samsung", "harris", "taiwan_meta", "houthi", "xavier",
                  "hk_open", "takaichi", "flood_watch", "kcse", "rand"]
# 3 slot Amerika baru (sketsa 36 cerita): BUKAN cerita terverifikasi —
# placeholder riset untuk build final.
AMERICA_SLOTS = [
    ("Amerika", "AMERICAS", "Slot cerita Amerika baru — riset saat build."),
    ("Amerika", "AMERICAS", "Slot cerita Amerika baru — riset saat build."),
    ("Amerika", "AMERICAS", "Slot cerita Amerika baru — riset saat build."),
]

NUMBERS = [
    ("300,000", "evacuated for Akvan", "ASIA"),
    ("$92.77", "Brent crude per barrel", "WORLD"),
    ("−2.5%", "MSCI Asia, Friday", "ASIA"),
    ("175*", "Nicholls' runs, day two", "OCEANIA"),
    ("423", "rescue teams deployed", "ASIA"),
    ("19,000", "YouTube channels removed", "ASIA"),
]
DECK_LINES = [
    "Akvan lands in India · COP31's last day · Nicholls lifts New Zealand",
    "Asia markets plunge · Prabowo and Xi sign $86.8bn in Shenzhen",
]
DATECHECK_REST = (
    "Not Friday's news, so not on this page: Senate vote · IAEA report · "
    "Sensex · Fiji · Europe talks · Dakar boat · Dhaka fire · Takaichi · "
    "Australia sanctions · hockey · Quad · Romania · Zelenskyy · rupee · "
    "Kenya flood · Thai pact · Husky · Dow — all 17–19 Nov. Every story "
    "here happened, or was first reported, on Friday 20 November 2026.")
DATECHECK_SOURCES = (
    "Sources: Reuters · AP · IMD · USGS · RSMC Nadi · AFP · Le Monde · "
    "IANS · Xinhua · ESPNcricinfo · Metacritic. Disputed claims are "
    "attributed, not stated as fact.")

# ------------------------------------------------------------------ tile painters
# Setiap painter menggambar area gambar panel (w×h) ke image temp, lalu
# ditempel — supaya audit warna atas bekerja sama seperti motif v1r.

def _fit_font(path, size, text, max_w):
    """Perkecil font sampai teks muat max_w."""
    while size > 10:
        f = F(path, size)
        if ImageDraw.Draw(Image.new("RGB", (10, 10))).textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return F(path, 10)


def paint_giant(w, h, word, bg):
    """Sketsa 2: tile warna blok + kata/angka RAKSASA putih (ala rank 2)."""
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    f = _fit_font(BOLD, 52 if h > 80 else 40, word, w - 16)
    d.text((w // 2, h // 2), word, font=f, fill=WHITE, anchor="mm")
    return im


def paint_radar(w, h):
    """Sketsa 3 hero Akvan: cincin radar di laut navy gelap."""
    im = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(im)
    cx, cy = w // 2, h // 2 + 6
    for r in (0.22, 0.42, 0.62, 0.82):
        rr = min(w, h) * r
        d.ellipse([cx - rr, cy - rr * 0.72, cx + rr, cy + rr * 0.72],
                  outline=(220, 230, 240), width=3)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=GOLD)
    return im


def paint_arcs(w, h):
    """Sketsa 3 hero Kyiv: langit malam + busur rudal titik-titik."""
    im = Image.new("RGB", (w, h), (12, 20, 38))
    d = ImageDraw.Draw(im)
    for k, (x0, peak) in enumerate(((0.08, 0.30), (0.42, 0.18), (0.72, 0.34))):
        col = (255, 140, 60) if k != 1 else (255, 200, 90)
        for t in range(0, 21):
            fx = x0 + t / 20 * 0.22
            fy = 0.85 - 4 * peak * fx * (0.22 - fx) / 0.0484 * 0.0 - peak * 4 * (t / 20) * (1 - t / 20)
            px, py = int(w * fx), int(h * (0.88 - fy))
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
    # siluet kota di bawah
    for i, bh in enumerate((0.28, 0.42, 0.22, 0.36, 0.30)):
        bx = int(w * (0.06 + i * 0.18))
        d.rectangle([bx, h * (0.98 - bh), bx + int(w * 0.13), h],
                    fill=(30, 42, 66))
    return im


def paint_landscape(w, h):
    """Sketsa 3 hero COP31: matahari + bukit + danau (ala rank 3)."""
    im = Image.new("RGB", (w, h), (250, 247, 240))
    d = ImageDraw.Draw(im)
    d.ellipse([int(w * 0.68), int(h * 0.08), int(w * 0.88), int(h * 0.42)],
              fill=(235, 150, 60))
    d.ellipse([int(w * 0.30), int(h * 0.34), int(w * 0.72), int(h * 0.62)],
              fill=(90, 140, 200))
    d.chord([-int(w * 0.1), int(h * 0.55), int(w * 1.1), int(h * 1.3)],
            180, 360, fill=(90, 150, 80))
    return im


def paint_chart(w, h):
    """Sketsa 3 kartu pasar: grafik turun merah di navy gelap."""
    im = Image.new("RGB", (w, h), (24, 28, 36))
    d = ImageDraw.Draw(im)
    pts = [(0.06, 0.30), (0.22, 0.42), (0.38, 0.34), (0.55, 0.62),
           (0.72, 0.55), (0.94, 0.82)]
    xy = [(int(w * a), int(h * b)) for a, b in pts]
    d.line(xy, fill=(220, 60, 50), width=4, joint="curve")
    d.polygon(xy + [(int(w * 0.94), h), (int(w * 0.06), h)],
              fill=(220, 60, 50))
    return im


def paint_flags(w, h, bg):
    """Sketsa 3 kartu diplomatik: 3 bendera sederhana di latar terang."""
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    cols = [(200, 40, 40), (40, 80, 160), (220, 180, 60)]
    for i, col in enumerate(cols):
        fx = int(w * (0.12 + i * 0.30))
        d.rectangle([fx, int(h * 0.22), fx + int(w * 0.20), int(h * 0.58)],
                    fill=col, outline=NAVY, width=1)
        d.line([(fx + int(w * 0.10), int(h * 0.22)),
                (fx + int(w * 0.10), int(h * 0.85))], fill=NAVY, width=2)
    d.rectangle([0, int(h * 0.85), w, h], fill=(120, 130, 120))
    return im


def paint_sunset(w, h):
    """Sketsa 3 kartu GTA: garis sunset + matahari + 'VI' besar."""
    im = Image.new("RGB", (w, h), (60, 40, 90))
    d = ImageDraw.Draw(im)
    bands = [(90, 60, 140), (200, 90, 80), (240, 140, 60), (250, 200, 90)]
    for i, col in enumerate(bands):
        d.rectangle([0, int(h * i / 4), w, int(h * (i + 1) / 4)], fill=col)
    d.ellipse([int(w * 0.62), int(h * 0.12), int(w * 0.82), int(h * 0.52)],
              fill=(250, 220, 120))
    f = _fit_font(BOLD, 40, "VI", w - 16)
    d.text((int(w * 0.16), int(h * 0.55)), "VI", font=f, fill=WHITE)
    return im


def paint_checkered(w, h):
    """Sketsa 3 kartu F1: kotak-kotak start di atas + 'P1'."""
    im = Image.new("RGB", (w, h), (30, 34, 44))
    d = ImageDraw.Draw(im)
    sq = max(5, int(w / 14))
    for i in range(0, w // sq + 1):
        for j in range(3):
            if (i + j) % 2 == 0:
                d.rectangle([i * sq, j * sq, (i + 1) * sq, (j + 1) * sq],
                            fill=WHITE)
    f = _fit_font(BOLD, 40, "P1", w - 16)
    d.text((w // 2, int(h * 0.68)), "P1", font=f, fill=WHITE, anchor="mm")
    return im


ABSTRACT = {
    "akvan": paint_radar,
    "kyiv": paint_arcs,
    "cop31": paint_landscape,
    "taipei": paint_chart,
    "gold": paint_chart,
    "mkt": paint_chart,
    "gta": paint_sunset,
    "f1": paint_checkered,
}
FLAGS_BG = {"sco": (200, 220, 235), "apec": (250, 247, 240),
            "prabowo": (220, 235, 210)}


def tile_image(story, w, h, tile):
    """Kembalikan image area gambar panel sesuai gaya sketsa."""
    if tile == "giant":
        return paint_giant(w, h, story["giant"], story["giant_color"])
    if tile == "abstract":
        key = story["key"]
        if key in ABSTRACT:
            return ABSTRACT[key](w, h)
        if key in FLAGS_BG:
            return paint_flags(w, h, FLAGS_BG[key])
        if key == "cricket":
            return paint_giant(w, h, "175*", GREEN_D)
        if key == "florida":
            return rs.motif("s_flood", w, h)
        return rs.motif(story["scene"], w, h)
    # motif (sketsa 1): ilustrasi geometris rapi v1r
    return rs.motif(story["scene"], w, h)


# ------------------------------------------------------------------ panel koran
def draw_panel_v4(im, x, y, w, h, story, cfg, is_hero):
    """Satu panel koran: [gambar (+caption hero)] [kicker merah]
    [judul serif tebal] [ringkasan serif]. Border tipis navy.
    Mengembalikan warna atas gambar (untuk audit tetangga)."""
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
    pic = tile_image(story, w, img_h, cfg["tile"])
    # caption hero di bawah gambar (ala rank 1: bar gelap di bawah hero)
    if is_hero and story.get("caption"):
        cap = ImageDraw.Draw(pic)
        f_cap = F(BOLD, 9)
        cap.rectangle([0, img_h - 16, w, img_h], fill=NAVY)
        cap.text((6, img_h - 8), story["caption"], font=f_cap,
                 fill=GOLD, anchor="lm")
    im.paste(pic, (x, y))
    d.rectangle([x, y, x + w, y + h], outline=NAVY, width=1)
    yy = y + img_h + 3
    d.text((x + 5, yy), kicker, font=f_kick, fill=RED)
    yy += kick_h
    for ln in tw:
        d.text((x + 5, yy), ln, font=f_title, fill=INK)
        yy += (cfg["hero_tpt"] if is_hero else cfg["card_tpt"]) + 3
    for ln in s_lines:
        d.text((x + 5, yy), ln, font=f_sum, fill=INK)
        yy += (cfg["hero_spt"] if is_hero else cfg["card_spt"]) + 3
    px = pic.crop((w // 2 - 10, 2, w // 2 + 10, 8))
    cols = list(px.getdata())
    avg = tuple(sum(c[i] for c in cols) // len(cols) for i in range(3))
    return avg


# ------------------------------------------------------------------ chrome koran
def draw_kicker_masthead_deck(d, W, y, total):
    """Kicker + masthead serif + deck merah italic. Kembalikan y baru."""
    f_kick = F(BOLD, 10)
    d.text((12, y), "THE WORLD IN ONE DAY", font=f_kick, fill=RED)
    right = f"FRIDAY'S NEWS · ONE PAGE · {total} STORIES · 6 CONTINENTS"
    d.text((W - 12, y), right, font=f_kick, fill=NAVY, anchor="ra")
    y += 13
    f_mast = F(DISPLAY_B, 46)
    d.text((W // 2, y), "Friday 20 November 2026", font=f_mast,
           fill=INK, anchor="ma")
    y += 46
    d.line([(12, y + 2), (W - 12, y + 2)], fill=NAVY, width=2)
    y += 5
    f_deck = F(SERIF_IT, 13)
    for ln in DECK_LINES:
        d.text((W // 2, y), ln, font=f_deck, fill=RED, anchor="ma")
        y += 17
    return y  # y = bawah deck


def draw_numbers_strip_v4(d, W, y, style):
    """Strip 6 angka: border tipis + bilah emas; angka merah serif
    (sketsa 1, ala rank 1) atau navy sans (sketsa 2/3)."""
    h = 50
    widths = [166, 166, 166, 166, 166, 170]
    x = 12
    for i, (num, cap, region) in enumerate(NUMBERS):
        cw = widths[i]
        x0, x1 = x, x + cw
        d.rectangle([x0, y, x1, y + h], fill=WHITE, outline=NAVY, width=1)
        d.rectangle([x0, y + h - 3, x1, y + h], fill=GOLD)
        if style == "red":
            f_n = F(SERIF_B, 22)
            col = RED
        else:
            f_n = F(BOLD, 22)
            col = NAVY
        d.text(((x0 + x1) // 2, y + 3), num, font=f_n, fill=col,
               anchor="ma")
        f_c = F(REG, 9)
        lines = rs.wrap(d, cap, f_c, cw - 12)
        assert len(lines) <= 2, f"caption strip pecah: {cap}"
        yy = y + 30
        for ln in lines:
            d.text(((x0 + x1) // 2, yy), ln, font=f_c, fill=INK,
                   anchor="ma")
            yy += 11
        x = x1
    return y + h


def draw_region_chips(d, W, y, counts):
    """Strip region ala rank 1: chip warna + angka putih. Tinggi 20."""
    h = 20
    disp = {"ASIA": "ASIA-PAC"}
    x = 12
    seg_w = (W - 24) // 7
    for i, r in enumerate(rs.REGION_ORDER):
        x0 = x + i * seg_w
        x1 = x0 + seg_w if i < 6 else W - 12
        d.rectangle([x0, y, x1, y + h], fill=REGION_COLORS[r])
        f = F(BOLD, 10)
        d.text(((x0 + x1) // 2, y + h // 2),
               f"{disp.get(r, r)} {counts[r]}", font=f, fill=WHITE,
               anchor="mm")
    return y + h


def draw_region_bar(d, W, y, counts, total):
    """Strip region ala rank 2: kotak 'N STORIES' + segmen warna.
    Reuse render_sketches.draw_region_section (tinggi 36)."""
    return rs.draw_region_section(d, W, y, counts, total)


def draw_map_v4(im, x, y, mw, mh, panels, hero_city, dark, pin_fill):
    """Peta dunia + pin bernomor (HANYA 13 cerita drawn; brief TIDAK
    ditandai). dark=True: laut navy gelap + pin merah (rank 1/3);
    dark=False: laut terang + pin emas (rank 2)."""
    d = ImageDraw.Draw(im)
    sea = NAVY if dark else (198, 220, 236)
    d.rectangle([x, y, x + mw, y + mh], fill=sea, outline=NAVY, width=1)
    mtmp = Image.new("RGB", (mw - 2, mh - 2), sea)
    md = ImageDraw.Draw(mtmp)
    for poly in rv.CONTINENTS:
        pts = [rv.project(lon, lat, 0, 0, mw - 2, mh - 2)
               for lon, lat in poly]
        md.polygon(pts, fill=rv.LAND, outline=(180, 160, 115))
    im.paste(mtmp, (x + 1, y + 1))
    md = ImageDraw.Draw(im)
    fp = F(BOLD, 8)
    placed = []
    skipped = []

    def place(px, py, r):
        for (qx, qy, _qr) in placed:
            if ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5 < 12:
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
            if place(px, py, 9):
                md.polygon(rv.star_points(px, py, 9, 4), fill=GOLD,
                           outline=NAVY)
            continue
        if not place(px, py, 7):
            skipped.append((city, p["num"]))
            continue
        md.ellipse([px - 7, py - 7, px + 7, py + 7], fill=pin_fill,
                   outline=WHITE, width=1)
        mark = str(p["num"])
        tw = md.textlength(mark, font=fp)
        md.text((px - tw / 2, py - 5), mark, font=fp, fill=WHITE)
    return skipped


def draw_briefs_v4(im, x, y, w, h, briefs, font_pt=10):
    """MORE STORIES 3 kolom, nomor merah + kota navy + teks.
    Tiap brief MAKS 2 baris (di-assert; teks sudah dipangkas di data).
    Slack dibagi rata (seperti v1r)."""
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


def draw_datecheck_redbox(d, W, y):
    """Kotak DATE CHECK ber-border MERAH (ala rank 1–3), 2 baris 9pt.
    Mengembalikan y bawah box."""
    f = F(BOLD, 9)
    pref = "DATE CHECK — "
    pref_w = d.textlength(pref, font=f)
    lines = rs.wrap(d, DATECHECK_REST, f, W - 48 - pref_w)
    assert len(lines) <= 3, f"datecheck pecah >3: {lines}"
    box_h = 8 + len(lines) * 13 + 6
    d.rectangle([12, y, W - 12, y + box_h], fill=CARD_BG,
                outline=RED, width=2)
    yy = y + 7
    for j, ln in enumerate(lines):
        if j == 0:
            total_w = pref_w + d.textlength(ln, font=f)
            x0 = (W - total_w) // 2
            d.text((x0, yy), pref, font=f, fill=RED)
            d.text((x0 + pref_w, yy), ln, font=f, fill=NAVY)
        else:
            d.text((W // 2, yy), ln, font=f, fill=NAVY, anchor="ma")
        yy += 13
    return y + box_h


def audit_footer(path):
    """Crosscheck programatik: baris tinta terbawah + margin kertas."""
    im = Image.open(path).convert("RGB")
    W, H = im.size
    paper = (246, 241, 231)
    ink_bottom = 0
    px = im.load()
    for yy in range(H - 1, -1, -1):
        row_ink = False
        for xx in range(0, W, 2):
            p = px[xx, yy]
            if abs(p[0] - paper[0]) + abs(p[1] - paper[1]) + abs(p[2] - paper[2]) > 60:
                row_ink = True
                break
        if row_ink:
            ink_bottom = yy
            break
    return ink_bottom, H - 1 - ink_bottom


# ------------------------------------------------------------------ layout
# Gap antar section (px) — dicatat untuk NOTE.md (bandingkan v3: 4–6 px).
# Urutan: [deck→angka, angka→region, region→hero, hero→kartu,
#          kartu→band, band→datecheck]
GAPS_S1 = [12, 12, 12, 12, 12, 12]   # Koran Serif: space paling lega
GAPS_S2 = [10, 10, 10, 10, 10, 10]   # Tile Berani
GAPS_S3 = [10, 10, 10, 10, 10, 10]   # Grafis Bersih
PANEL_GAP = 10   # gap antar kartu/hero (v3: 4 px)
ROW_GAP = 10     # gap antar baris kartu (v3: 4 px)
HERO_H = 178
CARD_H = 144


def build_sketch(cfg, path):
    W = 1024
    im = Image.new("RGB", (W, 1024), PAPER)
    d = ImageDraw.Draw(im)
    total = cfg["total"]
    brief_keys = BRIEFS_20_KEYS + (["slot"] * 3 if total == 36 else [])
    panels = [dict(p) for p in HEROES + CARDS]
    # renumber tampil: hero/kartu sudah 1–13; brief 14…
    briefs = []
    for i, key in enumerate(brief_keys):
        if key == "slot":
            city, region, text = AMERICA_SLOTS[i - len(BRIEFS_20_KEYS)]
        else:
            city, region, text = BRIEF_POOL[key]
        briefs.append((14 + i, city, region, text))
    counts = rs.region_counts(panels, briefs)
    assert sum(counts.values()) == total, \
        f"total {sum(counts.values())} != {total}"
    gaps = cfg["gaps"]

    y = 12
    y = draw_kicker_masthead_deck(d, W, y, total)
    y += gaps[0]
    y = draw_numbers_strip_v4(d, W, y, cfg["numbers"])
    y += gaps[1]
    if cfg["region"] == "chips":
        y = draw_region_chips(d, W, y, counts)
    else:
        y = draw_region_bar(d, W, y, counts, total)
    y += gaps[2]
    tops = {}
    hero_w = (W - 24 - 2 * PANEL_GAP) // 3
    for i, st in enumerate(panels[:3]):
        xx = 12 + i * (hero_w + PANEL_GAP)
        tops[(0, i)] = draw_panel_v4(im, xx, y, hero_w, HERO_H, st, cfg,
                                     True)
    y += HERO_H + gaps[3]
    card_w = (W - 24 - 4 * PANEL_GAP) // 5
    for r in range(2):
        for c in range(5):
            st = panels[3 + r * 5 + c]
            xx = 12 + c * (card_w + PANEL_GAP)
            tops[(1 + r, c)] = draw_panel_v4(im, xx, y, card_w, CARD_H,
                                             st, cfg, False)
        y += CARD_H + (ROW_GAP if r == 0 else 0)
    y += gaps[4]
    band_y = y
    # band (peta + brief) = sisa sampai DATE CHECK + sources + margin
    band_h = 1024 - band_y - gaps[5] - 46 - 14 - 12
    assert band_h >= 190, f"band terlalu pendek: {band_h}"
    map_w = 400
    map_h = band_h - 18
    dark = cfg["map_bg"] == "dark"
    pin_fill = RED if cfg["pin"] == "red" else GOLD
    skipped = draw_map_v4(im, 12, band_y, map_w, map_h, panels,
                          "Gopalpur", dark, pin_fill)
    f_lg = F(BOLD, 8)
    disp = {"ASIA": "ASIA-PAC"}
    legend = " · ".join(
        f"{disp.get(r, r)} {counts[r]}" for r in rs.REGION_ORDER)
    d.text((12 + map_w // 2, band_y + map_h + 3), legend, font=f_lg,
           fill=NAVY, anchor="ma")
    bx = 12 + map_w + 12
    bw = W - 12 - bx
    f_bh = F(BOLD, 12)
    d.text((bx, band_y), "MORE STORIES FROM 20 NOVEMBER", font=f_bh,
           fill=NAVY)
    draw_briefs_v4(im, bx, band_y + 20, bw, band_h - 20, briefs,
                   font_pt=cfg["brief_pt"])
    y = band_y + band_h + gaps[5]
    y = draw_datecheck_redbox(d, W, y)
    f2 = F(REG, 9)
    d.text((W // 2, y + 4), DATECHECK_SOURCES, font=f2,
           fill=(90, 90, 90), anchor="ma")
    y = y + 4 + 11
    im.save(path)
    top_bad = rs.check_top_colors(tops)
    ink_bottom, margin = audit_footer(path)
    return {"total": total, "counts": counts, "band_h": band_h,
            "map_skipped": skipped, "top_bad": top_bad,
            "ink_bottom": ink_bottom, "bottom_margin": margin,
            "gaps": gaps, "panel_gap": PANEL_GAP, "row_gap": ROW_GAP,
            "hero_w": hero_w, "card_w": card_w}


SKETCHES = {
    "v4-1": {"tile": "motif", "numbers": "red", "region": "chips",
             "map_bg": "dark", "pin": "red", "total": 36,
             "gaps": GAPS_S1, "hero_tpt": 16, "hero_spt": 11,
             "card_tpt": 13, "card_spt": 10, "brief_pt": 10,
             "file": "sketch-v4-1-koran-serif.png"},
    "v4-2": {"tile": "giant", "numbers": "navy", "region": "bar",
             "map_bg": "light", "pin": "gold", "total": 33,
             "gaps": GAPS_S2, "hero_tpt": 16, "hero_spt": 11,
             "card_tpt": 14, "card_spt": 10, "brief_pt": 10,
             "file": "sketch-v4-2-tile-berani.png"},
    "v4-3": {"tile": "abstract", "numbers": "navy", "region": "chips",
             "map_bg": "dark", "pin": "red", "total": 36,
             "gaps": GAPS_S3, "hero_tpt": 16, "hero_spt": 11,
             "card_tpt": 13, "card_spt": 10, "brief_pt": 10,
             "file": "sketch-v4-3-grafis-bersih.png"},
}


if __name__ == "__main__":
    out = "/home/hatch/workspace/makefun/news-image-20261120/sketches-v4"
    os.makedirs(out, exist_ok=True)
    results = {}
    for name, cfg in SKETCHES.items():
        path = f"{out}/{cfg['file']}"
        res = build_sketch(cfg, path)
        assert not res["top_bad"], f"{name}: pelanggaran warna atas {res['top_bad']}"
        assert res["ink_bottom"] <= 1012, f"{name}: tinta sampai y={res['ink_bottom']}"
        assert res["bottom_margin"] >= 12, f"{name}: margin bawah cuma {res['bottom_margin']}px"
        # determinisme: render ulang ke /tmp, sha256 harus sama
        import hashlib
        h1 = hashlib.sha256(open(path, "rb").read()).hexdigest()
        build_sketch(cfg, "/tmp/v4-determinism-check.png")
        h2 = hashlib.sha256(open("/tmp/v4-determinism-check.png", "rb").read()).hexdigest()
        assert h1 == h2, f"{name}: tidak deterministik"
        res["sha256"] = h1
        results[name] = res
        print(name, json.dumps(res, default=str))
    print("OK")
