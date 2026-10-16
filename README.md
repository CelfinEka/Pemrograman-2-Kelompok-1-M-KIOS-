# M-KIOS V28 — Deploy Lokal dengan Tampilan Asli

**SUMBER TUNGGAL:** `reference/M-KIOS-SPA-Admin-Professional-v28-ASLI.html` adalah salinan identik file yang Anda unggah.

Tujuan paket ini: jalankan **tampilan dan interaksi V28 yang sama persis**, bukan desain ulang seperti paket Django terdahulu. Source UI tidak diubah: hanya penyimpanan `save()` yang ditambahkan adapter ke database SQLite ketika dijalankan melalui Django.

## Jalankan di Windows VS Code

1. Ekstrak ZIP lalu buka folder yang mempunyai `manage.py` di VS Code.
2. Jalankan `start-windows.bat` melalui File Explorer **atau** dari PowerShell: `./start-windows.bat`.
3. Tunggu pemasangan Django dan proses migrasi.
4. Buka **http://127.0.0.1:8000/**.

Alternatif manual di PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

**Tidak memerlukan aktivasi .venv maupun `py` launcher.**

## Halaman yang dipertahankan 1:1

Beranda, pilih tiket, konfirmasi, pembayaran QRIS/E-Wallet/Kasir simulasi, pesanan selesai, cari dan preview QR tiket, cetak/download QR; login admin, dashboard, transaksi, scan QR, laporan, tiket, promo, payment settings, konten, pengguna, role CRUD, pengaturan.

## Database

- SQLite: `database/mkios.sqlite3` (kosong sebelum migrasi).
- Jalankan `python manage.py migrate` untuk membuat skema.
- Data V28 sebelumnya berbentuk state browser. Versi ini menyimpan salinannya ke tabel `kiosk_v28_v28snapshot` dalam kolom JSON setelah setiap perubahan; browser tetap punya localStorage untuk kesesuaian V28.
- Ketika halaman diakses ulang, state dari SQLite diutamakan.
- Buka `/health/` untuk memastikan Django dan SQLite berfungsi.
- Buka `/api/state/` untuk inspeksi data tersimpan (hanya untuk pengujian lokal).

## Batasan yang HARUS diketahui

Paket ini dirancang untuk **pengujian/deploy lokal satu komputer**, bukan publik atau multi-kasir. Mempertahankan V28 secara *identik* juga berarti mekanisme login demo di browser, izin role berbasis klien, QRIS/E-Wallet dummy, dan single snapshot JSON tidak menjadi autentikasi atau transaksi server yang aman. Check-in simultan beberapa perangkat tidak dijamin atomik. **Jangan paparkan port ke internet atau gunakan untuk menerima uang nyata.**

Untuk sistem produksi multi-user sesungguhnya, antarmuka ini dapat dijadikan UI kanonik, lalu event transaksi/login/check-in dipindahkan ke endpoint server yang memberi autentikasi, validasi dan lock database. Itu akan menjadi tahap berikut, bukan sesuatu yang diam-diam kami klaim selesai.

## Verifikasi parity

- `reference/` menyimpan file V28 asli, byte-for-byte.
- `kiosk_v28/v28_served.html` identik secara visual dan fungsional, kecuali adapter sync DB pada `save()` dan skrip bootstrap yang disisipkan.
- `manage.py` berada di **akar paket**, bukan folder lain.
