# BUILD-NOTE — Entry V2 ni20 (repo-v4)

**Status: KANDIDAT SUBMIT — belum submit, belum bundle.**
Dibangun 21 Nov 2026 ~17:40–18:00 WIB oleh builder daemon
(news-image-20261120-V2-improve-a1). Model: Muse Spark.
Dasar: repo-v4-trial/render_trial.py revisi-10 Kevin (sha entry
6ec960f8…) + change list loss report V2 (b3/b4/a1/a2).

## Output
- `entry.png` — 1024×1024, 245.695 byte (≤1 MiB ✓, ≤300 KB ✓)
- sha256: `9eb693e87318251bbbcf099de7f305add298ef7ee41226fc0341873b8fc0fdfa`
- Deterministik: 2 run → sha256 identik ✓ (juga sesudah optimize=True)
- Script: `compose_v4.py` + modul vendored (`render_v4.py`,
  `render_v4_1r.py`, `render_v4_1r3.py`, `render_v4_1r4.py`,
  `render_sketches.py`, `render_variants.py`) + `fonts/` +
  `ne_110m_land.geojson` — repo mandiri; modul vendored masih
  menyisipkan path absolut workspace (isi identik) saat build di sini.
- `main.py` (Python 3.13 stdlib) menyalin entry.png ke /output — sama
  seperti pola v3. `makefun check` lokal: lihat bawah.

## Yang berubah vs trial r10 (semua dari loss report V2)
1. **b3 — 4 kartu keras baru** (terverifikasi Jumat-murni dari sumber
   utama, bukti di STORIES.md): #5 Irak (Reuters — pasukan masuk
   Jurf al-Sakhar Jumat), #7 Italia (Reuters/AP — mogok umum CGIL
   Jumat, 100+ kota), #10 Polandia (AP/Reuters — 2 rudal Kh-101 +
   drone Jumat, Nowy Lipowiec, tanpa korban), #12 Kenya (Capital FM
   — spudding Amosing 1 Jumat, 20.000 bpd). Painter baru
   p_poland/p_iraq/p_italy/p_kenya (gaya datar, satu ide besar,
   selaras kartu 08/09/11); banner nilai: KH-101, TROOPS IN,
   100 CITIES, FIRST OIL; label sumber Reuters/Reuters/Reuters/
   Capital FM.
2. **Demote 3 kartu → brief:** SCO → #15, APEC → #16, Prabowo →
   #17 (menggantikan Brisbane/Jakarta/Loyalty). **HAPUS dari halaman:**
   konser Brisbane, GTA VI, Jakarta–Google, gempa Loyalty (soft
   news; semuanya terverifikasi Jumat — dihapus karena seleksi,
   bukan tanggal). Total tetap 31 cerita.
3. **Strip angka:** 19.000 (YouTube) → 1M+ (mogok Italia; klaim
   CGIL/Landini via AP).
4. **b4 — DATE CHECK:** + klausa "Not yet: BepiColombo's Mercury
   orbit entry; COP31 final text." — tetap 9pt, 2 baris. Klaim
   penutup absolut DIPERTAHANKAN: semua 31 cerita lolos cek tanggal
   final 1-per-1 (STORIES.md).
5. **Bar region:** EUROPE 7, AMERICAS 5, ASIA-PACIFIC 9, MIDEAST 3,
   AFRICA 3, OCEANIA 1, WORLD 3 = 31. OCEANIA 1 = trade-off dicatat
   (hanya kriket Wellington; Sydney dihapus Kevin rev-2, tidak
   ditambah lagi).
6. **a1 — PNG optimize=True:** 250.695 → 245.695 byte (sebelum
   perbaikan brief-16: 246.101). Determinisme 2× tetap ✓.
7. **a2 — hygiene tanggal:** tidak ada sisa Xavier/Takaichi di
   BRIEFS_REF maupun DATE CHECK (Xavier/Takaichi hanya disebut di
   daftar "Not Friday's news" DATE CHECK sebagai item yang DIBUANG).
   Duplikat Kyiv hero/brief #14 dipertahankan sadar (dicatat di
   STORIES.md). **Koreksi saat build:** brief #16 pertama ditulis
   Florida ("St. Johns River crests at 18.6 ft") — DUPLIKAT kartu #6
   (crest 18.6 ft); diganti APEC sebelum duel dijalankan ulang.
8. **Peta:** pin Italia di Milan (bukan Roma — pin Roma
   bertabrakan dengan klaster London/Kyiv, lalu London ikut
   bergeser; Milan salah satu kota mars terbesar, posisinya lolos
   tanpa offset). Offset terpakai: Antalya (0,+12), Jurf al-Sakhar
   (+14,0), London (0,−12), Nowy Lipowiec (0,−20 — pin duduk ~20px
   di utara Polandia, di atas Skandinavia utara; mekanisme offset
   ref-6, sama seperti Shenzhen +20 / Las Vegas +20 di trial).
   13 pin, 0 hilang.

## Pengukuran
- Tinta: **39,6%** (trial r10 38,8%; rank 1 ni20 ~36,6%) — naik 0,8pt
  karena 4 tile baru lebih gelap (langit malam Polandia, senja Kenya).
  Masih di bawah target loss report ≤42%.
- Saturasi: **25,5%** (trial r10 23,9%; target lama ≤18%) — di atas
  target; penyebab: oranye senja Kenya + navy Polandia + banner
  merah. Trial r10 sendiri sudah 23,9% (di atas target) dan
  disetujui Kevin; dicatat sebagai deviasi, bukan blocker.
- Margin bawah 15px; ink_bottom 1008 (sama seperti trial r10).

## Verifikasi (crosscheck 2x)
Programatik (build, semua lolos):
- no-overlap: 140 kotak terdaftar, 0 pelanggaran, TANPA whitelist.
- warna atas: 0 pelanggaran (top baru: Irak (205,180,130), Italia
  (120,140,170), Polandia (18,32,58), Kenya (210,140,70)).
- peta: 13 pin terpasang, 0 hilang.
- ukuran file + margin bawah tidak berubah.
- DATE CHECK 9pt 2 baris; Sources kiri 536 + kanan 419 = 955 < 976.
Visual (dibaca langsung oleh builder, bukan klaim):
- Tampilan penuh 1024px: masthead, strip (1M+), bar region (7/5/9/
  3/3/1/3), 3 hero + peta, 10 kartu, MORE 18 brief (14–31), DATE
  CHECK + "Not yet", Sources — semua utuh, tanpa overlap, tanpa
  teks/gambar terpotong.
- Crop 3x tiap kartu baru (05 Irak, 07 Italia, 10 Polandia, 12
  Kenya): banner 1 baris terbaca, label sumber terbaca, kicker +
  judul + ringkasan utuh, subjek tile jelas (rudal di langit malam,
  konvoi + bendera, kerumunan + plakat, menara bor + matahari).
- Crop 3x peta: 13 pin bernomor, tidak ada yang hilang; pin 10 di
  utara Skandinavia (offset, lihat atas); pin 7 di Italia utara
  (Milan); pin 12 di Kenya timur (Turkana).
- Crop 3x MORE: 18 brief, nomor 14–31 berurutan, tanpa duplikat
  (Florida hanya di kartu #6 + brief #27 flood watch).
- Downscale 512px: masthead + strip + judul hero + judul kartu +
  banner nilai terbaca; brief + DATE CHECK kecil (sama seperti
  trial r10 — inheren format satu halaman).
- Downscale 300px: masthead + strip angka + judul hero + banner
  kartu selamat; sama seperti profil top-3.

## Yang BELUM dilakukan (sengaja)
- TIDAK submit, TIDAK bundle, TIDAK sentuh keypair/API key.
- Sesi ini TIDAK ter-anchor (sama seperti sesi trial — `makefun
  anchor` bukan subcommand kit; `makefun init` terblokir security
  notice). Submit agent perlu menangani bundle sesi ini secara
  eksplisit (mis. --session) atau revisi diulang di sesi ter-anchor
  atas izin Kevin.
- Duel proxy: lihat duel-v2-v4/ + improve_2026-11-21.md (gate
  ≥7/10 + mean ≥0,60, dua arah, vs top-3 live).
- Kit fresh: diunduh 21 Nov 17:34 WIB ke
  ~/workspace/makefun/kit/news-image-20261120-v4/ (bundle
  63afd6ef…); `makefun status` — entries_made 2, day cap 6, left 6,
  can_submit true, hard_limit left 38.

## Repo GitHub
- BARU: `oraybora-source/news-image-20261120-v4` (repo lama
  `news-image-20261120` sudah dipakai v2/v3 — TIDAK disentuh).
- Publik, lisensi MIT (LICENSE), README 3 badge + link bounty,
  About: website bounty + topik makefun (diatur saat repo dibuat).
