# NutriScan AI

Aplikasi web untuk menganalisis status gizi berdasarkan gambar (pengukuran MUAC) dan data biometrik, menggunakan model deep learning.

## Dependencies

Install semua library berikut:

```bash
pip install flask numpy pandas opencv-python tensorflow scikit-learn
```

## Cara Menjalankan

1. Masuk ke folder `NutriScanAI`
2. Masuk ke folder `notebooks`
3. Jalankan server:
```bash
   python app.py
```
   atau buka `app.py` di VS Code lalu run
4. Buka alamat yang muncul di terminal (biasanya http://127.0.0.1:5000)
5. Upload gambar, isi data biometrik, lalu klik **Analyze**
6. Hasil analisis akan ditampilkan

## Struktur Folder

- `dataset/` : gambar dan label data
- `models/` : model terlatih (`muac_model_v1.keras`)
- `notebooks/` : kode training, inference, dan `app.py`
- `static/` : file CSS
- `templates/` : halaman HTML
