#!/usr/bin/env python3
"""compose_v4.py — ENTRY V2 ni20 (builder daemon 21 Nov 2026 ~17:40 WIB).

REV1 (revisi manual 21 Nov 2026 ~18:49 WIB, atas perintah Kevin +
OK eksplisit pakai script): HANYA 4 perubahan visual, isi/angka/teks
31 cerita TIDAK berubah — (1) border frame hero/kartu dihapus;
(2) label sumber jadi strip HITAM lebih lebar (min 100px); (3) segmen
bar region EUROPE/AMERICAS diperbesar; (4) pin peta r=10 + warna per
region. Lihat REV-NOTE.md di folder ini. Folder ini SALINAN repo-v4
(tanpa .git); repo-v4/ asli TIDAK disentuh.

REV2 (revisi manual 21 Nov 2026 ~19:05 WIB, lanjutan rev1, atas
perintah Kevin): HANYA 2 perubahan visual — (1) angka pin peta 10pt
-> 14px, pin r=10 -> r=12 (angka "13" 14px lebar 14,9px; muat di
r=12, offset teks -10 diukur supaya tinta digit terpusat); (2) 2 kotak
legenda bawah peta TIDAK lagi hitam (tidak kelihatan di atas laut
navy) -> TAN (MAP_HEADER_BG, sama seperti strip header peta), teks
8pt -> 14px, kotak 16px -> 26px. Lihat REV-NOTE.md di folder ini.
repo-v4-rev1/ TIDAK disentuh.

REV3 (revisi manual 21 Nov 2026 ~20:00 WIB, lanjutan varian foto, atas
perintah Kevin + audit konten 31 cerita): HANYA 3 perbaikan — (1) strip
sumber di tiap gambar HITAM -> TAN (MAP_HEADER_BG, sama seperti kotak
legenda peta), teks WHITE -> NAVY; (2) banner merah TIDAK BOLEH
mengulang kata headline/deskripsi — banner = NILAI (8 dari 13 banner
diubah: hero 2 "STRIKES 01:25" -> "01:25", hero 3 "NO FOSSIL DEAL" ->
"NO NEW TEXT", kartu 5 "TROOPS IN" -> "KATAIB", kartu 6 "CREST 18.6"
-> "18.6 FT", kartu 7 "100 CITIES" -> "100+", kartu 8 "TAIEX -6.4%"
-> "-6.4%", kartu 11 "NIKKEI -4.1%" -> "-4.1%", kartu 12 "FIRST OIL"
-> "20K BPD"); (3) banner 12pt -> 14pt, kotak 20px -> 24px (padding
teks +16 -> +12 supaya "175* RUNS" muat <=81px), kicker hero 11pt ->
12pt + kartu 9pt -> 12pt. Karena banner 24px: "ODISHA" hero 1 y 21
-> 25, globe COP31 gy 50 -> 54, plakat Italia y 20 -> 24. "(Reuters)"
/ "(Sumber)" TIDAK dihapus saat itu (poin 5 masih terbuka) — DIHAPUS
 di REV9d (Kevin 22 Nov 05:04 WIB). Lihat REV-NOTE.md di folder ini.
di folder ini. repo-v4-foto/ TIDAK disentuh.

Dasar: repo-v4-trial/render_trial.py (revisi-10 Kevin, sha entry
6ec960f8...) + change list loss report V2 (b3 kartu keras, b4 DATE CHECK,
a2 hygiene tanggal, a1 PNG optimize). Yang berubah vs trial r10:
(1) 4 kartu diganti — #5 SCO -> Irak (Jurf al-Sakhar), #7 APEC -> Italia
(mogok CGIL), #10 GTA -> Polandia (rudal Kh-101), #12 Prabowo -> Kenya
(minyak Turkana); SCO/APEC/Prabowo turun jadi brief #15/#16/#17;
Brisbane/Jakarta/Loyalty HAPUS dari halaman. (2) Strip angka 19.000
(YouTube) -> 1M+ (mogok Italia). (3) DATE CHECK + klausa "Not yet".
(4) Bar region: EUROPE 7, AMERICAS 5, ASIA-PACIFIC 9, MIDEAST 3,
AFRICA 3, OCEANIA 1, WORLD 3 = 31. (5) Painter baru poland/iraq/italy/
kenya (gaya datar, satu ide besar, selaras kartu 08/09/11).
Detail + verifikasi: repo-v4/BUILD-NOTE.md, STORIES.md.


REVISI-3 (Kevin 21 Nov 15:08 WIB): banner merah topik di kiri atas
tiap gambar DIPERBESAR (12px/8pt -> 16px/11pt) + BORDER PUTIH 2px
(outline di dalam kotak, seperti pin peta). Posisi + warna merah tetap.
HANYA gambar.

REVISI-4 (Kevin 21 Nov 15:10 + 15:12 WIB): (1) label sumber KEMBALI
ke ATAS gambar, kanan bawah (semua 13), DIPERBESAR (9pt -> 11pt,
kotak 15px, outline NAVY 1px); hero 1 lift 10px supaya tidak menutupi
"BAY OF BENGAL". (2) banner merah LEBIH BESAR lagi: 11pt -> 12pt
("COP31: FINAL DAY" 111px < 115; "SCO FORUM" 79px — assert kartu
78 -> 81, patch warna-atas di x 82). (3) teks BAR REGION BOLD +
LEBIH BESAR: SS700 9pt -> SS800 12pt ("ASIA-PACIFIC 10" 84,9px <
segmen 140px; tinggi bar tetap 16px, layout lain tidak berubah).
HANYA gambar.

REVISI-6 (Kevin 21 Nov 15:20-15:21 WIB): (1) teks "VI" kartu 10
(GTA) pindah ke TENGAH tile (dulu kiri, (0.08w, 0.50h) anchor "lm"
di p_gta sketches-v4/render_v4_1r.py — modul bersama TIDAK diubah;
salinan lokal p_gta_r6 di file ini, anchor "mm" di (w/2, h/2),
ukuran tetap 34pt = max(18, int(h*0.55))). (2) banner hero 1
"300K EVACUATED" 12pt -> 13pt (diukur: box 114px <= 115; 14pt =
121px tidak muat; teks lengkap dipertahankan, TIDAK disingkat jadi
"300K") — laporan Kevin "Teks Cyclone Akva ga keliatan": banner
hero 1 terlalu kecil di ukuran tampil HP. Tinggi kotak tetap 16px
("ODISHA" mulai y=16), outline putih tetap 2px. HANYA gambar.

REVISI-7 (Kevin 21 Nov 15:29 + 15:30 WIB): (1) baris footer Sources
di bawah DATE CHECK (fungsi draw_sources_ref) DIGEDEIN: teks kiri +
kanan 7pt -> 9pt (diukur dulu: kiri 536,0px + kanan 395,5px = 931,5px
< 976px tersedia, celah 44,5px; 10pt tidak muat). Isi teks TIDAK
diubah; SRC_Y 999 -> 997 supaya margin bawah tetap 15px (font lebih
tinggi 2px). (2) banner hero 1 "300K EVACUATED" DIGEDEIN lagi:
13pt -> 14pt; teks disingkat "300K" (14pt = 47px, muat; bentuk
lengkap 14pt = 121px > batas 115px). HANYA gambar.

REVISI-9 (Kevin 21 Nov 15:32-15:34 WIB): (1) "teks header" = baris
paling atas halaman ("THE WORLD IN ONE DAY" kiri + "FRIDAY'S NEWS ·
ONE PAGE · 31 STORIES · 6 CONTINENTS" kanan) DIGEDEIN: kicker
10pt -> 12pt, kiri + kanan ukuran sama supaya seimbang; tetap 1
baris, tidak menabrak judul. (2) banner hero 1 "300K" 14pt -> 11pt
(perintah Kevin "Cyclone 11px"; teks tetap "300K", merah, border
putih 2px). Banner lain TIDAK berubah (12pt, kartu 11 tetap 11pt).
HANYA gambar.

REVISI-10 (Kevin 21 Nov 15:37 WIB, "Tinggi 20 px coba" + "tambah
14px" = teks header -> 14pt): (1) kotak MERAH (banner) tinggi 16px
-> 20px, semua 13 banner; teks TETAP 12pt (hero 1 "300K" tetap 11pt,
kartu 11 tetap 11pt), lebar kotak tetap (teks + 16px), border putih
2px tetap. Karena banner lebih tinggi 4px, isi panel hero 1 digeser:
"ODISHA" y 16 -> 21, "INDIA" y 36 -> 41 (banner 20px menutupi
puncak "ODISHA" bila di y=16); titik/Gopalpur tidak digeser (sudah
di bawah). Ilustrasi di bawah banner (ujung busur rudal Kyiv,
atap rumah Florida, pemukul kriket) sedikit lebih tertutup — itu
overlay yang disengaja, bukan teks, DITERIMA. (2) kotak PUTIH
(label sumber) tinggi 15px -> 20px, semua 13 label; teks TETAP
NAVY 11pt BOLD, outline NAVY 1px, inset 2px, posisi kanan bawah
tetap (hero 1 lift 10 tetap: label y 63-83, bawah tetap 83, celah
3px ke "BAY OF BENGAL" tinta y 86-90 TIDAK berubah). Karena label
lebih tinggi 4px (atas label kartu y 45 -> 40), garis grafik kartu
08/09/11 DIGESER ke zona bersih: p_chart_ref + p_chart_gold_r8
titik dirapatkan ke y 22-38 (tinta garis) supaya garis UTUH —
tidak menabrak banner bawah (y=20) maupun label atas (y=40).
(3) teks "FINAL DAY · DEADLOCK" kartu putih hero 3 digeser +5px ke
atas (ky1-16 -> ky1-21): tinta lama y 73-76 (diukur) bertabrakan
dengan label 20px (atas y=73); kini tinta y 68-71, celah 2px.
(4) teks header masthead 12pt -> 14pt (kiri + kanan): diukur dulu
— 14pt di y=10 tinta bawah y=26, celah ke garis (y=27) = 0
(assert GAGAL); teks digambar di y=8 (tinta y 13-24, celah 2px),
garis tetap y=27, judul tidak digeser. Lebar: kiri 147px + kanan
350px, muat 1 baris. HANYA gambar.

REVISI-2 (Kevin 21 Nov 15:06 WIB): (A) hapus 2 baris bawah MORE
(brief lama #20 Tokyo, #21 Sydney, #28 Saipan, #29 Hong Kong,
#36 Washington) -> 31 cerita, MORE 18 brief, nomor ulang 14-31;
ruang bebas 32px (2 baris x 16px) ke gambar kartu 2x5 (46->62px).
(B) label sumber putih pindah ke kanan bawah panel teks untuk
SEMUA kartu DAN hero (hero tadinya kiri bawah). HANYA gambar.

Dasar: render_ref7.py — ni20 v4 REF-7: revisi sketsa-ref-6 dari 1 koreksi Kevin
(23:14 WIB) — "Bukan pin Zet, tapi teks header yang ada di peta".

Dasar: render_ref6.py (SEMUA dipertahankan kecuali yang di bawah ini).
REF-7 — SATU-SATUNYA PERUBAHAN (klarifikasi Kevin 23:14 WIB): teks
header peta "Pins 1–13 (Lead & Feature)" (REG 9pt abu-abu) TIDAK
TERBACA di ukuran tampil HP (peta ~110px lebar -> noda abu-abu),
sementara "WHERE IT HAPPENED" (BOLD 11pt NAVY) masih terbaca.
Perbaikan: teks pins jadi BOLD 12pt NAVY. Diukur: judul 103,0px +
note 140,6px + gap 6px = 249,6px < 276px tersedia — teks LENGKAP
muat, TIDAK dipersingkat. Satu baseline dipertahankan (assert).
Pin TETAP persis ref-6 (posisi + offset + r=7 + angka 8pt).
Instruksi revisi sebelumnya (garis penunjuk, pin ke kota asli,
perbesar pin Lead) DICABUT parent — tidak dikerjakan.

Dasar: render_ref5.py (SEMUA dipertahankan kecuali yang di bawah ini).
REF-6 — SATU-SATUNYA PERUBAHAN (koreksi Kevin 23:05 WIB; diagnosis
parent TERVERIFIKASI di peta 2x/3x + kode):
1. Bintang emas pin 1 (Gopalpur) DIHAPUS — cabang `hero_city` -> bintang
   di `draw_map_ref` dihapus; SEMUA 13 pin kini lingkaran merah bernomor
   putih (r=7, outline putih), termasuk pin 1 "1". Di ref-5 pin 1
   digambar sebagai bintang emas TANPA angka, dan legenda peta tidak
   menjelaskan bintang itu — jadi pin 1 tidak dikenali.
2. Jarak minimum antar pin 12px -> 18px (pusat ke pusat; lingkaran r=7
   -> celah nyata 4px, bukan sekadar tidak bertabrakan). Di ref-5 pin 2
   (Kyiv) dan pin 3 (Antalya) hanya 13,5px (tanpa offset — lolos ambang
   12px) sehingga lingkarannya tumpang tindih; pin 7 dan pin 12
   (sama-sama Shenzhen) hanya 12,8px. Daftar kandidat offset diperluas
   dan diurutkan agar perpindahan sekecil mungkin, diutamakan lurus
   (utara/selatan/timur/barat) supaya bujur/lintang tetap terjaga.
   Offset yang dipakai (simulasi terverifikasi, 0 pin hilang, semua
   pasangan >=18px): #3 Antalya (0,+12); #5 New Delhi (0,-12);
   #8 Taipei (+14,0); #11 Tokyo (0,-12); #12 Shenzhen (0,+20);
   #13 Las Vegas (0,+20). Pasangan terdekat setelah perbaikan:
   10-13: 18,1px; 7-12: 20,0px.

Riwayat ref-5/ref-4 (detail lengkap di render_ref5-NOTE.md dan
render_ref4-NOTE.md — hanya diringkas di sini):

Riwayat ref-3 (dipertahankan, hanya diringkas di sini):

Koreksi visual Kevin 21:50 WIB (semua sudah diverifikasi parent
berdampingan dengan referensi — /tmp/cc_masthead.png, cc_mapatas.png,
cc_herotext.png):
(1) MARGIN BAWAH JUDUL — deck merah terlalu mepet di bawah judul
    ("y" di "Friday" hampir kena teks merah). Jarak judul -> deck
    diperbesar dari ~9px menjadi ~16-18px (offset deck +4 -> +12);
    semua section di bawah masthead digeser +4px (strip 129->133,
    chips 184->188, hero 208->212, peta 208->212, kartu 521->525,
    MORE 792->796, DATE CHECK 943->947, Sources 990->994).
(2) WHERE IT HAPPENED SELARAS — chip judul yang menembus border atas
    peta DIHAPUS (perintah Kevin 21:50 WIB menggantikan permintaan chip
    18:54 WIB). "WHERE IT HAPPENED" (kiri, BOLD 11pt NAVY) dan
    "Pins 1-13 (Lead & Feature)" (kanan, REG 9pt GRAY) kini pada SATU
    baseline yang sama (tengah strip header tan), seperti referensi.
    Whitelist no-overlap untuk chip peta DIHAPUS (tidak ada lagi kotak
    yang sengaja bersinggungan — check_no_overlap_ref4 lokal, tanpa
    ALLOW_OVERLAP).
(3) ISI BERITA JANGAN KOSONG — ringkasan hero 1-3 dipanjangkan menjadi
    3 BARIS (dulu 1 baris, menyisakan area kosong besar di bawah teks),
    HANYA dari fakta STORIES.md yang terverifikasi. "Schools shut"
    SENGAJA TIDAK dipakai untuk hero 1 (fakta itu milik banjir Florida,
    kartu 6 — STORIES.md) meskipun contoh di brief menyebutnya.
(4) WARNA PANEL TEKS — area teks hero/kartu/brief + strip memakai latar
    hampir putih (251,250,245) seperti referensi (diukur langsung dari
    piksel referensi: hero text (251,250,245), strip (251,250,245),
    MORE box (244-250,243-247,238-242)); kertas halaman tetap krem
    (246,241,231). DATE CHECK tidak diubah (fill CARD_BG (250,247,240)
    sudah hampir putih, sama dengan referensi (252,248,239)).

Perbaikan isi dari verifikasi tanggal (laporan
verifikasi-tanggal-ref2.md; perintah "jangan ubah isi cerita" DICABUT
untuk 4 hal ini):
(5) #3 COP31 (HERO 3) SALAH TANGGAL — draf penghilang fossil fuels
    terbit Kamis 19 Nov. DIBINGKAI ULANG: judul "COP31 enters its
    final day" (1 baris, 20px Gelasio 700); ringkasan tekankan Jumat
    (pembicaraan memasuki hari terakhir, penghilangan masih ada di
    draf terbaru — UN News + phys.org 20 Nov, Reuters 20 Nov).
    Klaim "final text due midnight" DIHAPUS (jadwal masa depan).
(6) #28 Cyclone Xavier (brief) SALAH TANGGAL — puncak 17 Nov, shelter
    16 Nov, status darurat 19 Nov; tidak ada peristiwa Xavier Jumat.
    DIGANTI: "Northern Marianas vote in governor runoff." (SAIPAN,
    OCEANIA) — runoff election Jumat 20 Nov 2026, diverifikasi dari
    Commonwealth Election Commission (votecnmi.gov.mp: "November 20,
    2026 ELECTION DAY — 2026 Run-Off Election Day", polls 07:00–19:00
    ChST) + Wikipedia + liputan live Marianas Press 20 Nov (Torres
    54,8% vs Attao 45,2%). Reframe aksi Jumat malam #30 GAGAL
    diverifikasi (lihat (7)); kandidat lain yang DITOLAK untuk #28:
    Tonga state of emergency (diumumkan 19 Nov), Guam GEC (sertifikasi
    Rabu 18 Nov), Northern Marianas military consultations (rapat 18
    Nov, pertama terbit 19 Nov), RNZ finance boss (pengunduran diri
    2 Okt — artikel 20 Nov hanya detail baru).
(7) #30 Anti-Takaichi (brief) SALAH TANGGAL — aksi 13.000 orang itu
    Kamis 19 Nov. REFRAME ke aksi Jumat malam GAGAL: satu-satunya
    sumber (redhot.sg, ~9.000 orang, WE WANT OUR FUTURE) hampir pasti
    menulis ulang peristiwa JUMAT 30 OKTOBER (kata-kata identik dengan
    deskripsi video YouTube 31 Okt; tidak ada sumber kedua untuk
    20 Nov; semua kabel lain melapor aksi 19 Nov 13.000 orang).
    DIGANTI: "China holds lending rates for 18th month." (BEIJING,
    ASIA) — PBOC menahan 1-yr LPR 3,00% + 5-yr 3,50% bulan ke-18
    berturut-turut, diputuskan di review JUMAT 20 Nov (Reuters 19 Nov:
    "at Friday's review"; Baha Breaking News timestamp 11/20/2026
    03:07; Morval Universal 20 Nov 2026). Kandidat lain yang DITOLAK
    untuk #30: Modi FICCI (pidato 19 Nov, bukan 20 Nov), EPFO 90%
    (diputuskan 19 Nov — hanya dilaporkan 20 Nov, lebih lemah dari LPR
    yang diputuskan Jumat).
(8) Strip angka #19: label "$92.77 Brent crude, Friday close" SALAH
    ($92.77 = snapshot Jumat 04:04 GMT, BUKAN close). Label jadi
    "Brent crude, Friday morning" (angka tetap $92.77).
(9) #25 Harris-Macron (brief) TIDAK TERVERIFIKASI — PERTAHANKAN apa
    adanya, tandai di NOTE: cek ulang saat build (~00:30 WIB).
(10) #14 Kyiv brief — tanggal BENAR tapi duplikat hero #2 (gelombang
    lanjutan serangan yang sama). PERTAHANKAN, dicatat sebagai
    duplikat sadar.

Region tetap: EUROPE 5 · AMERICAS 6 · ASIA-PACIFIC 12 · MIDEAST 2 ·
AFRICA 2 · OCEANIA 5 · WORLD 4 = 36 (#28 Saipan tetap OCEANIA,
#30 Beijing tetap ASIA). Total 36 (35 nyata + #36 placeholder).
BUKAN entry final, BUKAN submit, BUKAN repo.

REV9 (Kevin Gas 22 Nov 04:40 WIB — legibilitas saja, HANYA ini):
(1) DATE CHECK 10 -> 12pt, tetap 2 baris di kotak 38px; teks dipangkas
(daftar "not Friday's news" 18 -> 12 item; "Mercury orbit entry" ->
"Mercury entry"; "20 November" -> "20 Nov") — klaim penutup + klausa
"Not yet" tidak berubah isinya; 31 cerita + semua angka SAMA.
(2) Brief MORE STORIES 11 -> 12pt, tetap 1 baris/kolom 312px; 5 brief
dipangkas katanya (#15, #26, #28, #29, #31 — lihat BRIEFS_REF),
fakta/angka tetap. Hero, kartu, peta, bar region, warna, layout
TIDAK berubah. Alasan: crosscheck rev8 membuktikan juri (model
vision) salah baca teks 10pt ("Very story…", "BELING") meski
pikselnya benar.

REV9d (Kevin 22 Nov 05:04 WIB — hapus dobel sumber): "(Sumber)" dihapus
dari deskripsi 13 kartu (3 hero + 10 feature) — nama sumber dobel dengan
chip navy di gambar (chip tetap, itu yang membawa nama sumber). Brief
MORE STORIES 14-31 + footer "Sources:" TIDAK disentuh (satu-satunya
atribusi di sana). Fakta/angka 31 cerita SAMA; hanya "(...)" di ujung
deskripsi yang hilang.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # modul vendored (render_v4, render_variants,
# render_v4_1r*, render_sketches) ada di root repo ini; modul-modul itu
# sendiri masih menyisipkan path absolut workspace (isi identik) — build
# di mesin ini memakai salinan workspace, salinan repo untuk reproduksi.

from PIL import Image, ImageDraw, ImageFont

import render_v4 as v4
import render_variants as rv
import render_v4_1r as r1
import render_v4_1r3 as r13
import render_v4_1r4 as r14
import render_sketches as rs

# Los Angeles belum ada di rv.PLACES (pin aproksimasi #10).
rv.PLACES["Los Angeles"] = (-118.2, 34.1)
# V2 (b3): kota pin kartu baru — koordinat peristiwa, bukan ibu kota.
rv.PLACES["Nowy Lipowiec"] = (22.7, 50.5)   # desa jatuhnya Kh-101
rv.PLACES["Jurf al-Sakhar"] = (44.2, 32.9)  # ~60 km barat daya Baghdad
rv.PLACES["Rome"] = (12.5, 41.9)
rv.PLACES["Milan"] = (9.2, 45.5)  # pin Italia: Milan, bukan Roma —
# pin Roma bertabrakan dengan klaster London/Kyiv (offset -14,0 lalu
# London ikut bergeser -12); Milan salah satu kota mars terbesar dan
# posisinya lolos tanpa offset.
rv.PLACES["Turkana"] = (35.7, 2.3)          # Lokichar, South Lokichar

# --- font (spesifikasi Kevin 21:37 WIB; diunduh dari Google Fonts, OFL) --
# Gelasio-Bold/Italic variable + SourceSans3 variable di-instance ke
# static weight dgn fontTools varLib.instancer (lihat fonts/; bobot
# terverifikasi via ink coverage: SS3 400=0,121 < 600=0,166 < 700=0,202
# < 800=0,216; Gelasio 700=0,185 vs Italic 400=0,133).
FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "fonts")
GEL700 = os.path.join(FONTS_DIR, "Gelasio-700.ttf")       # judul 700
GEL700_IT = os.path.join(FONTS_DIR, "Gelasio-700Italic.ttf")
GEL_IT = os.path.join(FONTS_DIR, "Gelasio-Italic.ttf")    # deck italic
SS400 = os.path.join(FONTS_DIR, "SourceSans3-400.ttf")    # isi 400
SS600 = os.path.join(FONTS_DIR, "SourceSans3-600.ttf")
SS700 = os.path.join(FONTS_DIR, "SourceSans3-700.ttf")    # angka strip 700
SS800 = os.path.join(FONTS_DIR, "SourceSans3-800.ttf")    # kicker/label 800
SS_IT = os.path.join(FONTS_DIR, "SourceSans3-Italic.ttf")  # sumber brief

W, H = 1024, 1024
MX = 24                      # margin kiri/kanan
CW = W - 2 * MX              # 976 lebar konten
PAPER, INK, NAVY, RED, GOLD, WHITE = (rv.PAPER, rv.INK, rv.NAVY, rv.RED,
                                       rv.GOLD, rv.WHITE)
NEAR_WHITE = (251, 250, 245)  # latar panel teks (ref-3, fix 4): diukur
# dari referensi — hero text area (251,250,245), strip (251,250,245),
# MORE box (244-250,243-247,238-242); kertas halaman tetap PAPER krem.
CARD_BG = rv.CARD_BG
GRAY = (110, 110, 110)
TAN_PANEL = (215, 195, 142)  # panel tempat hero 1 (diukur dari referensi)


def F(path, size):
    return ImageFont.truetype(path, size)


DISPLAY_B = GEL700            # judul utama (Gelasio 700, 56px)
SERIF_B = GEL700              # judul berita (Gelasio 700)
SERIF = SS400                 # teks isi (Source Sans 3 400)
SERIF_IT = GEL_IT             # deck (Gelasio Italic 11,6px -> 12px)
BOLD = SS800                  # kicker/label (Source Sans 3 800)
REG = SS400
LIB_REG = SS400
LIB_BOLD = SS800
LIB_IT = SS_IT
NUM_F = SS700                 # angka strip (Source Sans 3 700)
CHIP_F = SS700                # teks chip region / legenda peta

# --- warna atas: tint latar painter (tanpa bar aksen) -------------------
# Jarak RGB antar tetangga ortogonal dihitung di build(); semua pasangan
# ditargetkan >= 31 (ambang assert 25, margin >= 6).
SAGE_PALE = (200, 220, 180)   # cricket (tetangga: akvan krem, sco biru, gold krem)
# Catatan: sage awal (222,234,212) GAGAL — akvan tersampel (226,225,220)
# karena cincin radar menyentuh patch atas, jarak ke sage cuma 12,7.
# Sage diperdalam ke (200,220,180): jarak ke akvan 48, ke sco 74,
# ke gold 81. S=0,18 (tetap kalem, < 0,30).
BLUE_PALE = (203, 220, 238)   # sco (tetangga: cricket sage, florida, gta, kyiv)
LAVENDER = (233, 226, 240)    # apec (tetangga: florida, taipei, prabowo)
TEAL_PALE = (205, 228, 226)   # taipei + prabowo (tetangga: apec/f1, mkt/apec/f1)
GOLD_PALE = (242, 230, 198)   # mkt (tetangga: gta, prabowo, florida)
CREAM = (250, 247, 238)       # akvan, cop31, gold (tetangga sudah beda)

# --- warna chip region: diukur dari piksel chip referensi (y=388 @2048) --
CHIP_COLORS = {
    "EUROPE": (38, 66, 118), "AMERICAS": (125, 38, 40),
    "ASIA-PACIFIC": (165, 42, 40), "MIDEAST": (155, 115, 35),
    "AFRICA": (42, 108, 74), "OCEANIA": (30, 108, 114),
    "WORLD": (82, 62, 126),
}
# Hitung dari pool kita (V2: 31 cerita): EUROPE 7, AMERICAS 5,
# ASIA-PAC 9, MIDEAST 3, AFRICA 3, OCEANIA 1, WORLD 3. Perubahan vs
# trial r10: EUROPE +2 (Polandia, Italia), MIDEAST +1 (Irak),
# AFRICA +1 (Kenya), ASIA -1 (Jakarta hapus; SCO/APEC/Prabowo kartu
# -> brief, region sama), OCEANIA -2 (Brisbane, Loyalty hapus),
# WORLD -1 (GTA hapus). OCEANIA 1 = trade-off yang dicatat (hanya
# kartu kriket Wellington yang tersisa; Sydney dihapus Kevin rev-2).
CHIPS = [("EUROPE", 7), ("AMERICAS", 5), ("ASIA-PACIFIC", 9),
         ("MIDEAST", 3), ("AFRICA", 3), ("OCEANIA", 1), ("WORLD", 3)]

# ------------------------------------------------------------------ peta baru
# Outline benua DETAIL dari Natural Earth 110m land (127 fitur, 5143
# titik) — https://github.com/nvkelso/natural-earth-vector (Public Domain,
# file ne_110m_land.geojson di folder ini). Alasan ganti: poligon
# rv.CONTINENTS (10 poligon kasar) + proyeksi equirectangular lama
# (x-scale 0,78, y-scale 2,14 px/derajat -> regang vertikal 2,7x)
# membuat benua jadi blob aneh (koreksi Kevin 21:35 WIB).
# Proyeksi baru meniru referensi (diukur dari peta referensi 2048):
# x-scale 0,815 px/derajat, y-scale 1,0 px/derajat (regang 1,23x),
# daratan menempati ~130px dari 278px tinggi navy, gap atas ~53px,
# gap bawah ~89px (legenda di bawah). Antarktika (lat < -60) dibuang
# seperti referensi; tidak ada lompatan antimeridian di dataset.
MAP_LAND = (218, 190, 148)   # daratan referensi (diukur: Afrika 221,194,149)
MAP_LAND_OUT = (200, 175, 130)
MAP_SX, MAP_SY = 0.815, 1.0
MAP_LAT0 = 83.0              # lat di y = navy_top + 53


def load_land_polys():
    """Poligon daratan (lon,lat) — sederhanakan + buang Antarktika."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "ne_110m_land.geojson")
    with open(path) as fh:
        data = json.load(fh)
    polys = []
    for feat in data["features"]:
        for ring in feat["geometry"]["coordinates"]:
            if len(ring) < 4:
                continue
            lats = [p[1] for p in ring]
            if max(lats) < -60:      # Antarktika — tidak ada di referensi
                continue
            xs = [p[0] for p in ring]
            ys = lats
            if (max(xs) - min(xs)) < 0.4 and (max(ys) - min(ys)) < 0.4:
                continue             # pulau mungil (<0,4 derajat)
            out = [ring[0]]
            for p in ring[1:]:
                if (abs(p[0] - out[-1][0]) > 0.12
                        or abs(p[1] - out[-1][1]) > 0.12):
                    out.append(p)
            if out[-1] != ring[-1]:
                out.append(ring[-1])
            polys.append(out)
    return polys


LAND_POLYS = load_land_polys()


def map_xy(lon, lat, x0=701, y0=288):
    """lon/lat -> piksel absolut di peta (proyeksi referensi).
    y0 = navy_top + 1 + 53 (gap atas ~53px seperti referensi)."""
    return (x0 + (lon + 180.0) * MAP_SX, y0 + (MAP_LAT0 - lat) * MAP_SY)


# ------------------------------------------------------------------ teks tracking
def tracked_width(d, text, font, tracking=-0.4):
    """Lebar teks dgn letter-spacing manual (Pillow tidak dukung tracking)."""
    return (sum(d.textlength(ch, font=font) for ch in text)
            + tracking * (len(text) - 1))


def draw_tracked(d, cx, y, text, font, fill, tracking=-0.4):
    """Gambar teks per karakter dgn tracking, rata tengah, anchor atas
    (ascender). Kembalikan (x0, x1) piksel. Dipakai judul utama
    (Gelasio 700 56px, tracking -0,4px — spesifikasi Kevin 21:37 WIB)."""
    total = tracked_width(d, text, font, tracking)
    x = cx - total / 2.0
    x0 = x
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, anchor="la")
        x += d.textlength(ch, font=font) + tracking
    return x0, x0 + total

# ------------------------------------------------------------------ data
HEROES_REF = [
    {"num": 1, "city": "Gopalpur", "place": "ODISHA, INDIA",
     "topic": "CYCLONE", "region": "ASIA",
     "title": "Cyclone Akvan hits India's east coast",
     "sum": ("Landfall 07:30 IST near Gopalpur, winds 70-80 km/h "
             "gusting to 90. Over 300,000 evacuated to shelters as "
             "the storm crosses the Odisha coast; 423 rescue teams "
             "deployed."),
     "painter": "akvan", "map_city": "Gopalpur"},
    {"num": 2, "city": "Kyiv", "place": "KYIV, UKRAINE",
     "topic": "MISSILES", "region": "EUROPE",
     "title": "Missiles hit Kyiv in the early hours",
     "sum": ("Missiles strike the capital from 01:25, arriving in "
             "waves 20-30 minutes apart through the night. Blasts "
             "heard across the city as drones join the attack into "
             "the early hours, with more waves at 02:00 and "
             "03:00-04:30."),
     "painter": "kyiv", "map_city": "Kyiv"},
    {"num": 3, "city": "Antalya", "place": "ANTALYA, TURKIYE",
     "topic": "COP31", "region": "MIDEAST",
     "title": "COP31 enters its final day",
     "sum": ("Talks enter their final day in Antalya, with the "
             "latest draft still omitting any mention of fossil "
             "fuels. No new text by Friday afternoon; delegates "
             "demand a stronger deal as the clock runs down."),
     "painter": "cop31", "map_city": "Antalya"},
]

CARDS_REF = [
    # REV3 (Kevin 21 Nov 19:56 WIB, "double teks" + banner 14px):
    # banner = NILAI, TIDAK BOLEH mengulang kata judul/ringkasan.
    # Diubah: #5 "TROOPS IN" -> "KATAIB" ("TROOPS" duplikat judul;
    # kata fakta kunci = Kataib Hezbollah, terverifikasi STORIES.md);
    # #6 "CREST 18.6" -> "18.6 FT" ("CREST" duplikat ringkasan);
    # #7 "100 CITIES" -> "100+" ("CITIES" duplikat ringkasan);
    # #8 "TAIEX -6.4%" -> "-6.4%" ("TAIEX" duplikat judul);
    # #11 "NIKKEI -4.1%" -> "-4.1%" ("NIKKEI" duplikat ringkasan,
    # field banner_pt 11 DIHAPUS — "-4.1%" muat 14pt);
    # #12 "FIRST OIL" -> "20K BPD" ("FIRST"/"OIL" duplikat judul;
    # nilai = target 20.000 bpd). Tetap: #4 "175* RUNS", #9 "-2.8%",
    # #10 "KH-101" (fakta kunci, tidak duplikat), #13 "1:47.272".
    {"num": 4, "city": "Wellington", "place": "WELLINGTON, NZ",
     "topic": "CRICKET", "banner": "175* RUNS", "region": "OCEANIA",
     "title": "Nicholls 175* lifts New Zealand to 368",
     "sum": "Nicholls 175*; Phillips adds 118. NZ 368.",
     "painter": "cricket", "map_city": "Wellington"},
    {"num": 5, "city": "Jurf al-Sakhar", "place": "JURF AL-SAKHAR, IRAQ",
     "topic": "IRAQ", "banner": "KATAIB", "region": "MIDEAST",
     "title": "Iraqi troops enter militia stronghold",
     "sum": "State forces enter Jurf al-Sakhar; militia to withdraw.",
     "painter": "iraq", "map_city": "Jurf al-Sakhar"},
    {"num": 6, "city": "Florida", "place": "FLORIDA, USA",
     "topic": "FLOODS", "banner": "18.6 FT", "region": "AMERICAS",
     "title": "Florida river still rising",
     "sum": "Crest 18.6 ft Fri; schools shut.",
     "painter": "florida", "map_city": "Florida"},
    {"num": 7, "city": "Rome", "place": "ROME, ITALY",
     "topic": "STRIKE", "banner": "100+", "region": "EUROPE",
     "title": "Italy grinds to halt in general strike",
     "sum": "CGIL strike hits 100+ cities; 1m march for wages.",
     "painter": "italy", "map_city": "Milan"},
    {"num": 8, "city": "Taipei", "place": "TAIPEI, TAIWAN",
     "topic": "STOCKS", "banner": "-6.4%", "region": "ASIA",
     "title": "Taiex slides again Friday",
     "sum": "Taiwan stocks fall 6.4%; chips lead losses.",
     "painter": "taipei", "map_city": "Taipei"},
    {"num": 9, "city": "Markets", "place": "LONDON, UK",
     "topic": "GOLD", "banner": "-2.8%", "region": "WORLD",
     "title": "Gold plunges on Friday",
     "sum": "Gold falls 2.8% intraday to $3,520.",
     "painter": "gold", "map_city": "London"},   # aproksimasi (lihat docstring)
    {"num": 10, "city": "Nowy Lipowiec", "place": "NOWY LIPOWIEC, POLAND",
     "topic": "MISSILES", "banner": "KH-101", "region": "EUROPE",
     "title": "Russian missile lands in Poland",
     "sum": "Two missiles and a drone down; no casualties.",
     "painter": "poland", "map_city": "Nowy Lipowiec"},
    {"num": 11, "city": "Tokyo", "place": "TOKYO, JAPAN",
     "topic": "MARKETS", "banner": "-4.1%",
     "region": "ASIA",
     "title": "Asia markets plunge",
     "sum": "Asia -2.5%; Nikkei -4.1%, Kospi -4.7%.",
     "painter": "mkt", "map_city": "Tokyo"},
    {"num": 12, "city": "Turkana", "place": "TURKANA, KENYA",
     "topic": "OIL", "banner": "20K BPD", "region": "AFRICA",
     "title": "Kenya starts drilling first oil wells",
     "sum": "Gulf Energy spuds Amosing 1; 20,000 bpd targeted.",
     "painter": "kenya", "map_city": "Turkana"},
    {"num": 13, "city": "Brussels", "place": "BRUSSELS, BELGIUM",
     "topic": "EU–UK", "banner": "3 DEALS", "region": "EUROPE",
     "title": "EU-UK 'reset' sealed in Brussels",
     "sum": "3 deals: food checks eased, 100k youth visas, energy pact.",
     "painter": "euuk", "map_city": "Brussels"},
]

# Briefs 14-31: (num, city, teks, sumber). Teks terse 1 klausa, <=70 karakter
# total (termasuk nomor + kota + sumber) agar muat 1 baris di kolom 305px
# pada Liberation Sans 8pt. Sumber hanya yang terverifikasi — 22, 23, 24,
# 29 tanpa sumber (pool v3 tidak menyebut outlet) — TIDAK dikarang.
BRIEFS_REF = [
    (14, "KYIV", "Kyiv hit again overnight. Missiles strike.", "Reuters"),
    (15, "NEW DELHI", "Modi opens SCO forum.",
     "Nation Press"),  # REV9: "SCO civilisations forum" -> "SCO forum" (12pt)
    (16, "SHENZHEN", "Xi meets Albanese in Shenzhen.", "Reuters"),
    (17, "SHENZHEN", "Prabowo, Xi sign $86.8bn deals.", "Xinhua"),
    (18, "LAS VEGAS", "Russell fastest in wet FP2.", "Formula1.com"),
    (19, "GLOBAL", "Brent rises to $92.77; WTI $83.40.", "Reuters"),
    (20, "GLOBAL", "Pakistan beat Sri Lanka by 8 wickets.", None),
    (21, "MADRID", "Spain students strike over education cuts.", None),
    (22, "SEOUL", "Samsung names Choi to head Mobile.", None),
    (23, "PARIS", "Harris meets Macron in Paris.", "Le Monde"),
    (24, "TAIPEI", "Taiwan reports 2,700 accounts to Meta.", "Reuters"),
    (25, "RIYADH", "Saudi coalition intercepts Houthi missile.", "Reuters"),
    (26, "BEIJING", "China holds lending rates 18th month.",
     "Reuters"),  # REV9: hapus "for" (12pt)
    (27, "FLORIDA", "Flood watch holds through Saturday.", "NWS"),
    (28, "NAIROBI", "KCSE ends; record 1.05m.", "People Daily"),  # REV9: hapus " candidates" (12pt)
    (29, "JOHANNESBURG", "Rand hits 1-yr low, 17.56/USD", "Reuters"),  # REV9: "one-year ... at" -> "1-yr low," (12pt)
    (30, "NEW YORK", "Nasdaq futures slide 1.6% in AI rout.", "Reuters"),
    (31, "VICTORIA", "1st Conservative premier in a century",
     None),  # REV10: "Tory" -> "Conservative" (juri crosscheck rev9:
     # "Tory" membingungkan; "Conservative" + sumber = 339,5px > 312px,
     # jadi sumber dihapus — 3 brief lain (#20-22) juga tanpa sumber)
    # REVISI-2 (Kevin 21 Nov 15:06 WIB): hapus 2 baris bawah MORE —
    # lama #20 Tokyo, #21 Sydney, #28 Saipan, #29 Hong Kong,
    # #36 Washington — sisa 18 brief, nomor ulang 14-31 (tanpa lompatan).
]

# Strip 6 angka — dari pool kita (bukan referensi). Captions 1 baris.
NUMBERS_REF = [
    ("300,000", "evacuated ahead of Akvan"),
    ("$92.77", "Brent crude, Friday morning"),
    ("\u22122.5%", "MSCI Asia, Friday"),
    ("175*", "Nicholls' runs vs India"),
    ("423", "rescue teams deployed"),
    ("1M+", "march in Italy's general strike"),
]

DECK_REF = ("Cyclone Akvan strikes India \u2022 Missiles hit Kyiv \u2022 "
            "COP31's final day \u2022 Asia markets plunge \u2022 "
            "Gold plunges on Friday")

# REV9 (Kevin Gas 22 Nov 04:40 WIB — legibilitas): daftar "not Friday's
# news" dipangkas 18 -> 12 item (Romania, rupee, Kenya flood, Thai pact,
# Husky, Dow keluar — daftar ini contoh, bukan cerita halaman) + "Mercury
# orbit entry" -> "Mercury entry" + "20 November" -> "20 Nov", supaya teks
# DATE CHECK muat 2 baris di 12pt (diukur font asli: 869/830 dari max 878).
# Klaim penutup + klausa "Not yet" TIDAK berubah isinya; 31 cerita sama.
DATECHECK_REST = (
    "Not Friday's news, so not on this page: Senate vote · IAEA report · "
    "Sensex · Fiji · Europe talks · Dakar boat · Dhaka fire · Takaichi · "
    "Australia sanctions · hockey · Quad · Zelenskyy — all 17–19 Nov. "
    "Not yet: BepiColombo's Mercury entry; COP31 final text. "
    "Every story here happened, or was first reported, on Friday 20 Nov 2026.")

SOURCES_LEFT = ("Every story here happened, or was first reported, on "
                "Friday 20 November 2026 in at least one time zone. "
                "Claims are attributed, not stated as fact.")
SOURCES_RIGHT = ("Sources: Reuters, AP, AFP, IMD, UN News, "
                 "Al Jazeera, ICC, EU Council, PBOC, Capital FM. "
                 "Original vector drawings.")

# REV8 (Kevin 21 Nov 20:30 WIB, "teks di bawah date check kok ga
# selaras"): DIAGNOSIS terukur (font asli 11pt) — baris 1 SOURCES_LEFT
# digambar kiri-rata di x 24..679 (lebar 655,3px), baris 2
# SOURCES_RIGHT digambar KANAN-rata di x 488..1000 (lebar 512,3px):
# kedua tepi tidak sejajar, blok footer terlihat miring/tidak rata.
# Seluruh teks footer dibagi ulang jadi 2 baris SEIMBANG (diukur font
# asli: 590,1 / 577,5px, selisih 12,6px — belahan terbaik; alternatif
# terdekat setelah "attributed," selisih 22,8px), keduanya rata kiri
# di MX (= tepi kiri kotak DATE CHECK). Kata-kata TIDAK diubah, hanya
# pembagian barisnya.
SOURCES_LINE1 = ("Every story here happened, or was first reported, on "
                 "Friday 20 November 2026 in at least one time zone. "
                 "Claims are attributed, not")
SOURCES_LINE2 = ("stated as fact. Sources: Reuters, AP, AFP, IMD, UN News, "
                 "Al Jazeera, ICC, EU Council, PBOC, Capital FM. "
                 "Original vector drawings.")

# ------------------------------------------------------------------ painters
# Salinan painter 1r/1r4 dengan parameter bg (tint warna atas). Isi grafik
# TIDAK diubah — hanya latar krem diganti tint. Painter yang latarnya
# sudah beda (flood, gold, gta, f1, hero) dipakai langsung dari r1/r14.
NAVY = rv.NAVY
SLATE = r1.SLATE
RED_M = r1.RED_M
GOLD_M = r1.GOLD_M


def p_cricket_ref(w, h, bg=SAGE_PALE):
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    gy = int(h * 0.90)
    d.line([(0, gy), (w, gy)], fill=NAVY, width=2)
    d.polygon([(int(w * 0.30), int(h * 0.16)), (int(w * 0.36), int(h * 0.20)),
               (int(w * 0.58), int(h * 0.88)), (int(w * 0.52), int(h * 0.90))],
              fill=(150, 110, 70), outline=NAVY)
    d.ellipse([int(w * 0.64), int(h * 0.22), int(w * 0.74), int(h * 0.38)],
              fill=RED_M, outline=NAVY, width=1)
    for i in range(3):
        sx = int(w * (0.80 + i * 0.05))
        d.rectangle([sx, int(h * 0.32), sx + 4, int(h * 0.90)],
                    fill=GOLD_M, outline=NAVY, width=1)
    d.rectangle([int(w * 0.80), int(h * 0.295), int(w * 0.90) + 4,
                 int(h * 0.32)], fill=GOLD_M, outline=NAVY, width=1)
    return im


def p_sco_ref(w, h, bg=BLUE_PALE):
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    bx0, bx1 = int(w * 0.30), int(w * 0.70)
    by0, by1 = int(h * 0.30), int(h * 0.82)
    d.rectangle([bx0, by0, bx1, by1], fill=(200, 180, 140), outline=NAVY,
                width=2)
    d.polygon([(bx0 - 8, by0), (bx1 + 8, by0),
               ((bx0 + bx1) // 2, int(h * 0.12))], fill=NAVY)
    d.rectangle([(bx0 + bx1) // 2 - 8, int(h * 0.60),
                 (bx0 + bx1) // 2 + 8, by1], fill=NAVY)
    for i, col in enumerate((NAVY, RED_M)):
        fx = int(w * (0.16 + i * 0.62))
        d.line([(fx, int(h * 0.22)), (fx, int(h * 0.82))], fill=NAVY, width=2)
        d.rectangle([fx, int(h * 0.22), fx + int(w * 0.13), int(h * 0.38)],
                    fill=col, outline=NAVY, width=1)
    d.line([(0, by1), (w, by1)], fill=SLATE, width=3)
    return im


def p_flags3_ref(w, h, cols, bg):
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    for i, col in enumerate(cols):
        fx = int(w * (0.12 + i * 0.30))
        d.line([(fx + int(w * 0.10), int(h * 0.18)),
                (fx + int(w * 0.10), int(h * 0.78))], fill=NAVY, width=2)
        d.rectangle([fx, int(h * 0.18), fx + int(w * 0.20), int(h * 0.48)],
                    fill=col, outline=NAVY, width=1)
        if col == WHITE:
            d.ellipse([fx + int(w * 0.07), int(h * 0.27),
                       fx + int(w * 0.13), int(h * 0.39)], fill=RED_M)
    d.rectangle([int(w * 0.08), int(h * 0.78), int(w * 0.92), int(h * 0.86)],
                fill=(150, 110, 70), outline=NAVY, width=1)
    return im


def p_chart_ref(w, h, bg):
    # REVISI-10: polyline dirapatkan ke zona bersih y 22-38 (tinta) —
    # tidak menabrak banner merah bawah (y=20) maupun label putih atas
    # (y=40, kotak 20px): titik lama (0.76,0.50),(0.90,0.78) turun ke
    # y 48 — ekor garis + panah tertutup label. Titik baru mulai y=24
    # (bukan 14 — dulu sebagian di bawah banner) supaya garis UTUH.
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    for gy in (0.25, 0.50, 0.75):
        d.line([(int(w * 0.06), int(h * gy)), (int(w * 0.94), int(h * gy))],
               fill=(215, 210, 200), width=1)
    pts = [(0.08, 0.38), (0.26, 0.42), (0.42, 0.38), (0.60, 0.48),
           (0.76, 0.54), (0.90, 0.58)]
    xy = [(int(w * a), int(h * b)) for a, b in pts]
    d.line(xy, fill=RED_M, width=4, joint="curve")
    ex, ey = xy[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED_M)
    d.line([(int(w * 0.06), int(h * 0.90)), (int(w * 0.94), int(h * 0.90))],
           fill=SLATE, width=2)
    return im


def p_chart_gold_r8(w, h):
    """REVISI-8 (Kevin 21 Nov 15:31 WIB): tile kartu 09 (Gold) digambar
    ulang SELARAS dengan kartu 08/11 — grafik GARIS merah tipis menurun
    (p_chart_ref), bukan lagi batang emas tebal + panah merah besar dari
    r1.TILE_1R["gold"]. Salinan lokal (modul bersama TIDAK diubah):
    gridlines + baseline + garis width=4 + panah kecil di ujung SAMA
    seperti p_chart_ref, tapi polyline digeser ke zona bersih supaya
    garis UTUH: tidak menabrak banner "-2.8%" (y 0-20) di kiri atas dan
    tidak tertutup label "KuCoin News" (x ~92-183, y 40-60) di kanan
    bawah. Titik diukur (tile 185x62): y 25-36, stroke +-2 -> celah
    >=3px dari banner bawah (y=20) dan >=2px dari label atas (y=40).
    REVISI-10: titik dirapatkan dari y 22-41 (label lama atas y=45)
    karena label kini 20px (atas y=40).
    Latar GOLD_PALE sama seperti kartu 11 (mkt); warna atas GOLD_PALE
    (242,230,198) lolos aturan tetangga >=25: vs kartu 04 SAGE_PALE
    ~46.8, vs kartu 10 GTA (205,170,130) ~97.9."""
    im = Image.new("RGB", (w, h), GOLD_PALE)
    d = ImageDraw.Draw(im)
    for gy in (0.25, 0.50, 0.75):
        d.line([(int(w * 0.06), int(h * gy)), (int(w * 0.94), int(h * gy))],
               fill=(215, 210, 200), width=1)
    pts = [(0.06, 0.40), (0.24, 0.44), (0.42, 0.40), (0.60, 0.55),
           (0.76, 0.48), (0.92, 0.58)]
    xy = [(int(w * a), int(h * b)) for a, b in pts]
    d.line(xy, fill=RED_M, width=4, joint="curve")
    ex, ey = xy[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED_M)
    d.line([(int(w * 0.06), int(h * 0.90)), (int(w * 0.94), int(h * 0.90))],
           fill=SLATE, width=2)
    return im


def p_poland(w, h):
    """V2 (b3) kartu #10 Polandia — gaya datar, satu ide besar: rudal
    di langit malam di atas siluet hutan. Latar navy gelap (18,32,58):
    patch atas (tengah, y 2-8) = navy — jauh dari GOLD_PALE tetangga
    (242,230,198) kiri-kanan. Rudal di zona bersih y 14-40 (di bawah
    banner 20px, di atas label 20px); hutan segitiga y 44-62."""
    im = Image.new("RGB", (w, h), (18, 32, 58))
    d = ImageDraw.Draw(im)
    for sx, sy in ((28, 9), (58, 14), (122, 6), (152, 12), (172, 8),
                   (140, 22), (36, 26)):
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 210, 225))
    # siluet hutan: deret segitiga gelap di bawah
    d.rectangle([0, 48, w, h], fill=(14, 40, 28))
    for x0, peak in ((0, 42), (24, 38), (48, 44), (72, 39), (96, 43),
                     (120, 38), (144, 44), (168, 40)):
        d.polygon([(x0, 62), (x0 + 12, peak), (x0 + 24, 62)],
                  fill=(16, 48, 32))
    # jejak asap putus-putus di belakang rudal
    for i in range(5):
        fx0 = 52 - i * 9
        d.ellipse([fx0, 40 - i * 2, fx0 + 4, 44 - i * 2],
                  fill=(150, 160, 175))
    # rudal: badan putih diagonal + hidung merah + api oranye
    d.line([(58, 40), (118, 16)], fill=(235, 238, 240), width=5)
    d.polygon([(118, 16), (128, 12), (124, 22)], fill=RED_M)
    d.polygon([(58, 40), (48, 44), (52, 34)], fill=(230, 140, 40))
    d.polygon([(58, 40), (50, 46), (56, 32)], fill=(240, 180, 60))
    return im


def p_iraq(w, h):
    """V2 (b3) kartu #05 Irak — gaya datar, satu ide besar: konvoi +
    bendera di kota gurun. Latar pasir kabur (205,180,130): patch atas
    = pasir — jauh dari cricket (200,220,180) ~64, Florida
    (185,200,210) ~85, Kyiv (16,23,38). Bendera + bangunan di bawah
    y 14; kendaraan di jalan y 50-60 (label kanan-bawah menutupi
    ujung jalan saja, bukan kendaraan)."""
    im = Image.new("RGB", (w, h), (205, 180, 130))
    d = ImageDraw.Draw(im)
    d.ellipse([148, 6, 166, 24], fill=(228, 214, 168))  # matahari pucat
    # bangunan kota datar di bawah
    for bx, bw, bh, col in ((0, 34, 20, (170, 140, 100)),
                            (36, 26, 26, (150, 120, 85)),
                            (110, 30, 18, (185, 155, 115)),
                            (142, 43, 24, (160, 130, 95))):
        d.rectangle([bx, h - bh, bx + bw, h], fill=col, outline=NAVY,
                    width=1)
        d.rectangle([bx + 5, h - bh + 5, bx + 10, h - bh + 10],
                    fill=(90, 75, 55))
    # tiang + bendera Irak (tiga lajur merah-putih-hitam)
    d.line([(64, 14), (64, 52)], fill=NAVY, width=2)
    d.rectangle([64, 14, 92, 20], fill=(178, 34, 34))
    d.rectangle([64, 20, 92, 26], fill=WHITE)
    d.rectangle([64, 26, 92, 32], fill=(20, 20, 20))
    # jalan + 2 kendaraan konvoi
    d.rectangle([0, 52, w, 58], fill=(120, 105, 80))
    for vx in (96, 128):
        d.rectangle([vx, 46, vx + 22, 54], fill=(60, 70, 60),
                    outline=NAVY, width=1)
        d.ellipse([vx + 3, 53, vx + 8, 58], fill=(20, 20, 20))
        d.ellipse([vx + 14, 53, vx + 19, 58], fill=(20, 20, 20))
    return im


def p_italy(w, h):
    """V2 (b3) kartu #07 Italia — gaya datar, satu ide besar: kerumunan
    mogok + plakat. Latar langit biru-abu (120,140,170): patch atas =
    langit — jauh dari Florida (185,200,210) ~97, Taipei
    (205,228,226) ~135. Plakat y 26-38 (di bawah banner, di atas
    label); kerumunan y 44-62."""
    im = Image.new("RGB", (w, h), (120, 140, 170))
    d = ImageDraw.Draw(im)
    # gedung kota di tengah (latar)
    for bx, bw, bh, col in ((0, 30, 18, (150, 130, 110)),
                            (34, 26, 24, (130, 110, 90)),
                            (150, 35, 20, (170, 150, 125))):
        d.rectangle([bx, 52 - bh, bx + bw, 52], fill=col, outline=NAVY,
                    width=1)
    # plakat di atas kerumunan (putih + 1 merah)
    for px, col in ((26, WHITE), (82, (178, 44, 36)), (138, WHITE)):
        d.line([(px + 8, 38), (px + 8, 48)], fill=NAVY, width=2)
        d.rectangle([px, 26, px + 16, 38], fill=col, outline=NAVY,
                    width=1)
    # kerumunan: kepala + bahu warna kalem
    for cx, col in ((14, NAVY), (34, (178, 44, 36)), (54, (240, 238, 230)),
                    (74, (90, 90, 90)), (94, NAVY), (114, (178, 44, 36)),
                    (134, (240, 238, 230)), (154, (90, 90, 90)),
                    (172, NAVY)):
        d.ellipse([cx - 4, 46, cx + 4, 54], fill=col, outline=NAVY,
                  width=1)
        d.rectangle([cx - 6, 54, cx + 6, 62], fill=col, outline=NAVY,
                    width=1)
    return im


def p_kenya(w, h):
    """V2 (b3) kartu #12 Kenya — gaya datar, satu ide besar: menara bor
    minyak di bawah matahari terbenam. Latar oranye senja (210,140,70):
    patch atas = oranye — jauh dari Mkt GOLD_PALE (242,230,198) ~160,
    F1 (165,166,170) ~113. Menara di x 55-95 (tengah-kiri, jauh dari
    label kanan-bawah); matahari x 140-160 (jauh dari patch tengah)."""
    im = Image.new("RGB", (w, h), (210, 140, 70))
    d = ImageDraw.Draw(im)
    d.ellipse([140, 4, 160, 24], fill=(240, 210, 130))  # matahari
    # tanah gelap di bawah
    d.rectangle([0, 52, w, h], fill=(60, 45, 35))
    # menara bor: dua kaki miring + palang + puncak
    d.line([(55, 62), (75, 16)], fill=(70, 50, 40), width=4)
    d.line([(95, 62), (75, 16)], fill=(70, 50, 40), width=4)
    for yy in (30, 40, 50):
        d.line([(60, yy), (90, yy)], fill=(70, 50, 40), width=3)
    d.rectangle([70, 12, 80, 18], fill=(70, 50, 40))
    # pipa horizontal ke kanan + tangki kecil
    d.line([(95, 56), (150, 56)], fill=(70, 50, 40), width=3)
    d.rectangle([150, 46, 172, 56], fill=(90, 65, 45), outline=NAVY,
                width=1)
    return im


def p_gta_r6(w, h):
    """REVISI-6 (Kevin 21 Nov 15:21 WIB): salinan lokal p_gta dari
    sketches-v4/render_v4_1r.py (modul bersama TIDAK diubah) — SATU-
    SATUNYA perbedaan: teks "VI" PUTIH pindah ke TENGAH tile (anchor
    "mm" di (w/2, h/2)), bukan kiri (0.08w, 0.50h, anchor "lm").
    Ukuran tetap 34pt = max(18, int(h*0.55)) (tile kartu 62px).
    Diukur: tinta "VI" 34pt ~31x23px, terpusat (92,31) -> x ~77-108,
    y ~20-43: tidak menabrak banner merah (y 0-20, x 0-66), label
    putih "GeekRadar" (y 40-60, x ~105-183), maupun matahari emas
    (x 115-156, y 4-27)."""
    im = Image.new("RGB", (w, h), CREAM)  # sama seperti _base() r1
    d = ImageDraw.Draw(im)
    bands = [(205, 170, 130), (198, 150, 135), (150, 140, 160)]
    for i, col in enumerate(bands):
        d.rectangle([0, int(h * i / 3), w, int(h * (i + 1) / 3)], fill=col)
    d.ellipse([int(w * 0.62), int(h * 0.06), int(w * 0.84), int(h * 0.44)],
              fill=GOLD_M, outline=NAVY, width=1)
    f = F(BOLD, max(18, int(h * 0.55)))
    d.text((w // 2, h // 2), "VI", font=f, fill=WHITE, anchor="mm")
    return im


# --- painter FOTO (varian foto, Kevin 21 Nov 19:14 WIB) ------------------
# Mengganti ISI FOTO ke-13 tile supaya cocok literal dengan judul.
# Latar (warna atas) tiap tile TIDAK diubah — cek tetangga tetap lolos.
# TIDAK ada teks di dalam ilustrasi (banner + strip sumber digambar
# terpisah oleh draw_hero_ref/draw_card_ref, tidak disentuh).
# Zona bersih: banner merah kiri-atas (hero <=115px, kartu <=81px,
# tinggi 24px — REV3, dulu 20px); strip sumber TAN kanan-bawah
# (min 100px, tinggi 20px — REV3, dulu hitam); patch warna-atas di
# tengah-atas (hero x 120-140, kartu x 83-103, y 2-8) harus tetap
# warna latar — elemen gambar dijaga di luar patch itu (mulai y >= 8
# atau di luar x patch).
# Panel tan hero 1 (x 0-78) tetap digambar hero_image_with_panel
# di atas painter — foto Akvan digambar di kanan panel (x >= 84).


def p_akvan_foto(w, h):
    """FOTO hero 1: spiral siklon BESAR + garis hujan + garis pantai
    dengan rumah + palem di bawah (kanan panel tan). Tanpa teks
    'BAY OF BENGAL' (dihapus — teks tidak boleh di dalam ilustrasi)."""
    im = Image.new("RGB", (w, h), AKVAN_BG)
    d = ImageDraw.Draw(im)
    cx, cy = 185, 50
    for r, a0, a1 in ((13, 20, 320), (23, 140, 80), (32, 260, 200),
                      (40, 60, 300)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1,
              fill=(200, 220, 235), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=WHITE)
    # garis hujan miring di sekitar spiral
    for x0, y0 in ((120, 18), (140, 12), (225, 20), (240, 30), (105, 45)):
        d.line([(x0, y0), (x0 - 6, y0 + 12)], fill=(140, 170, 200), width=2)
    # garis pantai + rumah + palem di bawah (kanan panel tan x>=84)
    d.rectangle([84, 84, w, h], fill=(52, 84, 66))
    d.rectangle([100, 76, 122, 84], fill=(240, 238, 230), outline=NAVY,
                width=1)
    d.polygon([(98, 76), (124, 76), (111, 68)], fill=RED_M, outline=NAVY)
    d.rectangle([132, 78, 150, 84], fill=(220, 210, 190), outline=NAVY,
                width=1)
    d.polygon([(130, 78), (152, 78), (141, 71)], fill=(178, 44, 36),
              outline=NAVY)
    # palem kecil (kiri rumah 1, kanan panel tan)
    d.line([(88, 84), (88, 70)], fill=(70, 55, 35), width=2)
    d.line([(88, 70), (79, 64)], fill=(90, 140, 80), width=2)
    d.line([(88, 70), (97, 64)], fill=(90, 140, 80), width=2)
    d.line([(88, 70), (88, 62)], fill=(90, 140, 80), width=2)
    return im


def p_kyiv_foto(w, h):
    """FOTO hero 2: 2 rudal BESAR menukik + langit Kyiv (gereja kubah
    emas besar di tengah) + ledakan di titik jatuh. Latar malam
    tetap (16,23,38)."""
    im = Image.new("RGB", (w, h), (16, 23, 38))
    d = ImageDraw.Draw(im)
    # bintang (jauh dari patch atas x 120-140, y 2-8)
    for sx, sy in ((18, 26), (48, 30), (110, 26), (170, 10), (205, 8),
                   (232, 20), (248, 12)):
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 220, 200))
    # langit kota: siluet gedung + gereja kubah emas (tengah, besar)
    d.rectangle([0, 78, w, h], fill=(30, 42, 66))
    for bx, bw, bh in ((8, 26, 12), (40, 20, 18), (200, 24, 14),
                       (228, 22, 20)):
        d.rectangle([bx, 78 - bh, bx + bw, 78], fill=(30, 42, 66))
    d.rectangle([112, 44, 148, 78], fill=(48, 58, 82))
    d.pieslice([116, 30, 144, 58], 180, 360, fill=(200, 160, 60),
               outline=NAVY, width=1)  # kubah setengah lingkaran
    d.line([(130, 30), (130, 20)], fill=(200, 160, 60), width=2)
    d.line([(124, 24), (136, 24)], fill=(200, 160, 60), width=2)
    # rudal 1: menukik dari kanan-atas ke arah kubah
    d.line([(218, 12), (158, 56)], fill=(235, 238, 240), width=6)
    d.polygon([(158, 56), (150, 52), (154, 62)], fill=RED_M)
    d.polygon([(218, 12), (228, 8), (226, 20)], fill=(255, 140, 40))
    d.polygon([(218, 12), (230, 14), (224, 24)], fill=(240, 180, 60))
    # rudal 2: menukik dari kiri-atas
    d.line([(102, 10), (60, 48)], fill=(235, 238, 240), width=6)
    d.polygon([(60, 48), (52, 44), (56, 54)], fill=RED_M)
    d.polygon([(102, 10), (112, 6), (110, 18)], fill=(255, 140, 40))
    d.polygon([(102, 10), (114, 12), (108, 22)], fill=(240, 180, 60))
    # ledakan di titik jatuh
    for bx, by in ((158, 56), (60, 48)):
        d.polygon(rv.star_points(bx, by, 10, 5), fill=(255, 180, 60),
                  outline=(255, 220, 120))
    return im


def p_cop31_foto(w, h):
    """FOTO hero 3: globe BESAR + termometer + meja summit dengan
    5 delegasi (kepala polos, tanpa wajah; rambut beda-beda).
    Kartu putih berteks 'COP31' DIHAPUS — teks tidak boleh di dalam
    ilustrasi. Latar teal gelap tetap."""
    im = Image.new("RGB", (w, h), COP31_BG)
    d = ImageDraw.Draw(im)
    # globe besar kiri-tengah (puncak y 26, di bawah banner — REV3:
    # gy 50 -> 54 karena banner 24px; bawah globe y 82 menempel meja
    # y 80, meja digambar sesudah globe jadi menutup 2px — wajar)
    gx, gy, gr = 62, 54, 28
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 130, 180),
              outline=NAVY, width=2)
    d.ellipse([gx - 16, gy - 12, gx + 2, gy + 4], fill=(90, 150, 90))
    d.ellipse([gx - 2, gy + 8, gx + 14, gy + 18], fill=(90, 150, 90))
    d.ellipse([gx + 6, gy - 18, gx + 16, gy - 6], fill=(90, 150, 90))
    # termometer (tengah, puncak y 16 — jauh dari patch atas)
    tx = 122
    d.rounded_rectangle([tx, 16, tx + 12, 66], radius=6,
                        fill=(240, 244, 246), outline=NAVY, width=1)
    d.rectangle([tx + 4, 34, tx + 8, 62], fill=RED_M)
    d.ellipse([tx - 3, 60, tx + 15, 78], fill=RED_M, outline=NAVY, width=1)
    # meja summit + delegasi (kepala polos, warna rambut beda)
    d.rectangle([0, 80, w, 90], fill=(150, 110, 70))
    for cx, hair in ((30, (40, 40, 40)), (60, (120, 120, 120)),
                     (90, (90, 60, 30)), (120, (40, 40, 40)),
                     (150, (150, 150, 150))):
        d.ellipse([cx - 7, 62, cx + 7, 76], fill=(232, 200, 170),
                  outline=NAVY, width=1)
        d.arc([cx - 7, 62, cx + 7, 76], 180, 360, fill=hair, width=4)
        d.rectangle([cx - 9, 76, cx + 9, 80], fill=(70, 70, 90),
                    outline=NAVY, width=1)
    return im


def p_cricket_foto(w, h, bg=SAGE_PALE):
    """FOTO kartu 4: bat BESAR (tebal) + bola merah BESAR + stumps
    BESAR + bails. Latar SAGE_PALE tetap."""
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    gy = int(h * 0.90)
    d.line([(0, gy), (w, gy)], fill=NAVY, width=2)
    # bat BESAR diagonal — seluruhnya di zona terlihat (di bawah
    # banner y<=20, kiri strip sumber x<83)
    d.polygon([(28, 24), (48, 28), (82, 56), (62, 56)],
              fill=(150, 110, 70), outline=NAVY)
    d.ellipse([int(w * 0.66), int(h * 0.14), int(w * 0.80), int(h * 0.36)],
              fill=RED_M, outline=NAVY, width=1)
    for i in range(3):
        sx = int(w * (0.82 + i * 0.05))
        d.rectangle([sx, int(h * 0.30), sx + 5, int(h * 0.90)],
                    fill=GOLD_M, outline=NAVY, width=1)
    d.rectangle([int(w * 0.82), int(h * 0.27), int(w * 0.92) + 5,
                 int(h * 0.30)], fill=GOLD_M, outline=NAVY, width=1)
    return im


def p_iraq_foto(w, h):
    """FOTO kartu 5: bendera Irak BESAR di tengah + konvoi 2 kendaraan
    BESAR di jalan kiri-bawah + gedung kota + matahari pucat.
    Latar pasir tetap (205,180,130)."""
    im = Image.new("RGB", (w, h), (205, 180, 130))
    d = ImageDraw.Draw(im)
    d.ellipse([155, 2, 173, 20], fill=(228, 214, 168))  # matahari pucat
    # gedung kota di belakang (di atas strip sumber)
    for bx, bw, bh, col in ((120, 26, 14, (170, 140, 100)),
                            (150, 24, 12, (150, 120, 85))):
        d.rectangle([bx, 40 - bh, bx + bw, 40], fill=col, outline=NAVY,
                    width=1)
        d.rectangle([bx + 5, 40 - bh + 4, bx + 10, 40 - bh + 9],
                    fill=(90, 75, 55))
    # bendera Irak BESAR (kanan banner, tengah)
    d.line([(80, 12), (80, 44)], fill=NAVY, width=2)
    d.rectangle([80, 12, 118, 19], fill=(178, 34, 34))
    d.rectangle([80, 19, 118, 26], fill=WHITE)
    d.rectangle([80, 26, 118, 33], fill=(20, 20, 20))
    # jalan + 2 kendaraan BESAR (kiri-bawah, kiri strip sumber)
    d.rectangle([0, 48, w, 56], fill=(120, 105, 80))
    for vx in (10, 44):
        d.rectangle([vx, 40, vx + 26, 50], fill=(60, 70, 60),
                    outline=NAVY, width=1)
        d.ellipse([vx + 4, 49, vx + 10, 55], fill=(20, 20, 20))
        d.ellipse([vx + 16, 49, vx + 22, 55], fill=(20, 20, 20))
    return im


def p_florida_foto(w, h):
    """FOTO kartu 6: rumah BESAR setengah terendam — air naik sampai
    jendela, pohon + perahu kecil. Atap puncak y 10 (di bawah patch
    atas y 2-8). Latar langit biru-abu tetap."""
    im = Image.new("RGB", (w, h), (185, 200, 210))
    d = ImageDraw.Draw(im)
    hx0, hx1 = int(w * 0.28), int(w * 0.68)
    hy0, hy1 = int(h * 0.30), int(h * 0.66)
    d.rectangle([hx0, hy0, hx1, hy1], fill=CREAM, outline=NAVY, width=2)
    d.polygon([(hx0 - 8, hy0), (hx1 + 8, hy0),
               ((hx0 + hx1) // 2, int(h * 0.16))], fill=RED_M, outline=NAVY)
    d.rectangle([int(w * 0.44), int(h * 0.48), int(w * 0.56), hy1],
                fill=NAVY)
    # pohon kanan (di atas air)
    d.line([(int(w * 0.80), int(h * 0.34)), (int(w * 0.80), int(h * 0.62))],
           fill=(90, 70, 50), width=3)
    d.ellipse([int(w * 0.74), int(h * 0.20), int(w * 0.86), int(h * 0.38)],
              fill=(90, 140, 80), outline=NAVY, width=1)
    # air banjir: menutupi bawah rumah (y 0.62h ke bawah)
    d.rectangle([0, int(h * 0.62), w, h], fill=(90, 120, 140))
    for i, wx in enumerate((0.06, 0.36, 0.66)):
        d.arc([int(w * wx), int(h * 0.68), int(w * (wx + 0.22)),
               int(h * 0.88)], 180, 360, fill=WHITE, width=3)
    # perahu kecil kiri
    d.polygon([(int(w * 0.04), int(h * 0.74)), (int(w * 0.20), int(h * 0.74)),
               (int(w * 0.17), int(h * 0.84)), (int(w * 0.07), int(h * 0.84))],
              fill=(120, 80, 50), outline=NAVY, width=1)
    return im


def p_italy_foto(w, h):
    """FOTO kartu 7: kerumunan mogok BESAR — kepala + bahu lebih besar,
    3 plakat BESAR di zona bersih y 20-40, gedung kota di belakang.
    Latar biru-abu tetap (120,140,170)."""
    im = Image.new("RGB", (w, h), (120, 140, 170))
    d = ImageDraw.Draw(im)
    for bx, bw, bh, col in ((0, 30, 16, (150, 130, 110)),
                            (155, 30, 20, (170, 150, 125))):
        d.rectangle([bx, 46 - bh, bx + bw, 46], fill=col, outline=NAVY,
                    width=1)
    # plakat BESAR (y 24-38, di bawah banner — REV3: y 20 -> 24
    # karena banner 24px; kepala kerumunan y 42 tetap, celah 4px)
    for px, col in ((22, WHITE), (78, (178, 44, 36)), (134, WHITE)):
        d.line([(px + 9, 38), (px + 9, 46)], fill=NAVY, width=2)
        d.rectangle([px, 24, px + 18, 38], fill=col, outline=NAVY, width=1)
    # kerumunan: kepala + bahu BESAR — semua di kiri strip sumber
    # (x<83); kepala di kanan strip akan tertutup label tan
    for cx, col in ((8, NAVY), (24, (178, 44, 36)), (40, (240, 238, 230)),
                    (56, (90, 90, 90)), (72, NAVY)):
        d.ellipse([cx - 6, 42, cx + 6, 54], fill=col, outline=NAVY,
                  width=1)
        d.rectangle([cx - 8, 54, cx + 8, 62], fill=col, outline=NAVY,
                    width=1)
    return im


def p_taipei_foto(w, h, bg):
    """FOTO kartu 8: menara Taipei 101 BESAR (tengah-kanan) + garis
    merah jatuh. Latar TEAL_PALE tetap."""
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    for gy in (0.25, 0.50, 0.75):
        d.line([(int(w * 0.06), int(h * gy)), (int(w * 0.94), int(h * gy))],
               fill=(215, 210, 200), width=1)
    # Taipei 101: menara bertingkat menyempit ke atas (lebih lebar
    # supaya terbaca sebagai menara)
    tx0 = int(w * 0.54)
    for tw, ty0, ty1 in ((36, 44, 56), (30, 32, 44), (22, 22, 32),
                         (16, 12, 22)):
        d.rectangle([tx0 - tw // 2, ty0, tx0 + tw // 2, ty1],
                    fill=(60, 70, 85), outline=NAVY, width=1)
    d.line([(tx0, 8), (tx0, 12)], fill=(60, 70, 85), width=2)
    # garis merah jatuh (di depan menara)
    pts = [(0.08, 0.42), (0.26, 0.46), (0.42, 0.44), (0.60, 0.56),
           (0.76, 0.52), (0.92, 0.66)]
    xy = [(int(w * a), int(h * b)) for a, b in pts]
    d.line(xy, fill=RED_M, width=4, joint="curve")
    ex, ey = xy[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED_M)
    d.line([(int(w * 0.06), int(h * 0.90)), (int(w * 0.94), int(h * 0.90))],
           fill=SLATE, width=2)
    return im


def p_gold_foto(w, h):
    """FOTO kartu 9: tumpukan batangan emas BESAR (piramida 3 ingot)
    + panah merah turun BESAR di kanan. Latar GOLD_PALE tetap."""
    im = Image.new("RGB", (w, h), GOLD_PALE)
    d = ImageDraw.Draw(im)

    def ingot(x0, y0, x1, y1):
        d.polygon([(x0 + 4, y0), (x1 - 4, y0), (x1, y1), (x0, y1)],
                  fill=(200, 160, 60), outline=NAVY, width=1)
        d.polygon([(x0 + 4, y0), (x1 - 4, y0), (x1 - 8, y0 + 4),
                   (x0 + 8, y0 + 4)], fill=(240, 205, 110))

    # batangan emas: piramida 3 ingot — seluruhnya di kiri strip
    # sumber (x<83); panah merah turun di kanan-atas (y<40)
    ingot(12, 42, 46, 56)
    ingot(50, 42, 82, 56)
    ingot(31, 26, 65, 40)
    # panah merah turun BESAR (kanan-atas, utuh di atas strip)
    ax = 130
    d.line([(ax, 10), (ax, 30)], fill=RED_M, width=5)
    d.polygon([(ax - 10, 24), (ax + 10, 24), (ax, 38)], fill=RED_M)
    d.line([(int(w * 0.06), int(h * 0.90)), (int(w * 0.94), int(h * 0.90))],
           fill=SLATE, width=2)
    return im


def p_poland_foto(w, h):
    """FOTO kartu 10: rudal BESAR menukik + ledakan di hutan.
    Latar navy malam tetap (18,32,58)."""
    im = Image.new("RGB", (w, h), (18, 32, 58))
    d = ImageDraw.Draw(im)
    for sx, sy in ((70, 8), (52, 20), (160, 8), (176, 18), (36, 30)):
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(200, 210, 225))
    # hutan: segitiga gelap di bawah
    d.rectangle([0, 48, w, h], fill=(14, 40, 28))
    for x0, peak in ((0, 42), (24, 38), (48, 44), (72, 39), (96, 43),
                     (120, 38), (144, 44), (168, 40)):
        d.polygon([(x0, 62), (x0 + 12, peak), (x0 + 24, 62)],
                  fill=(16, 48, 32))
    # ledakan di titik jatuh (kiri-bawah)
    d.polygon(rv.star_points(52, 50, 12, 6), fill=(255, 180, 60),
              outline=(255, 220, 120))
    d.polygon(rv.star_points(52, 50, 6, 3), fill=(255, 230, 150))
    # rudal BESAR: badan putih diagonal + hidung merah + api oranye
    d.line([(72, 44), (150, 12)], fill=(235, 238, 240), width=7)
    d.polygon([(150, 12), (162, 8), (158, 20)], fill=RED_M)
    d.polygon([(72, 44), (60, 48), (64, 36)], fill=(230, 140, 40))
    d.polygon([(72, 44), (62, 50), (68, 34)], fill=(240, 180, 60))
    return im


def p_mkt_foto(w, h, bg):
    """FOTO kartu 11: skyline Tokyo + Tokyo Tower merah + candlestick
    merah jatuh + panah merah turun. Latar GOLD_PALE tetap."""
    im = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(im)
    # skyline Tokyo (bawah)
    for bx, bw, bh in ((6, 22, 20), (32, 18, 28), (54, 24, 16),
                       (82, 20, 24), (106, 22, 18)):
        d.rectangle([bx, 56 - bh, bx + bw, 56], fill=(70, 75, 90),
                    outline=NAVY, width=1)
    # Tokyo Tower merah — kerangka kisi (bukan segitiga padat):
    # 2 kaki miring + 2 palang + puncak, tengahnya tembus (latar)
    d.line([(128, 56), (140, 14)], fill=(178, 60, 50), width=4)
    d.line([(152, 56), (140, 14)], fill=(178, 60, 50), width=4)
    d.line([(137, 26), (143, 26)], fill=(178, 60, 50), width=2)
    d.line([(134, 36), (146, 36)], fill=(178, 60, 50), width=2)
    d.line([(140, 14), (140, 8)], fill=(178, 60, 50), width=2)
    # candlestick merah jatuh (atas, kiri-tengah)
    for cx, cy0, cy1 in ((88, 20, 30), (108, 16, 28)):
        d.line([(cx, cy0 - 4), (cx, cy1 + 4)], fill=RED_M, width=2)
        d.rectangle([cx - 4, cy0, cx + 4, cy1], fill=RED_M)
    # panah merah turun (kanan-atas, utuh di atas strip y<40)
    ax = 170
    d.line([(ax, 10), (ax, 30)], fill=RED_M, width=4)
    d.polygon([(ax - 8, 24), (ax + 8, 24), (ax, 38)], fill=RED_M)
    return im


def p_kenya_foto(w, h):
    """FOTO kartu 12: menara bor BESAR di tengah + pumpjack di kanan
    + matahari senja. Puncak menara y 10 (di bawah patch atas y 2-8).
    Latar oranye senja tetap (210,140,70)."""
    im = Image.new("RGB", (w, h), (210, 140, 70))
    d = ImageDraw.Draw(im)
    d.ellipse([148, 4, 168, 24], fill=(240, 210, 130))  # matahari
    # tanah gelap di bawah
    d.rectangle([0, 52, w, h], fill=(60, 45, 35))
    # menara bor BESAR tengah: kaki + palang + puncak
    d.line([(62, 58), (88, 12)], fill=(70, 50, 40), width=5)
    d.line([(114, 58), (88, 12)], fill=(70, 50, 40), width=5)
    d.line([(80, 24), (96, 24)], fill=(70, 50, 40), width=3)
    d.line([(75, 34), (101, 34)], fill=(70, 50, 40), width=3)
    d.line([(69, 44), (107, 44)], fill=(70, 50, 40), width=3)
    d.rectangle([83, 10, 93, 16], fill=(70, 50, 40))
    # pumpjack (angguk) kanan: balok + kepala kuda di ATAS strip
    # sumber (y<40) supaya terbaca; alasnya di balik strip
    d.line([(120, 52), (152, 30)], fill=(70, 50, 40), width=5)
    d.rectangle([146, 22, 160, 34], fill=(70, 50, 40))
    return im


def p_f1_foto(w, h):
    """FOTO kartu 13: mobil balap BESAR di trek basah + semprotan air
    + band kotak-kotak di atas. Tanpa teks 'P1'. Latar gelap tetap."""
    im = Image.new("RGB", (w, h), (30, 34, 44))
    d = ImageDraw.Draw(im)
    # band kotak-kotak (2 baris, atas)
    sq = 13
    for i in range(0, w // sq + 1):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([i * sq, j * sq, (i + 1) * sq, (j + 1) * sq],
                            fill=WHITE)
    # trek basah
    d.rectangle([0, 52, w, h], fill=(52, 56, 66))
    d.line([(0, 52), (w, 52)], fill=(120, 125, 135), width=1)
    # mobil balap BESAR (profil samping) — massa utama di kiri strip
    # sumber (x<83) dan di atasnya (y<40): sayap belakang, bodi,
    # kokpit + halo, sayap depan, 2 roda
    d.rectangle([84, 28, 98, 33], fill=(178, 40, 40), outline=NAVY,
                width=1)  # sayap belakang
    d.line([(91, 33), (91, 40)], fill=NAVY, width=2)
    d.polygon([(16, 48), (22, 36), (64, 32), (84, 36), (88, 44),
               (88, 48)], fill=(178, 40, 40), outline=NAVY)  # bodi
    d.polygon([(52, 34), (60, 27), (72, 27), (76, 34)], fill=(30, 34, 44),
              outline=NAVY)  # kokpit
    d.arc([50, 25, 78, 36], 180, 360, fill=NAVY, width=2)  # halo
    d.rectangle([10, 42, 20, 48], fill=(178, 40, 40), outline=NAVY,
                width=1)  # sayap depan
    # roda BESAR
    for wx in (38, 78):
        d.ellipse([wx - 8, 36, wx + 8, 52], fill=(15, 15, 18),
                  outline=NAVY, width=1)
        d.ellipse([wx - 4, 40, wx + 4, 48], fill=(120, 125, 135))
    return im


def painter_for(key, w, h):
    """Painter tile (w x h) untuk kartu/hero — TANPA bar aksen, TANPA strip."""
    # FOTO (varian foto, Kevin 21 Nov 19:14 WIB): isi foto digambar
    # ulang supaya cocok literal dengan judul. Cabang lama di bawah
    # tetap ada (revert) tapi tidak terjangkau untuk 13 key ini.
    if key == "akvan":
        return p_akvan_foto(w, h)
    if key == "kyiv":
        return p_kyiv_foto(w, h)
    if key == "cop31":
        return p_cop31_foto(w, h)
    if key == "cricket":
        return p_cricket_foto(w, h, SAGE_PALE)
    if key == "iraq":
        return p_iraq_foto(w, h)
    if key == "florida":
        return p_florida_foto(w, h)
    if key == "italy":
        return p_italy_foto(w, h)
    if key == "taipei":
        return p_taipei_foto(w, h, TEAL_PALE)
    if key == "gold":
        return p_gold_foto(w, h)
    if key == "poland":
        return p_poland_foto(w, h)
    if key == "mkt":
        return p_mkt_foto(w, h, GOLD_PALE)
    if key == "kenya":
        return p_kenya_foto(w, h)
    if key == "f1":
        return p_f1_foto(w, h)
    if key == "gta":
        return p_gta_r6(w, h)  # REVISI-6: "VI" di tengah (lokal)
    if key == "sco":
        return p_sco_ref(w, h, BLUE_PALE)
    if key == "apec":
        return p_flags3_ref(w, h, [RED_M, NAVY, WHITE], LAVENDER)
    if key == "euuk":
        # REV10: KTT EU-UK — 3 tiang bendera abstrak (biru EU, merah,
        # abu terang; putih murni dihindari karena p_flags3_ref
        # menggambar dot merah di bendera putih = mirip Jepang).
        return p_flags3_ref(w, h, [NAVY, RED_M, (210, 215, 225)],
                            LAVENDER)
    if key == "taipei":
        return p_chart_ref(w, h, TEAL_PALE)
    if key == "mkt":
        return p_chart_ref(w, h, GOLD_PALE)
    if key == "gold":
        return p_chart_gold_r8(w, h)  # REVISI-8: selaras 08/11 (garis tipis)
    if key == "prabowo":
        return p_flags3_ref(w, h, [RED_M, WHITE, GOLD_M], TEAL_PALE)
    return r1.TILE_1R[key](w, h)


# --- painter baru ref-2 ------------------------------------------------
AKVAN_BG = (22, 54, 78)      # navy-teal hero 1 (beda dari kyiv (16,23,38))
COP31_BG = (17, 54, 60)      # panel teal gelap hero 3 (diukur dari referensi)


def p_akvan_ref2(w, h):
    """Hero 1 Akvan ala referensi (koreksi Kevin 21:36 WIB): latar navy
    gelap + SPIRAL UTUH kecil di dalam tile (3 busur konsentris, radius
    maks 28px, pusat (150,47) — margin >= 19px dari semua tepi, TIDAK
    ada lingkaran yang menyentuh/terpotong tepi) + panah merah ke
    Gopalpur + garis putus-putus emas + label 'BAY OF BENGAL'.
    Panel tan 'ODISHA / INDIA / Gopalpur' digambar terpisah di
    hero_image_with_panel (di atas painter ini)."""
    im = Image.new("RGB", (w, h), AKVAN_BG)
    d = ImageDraw.Draw(im)
    cx, cy = 150, 47
    for r, a0, a1 in ((12, 20, 320), (20, 140, 80), (28, 260, 200)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1,
              fill=(200, 220, 235), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=WHITE)
    # panah merah dari spiral ke tepi panel (Gopalpur) — berhenti di
    # x=70 (tepi panel di y~79), tidak masuk ke panel
    d.line([(126, 60), (70, 79)], fill=RED_M, width=3)
    d.polygon([(70, 79), (80, 74), (80, 84)], fill=RED_M)
    # garis putus-putus emas ke kanan (seperti referensi)
    x0, y0, x1, y1 = 182, 42, 250, 28
    steps = 8
    for i in range(steps):
        fx0 = x0 + (x1 - x0) * i / steps
        fy0 = y0 + (y1 - y0) * i / steps
        fx1 = x0 + (x1 - x0) * (i + 0.6) / steps
        fy1 = y0 + (y1 - y0) * (i + 0.6) / steps
        d.line([(fx0, fy0), (fx1, fy1)], fill=(220, 190, 90), width=2)
    f_lab = F(SS700, 8)
    d.text((w - 6, h - 13), "BAY OF BENGAL", font=f_lab,
           fill=(170, 190, 205), anchor="ra")
    return im


def p_cop31_ref2(w, h):
    """Hero 3 COP31 diperkaya ala referensi: panel teal gelap + globe +
    termometer + KARTU PUTIH 'COP31 / FINAL DAY · DEADLOCK' di kanan.
    Gambar mengisi tile (tanpa strip bawah — perintah Kevin 19:09)."""
    im = Image.new("RGB", (w, h), COP31_BG)
    d = ImageDraw.Draw(im)
    # globe: laut biru + daratan hijau (kiri)
    gx, gy, gr = 55, 47, 24
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 130, 180),
              outline=NAVY, width=2)
    d.ellipse([gx - 14, gy - 10, gx + 2, gy + 4], fill=(90, 150, 90))
    d.ellipse([gx - 2, gy + 8, gx + 14, gy + 18], fill=(90, 150, 90))
    d.ellipse([gx + 6, gy - 16, gx + 16, gy - 4], fill=(90, 150, 90))
    # termometer (tengah)
    tx = 102
    d.rounded_rectangle([tx, 14, tx + 12, 66], radius=6,
                        fill=(240, 244, 246), outline=NAVY, width=1)
    d.rectangle([tx + 4, 34, tx + 8, 62], fill=RED_M)
    d.ellipse([tx - 3, 60, tx + 15, 78], fill=RED_M, outline=NAVY, width=1)
    # kartu putih COP31 (kanan)
    kx0, ky0, kx1, ky1 = 130, 10, w - 5, h - 10
    d.rectangle([kx0, ky0, kx1, ky1], fill=WHITE, outline=NAVY, width=1)
    f_top = F(SS800, 7)
    d.text(((kx0 + kx1) // 2, ky0 + 6), "ANTALYA \u00b7 NOV 20",
           font=f_top, fill=RED_M, anchor="ma")
    f_big = F(GEL700, 22)
    d.text(((kx0 + kx1) // 2, ky0 + 18), "COP31", font=f_big, fill=NAVY,
           anchor="ma")
    f_bot = F(SS800, 7)
    # REVISI-10: teks digeser +5px ke atas (ky1-16 -> ky1-21) — tinta
    # lama y 73-76 (diukur di revisi-9) bertabrakan dengan label sumber
    # 20px (atas y=73); kini tinta y 68-71, celah 2px ke label.
    d.text(((kx0 + kx1) // 2, ky1 - 21), "FINAL DAY \u00b7 DEADLOCK",
           font=f_bot, fill=RED_M, anchor="ma")
    # Pengayaan suasana summit (spek build final v4): deret 5 bendera
    # kecil di strip bawah (y 80-94) — di bawah globe/termometer, di
    # kiri kartu putih. Gaya flat, warna kalem.
    for fx, fc in ((12, (178, 34, 34)), (34, (36, 84, 160)),
                   (56, (30, 60, 110)), (78, (46, 120, 80)),
                   (100, (180, 140, 50))):
        d.line([(fx, 82), (fx, 94)], fill=(90, 90, 90), width=1)
        d.rectangle([fx, 80, fx + 11, 87], fill=fc)
    return im


# --- label ATAS + label sumber di dalam gambar (pola PRIORITAS #1 Kevin
# 21 Nov 14:41 WIB, dari rank 1 ni21 samatch-we) -------------------------
# Banner MERAH topik di kiri atas tiap gambar + label sumber PUTIH di
# ATAS gambar, kanan bawah (REVISI-4, Kevin 21 Nov 15:10 WIB): label
# kembali ke posisi semula (di atas gambar, bukan panel teks) dan
# DIPERBESAR (teks NAVY 11pt BOLD, kotak 15px, outline NAVY 1px —
# outline abu revisi-1 terlalu samar di atas kartu putih COP31).
# REVISI-1/2 (panel teks) DIBATALKAN oleh perintah ini.
# Banner kiri-atas TIDAK boleh mencapai patch warna-atas di tengah
# (kartu x 82-102, hero x 120-140) — lebar banner topik: hero <=115,
# kartu <=81 (REVISI-4: assert kartu 78 -> 81 karena "SCO FORUM" 12pt
# = 79px; patch baru mulai x 82). REVISI-4: banner 16px/12pt
# (terlebar hero 111px "COP31: FINAL DAY", kartu 79px "SCO FORUM").
# REVISI-5 (Kevin 21 Nov 15:17-15:18 WIB): banner merah isi NILAI berita
# (angka/hasil terpenting tiap cerita, seperti rank 1 "42 HURT") — BUKAN
# topik lagi. Topik tetap ada di kicker bawah gambar ("01 · ODISHA ·
# CYCLONE", dst.) — karena itu `topic` TIDAK diubah; nilai banner ada
# di field baru `banner` (kartu) / dict HERO_BANNERS (hero).
# Nilai disingkat supaya muat 12pt (hero <=115, kartu <=81; diukur):
# hero 1 "300,000 EVACUATED" (122) -> "300K EVACUATED" (106);
# hero 2 "STRIKES FROM 01:25" (126) -> "STRIKES 01:25" (92);
# kartu 5 "OPENS 20-22 NOV" (110) -> "20-22 NOV" (70);
# kartu 6 "CREST 18.6 FT" (91) -> "CREST 18.6" (75);
# kartu 7 "XI MEETS ALBANESE" (122) -> "ALBANESE" (71; "XI+ALBANESE"
# 88 juga tidak muat); kartu 9 "-2.8% TO $3,520" (102) -> "-2.8%" (46);
# kartu 10 "METASCORE 99" (95) -> "SCORE 99" (66);
# kartu 12 "$86.8BN DEALS" (96) -> "$86.8BN" (60);
# kartu 11 "NIKKEI -4.1%" 12pt (86) tidak muat -> 11pt (80), satu-
# satunya banner 11pt (field `banner_pt`). Semua nilai diverifikasi ke
# repo-v3/STORIES.md (bukan karangan). Kotak putih sumber TIDAK berubah.
# Banner kiri-atas TIDAK boleh mencapai patch warna-atas di tengah
# (kartu x 82-102, hero x 120-140) — lebar banner topik: hero <=115,
# kartu <=81 (REVISI-4: assert kartu 78 -> 81 karena "SCO FORUM" 12pt
# = 79px; patch baru mulai x 82). REVISI-4: banner 16px/12pt
# (terlebar hero 111px "COP31: FINAL DAY", kartu 79px "SCO FORUM").
# Label data navy lama (CARD_LABELS: "175* · RECORD" dll) DIHAPUS —
# datanya sudah ada di judul/ringkasan di bawah gambar.
HERO_BANNERS = {1: "300K", 2: "01:25",
                3: "NO NEW TEXT"}
# REV3 (Kevin 21 Nov 19:56 WIB, "double teks" + banner 14px): SEMUA
# banner 14pt (HERO_BANNER_PT lama DIHAPUS — hero 1 "300K" kembali
# 14pt seperti REVISI-7; REVISI-9 "Cyclone 11px" dicabut REV3 karena
# Kevin minta banner digedein lagi). Hero 2 "STRIKES 01:25" ->
# "01:25" ("STRIKES" duplikat "strike" di ringkasan; nilai = jam
# serangan pertama). Hero 3 "NO FOSSIL DEAL" -> "NO NEW TEXT"
# ("FOSSIL"/"DEAL" duplikat ringkasan; nilai = tidak ada teks baru
# sampai Jumat sore, terverifikasi STORIES.md; "FINAL DAY" duplikat
# judul, "DEADLOCK" tidak terverifikasi). Hero 1 "300K" tetap (nilai).
HERO_SOURCES = {1: "IMD", 2: "Reuters", 3: "Reuters"}
# Lift label hero 1 (+10px): sudut kanan bawah gambar penuh sesak —
# label "BAY OF BENGAL" tinta y 86-90 (diukur); label 20px di y 63-83
# (bawah 83, celah 3px) tidak menutupinya; area itu latar navy kosong
# (spiral maks x 178, garis emas y <=42).
CARD_SOURCES = {4: "ESPNcricinfo", 5: "Reuters",
                6: "Florida Today", 7: "Reuters", 8: "Reuters",
                9: "KuCoin News", 10: "Reuters", 11: "Reuters",
                12: "Capital FM", 13: "The Times"}


def add_banner(img, text, pt=14):
    """Banner merah NILAI BERITA di kiri atas gambar (0,0), tinggi 24px
    (REV3: 20 -> 24px, teks 12pt -> 14pt supaya nomor/teks kelihatan di
    ukuran tampil — perintah Kevin 21 Nov 19:56 WIB), teks putih
    (REVISI-5: isi = nilai berita, bukan topik lagi; pt default 14 —
    pengecualian 11pt DIHAPUS REV3), BORDER PUTIH 2px (REVISI-3).
    Padding teks +16 -> +12 (REV3) supaya "175* RUNS" 14pt muat
    <=81px (diukur box 79px). Outline digambar DI DALAM kotak (PIL
    outline) supaya ukuran luar tetap cw x 24 — tidak menabrak patch
    warna-atas (hero x 120-140, kartu x 82-102). Karena banner lebih
    tinggi 4px, isi panel digeser (REV3, pola REVISI-10): "ODISHA"
    hero 1 y 21 -> 25, globe COP31 gy 50 -> 54, plakat Italia y 20
    -> 24. Kembalikan (img, lebar_banner).
    KOREKSI (Kevin 22 Nov 04:54 WIB, "Bukan label atas win"): REV10
    (22 Nov 04:46 WIB, latar HITAM + padding +8) DIBATALKAN — label
    atas kembali MERAH + padding +12 seperti semula; yang diubah
    justru chip sumber BAWAH (lihat add_source_on_image)."""
    d = ImageDraw.Draw(img)
    f_l = F(SS800, pt)
    tw = d.textlength(text, font=f_l)
    cw, ch = int(tw) + 12, 24
    d.rectangle([0, 0, cw, ch], fill=RED, outline=WHITE, width=2)
    d.text((6, ch // 2), text, font=f_l, fill=WHITE, anchor="lm")
    return img, cw


# Lift label sumber hero (px ke atas dari posisi kanan-bawah baku) —
# hanya hero 1 yang penuh sesak (lihat HERO_SOURCES di atas).
HERO_SRC_LIFT = {1: 10}


def add_source_on_image(img, text, lift=0):
    """Kotak label sumber NAVY di ATAS gambar, kanan bawah (KOREKSI
    Kevin 22 Nov 04:54 WIB, "Bukan label atas win, tapi yang bawah
    warna navy" — instruksi asli 04:46 WIB: lebar pas teks + ganti
    warna): background NAVY (15,36,64), teks WHITE 16pt BOLD —
    kontras putih-di-navy 15,59:1 (diukur, jauh di atas 4,5:1).
    FONT 16pt = lantai legibility Kevin (keputusan 04:55 WIB, "Potong
    teks label biar muat 16pt"; aturan: tidak ada teks di bawah 16px
    di file). Semua 7 nama sumber MUAT utuh di 16pt di gambar
    tersempit (kartu 187px): terpanjang "Formula1.com" 102,9px ->
    chip 114px < 183px — TIDAK ADA singkatan yang dipakai.
    Sebelumnya background TAN (MAP_HEADER_BG) + teks INK 11pt sejak
    REV3/REV8. Lebar PAS TEKS: cw = teks + 12 (6px tiap sisi), aturan
    min 100px DIHAPUS (dulu "diperlebar" vs rank 1 — Kevin minta
    lebar sesuai teks saja). Kotak 20px, inset 2px dari tepi
    kanan/bawah gambar. `lift`: geser ke atas (px) bila sudut kanan
    bawah penuh sesak (hero 1: lift 10, supaya tidak menutupi
    "BAY OF BENGAL" — label y 63-83, bawah tetap 83, celah 3px ke
    tinta y 86-90). Kembalikan (img, bbox_dalam_tile) — pemanggil
    mendaftarkan bbox halaman sebagai 'image' (label di atas gambar
    pengecualian yang disengaja; tidak boleh menutupi teks lain —
    diverifikasi check no-overlap + cek piksel)."""
    w, h = img.size
    d = ImageDraw.Draw(img)
    f_s = F(SS800, 16)
    tw = d.textlength(text, font=f_s)
    # KOREKSI (Kevin 22 Nov 04:54 WIB): strip NAVY + teks WHITE;
    # lebar PAS TEKS (teks + 12), tanpa min 100px. Full-width TIDAK
    # dipakai: menutupi "Gopalpur" + "BAY OF BENGAL" (hero 1) dan
    # bendera-bendera (hero 3) — dicek visual.
    cw, ch = int(tw) + 12, 20
    x0 = w - cw - 2
    y0 = h - ch - 2 - lift
    d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=NAVY)
    d.text((x0 + cw // 2, y0 + ch // 2), text, font=f_s, fill=WHITE,
           anchor="mm")
    return img, (x0, y0, x0 + cw, y0 + ch)


# REV10 (22 Nov 05:24 WIB — perbaiki C3 duel rev9: juri memuji tag
# status lawan CONFIRMED/OFFICIAL/REPORTED): pill status kecil di
# kanan atas tiap gambar hero/kartu. Posisi sengaja di kanan atas:
# tidak menyentuh patch warna-atas (tengah-atas, hero x 120-140,
# kartu x 82-102) dan tidak menutupi banner (kiri atas) maupun chip
# sumber (kanan bawah). 10pt BOLD — terbaca juri di resolusi penuh.
# Status dari sumber tiap cerita (STORIES.md): OFFICIAL = diumumkan
# badan resmi (IMD, upacara pemerintah); CONFIRMED = 2+ wire besar
# atau skor resmi; REPORTED = satu outlet sekunder saja.
STATUS_COLORS = {"CONFIRMED": (27, 110, 62),
                 "OFFICIAL": (15, 36, 64),
                 "REPORTED": (96, 100, 108)}
HERO_STATUS = {1: "OFFICIAL", 2: "CONFIRMED", 3: "CONFIRMED"}
CARD_STATUS = {4: "CONFIRMED", 5: "CONFIRMED", 6: "CONFIRMED",
               7: "CONFIRMED", 8: "CONFIRMED", 9: "REPORTED",
               10: "CONFIRMED", 11: "CONFIRMED", 12: "OFFICIAL",
               13: "CONFIRMED"}


def add_status_tag(img, status):
    """Pill status di kanan atas gambar. Kembalikan img (tanpa bbox —
    di dalam area gambar yang sudah terdaftar)."""
    w, h = img.size
    d = ImageDraw.Draw(img)
    f_t = F(BOLD, 10)
    tw = d.textlength(status, font=f_t)
    pw, ph = int(tw) + 14, 15
    x0, y0 = w - pw - 4, 4
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=7,
                        fill=STATUS_COLORS[status])
    d.text((x0 + pw // 2, y0 + ph // 2), status, font=f_t, fill=WHITE,
           anchor="mm")
    return img


def top_color(img):
    """Warna atas tile: rata-rata patch 20x6 di tengah-atas (metode 1r)."""
    w, _ = img.size
    patch = img.crop((w // 2 - 10, 2, w // 2 + 10, 8))
    px = list(patch.getdata())
    n = len(px)
    return tuple(sum(c[i] for c in px) // n for i in range(3))

# ------------------------------------------------------------------ layout
# Posisi vertikal (skala 1024, diukur dari referensi 2048/2) — REF-3:
# semua section di bawah masthead digeser +4px untuk memberi ruang
# judul -> deck yang lebih besar (fix 1); margin bawah ~20px.
STRIP_Y, STRIP_H = 133, 47
CHIPS_Y, CHIPS_H = 186, 16   # REF-4: 188->186 (gap strip->chips 8->6)
HERO_Y = [210, 313, 417]  # REF-4: 212->210 (gap chips->hero 8->6); gap antar-hero tetap 8/9
HERO_H = 95
MAP_X, MAP_Y, MAP_W, MAP_H = 700, 210, 300, 302  # REF-4: 212->210 (ikut hero1; bawah 512 = bawah hero3)
MAP_HEADER_H = 22            # strip header tan (referensi y 207-230)
MAP_NAVY_Y = MAP_Y + MAP_HEADER_H   # 234 — navy 234-514 (h 280)
MAP_NAVY_H = MAP_H - MAP_HEADER_H
MAP_HEADER_BG = (235, 230, 212)  # tan strip header (ref-3: diukur dari
# referensi (231-236, 228-229, 211-213); ref-2 (232,225,207) sedikit
# lebih gelap/merah)
CARD_Y = [520, 669]  # REVISI-2: CARD_H 125->141 (ruang bebas MORE
# 32px ke kartu, 16px/baris); gap antar-baris tetap 8; gambar kartu 46->62px
CARD_H = 141
CARD_X = [24, 221, 418, 615, 812]
CARD_W = [187, 187, 187, 187, 188]
MORE_Y, MORE_H = 818, 126  # REVISI-2: MORE 8 baris -> 6 baris
# (18 brief, 6/kolom); H 158->126; MORE_Y 786->818 (kartu memanjang
# +32px); bawah MORE tetap 944, gap ke DATE CHECK tetap 8
DC_Y, DC_H = 952, 38  # REV7: 950->952, 42->38 (teks DC 11->10pt,
# diukur font asli: 2 baris (855/862 dari max 878), tinta 21px;
# gap MORE->DC 8, kotak 952-990, gap DC->footer 5)
SRC_Y = 995  # REV6: 991->995 (footer 11pt tetap 2 baris: 995 + 1006;
# tinta bawah 1021, margin bawah 3px; gap DC->footer 3px)


def draw_wrapped(d, x, y, text, font, max_w, lh, fill, label):
    """Wrap + gambar per baris, daftarkan tiap bbox. Kembalikan y bawah."""
    lines = rv.wrap(d, text, font, max_w)
    for ln in lines:
        b = d.textbbox((x, y), ln, font=font, anchor="la")
        d.text((x, y), ln, font=font, fill=fill, anchor="la")
        r1.reg("text", b, label)
        y += lh
    return y, lines


def draw_masthead_ref(d):
    """Kicker + garis + judul HITAM Gelasio 700 56px tengah + deck
    Gelasio Italic + garis (spesifikasi Kevin 21:37 WIB).

    Judul hitam seragam satu baris (pelajaran 19:01 WIB), tracking
    -0,4px (digambar per karakter — Pillow tidak dukung tracking).
    Lebar terukur 743px (target referensi ~737px). Posisi deck + garis
    dihitung dari bbox judul yang terukur agar ada jarak >= 3px."""
    # REVISI-9: kicker 12pt — teks digambar di y=10 (bukan 12) supaya
    # celah ke garis (rule_y=27) tetap >= 2px: bbox bawah 12pt = 24.
    # REVISI-10: kicker 14pt — diukur: 14pt di y=10 tinta bawah y=26
    # (celah 0, assert GAGAL); teks digambar di y=8 (tinta y 13-24,
    # celah 2px), garis tetap y=27, judul tidak digeser.
    f_kick = F(BOLD, 14)
    kl = "THE WORLD IN ONE DAY"
    b = d.textbbox((MX, 8), kl, font=f_kick, anchor="la")
    d.text((MX, 8), kl, font=f_kick, fill=RED)
    r1.reg("text", b, "kicker-left")
    right = "FRIDAY'S NEWS \u00b7 ONE PAGE \u00b7 31 STORIES \u00b7 6 CONTINENTS"
    b = d.textbbox((W - MX, 8), right, font=f_kick, anchor="ra")
    d.text((W - MX, 8), right, font=f_kick, fill=NAVY, anchor="ra")
    r1.reg("text", b, "kicker-right")
    rule_y = 27
    d.line([(MX, rule_y), (W - MX, rule_y)], fill=INK, width=2)
    r1.reg("rule", (MX, rule_y - 1, W - MX, rule_y + 1), "kicker-rule")
    assert rule_y - 1 - b[3] >= 2, "garis kicker terlalu dekat ke kicker"

    # --- Judul HITAM Gelasio 700 56px, tracking -0,4px, TENGAH ---
    # Anchor "mt" (atas tinta): tinta judul y 36-92 (ink_h 56px).
    f_title = F(DISPLAY_B, 56)
    title = "Friday 20 November 2026"
    tw = tracked_width(d, title, f_title)
    assert tw <= CW, f"judul terlalu lebar: {tw:.0f}px"
    tb = d.textbbox((W // 2, 36), title, font=f_title, anchor="mt")
    x0, x1 = draw_tracked(d, W // 2, 36, title, f_title, INK)
    b = (int(x0), tb[1], int(x1), tb[3])
    r1.reg("text", b, "title")
    assert b[3] - b[1] >= 40, f"judul terlalu pendek? {b}"
    title_bottom = b[3]

    # --- Deck merah Gelasio Italic 11,6px -> 12px (PIL butuh integer) ---
    # REF-3 fix 1 (koreksi Kevin 21:50 WIB): deck TERLALU MEPET di bawah
    # judul di ref-2 (offset +4 -> celah ~9px visual; "y" di "Friday"
    # hampir kena teks merah). Offset kini +17 -> celah tinta ~17px
    # (diukur dari bbox teks; visual ~17px di descender "y", ~22px di
    # kolom biasa — samakan kesan ruang dengan referensi).
    # Konsekuensi: garis deck turun ke ~126, celah garis->strip tinggal
    # ~7px (dulu 16px) — masih pemisah jelas, dicatat di NOTE.
    # Judul tetap Gelasio 700 56px, tracking -0,4px, hitam, tengah,
    # satu baris.
    # REV6 (Kevin 20:18 WIB: deck digedein 3px, harus tetap 1 baris):
    # 12 -> 15pt. Diukur font asli (Gelasio Italic): lebar 758px
    # (CW 976, muat 1 baris); tinta 17px -> rule2_y = 130, TEPAT di
    # batas assert (<= STRIP_Y-3 = 130); celah garis->strip 3px.
    f_deck = F(SERIF_IT, 15)
    dw = d.textlength(DECK_REF, font=f_deck)
    assert dw <= CW, f"deck terlalu lebar: {dw:.0f}px"
    b = d.textbbox((W // 2, title_bottom + 17), DECK_REF, font=f_deck,
                   anchor="mt")
    d.text((W // 2, title_bottom + 17), DECK_REF, font=f_deck, fill=RED,
           anchor="mt")
    r1.reg("text", b, "deck")
    deck_top = b[1]
    deck_bottom = b[3]
    assert 16 <= deck_top - title_bottom <= 18, (
        f"celah judul->deck {deck_top - title_bottom}px, target 16-18px")

    rule2_y = deck_bottom + 4
    d.line([(MX, rule2_y), (W - MX, rule2_y)], fill=INK, width=2)
    r1.reg("rule", (MX, rule2_y - 1, W - MX, rule2_y + 1), "deck-rule")
    assert rule2_y <= STRIP_Y - 3, f"garis deck y={rule2_y} menabrak strip"
    return {"title_box": (36, title_bottom), "deck_bottom": deck_bottom,
            "rule2_y": rule2_y, "title_w": round(tw, 1),
            "deck_w": round(dw, 1),
            "title_deck_gap": deck_top - title_bottom}


def draw_strip_ref(d):
    """Strip 6 angka: angka merah serif bold 26pt + caption 9pt, 1 baris.

    Referensi: TANPA bar emas di bawah strip; antar sel ada divider tipis.
    Angka dari pool kita."""
    f_n = F(NUM_F, 26)
    f_c = F(REG, 9)
    d.rectangle([MX, STRIP_Y, W - MX, STRIP_Y + STRIP_H], outline=NAVY,
                width=1)
    # REF-3 fix 4: interior strip hampir putih (251,250,245) seperti
    # referensi (diukur (251,250,245) di dua titik strip referensi).
    d.rectangle([MX + 1, STRIP_Y + 1, W - MX - 1,
                 STRIP_Y + STRIP_H - 1], fill=NEAR_WHITE)
    widths = [163, 163, 163, 163, 163, 161]
    x = MX
    for i, (num, cap) in enumerate(NUMBERS_REF):
        cw = widths[i]
        cx = x + cw // 2
        for xx in (x + cw,) if i < 5 else ():
            d.line([(xx, STRIP_Y + 4), (xx, STRIP_Y + STRIP_H - 4)],
                   fill=(200, 195, 185), width=1)
        b = d.textbbox((cx, STRIP_Y + 2), num, font=f_n, anchor="ma")
        d.text((cx, STRIP_Y + 2), num, font=f_n, fill=RED, anchor="ma")
        r1.reg("text", b, f"strip-n{i + 1}")
        assert b[2] - b[0] <= cw - 4, f"angka strip {num} terlalu lebar"
        b = d.textbbox((cx, STRIP_Y + 32), cap, font=f_c, anchor="ma")
        d.text((cx, STRIP_Y + 32), cap, font=f_c, fill=NAVY, anchor="ma")
        r1.reg("text", b, f"strip-c{i + 1}")
        assert b[2] - b[0] <= cw - 4, f"caption strip '{cap}' terlalu lebar"
        x += cw


def draw_chips_ref(d):
    """Bar region: 7 segmen persegi panjang bewarna penuh lebar konten
    (pola PRIORITAS #1 Kevin 21 Nov 14:45 WIB, dari rank 2 ni21
    madsrepo) — satu segmen per region + jumlah cerita, warna konsisten
    dengan pin peta. MENGGANTIKAN chip kecil + teks kanan: aturan lama
    butir 3 checklist (hapus bar region) DICABUT oleh aturan baru 33 —
    legenda peta kini 'Lead/Feature', bukan hitungan region, jadi tidak
    ada duplikasi. Slot geometri sama (CHIPS_Y/H) — layout tidak
    bergeser."""
    # REVISI-4 (Kevin 21 Nov 15:12 WIB): teks bar region BOLD + LEBIH
    # BESAR — SS700 9pt -> SS800 12pt. Terlebar "ASIA-PACIFIC 10"
    # 84,9px < segmen 132px (REV1, diukur), tetap 1 baris, tidak
    # menabrak kotak sebelah; tinggi bar tetap 16px (tidak perlu
    # ditinggikan), layout lain tidak berubah.
    # REV1 (Kevin 21 Nov 18:41 WIB, "perbesar section Europe Amerika"):
    # EUROPE 140->175, AMERICAS 139->165; sisanya mengecil proporsional.
    f_ch = F(SS800, 12)
    widths = [175, 165, 132, 126, 126, 126, 126]  # total 976 = CW
    assert sum(widths) == CW, f"lebar bar region {sum(widths)} != {CW}"
    x = MX
    for (label, cnt), seg_w in zip(CHIPS, widths):
        txt = f"{label} {cnt}"
        d.rectangle([x, CHIPS_Y, x + seg_w, CHIPS_Y + CHIPS_H],
                    fill=CHIP_COLORS[label])
        cx = x + seg_w // 2
        b = d.textbbox((cx, CHIPS_Y + CHIPS_H // 2), txt, font=f_ch,
                       anchor="mm")
        d.text((cx, CHIPS_Y + CHIPS_H // 2), txt, font=f_ch, fill=WHITE,
               anchor="mm")
        r1.reg("text", b, f"bar-{label}")
        x += seg_w
    return {"bar_end": x, "segments": len(CHIPS)}


def hero_image_with_panel(key, w, h, hero):
    """Gambar hero 261x95. Hero 1: panel tan tempat di kiri (seperti
    referensi — hero 2/3 referensi TIDAK punya panel). TANPA strip bawah
    (perintah Kevin 19:09 WIB)."""
    im = painter_for(key, w, h)
    if hero["num"] != 1:
        return im
    d = ImageDraw.Draw(im)
    # panel tan, tepi kanan miring (seperti referensi)
    d.polygon([(0, 0), (78, 0), (64, h), (0, h)], fill=TAN_PANEL)
    f1 = F(BOLD, 15)
    f2 = F(BOLD, 11)
    f3 = F(REG, 9)
    # REV3: banner merah kini 24px (dulu 20px) — "ODISHA" digeser
    # +4px ke bawah (y 21 -> 25) supaya puncaknya tidak tertutup
    # banner; "INDIA" tetap y 41 (celah 5px dari bawah "ODISHA").
    # Titik + "Gopalpur" tidak digeser (sudah jauh di bawah).
    d.text((10, 25), "ODISHA", font=f1, fill=NAVY, anchor="la")
    d.text((10, 41), "INDIA", font=f2, fill=NAVY, anchor="la")
    d.ellipse([10, 84, 18, 92], fill=RED)
    d.text((22, 81), "Gopalpur", font=f3, fill=NAVY, anchor="la")
    return im


def draw_hero_ref(im, d, hero, y):
    """Satu baris hero horizontal: gambar kiri 261 + teks kanan 393,
    dalam satu frame border. Teks di-vertikal-tengah. REF-3 fix 3:
    ringkasan 3 baris (dulu 1 baris — area kosong besar di bawah teks);
    fix 4: area teks latar hampir putih (251,250,245)."""
    img = hero_image_with_panel(hero["painter"], 261, HERO_H, hero)
    # Pola label PRIORITAS #1 (21 Nov): banner merah NILAI BERITA di atas.
    # REVISI-4 (21 Nov 15:10 WIB): label sumber putih KEMBALI ke atas
    # gambar, kanan bawah, DIPERBESAR (11pt) — revisi-1/2 (panel teks)
    # dibatalkan Kevin ("taruh semula").
    img, bw = add_banner(img, HERO_BANNERS[hero["num"]])
    assert bw <= 115, f"banner hero {hero['num']} terlalu lebar: {bw}"
    img, lb = add_source_on_image(
        img, HERO_SOURCES[hero["num"]],
        lift=HERO_SRC_LIFT.get(hero["num"], 0))
    img = add_status_tag(img, HERO_STATUS[hero["num"]])  # REV10: C3
    r1.reg("image", (MX + lb[0], y + lb[1], MX + lb[2], y + lb[3]),
           f"hero{hero['num']}-src")
    im.paste(img, (MX, y))
    r1.reg("image", (MX, y, MX + 261, y + HERO_H), f"hero{hero['num']}-img")
    # Area teks hampir putih (fix 4) — gambar tidak tertutup (mulai x 262).
    d.rectangle([MX + 262, y + 1, 687, y + HERO_H - 1], fill=NEAR_WHITE)
    # REV1 (Kevin 21 Nov 18:41 WIB, "jangan pake border di gambar"):
    # frame border hero DIHAPUS (dulu outline INK 1px) — seperti rank 1.
    tx0, tx1 = 295, 688
    f_k = F(BOLD, 18)  # REV6: kicker KETIGA hero 18pt (Kevin 20:18 WIB:
    # koreksi "12/11 px" — hero 1 tetap 18pt, hero 2/3 naik 12 -> 18pt).
    # Diukur font asli (SourceSans3-800): lebar 234/235/246px
    # (slot 393px, muat satu baris), tinta 16px.
    f_t = F(SERIF_B, 20)
    f_s = F(SERIF, 12)  # REV6: brief hero 11 -> 12pt (Kevin 20:19 WIB:
    # +2px). 13pt TIDAK MUAT: hero 2 jadi 4 baris (blok 107 > 89) dan
    # hero 1/3 blok 92 > 89; 12pt = TERBESAR yang muat (blok 89 = batas,
    # 3 baris semua hero, diukur font asli). lh 13 -> 14.
    kick = f"{hero['num']:02d} \u00b7 {hero['place']} \u00b7 {hero['topic']}"
    title_lines = rv.wrap(d, hero["title"], f_t, tx1 - tx0)
    sum_lines = rv.wrap(d, hero["sum"], f_s, tx1 - tx0)
    assert len(title_lines) <= 2, f"judul hero {hero['num']} >2 baris"
    assert len(sum_lines) <= 3, f"ringkasan hero {hero['num']} >3 baris"
    assert len(sum_lines) == 3, (
        f"ringkasan hero {hero['num']} harus 3 baris (fix 3), "
        f"dapat {len(sum_lines)}: {sum_lines}")
    kslot = 20  # REV6: slot kicker KETIGA hero 20px (tinta 18pt:
    # top_off 7 + 16px = butuh 23px cy->judul; dulu 15 untuk 12pt)
    block = kslot + 3 + len(title_lines) * 22 + 2 + len(sum_lines) * 14  # REV6: lh brief 13 -> 14
    assert block <= HERO_H - 6, f"teks hero {hero['num']} tidak muat: {block}"
    # REVISI-1: blok teks digeser +5px ke atas (cy -5) — dipertahankan
    # di revisi-4 (tidak ada salahnya: panel teks kini kosong di bawah
    # tanpa label; teks tetap di tengah-ish, tidak ada yang berubah
    # selain posisi label yang pindah ke gambar).
    cy = y + (HERO_H - block) // 2 - 5
    b = d.textbbox((tx0, cy), kick, font=f_k, anchor="la")
    d.text((tx0, cy), kick, font=f_k, fill=RED, anchor="la")
    r1.reg("text", b, f"hero{hero['num']}-kick")
    yy = cy + kslot + 3
    for ln in title_lines:
        b = d.textbbox((tx0, yy), ln, font=f_t, anchor="la")
        d.text((tx0, yy), ln, font=f_t, fill=INK, anchor="la")
        r1.reg("text", b, f"hero{hero['num']}-title")
        yy += 22
    yy += 2
    for ln in sum_lines:
        b = d.textbbox((tx0, yy), ln, font=f_s, anchor="la")
        d.text((tx0, yy), ln, font=f_s, fill=INK, anchor="la")
        r1.reg("text", b, f"hero{hero['num']}-sum")
        yy += 14  # REV6: lh brief 13 -> 14
    # REVISI-4: label sumber sudah digambar DI ATAS gambar (lihat atas,
    # setelah add_banner) — tidak ada lagi label di panel teks.
    return img


def draw_card_ref(im, d, card, r, c):
    """Satu kartu: gambar ATAS (46px, tanpa band bawah, tanpa bar aksen)
    -> kicker -> judul (<=2 baris) -> ringkasan (<=2 baris)."""
    x, y = CARD_X[c], CARD_Y[r]
    w = CARD_W[c]
    img = painter_for(card["painter"], w - 2, 62)  # REVISI-2: 46->62
    # Pola label PRIORITAS #1 (21 Nov): banner merah NILAI BERITA di atas.
    # REVISI-4 (21 Nov 15:10 WIB): label sumber putih KEMBALI ke atas
    # gambar, kanan bawah, DIPERBESAR (11pt) — revisi-1/2 (panel teks)
    # dibatalkan Kevin ("taruh semula").
    img, bw = add_banner(img, card["banner"])
    assert bw <= 81, f"banner kartu {card['num']} terlalu lebar: {bw}"
    img, lb = add_source_on_image(img, CARD_SOURCES[card["num"]])
    img = add_status_tag(img, CARD_STATUS[card["num"]])  # REV10: C3
    r1.reg("image", (x + 1 + lb[0], y + 1 + lb[1],
                     x + 1 + lb[2], y + 1 + lb[3]),
           f"card{card['num']}-src")
    im.paste(img, (x + 1, y + 1))
    r1.reg("image", (x + 1, y + 1, x + w - 1, y + 63),
           f"card{card['num']}-img")
    # REF-3 fix 4: area teks kartu (di bawah gambar) hampir putih.
    d.rectangle([x + 1, y + 64, x + w - 1, y + CARD_H - 1],
                fill=NEAR_WHITE)
    # REV1 (Kevin 21 Nov 18:41 WIB, "jangan pake border di gambar"):
    # frame border kartu DIHAPUS (dulu outline NAVY 1px) — seperti rank 1.
    f_k = F(BOLD, 12)  # REV3: kicker kartu 9pt -> 12pt (nomor + teks
    # kelihatan di ukuran tampil — perintah Kevin 21 Nov 19:56 WIB;
    # diukur: kicker terpanjang "10 · NOWY LIPOWIEC · MISSILES" 12pt
    # = 166,9px < 175px; celah ke judul 1px, tidak overlap)
    f_t = F(SERIF_B, 13)
    f_s = F(SERIF, 10)
    # Kicker kartu: kota saja (seperti referensi "06 · BRUSSELS · EUROPE";
    # "kota, negara" tidak muat di 175px pada 9pt).
    kplace = card["place"].split(",")[0]
    kick = f"{card['num']:02d} \u00b7 {kplace} \u00b7 {card['topic']}"
    b = d.textbbox((x + 6, y + 68), kick, font=f_k, anchor="la")
    d.text((x + 6, y + 68), kick, font=f_k, fill=RED, anchor="la")
    r1.reg("text", b, f"card{card['num']}-kick")
    assert b[2] - b[0] <= w - 12, f"kicker kartu {card['num']} terlalu lebar"
    y2, tlines = draw_wrapped(d, x + 6, y + 82, card["title"], f_t, w - 12,
                              15, INK, f"card{card['num']}-title")
    assert len(tlines) <= 2, f"judul kartu {card['num']} >2 baris"
    y3, slines = draw_wrapped(d, x + 6, y + 114, card["sum"], f_s, w - 12,
                              12, INK, f"card{card['num']}-sum")
    assert len(slines) <= 2, f"ringkasan kartu {card['num']} >2 baris"
    assert y3 <= y + CARD_H - 2, f"kartu {card['num']} meluber ke bawah"
    # REVISI-4: label sumber sudah digambar DI ATAS gambar (lihat atas,
    # setelah add_banner) — tidak ada lagi label di panel teks.
    return img


def draw_map_ref(im, d, panels):
    """Peta tinggi: kotak 212-514 (setinggi 3 hero) = strip header tan
    212-234 + navy 234-514 (h 280, seperti referensi). Daratan DETAIL
    Natural Earth 110m dgn proyeksi referensi (ref-2; koreksi Kevin
    21:35 WIB). REF-3 fix 2 (koreksi Kevin 21:50 WIB): chip judul yang
    menembus batas strip/navy DIHAPUS — "WHERE IT HAPPENED" (kiri, BOLD
    11pt NAVY) dan "Pins 1-13 (Lead & Feature)" (kanan, REG 9pt GRAY)
    kini pada SATU baseline yang sama, di tengah strip header tan,
    seperti referensi (cc_mapatas.png). Legenda 2 chip gelap DI DALAM
    navy bawah-kiri. REF-6 (koreksi Kevin 23:05 WIB, "Pins 1-3 ga
    keliatan"): (1) bintang emas hero DIHAPUS — SEMUA 13 pin adalah
    lingkaran bernomor putih, termasuk pin 1 Gopalpur (REV1: warna
    per region, dulu merah semua; REV2: r=10 -> r=12, angka 14px);
    (2) jarak minimum antar pin 28px (REV2; REV1 24px, dulu 18px)
    (pusat-pusat; celah nyata 4px antar lingkaran r=12) — pin yang
    posisinya bertabrakan digeser
    sedikit (offset fallback, diurutkan lurus dulu supaya bujur/lintang
    terjaga) — dicatat di offset_used, bukan di-skip diam-diam."""
    x, y, mw, mh = MAP_X, MAP_Y, MAP_W, MAP_H
    ny, nh = MAP_NAVY_Y, MAP_NAVY_H
    # --- kotak peta: strip header tan + navy ---
    d.rectangle([x, y, x + mw, y + mh], fill=MAP_HEADER_BG, outline=NAVY,
                width=1)
    d.rectangle([x, ny, x + mw, y + mh], fill=r1.SEA_1R)
    mtmp = Image.new("RGB", (mw - 2, nh - 2), r1.SEA_1R)
    md = ImageDraw.Draw(mtmp)
    # garis khatulistiwa putus-putus (seperti referensi) — di atas laut,
    # di bawah daratan
    eq_y = int(map_xy(0, 0, x + 1, ny + 1 + 53)[1] - (ny + 1))
    for xx in range(0, mw - 2, 8):
        md.line([(xx, eq_y), (xx + 4, eq_y)], fill=(60, 80, 110), width=1)
    # daratan DETAIL (Natural Earth 110m) dgn proyeksi referensi
    # (x-scale 0,815, y-scale 1,0 — BUKAN equirectangular lama 2,7x)
    for poly in LAND_POLYS:
        pts = [(map_xy(lon, lat, x + 1, ny + 1 + 53)[0] - (x + 1),
                map_xy(lon, lat, x + 1, ny + 1 + 53)[1] - (ny + 1))
               for lon, lat in poly]
        md.polygon(pts, fill=MAP_LAND, outline=MAP_LAND_OUT)
    im.paste(mtmp, (x + 1, ny + 1))
    md = ImageDraw.Draw(im)
    fp = F(BOLD, 14)  # REV2: angka pin 10pt -> 14px (pin r=12)
    placed = []
    offset_used = []
    skipped = []

    def place(px, py):
        # REV2: minimum 28px antar pusat pin (lingkaran r=12 -> celah
        # nyata 4px, sama seperti REF-6/REV1). Ambang lama 24px (r=10)
        # membiarkan lingkaran r=12 bersentuhan.
        for (qx, qy) in placed:
            if ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5 < 28:
                return False
        placed.append((px, py))
        return True

    def place_with_offset(px, py):
        # REV2: lingkaran r=12 harus UTUH di dalam panel peta — pin 4
        # (Wellington, pusat x~990) menembus border kanan x=1000
        # sebanyak 2px pada build pertama rev2. Kandidat yang
        # menembus tepi panel ditolak sebelum cek jarak.
        # REF-6: kandidat diurutkan lurus dulu (utara/selatan/timur/barat)
        # supaya bujur/lintang pin tetap terjaga, lalu diagonal, lalu
        # lompatan besar. Perpindahan terkecil yang lolos ambang 28px
        # yang dipakai.
        # REV2: daftar kandidat DIPERPANJANG LAGI — pin r=12 (min 28px)
        # membuat pin 5 (Jurf al-Sakhar) dan pin 10 (Nowy Lipowiec)
        # tidak menemukan tempat dari daftar lama (build pertama GAGAL:
        # pin hilang collision). Tambahan diurutkan seperti semula:
        # lurus dulu, lalu diagonal, lalu lompatan besar.
        for dx, dy in [(0, 0), (0, 12), (0, -12), (14, 0), (-14, 0),
                       (10, 8), (10, -8), (-10, 8), (-10, -8),
                       (18, 0), (-18, 0), (0, 20), (0, -20),
                       (0, 18), (0, -18),
                       (14, 14), (14, -14), (-14, 14), (-14, -14),
                       (20, 0), (-20, 0), (24, 0), (-24, 0),
                       (0, 24), (0, -24), (0, -26), (0, 26),
                       (10, -24), (-10, -24), (10, 24), (-10, 24),
                       (28, 0), (-28, 0), (0, -28), (0, 28),
                       (0, -30), (0, 30),
                       (0, -32), (0, 32), (32, 0), (-32, 0),
                       (0, -34), (0, 34), (34, 0), (-34, 0),
                       (14, -28), (-14, -28), (14, 28), (-14, 28),
                       (28, -14), (-28, -14), (28, 14), (-28, 14),
                       (0, -36), (0, 36), (36, 0), (-36, 0),
                       (0, -40), (0, 40), (40, 0), (-40, 0),
                       # REV10: DIPERPANJANG LAGI — pin 13 Brussels
                       # (4,35E/50,85N) bertabrakan dengan klaster Eropa
                       # (London/Milan/Kyiv/Nowy Lipowiec semua dalam
                       # 21px); kandidat s.d. 40px habis. Tambahan
                       # lurus dulu lalu diagonal, seperti semula.
                       # Simulasi: (0,-44)/(0,44)/(44,0)/(-44,0)
                       # tabrakan; (0,-48) bebas pertama.
                       (0, -44), (0, 44), (44, 0), (-44, 0),
                       (0, -48), (0, 48), (48, 0), (-48, 0),
                       (36, -28), (-36, -28), (36, 28), (-36, 28),
                       (0, -52), (0, 52), (52, 0), (-52, 0)]:
            cx, cy = px + dx, py + dy
            if not (x + 13 <= cx <= x + mw - 13 and
                    ny + 13 <= cy <= y + mh - 13):
                continue
            if place(cx, cy):
                return (cx, cy), (dx, dy)
        return None, None

    for p in panels:
        city = p["map_city"]
        if city not in rv.PLACES:
            skipped.append((city, p["num"], "no-coords"))
            continue
        lon, lat = rv.PLACES[city]
        px, py = map_xy(lon, lat, x + 1, ny + 1 + 53)
        pos, off = place_with_offset(px, py)
        if pos is None:
            skipped.append((city, p["num"], "collision"))
            continue
        if off != (0, 0):
            offset_used.append((p["num"], city, off))
        qx, qy = pos
        # REF-6: SEMUA pin lingkaran bernomor — bintang emas hero
        # DIHAPUS (di ref-5 pin 1 Gopalpur digambar bintang tanpa angka
        # sehingga tidak dikenali sebagai pin 1).
        # REV1 (Kevin 21 Nov 18:41 WIB, "warnanya buat menarik kayak
        # rank 1"): pin BUKAN merah semua — warna per region, sama
        # dengan CHIP_COLORS bar region (aturan 33 Kevin). "ASIA" di
        # data -> "ASIA-PACIFIC" di CHIP_COLORS.
        pin_region = {"ASIA": "ASIA-PACIFIC"}.get(p["region"],
                                                 p["region"])
        pin_fill = CHIP_COLORS[pin_region]
        # REV2 (Kevin 21 Nov 19:05 WIB, "angka pada lingkaran di peta
        # kecil banget, gedein 14px"): pin r=10 -> r=12, angka 14px.
        # "13" 14px lebar 14,9px — muat di r=12 (chord di +-5,5px dari
        # pusat ~21,3px). Offset teks -10 DIUKUR (bukan tebakan):
        # tinta digit "13" terpusat tepat di pusat lingkaran.
        md.ellipse([qx - 12, qy - 12, qx + 12, qy + 12], fill=pin_fill,
                   outline=WHITE, width=1)
        mark = str(p["num"])
        tw = md.textlength(mark, font=fp)
        md.text((qx - tw / 2, qy - 10), mark, font=fp, fill=WHITE)
    r1.reg("image", (x, ny, x + mw, y + mh), "map")
    d.rectangle([x, y, x + mw, y + mh], outline=NAVY, width=1)

    # --- Header strip tan: DUA teks pada SATU baseline (fix 2) ---
    # Referensi (diukur): tinta "WHERE IT HAPPENED" y 438-441 (@2048)
    # dan tinta "Pins..." y 438-443 (@2048) — SATU baseline, keduanya di
    # atas peta (di dalam strip header tan). Judul BOLD 11pt NAVY (bukan
    # merah — referensi gelap (30,27,20)); teks pins REG 9pt GRAY.
    # Keduanya di-vertikal-tengah di strip header (cy = MAP_Y + 11).
    # Chip penembus border DIHAPUS — tidak ada whitelist lagi.
    # REF-7 (klarifikasi Kevin 23:14 WIB — "Bukan pin, tapi teks header
    # yang ada di peta"): teks pins 9pt REG abu-abu TIDAK TERBACA di
    # ukuran tampil HP (peta ~110px lebar -> teks jadi noda abu-abu),
    # sementara judul 11pt BOLD NAVY masih terbaca. Perbaikan: teks
    # pins jadi BOLD 12pt NAVY (diukur: judul 103,0px + note 140,6px +
    # gap = 249,6px < 276px tersedia — teks LENGKAP muat, tidak perlu
    # dipersingkat). Baseline tetap satu (assert di bawah).
    f_t = F(BOLD, 11)
    f_n = F(BOLD, 12)
    title = "WHERE IT HAPPENED"
    note = "Pins 1\u201313 (Lead & Feature)"
    hdr_cy = y + MAP_HEADER_H // 2
    tb = d.textbbox((x + 10, hdr_cy), title, font=f_t, anchor="lm")
    d.text((x + 10, hdr_cy), title, font=f_t, fill=NAVY, anchor="lm")
    r1.reg("text", tb, "map-title")
    nb = d.textbbox((x + mw - 8, hdr_cy), note, font=f_n, anchor="rm")
    d.text((x + mw - 8, hdr_cy), note, font=f_n, fill=NAVY, anchor="rm")
    r1.reg("text", nb, "map-pins-note")
    assert nb[0] - tb[2] >= 6, "teks pins menabrak judul peta"
    assert tb[1] >= y + 1 and tb[3] < ny, "judul peta keluar strip header"
    assert nb[1] >= y + 1 and nb[3] < ny, "teks pins keluar strip header"
    assert tb[1] == nb[1] or abs((tb[1] + tb[3]) // 2
                                 - (nb[1] + nb[3]) // 2) <= 1, (
        "judul peta dan teks pins tidak satu baseline")

    # --- Legenda 2 chip DI DALAM navy, bawah-kiri (referensi) ---
    # REV2 (Kevin 21 Nov 19:05 WIB, "kotak 2 bawah pada peta, warnanya
    # jangan hitam karna background peta hitam jadi ga keliatan. Gedein
    # juga kotak dan teks nya 14px"): fill HITAM (10,18,36) -> TAN
    # (MAP_HEADER_BG, sama seperti strip header peta — kontras kuat di
    # atas laut navy gelap, selaras palet); teks 8pt -> 14px, kotak
    # 16px -> 26px. Teks NAVY di atas tan, dot tetap RED.
    # Geometri baru: dot 8px di (lx+7..lx+15, tengah ly+13), teks di
    # lx+21 anchor lm (tengah ly+13), padding kanan 10px -> cw=tw+31.
    # Total terukur 248,6px (muat di 288px tersedia). Bawah kotak
    # tetap 8px di atas bawah panel (ly+26 = y+mh-8).
    f_l = F(BOLD, 14)
    ly = y + mh - 34
    lx = x + 8
    for txt in ("1\u20133 Lead", "4\u201313 Feature Stories"):
        tw = d.textlength(txt, font=f_l)
        cw = int(tw) + 31
        d.rounded_rectangle([lx, ly, lx + cw, ly + 26], radius=4,
                            fill=MAP_HEADER_BG)
        d.ellipse([lx + 7, ly + 9, lx + 15, ly + 17], fill=RED)
        d.text((lx + 21, ly + 13), txt, font=f_l, fill=NAVY, anchor="lm")
        lx += cw + 6
    assert lx - 6 <= x + mw - 4, "legenda peta keluar panel"
    return {"skipped": skipped, "offset_used": offset_used,
            "placed": len(placed), "title_pt": 11, "note_pt": 12,
            "header_cy": hdr_cy, "title_top": tb[1], "note_top": nb[1]}


def draw_more_ref(d):
    """MORE STORIES: judul + 'World Briefs (14-31)' kanan, 3 kolom brief
    1 BARIS @12pt (REV9, Kevin Gas 22 Nov 04:40 WIB — legibilitas juri:
    teks 10pt salah dibaca juri di crosscheck rev8; 5 brief dipangkas
    katanya supaya muat 312px @12pt, lihat BRIEFS_REF). Pemisah
    titik-titik antar baris (seperti referensi)."""
    d.rectangle([MX, MORE_Y, W - MX, MORE_Y + MORE_H], outline=NAVY,
                width=1)
    # REF-3 fix 4: interior MORE STORIES hampir putih (251,250,245)
    # seperti referensi (diukur (244-250,243-247,238-242)).
    d.rectangle([MX + 1, MORE_Y + 1, W - MX - 1,
                 MORE_Y + MORE_H - 1], fill=NEAR_WHITE)
    f_t = F(BOLD, 13)  # REF-4: judul 12->13pt (seimbang dgn brief 11pt)
    f_r = F(REG, 11)  # REF-4: 10->11pt
    btitle = "ALSO ON FRIDAY 20 NOVEMBER \u2014 18 MORE STORIES"
    b = d.textbbox((MX + 12, MORE_Y + 7), btitle, font=f_t, anchor="la")
    d.text((MX + 12, MORE_Y + 7), btitle, font=f_t, fill=INK, anchor="la")
    r1.reg("text", b, "more-title")
    b = d.textbbox((W - MX - 12, MORE_Y + 8), "World Briefs (14\u201331)",
                   font=f_r, anchor="ra")
    d.text((W - MX - 12, MORE_Y + 8), "World Briefs (14\u201331)", font=f_r,
           fill=GRAY, anchor="ra")
    r1.reg("text", b, "more-right")
    f_n = F(LIB_BOLD, 12)  # REV9: 11 -> 12pt (legibilitas)
    f_c = F(LIB_BOLD, 12)
    f_x = F(LIB_REG, 12)
    f_s = F(LIB_IT, 12)
    # Warna kotak nomor = warna region cerita itu (pola PRIORITAS #1
    # Kevin 21 Nov 14:42 WIB, dari rank 2 ni21 madsrepo).
    # REVISI-2: nomor ulang 14-31 (lama 22->20, 23->21, 24->22,
    # 25->23, 26->24, 27->25, 30->26, 31->27, 32->28, 33->29, 34->30,
    # 35->31); dihapus: lama 20, 21, 28, 29, 36.
    # V2 (b3): SCO/APEC/Prabowo kartu -> brief; Brisbane/Jakarta/
    # Loyalty hapus. Region brief baru: 15 ASIA, 16 AMERICAS, 17 ASIA.
    BRIEF_REGIONS = {14: "EUROPE", 15: "ASIA-PACIFIC", 16: "ASIA-PACIFIC",
                     17: "ASIA-PACIFIC", 18: "AMERICAS", 19: "WORLD",
                     20: "WORLD", 21: "EUROPE", 22: "ASIA-PACIFIC",
                     23: "EUROPE", 24: "ASIA-PACIFIC", 25: "MIDEAST",
                     26: "ASIA-PACIFIC", 27: "AMERICAS", 28: "AFRICA",
                     29: "AFRICA", 30: "AMERICAS", 31: "AMERICAS"}
    cols = [BRIEFS_REF[0:6], BRIEFS_REF[6:12], BRIEFS_REF[12:18]]
    # REF-4: kolom 305->312px (padding 12->8, gap antar-kolom 18->12);
    # x 32..992, kolom terakhir berakhir 992 (margin kanan 8px).
    col_x = [MX + 8, MX + 8 + 312 + 12, MX + 8 + 2 * (312 + 12)]
    col_w = 312
    # REF-4: row0 MORE_Y+26 (judul 13pt berakhir ~MORE_Y+22, celah 4px);
    # lh 16 (tinta 11pt y+3..y+15 = 12px; celah antar-baris 4px).
    row0, lh = MORE_Y + 26, 16
    for ci, col in enumerate(cols):
        for ri, (n, city, text, src) in enumerate(col):
            y = row0 + ri * lh
            # Kotak nomor bewarna (lebar neto 0: nomor tanpa spasi di
            # dalam kotak, kota mulai di x yang sama seperti dulu —
            # total lebar tidak berubah, assert lama tetap berlaku).
            num_txt = str(n)
            num_w = d.textlength(num_txt, font=f_n)
            chip_c = CHIP_COLORS[BRIEF_REGIONS[n]]
            d.rectangle([col_x[ci] - 1, y + 2,
                         col_x[ci] + num_w + 1, y + 14], fill=chip_c)
            d.text((col_x[ci], y), num_txt, font=f_n, fill=WHITE,
                   anchor="la")
            segs = [(f"{city} ", f_c, NAVY), (f"{text} ", f_x, INK)]
            if src:
                segs.append((f"({src})", f_s, GRAY))
            total = num_w + 3 + sum(d.textlength(t, font=f)
                                    for t, f, _ in segs)
            assert total <= col_w, (
                f"brief {n} terlalu panjang: {total:.0f}px > {col_w}")
            xx = col_x[ci] + num_w + 3
            x0 = col_x[ci]
            for t, f, colr in segs:
                d.text((xx, y), t, font=f, fill=colr, anchor="la")
                xx += d.textlength(t, font=f)
            b = (x0, y, int(xx), y + 16)  # REV9: kotak tinta 12pt (y+3..y+16)
            r1.reg("text", b, f"brief-{n}")
            if ri < len(col) - 1:
                for dx in range(0, col_w, 3):
                    d.point((col_x[ci] + dx, y + 16), fill=(180, 175, 165))  # REF-4: 1px di bawah tinta (y+15)


def draw_datecheck_ref(d):
    """DATE CHECK: kotak border merah tipis + chip merah kiri.
    REV9: teks 10 -> 12pt (Kevin Gas 22 Nov 04:40 WIB — juri salah baca
    teks 10pt di crosscheck rev8); teks dipangkas supaya tetap 2 baris
    (diukur font asli: 869/830 dari max 878). Kotak tetap 38px (tinta
    2 baris ~25px + celah ~6+7); chip tetap 10pt."""
    d.rectangle([MX, DC_Y, W - MX, DC_Y + DC_H], outline=RED, width=2,
                fill=CARD_BG)
    f_chip = F(BOLD, 10)  # REV7: 11 -> 10pt (chip 76 -> 70px)
    tw = d.textlength("DATE CHECK", font=f_chip)
    chip_w = int(tw) + 16
    chip_h = 22
    cx0, cy0 = MX + 8, DC_Y + (DC_H - chip_h) // 2
    d.rectangle([cx0, cy0, cx0 + chip_w, cy0 + chip_h], fill=RED)
    b = d.textbbox(((cx0 + cx0 + chip_w) // 2, (cy0 + cy0 + chip_h) // 2),
                   "DATE CHECK", font=f_chip, anchor="mm")
    d.text(((cx0 + cx0 + chip_w) // 2, (cy0 + cy0 + chip_h) // 2),
           "DATE CHECK", font=f_chip, fill=WHITE, anchor="mm")
    r1.reg("text", b, "dc-chip")
    tx0 = cx0 + chip_w + 12
    max_w = W - MX - 8 - tx0
    for pt in (12,):  # REV9: 10 -> 12pt (teks 2 baris, diukur font asli)
        f_t = F(BOLD, pt)
        lines = rv.wrap(d, DATECHECK_REST, f_t, max_w)
        if len(lines) <= 2:
            break
    assert len(lines) <= 2, f"DATE CHECK tidak muat 2 baris: {len(lines)}"
    lh = 12  # REV9: 12pt
    # REV9: tinggi tinta diukur dari bbox asli (bukan hardcode); y
    # dipusatkan dari TINTA: tinta 2 baris = (2-1)*12 + ink_h.
    bb = d.textbbox((tx0, 0), lines[0], font=f_t, anchor="la")
    ink_top, ink_h = bb[1], bb[3] - bb[1]
    ink_span = (len(lines) - 1) * lh + ink_h
    y = DC_Y + (DC_H - ink_span) // 2 - ink_top
    for ln in lines:
        b = d.textbbox((tx0, y), ln, font=f_t, anchor="la")
        d.text((tx0, y), ln, font=f_t, fill=NAVY, anchor="la")
        r1.reg("text", b, "dc-text")
        y += lh
    return {"dc_pt": pt, "lines": len(lines)}


def draw_sources_ref(d):
    """Baris Sources di bawah DATE CHECK (seperti referensi).
    REV6: 13pt -> 11pt (Kevin 20:17 WIB: rev5 "kegedean"). 1 baris
    TETAP TIDAK MUAT (kiri+kanan 11pt = 1168px > 976px), jadi tetap
    2 baris. REV8 (Kevin 20:30 WIB, "teks di bawah date check kok ga
    selaras"): teks gabung dibagi ulang jadi 2 baris SEIMBANG
    (SOURCES_LINE1 590,1px / SOURCES_LINE2 577,5px, selisih 12,6px,
    diukur font asli), keduanya rata kiri di MX (tepi kiri kotak
    DATE CHECK) — baris lama kiri-rata + kanan-rata bikin kedua tepi
    tidak sejajar."""
    f_s = F(REG, 11)
    y1, y2 = SRC_Y, SRC_Y + 11
    b = d.textbbox((MX, y1), SOURCES_LINE1, font=f_s, anchor="la")
    d.text((MX, y1), SOURCES_LINE1, font=f_s, fill=GRAY, anchor="la")
    r1.reg("text", b, "src-line1")
    b2 = d.textbbox((MX, y2), SOURCES_LINE2, font=f_s, anchor="la")
    d.text((MX, y2), SOURCES_LINE2, font=f_s, fill=GRAY,
           anchor="la")
    r1.reg("text", b2, "src-line2")
    assert b[2] - b[0] <= W - 2 * MX, "footer baris 1 terlalu lebar"
    assert b2[2] - b2[0] <= W - 2 * MX, "footer baris 2 terlalu lebar"
    return {"src_line1_w": round(b[2] - b[0], 1),
            "src_line2_w": round(b2[2] - b2[0], 1)}

# ------------------------------------------------------------------ build

def check_no_overlap_ref4():
    """Aturan keras Kevin: TIDAK ada yang boleh bersinggungan.
    Sama seperti r13.check_no_overlap_1r3 TAPI TANPA whitelist —
    whitelist chip peta (map-title vs map) DIHAPUS di ref-3 karena chip
    penembus border sudah tidak ada (fix 2); tidak ada lagi pasangan
    kotak yang sengaja dibiarkan bersinggungan."""
    bad = []
    for i, (k1, b1, l1) in enumerate(r1.BOXREG):
        for k2, b2, l2 in r1.BOXREG[i + 1:]:
            if not r1._overlap(b1, b2):
                continue
            pair = {k1, k2}
            if pair <= {"text", "rule"} or pair == {"text"} or pair == {
                    "text", "image"}:
                bad.append((l1, l2, k1, k2))
    assert not bad, f"OVERLAP (aturan keras Kevin): {bad}"
    return len(r1.BOXREG)


def build(path):
    r1.BOXREG.clear()
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    mast = draw_masthead_ref(d)
    draw_strip_ref(d)
    chips = draw_chips_ref(d)
    tops = {}
    for i, hero in enumerate(HEROES_REF):
        img = draw_hero_ref(im, d, hero, HERO_Y[i])
        tops[(0, i)] = top_color(img)
    panels = HEROES_REF + CARDS_REF
    mapinfo = draw_map_ref(im, d, panels)
    for idx, card in enumerate(CARDS_REF):
        r, c = (0, idx) if idx < 5 else (1, idx - 5)
        img = draw_card_ref(im, d, card, r, c)
        tops[(1 + r, c)] = top_color(img)
    draw_more_ref(d)
    dcinfo = draw_datecheck_ref(d)
    srcinfo = draw_sources_ref(d)
    im.save(path, optimize=True)  # V2 (a1): optimize, target <=300 KB
    top_bad = rs.check_top_colors(tops)
    nreg = check_no_overlap_ref4()   # TANPA whitelist (fix 2)
    m = r13.measure(path)
    ink_bottom, margin = v4.audit_footer(path)
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    return {"path": path, "sha256": sha, "masthead": mast,
            "chips": chips, "map": mapinfo, "dc": dcinfo,
            "sources": srcinfo, "top_bad": top_bad, "tops": tops,
            "ink_pct": m["ink_pct"], "saturated_pct": m["saturated_pct"],
            "ink_bottom": ink_bottom, "bottom_margin": margin,
            "registered_boxes": nreg}


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    path = f"{out}/entry.png"
    res = build(path)
    assert not res["top_bad"], f"pelanggaran warna atas: {res['top_bad']}"
    assert res["map"]["skipped"] == [], (
        f"pin hilang: {res['map']['skipped']}")
    assert res["map"]["placed"] == 13, (
        f"pin terpasang {res['map']['placed']} != 13")
    print("OK", path)
    print("sha256:", res["sha256"])
    print("masthead:", res["masthead"])
    print("chips:", res["chips"])
    print("map:", res["map"])
    print("datecheck:", res["dc"])
    print("sources:", res["sources"])
    print("top_bad:", res["top_bad"])
    print("tops:", {k: v for k, v in sorted(res["tops"].items())})
    print(f"ink={res['ink_pct']}% saturated={res['saturated_pct']}% "
          f"ink_bottom={res['ink_bottom']} bottom_margin="
          f"{res['bottom_margin']} boxes={res['registered_boxes']}")
