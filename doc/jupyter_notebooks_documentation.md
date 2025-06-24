# Dokumentasi Notebook Jupyter - ITB Chatbot

## Overview
Proyek chatbot ITB menggunakan 2 notebook Jupyter untuk proses development dan data processing yang berbeda.

## 1. explore.ipynb - Notebook Eksplorasi & Testing

### **Fungsi Utama:**
- **Data Exploration**: Eksplorasi dan analisis data CSV mentah
- **Algorithm Testing**: Testing berbagai algoritma matching 
- **Integration Testing**: Testing integrasi antar komponen
- **Development Support**: Support untuk development dan debugging

### **Use Cases:**
- Development dan testing selama tahap pengembangan
- Debugging algoritma matching
- Eksperimen dengan parameter dan threshold
- Validasi preprocessing pipeline
- Testing performa algoritma

### **Key Features:**
- Loading dan analisis data CSV mentah
- Testing function `matchIntent()` dan `matchWithCsvData()`
- Preprocessing testing dengan function `preprocess()`
- Jaccard similarity testing
- Sample data preview dan distribution analysis

---

## 2. chatbot.ipynb - Notebook Data Processing Pipeline

### **Fungsi Utama:**
- **Production Data Pipeline**: Pipeline lengkap untuk memproses data production
- **Data Quality Enhancement**: Membersihkan dan meningkatkan kualitas data
- **Dataset Generation**: Menghasilkan dataset berkualitas tinggi untuk production
- **System Integration**: Integrasi dengan sistem chatbot utama

### **Use Cases:**
- Memproses data mentah menjadi dataset production-ready
- Quality control dan scoring data
- Export dataset terstruktur untuk chatbot
- Live testing dan validasi sistem
- Dokumentasi arsitektur sistem

### **Pipeline Steps:**
1. **Data Loading & Analysis**: Load dan analisis data mentah
2. **Data Cleaning & Enhancement**: Pembersihan dan peningkatan data
3. **Quality Scoring**: Pemberian skor kualitas untuk setiap entry
4. **Export & Integration**: Export dataset dan integrasi dengan sistem
5. **Testing & Validation**: Testing lengkap dengan query representatif
6. **System Documentation**: Dokumentasi arsitektur dan flow

---

## Perbandingan Fungsi

| Aspek | explore.ipynb | chatbot.ipynb |
|-------|---------------|---------------|
| **Tujuan** | Development & Testing | Production Pipeline |
| **Scope** | Algorithm testing | Full data processing |
| **Output** | Testing results | Production datasets |
| **Target User** | Developer | System Administrator |
| **Frequency** | During development | Before deployment |
| **Data Focus** | Raw data exploration | Quality enhancement |

---

## Hasil Konversi camelCase

### **Files Updated:**
- ✅ `explore.ipynb` - Semua variable dan function calls dikonversi ke camelCase
- ✅ `chatbot.ipynb` - Semua variable dan function calls dikonversi ke camelCase

### **Key Changes:**
- `load_csv_data()` → `loadCsvData()`
- `match_with_csv_data()` → `matchWithCsvData()`
- `jaccard_similarity()` → `jaccardSimilarity()`
- Variable naming: `csv_files` → `csvFiles`, `test_queries` → `testQueries`
- Function parameters: `source_name` → `sourceName`, `user_question` → `userQuestion`

### **Simbol Cleanup:**
- Removed excessive emoji dan simbol berlebihan
- Simplified markdown headers
- Cleaned up output formatting
- Maintained essential visual elements untuk readability

---

## Rekomendasi Penggunaan

### **Development Phase:**
1. Gunakan `explore.ipynb` untuk testing dan debugging
2. Experiment dengan parameter algoritma
3. Validate preprocessing changes

### **Production Deployment:**
1. Jalankan `chatbot.ipynb` untuk generate dataset berkualitas
2. Export high-quality CSV untuk production
3. Update dataLoader.py dengan processed data
4. Deploy dengan dataset yang sudah dioptimasi

### **Maintenance:**
1. `explore.ipynb` untuk debugging issues
2. `chatbot.ipynb` untuk regenerate dataset jika ada data baru
3. Monitor quality scores dan performance metrics

## File Dependencies

```
jupyter/
├── explore.ipynb
│   ├── Depends on: ../dataLoader.py, ../matching.py, ../preprocessing.py
│   └── Purpose: Development testing
│
└── chatbot.ipynb
    ├── Depends on: ../dataLoader.py, ../matching.py, ../preprocessing.py
    ├── Generates: ../database/processed/*.csv
    ├── Updates: ../dataLoaderProcessed.py
    └── Purpose: Production pipeline
```

## Status
✅ **SELESAI** - Kedua notebook telah dikonversi ke camelCase
✅ **CLEANED** - Simbol berlebihan telah dihapus
✅ **DOCUMENTED** - Fungsi setiap notebook telah didokumentasikan
✅ **READY** - Siap digunakan untuk development dan production
