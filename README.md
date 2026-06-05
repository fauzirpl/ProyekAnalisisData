# Proyek Analisis Data: Bike Sharing Dataset 🚲

Submission untuk kelas **Belajar Analisis Data dengan Python** dari Dicoding.

## Struktur Direktori
```
submission/
├───dashboard/
│   ├───dashboard.py       # Berkas Python untuk aplikasi Streamlit
│   └───main_data.csv      # Dataset yang telah dibersihkan & diproses
├───data/
│   ├───day.csv            # Dataset harian (asli)
│   ├───hour.csv           # Dataset per jam (asli)
│   └───Readme.txt         # Keterangan dataset
├───notebook.ipynb         # Jupyter Notebook proses analisis data
├───README.md              # Dokumentasi ini
├───requirements.txt       # Daftar pustaka / library Python
└───url.txt                # Tautan dashboard yang sudah di-deploy
```

## Persyaratan Pustaka (Requirements)
Seluruh pustaka yang digunakan tercantum di dalam berkas `requirements.txt`. Anda dapat menginstalnya dengan menjalankan perintah berikut:
```bash
pip install -r requirements.txt
```

## Cara Menjalankan Dashboard Streamlit Secara Lokal
Pastikan Anda berada di direktori root proyek (`dicodinganalisidata`), lalu jalankan perintah berikut di terminal Anda:

```bash
streamlit run dashboard/dashboard.py
```

Jika perintah di atas berhasil dijalankan, browser Anda akan terbuka secara otomatis dan mengarah ke `http://localhost:8501`. Jika tidak, Anda dapat menyalin URL tersebut dan membukanya secara manual di web browser Anda.

## Deploy ke Streamlit Cloud
Dashboard ini dapat dideploy ke Streamlit Cloud dengan mengikuti langkah berikut:
1. Unggah seluruh isi repositori ini ke akun GitHub Anda.
2. Masuk ke [Streamlit Share](https://share.streamlit.io/).
3. Hubungkan repositori GitHub Anda dan pilih berkas utama `dashboard/dashboard.py`.
4. Klik **Deploy** dan tunggu beberapa menit hingga aplikasi selesai dibangun.
5. Simpan tautan yang dihasilkan dan letakkan di berkas `url.txt`.
