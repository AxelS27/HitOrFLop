# User Testing Kit — Music Hit Predictor

Dokumen ini berisi **desain user testing** + **template kuesioner** untuk memenuhi
syarat wajib *Real User Testing* (min. 5 user nyata di luar tim). Sebar ke responden
(mis. lewat Google Form), lalu hasilnya dirangkum ke slide #11–12.

> ⚠️ Hard constraint dari panduan: **tanpa user testing di PPT, nilai maksimum = 70.**

---

## 1. Tujuan Testing
Mengukur **usability** (kemudahan pakai) dan **usefulness** (kebermanfaatan) dari
aplikasi Music Hit Predictor saat dipakai oleh user nyata yang bukan anggota tim.

## 2. Profil Responden (anonim)
Minimal **5 user**, di luar tim proyek. Setiap user dicatat secara anonim:

| Kode User | Umur | Latar Belakang | Kebiasaan Dengar Musik | Familiar dengan ML? |
|-----------|------|----------------|------------------------|---------------------|
| U1 | … | mis. mahasiswa non-IT | mis. 2 jam/hari Spotify | Tidak |
| U2 | … | mis. musisi indie | … | Sedikit |
| U3 | … | … | … | … |
| U4 | … | … | … | … |
| U5 | … | … | … | … |

## 3. Skenario Penggunaan (Task Scenario)
Setiap user diminta menyelesaikan task berikut tanpa dibantu:

1. Buka aplikasi (link / demo lokal).
2. Masukkan **1 lagu** (upload file ATAU paste link YouTube).
3. Jalankan prediksi memakai **Multi-Vote Model**.
4. Baca hasil: HIT/FLOP, confidence, dan analisis fitur (tempo/energy/loudness).
5. Buka halaman **Model Performance**, coba urutkan tabel berdasarkan F1.
6. Berikan kesan keseluruhan.

Catat: apakah user berhasil tiap langkah tanpa bantuan (✓/✗) + waktu total.

---

## 4. Kuesioner Kuantitatif (Skala Likert 1–5)
*1 = Sangat Tidak Setuju, 5 = Sangat Setuju*

**A. Usability**
1. Tampilan aplikasi mudah dipahami.
2. Alur memasukkan lagu & menjalankan prediksi terasa intuitif.
3. Hasil prediksi ditampilkan dengan jelas dan mudah dibaca.
4. Saya tidak kebingungan saat memakai aplikasi pertama kali.

**B. Usefulness**
5. Hasil prediksi HIT/FLOP terasa masuk akal.
6. Penjelasan fitur (tempo, energy, loudness) membantu saya memahami hasil.
7. Aplikasi ini berguna untuk menilai potensi sebuah lagu.
8. Saya mau memakai/merekomendasikan aplikasi ini.

**C. Performa**
9. Aplikasi merespons cukup cepat (tidak terasa lama menunggu).
10. Saya tidak menemui error/crash saat memakai.

## 5. Pertanyaan Kualitatif (isian bebas)
- Q1. Bagian mana yang paling kamu suka?
- Q2. Bagian mana yang membingungkan / sulit?
- Q3. Apa satu hal yang ingin kamu perbaiki?
- Q4. Apakah kamu percaya dengan hasil prediksinya? Kenapa?

---

## 6. Template Rekap Hasil (untuk slide #12)

### 6a. Rata-rata skor Likert per item
| No | Pernyataan | U1 | U2 | U3 | U4 | U5 | Rata² |
|----|-----------|----|----|----|----|----|-------|
| 1 | Tampilan mudah dipahami | | | | | | |
| 2 | Alur intuitif | | | | | | |
| … | … | | | | | | |
| 10 | Tidak ada error | | | | | | |
| | **Rata² keseluruhan** | | | | | | |

### 6b. Ringkasan per kategori (buat bar chart di slide)
| Kategori | Rata² (1–5) |
|----------|-------------|
| Usability | |
| Usefulness | |
| Performa | |
| **SUS-style overall** | |

### 6c. Tema kualitatif
- **Yang disuka:** (mis. UI dark theme keren, hasil cepat) …
- **Keluhan utama:** (mis. bingung pilih model, butuh contoh lagu) …
- **Saran perbaikan:** …

---

## 7. Analisis & Tindak Lanjut (slide #13)
Tuliskan 2–3 insight + rencana perbaikan, contoh format:
- *Temuan:* 3/5 user bingung memilih model → *Aksi:* set Multi-Vote sebagai default + tooltip.
- *Temuan:* user ingin contoh lagu siap-coba → *Aksi:* tambah tombol "Coba lagu contoh".

---

### Cara pakai cepat
1. Salin Bagian 4 & 5 ke **Google Form** (Likert = linear scale 1–5).
2. Sebar ke ≥5 orang non-tim, dampingi untuk catat keberhasilan task (Bagian 3).
3. Ekspor jawaban → isi tabel Bagian 6 → masukkan ke slide #11–12.
