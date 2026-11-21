# REV-NOTE — news-image-20261120 rev9 (legibilitas saja)

Revisi dari rev8 sesuai perintah Kevin (Gas 22 Nov 2026 04:40 WIB):
"rev9 kecil — perbesar teks + kurangi kata". Alasan: crosscheck rev8
membuktikan juri (model vision) SALAH BACA teks 10pt ("Very story…",
"BELING") meski pikselnya benar — jadi teks DATE CHECK + brief harus
LEBIH BESAR / LEBIH SEDIKIT kata. HANYA itu yang berubah.

## File hasil

- `entry.png` — 1024×1024, **261.033 byte** (≤1 MiB), sha256
  `803a9fba34063202c5d5687c0b567116a410dd078d857b9da78e13e8826f2f97`
  (rev8: 256.309 byte, sha `2d9954ab…`)
- `compose_v4.py` — salinan script render rev8 yang sudah diedit
  (penanda `REV9` di komentar kode)
- `README.md` — badge repo diubah ke `-v6`; kalimat DATE CHECK
  "names 18 stories" -> "names 12 stories" (lihat bawah)
- `REV-NOTE.md` — catatan ini
- File lain (BUILD-NOTE.md, STORIES.md, main.py, render_*.py, fonts/,
  ne_110m_land.geojson) salinan rev8 apa adanya.
  `entry-manifest.json` masih salinan V2 (build tidak menulis ulang
  manifest) — fakta rev9 yang berlaku adalah yang di catatan ini.
- repo-v4-rev8/ dan repo-v5/ TIDAK disentuh. Standing entry tetap
  rev8 di repo-v5 (submission 01a1fffc-3a59-72f9-8645-a7fae2adee05,
  dev 985,464) sampai ada keputusan submit rev9.

## Perubahan 1 — DATE CHECK 10 -> 12pt, tetap 2 baris, kotak 38px

Teks dipangkas supaya muat 2 baris di 12pt (diukur font asli:
869/830 dari max 878px):
- Daftar "not Friday's news" 18 -> 12 item (keluar: Romania, rupee,
  Kenya flood, Thai pact, Husky, Dow). Daftar ini contoh cerita yang
  TIDAK ada di halaman — bukan cerita halaman; klaim penutup tidak
  berubah.
- "BepiColombo's Mercury orbit entry" -> "BepiColombo's Mercury entry".
- "Friday 20 November 2026" -> "Friday 20 Nov 2026".
- Klausa "Not yet: …; COP31 final text." + kalimat penutup isinya
  TIDAK berubah. Chip "DATE CHECK" tetap 10pt.

## Perubahan 2 — brief MORE STORIES 11 -> 12pt, tetap 1 baris

5 brief dipangkas katanya supaya muat kolom 312px di 12pt
(diukur font asli; 13 brief lain muat tanpa diubah):
- #15 "Modi opens SCO civilisations forum." -> "Modi opens SCO forum."
  (266px)
- #26 "China holds lending rates for 18th month." -> "China holds
  lending rates 18th month." (298px)
- #28 "KCSE ends; record 1.05m candidates." -> "KCSE ends; record
  1.05m." (260px)
- #29 "Rand hits one-year low at 17.56/USD" -> "Rand hits 1-yr low,
  17.56/USD" (301px)
- #31 "1st Conservative premier in a century" -> "1st Tory premier
  in a century" (297px)
Semua fakta/angka tetap (1.05m, 17.56/USD, 18th month, SCO forum,
premier pertama dalam seabad). "Tory" = shorthand standar untuk
Conservative (B.C.).

## Yang TIDAK berubah

Hero (3), kartu feature (10), peta + 13 pin, bar region, strip angka,
masthead, deck, warna, layout, SEMUA 31 cerita + angka — diverifikasi
dengan `diff` lawan rev8: hanya `compose_v4.py` + `entry.png` yang
berbeda, dan di dalam `compose_v4.py` hanya 5 teks brief + teks
DATE CHECK + ukuran font + komentar.

## Verifikasi

- Render `python3 compose_v4.py` 2× -> sha256 identik
  `803a9fba…` (deterministik ✓); semua assert script lolos
  (top_bad kosong, 13 pin, 140 box, ink 39,7%, saturated 24,3%,
  ink_bottom 1020, bottom_margin 3).
- `datecheck: {'dc_pt': 12, 'lines': 2}`.
- Visual di ukuran tampil (512px) + zoom DATE CHECK + zoom MORE:
  teks DATE CHECK 2 baris terbaca penuh tanpa terpotong; 18 brief
  (14–31) terbaca, tanpa overlap dengan pemisah titik-titik;
  layout lain identik rev8 (piksel beda 4,6% — hanya area teks
  DATE CHECK + brief).
- TIDAK submit, TIDAK bundle, TIDAK sentuh keypair/API key.
  Submit rev9 hanya setelah crosscheck GO atau Gas Kevin lagi.
  Batas internal: STOP 06:30 WIB 22 Nov bila belum selesai —
  tidak tercapai (selesai ~04:50 WIB).

## rev9c — koreksi sasaran label (Kevin 22 Nov 04:54–04:55 WIB)

- KESALAHAN rev9b (commit 2765199) DIBATALKAN: label ATAS (banner nilai
  berita) kembali MERAH + padding +12 seperti semula — Kevin: "Bukan
  label atas win".
- Yang diubah justru chip sumber BAWAH (13 chip): latar TAN -> NAVY
  (15,36,64), teks INK 11pt -> WHITE 16pt (kontras 15,59:1); lebar PAS
  TEKS (teks + 12, tanpa min 100px). Font 16pt = lantai legibility
  Kevin (keputusan 04:55 WIB "Potong teks label biar muat 16pt").
- TIDAK ADA singkatan: semua 7 nama sumber muat utuh di 16pt di gambar
  tersempit (kartu 187px) — terpanjang "Formula1.com" 102,9px -> chip
  114px < 183px. "Reuters", "IMD", "Capital FM", "KuCoin News" utuh.

## Verifikasi rev9c

- Render `python3 compose_v4.py` 2× -> sha256 identik `a54d4340…`
  (deterministik ✓); semua assert script lolos (top_bad kosong, 13 pin,
  140 box, ink 39,7%).
- Diff vs render 2765199: 4,16% piksel, bbox y 210–730 — hanya area
  label atas + chip bawah (hero + 2 baris kartu); MORE/DATE CHECK/
  peta tidak berubah.
- Cek piksel: banner atas hero1 + kartu4 = RED (178,44,36) ✓; 13 chip
  bawah NAVY teridentifikasi (IMD 40px, Reuters 68px, ESPNcricinfo
  106px, Florida Today 109px, KuCoin News 106px, Capital FM 87px,
  Formula1.com 114px).
- Cek visual di ukuran tampil penuh + downscale lebar 390px: 13/13
  label atas merah terbaca; 13/13 chip bawah navy + teks putih
  terbaca di 390px (16pt di file = ~6px di layar 390px — sesuai
  lantai 16px); chip tidak menutupi subjek, tidak menabrak elemen lain.
- TIDAK submit, TIDAK bundle, TIDAK sentuh keypair/API key.
  Crosscheck rev9 masih ditahan parent sampai gambar final.
