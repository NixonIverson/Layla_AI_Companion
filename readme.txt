# Layla: teman AI lokal yang menemani layarmu

Layla adalah aplikasi web kecil yang memberimu teman AI yang ngobrol santai seperti sahabat dekat, bisa melihat layarmu (saat kamu membagikannya) dan mengomentari apa yang sedang kamu lakukan, serta bisa mengambang di atas jendela aplikasi lain.

Semuanya berjalan **di komputermu sendiri** lewat [Ollama](https://ollama.com). Pesan dan tangkapan layarmu tidak pernah dikirim ke cloud.

![Screenshot Layla](screenshot.png)

## Fitur

- Obrolan santai ala teman dengan nama dan kepribadian yang bisa diubah
- Pantau layar (opsional): dia mengomentari game, video, atau apa pun yang sedang kamu lakukan
- Jendela obrolan mengambang yang selalu di atas aplikasi lain (Document Picture-in-Picture)
- Dia bisa memulai obrolan sendiri saat suasana sepi
- Memori jangka panjang: dia mengingat hal-hal yang kamu ceritakan
- Tiga suasana (Quiet, Normal, Clingy) yang mengatur seberapa sering dia bicara
- Tanpa dependensi: satu file HTML dan server Python kecil

## Kebutuhan

| Apa | Versi / catatan |
| --- | --- |
| [Ollama](https://ollama.com/download) | Versi terbaru |
| Python | 3.8 atau lebih baru (hanya library bawaan, tanpa `pip install`) |
| Browser | Disarankan Chrome atau Edge 116+ (dibutuhkan untuk jendela mengambang yang selalu di atas) |
| Model | Harus mendukung **vision** jika ingin fitur pantau layar, misalnya `gemma3:4b` |

## Cara menjalankan, langkah demi langkah

### 1. Pasang Ollama

Unduh dari [ollama.com/download](https://ollama.com/download) lalu instal. Setelah terpasang, Ollama berjalan di latar belakang pada `http://127.0.0.1:11434`.

Cek apakah sudah berfungsi:

```bash
ollama --version
```

### 2. Unduh model

Model bawaan adalah `gemma3:4b`, yang mendukung gambar dan bisa berjalan di sebagian besar laptop modern:

```bash
ollama pull gemma3:4b
```

Model vision lain yang cocok: `gemma3:12b`, `gemma3:27b`, `qwen3-vl:8b`, `qwen2.5vl:7b`. Model yang lebih besar memberi komentar yang lebih bagus, tetapi butuh RAM/VRAM lebih banyak dan lebih lambat merespons.

### 3. Ambil proyeknya

```bash
git clone https://github.com/<username-kamu>/<nama-repo>.git
cd <nama-repo>
```

Kamu akan melihat file-file berikut:

```
index.html   # seluruh aplikasi (UI + logika)
server.py    # menyajikan index.html dan meneruskan /api/* ke Ollama
README.md
```

### 4. Jalankan server

```bash
python server.py
```

Di Windows kamu juga bisa memakai `py server.py`. Kamu akan melihat:

```
Open http://localhost:8000  (Ollama: http://127.0.0.1:11434)
```

### 5. Buka aplikasinya

Buka **http://localhost:8000** di Chrome atau Edge. Layla akan menyapa sendiri.

## Cara memakai Layla

1. **Ngobrol:** ketik di kolom pesan lalu tekan Enter.
2. **Bagikan layar:** klik **Share screen** dan pilih jendela atau layar. Pilih selain tab Layla, kalau tidak dia cuma akan melihat dirinya sendiri.
3. **Mengambang:** klik **Float** untuk memunculkan obrolan di jendela kecil yang selalu di atas. Tutup jendela itu (atau klik **Dock**) untuk mengembalikannya ke halaman.
4. **Atur dia:** gunakan panel Settings di kiri untuk mengubah nama, kepribadian, suasana, dan seberapa sering dia melihat dan bicara.
5. **Mulai dari awal:** **Clear chat and memory** menghapus percakapan dan semua yang dia ingat.

### Pengaturan

| Pengaturan | Fungsi |
| --- | --- |
| Her name | Nama yang tampil di UI dan dipakai dalam prompt kepribadiannya |
| Ollama model | Model apa pun yang sudah kamu pasang (perlu vision untuk pantau layar) |
| Personality | System prompt. `{name}` diganti dengan namanya |
| Vibe | Quiet, Normal, atau Clingy. Mengatur semua waktu di bawah sekaligus |
| She watches my screen | Menyalakan atau mematikan komentar soal layar |
| Look every (sec) | Seberapa sering dia mengecek layar |
| Min gap between comments (sec) | Jeda minimum antar komentar soal layar |
| Starts chats on her own | Membolehkan dia mengirim pesan duluan saat sepi |
| Quiet min / max (sec) | Rentang acak waktu diam sebelum dia bersuara |

Pengaturan, riwayat obrolan, dan memori disimpan di `localStorage` browsermu.

## Konfigurasi

`server.py` membaca dua variabel lingkungan opsional:

| Variabel | Bawaan | Fungsi |
| --- | --- | --- |
| `PORT` | `8000` | Port untuk aplikasi web |
| `OLLAMA_URL` | `http://127.0.0.1:11434` | Alamat Ollama berjalan |

Contoh:

```bash
# macOS / Linux
PORT=9000 python server.py

# Windows PowerShell
$env:PORT=9000; python server.py

# Ollama di komputer lain dalam jaringanmu
OLLAMA_URL=http://192.168.1.50:11434 python server.py
```

## Pemecahan masalah

**"Can't reach Ollama"**: Pastikan Ollama berjalan (`ollama list` harus bisa dijalankan), lalu muat ulang halaman. Jika Ollama memakai port atau komputer lain, atur `OLLAMA_URL`.

**"Model isn't installed yet"**: Jalankan `ollama pull <model>` dengan nama persis seperti di pesan, atau ganti model di Settings.

**Dia tidak bereaksi pada layarku**: Modelmu harus mendukung vision. Pastikan juga "She watches my screen and comments" menyala dan kamu membagikan jendela selain tab Layla. Komentar dibatasi oleh pengaturan "Min gap".

**Balasan lambat**: Pakai model yang lebih kecil (mis. `gemma3:4b`), naikkan "Look every (sec)", atau pilih suasana Quiet. Balasan pertama setelah Ollama dinyalakan lebih lambat karena model sedang dimuat.

**Jendela mengambang hanya popup biasa, tidak selalu di atas**: Document Picture-in-Picture butuh Chrome atau Edge 116+. Browser lain memakai jendela popup biasa yang bisa tertutup aplikasi lain.

**Notifikasi desktop tidak muncul**: Izinkan notifikasi untuk `localhost:8000` saat browser menanyakannya.

**Port sudah dipakai**: Jalankan server di port lain dengan `PORT=9000 python server.py`.

## Cara kerjanya

- `server.py` menyajikan `index.html` dan meneruskan semua permintaan `/api/*` ke Ollama, sehingga browser tidak terkena masalah CORS.
- Saat kamu membagikan layar, sebuah timer latar belakang membandingkan salinan layar berukuran kecil (32×18) untuk melihat seberapa banyak yang berubah. Hanya saat ada perubahan menarik (atau sudah lama diam) frame sekarang dan sebelumnya dikirim ke model.
- Timer itu dijalankan oleh Web Worker, jadi dia tetap mengawasi meski tab ada di latar belakang.
- Setiap ~10 pesan, model menulis ulang daftar singkat fakta penting tentangmu, yang dimasukkan kembali ke prompt-nya sebagai memori.

## Privasi

Frame layar dan obrolan hanya dikirim ke instance Ollama yang kamu atur, yang secara bawaan ada di komputermu sendiri. Tidak ada yang diunggah ke tempat lain. Perhatikan apa saja yang terlihat di layar yang kamu bagikan, karena model dapat melihatnya.

## Lisensi

Tambahkan lisensi pilihanmu di sini (misalnya MIT).