# Text Preprocessing Pipeline - Normalisasi teks
import re  # Regular expression untuk pola text
import csv  # CSV file handler

# Daftar stopword bahasa Indonesia
STOPWORDS = set([  # Set stopword untuk filter
    'dan', 'di', 'ke', 'dari', 'yang', 'untuk', 'pada', 'dengan', 'atau', 'juga', 'sebagai', 'dalam', 'adalah', 'itu', 'ini', 'saya', 'kamu', 'kami', 'kita', 'mereka', 'akan', 'tidak', 'bisa', 'telah', 'sudah', 'belum', 'oleh', 'karena', 'agar', 'sehingga', 'supaya', 'tentang', 'tanpa', 'setelah', 'sebelum', 'sesudah', 'sejak', 'hingga', 'sampai', 'selama', 'antara', 'bahwa', 'namun', 'tetapi', 'jadi', 'hanya', 'masih', 'lagi', 'pun', 'lah', 'punya', 'ada'
])

def caseFolding(text):  # Ubah ke huruf kecil
    return text.lower()  # Convert semua ke lowercase

def removePunctuation(text):  # Hapus tanda baca
    return re.sub(r'[^\w\s]', '', text)  # Hapus karakter non-alphanumeric

def tokenize(text):  # Pecah jadi kata-kata
    return text.split()  # Split berdasarkan spasi

def removeStopwords(tokens):  # Hapus stopword
    return [word for word in tokens if word not in STOPWORDS]  # Filter stopword

def stemming(tokens):  # Stemming pintar
    result = []  # List hasil stemming
    for word in tokens:  # Loop setiap kata
        if len(word) <= 6:  # Kata pendek tetap utuh
            result.append(word)  # Tambah tanpa perubahan
        else:  # Kata panjang di-stem
            importantTerms = ['akreditasi', 'universitas', 'fakultas', 'teknologi', 'bandung', 'institut', 'kampus', 'program', 'mahasiswa', 'penelitian']  # Term penting
            if word in importantTerms or any(term in word for term in importantTerms):  # Cek term penting
                result.append(word)  # Tetap utuh jika penting
            else:  # Term biasa
                result.append(word[:6])  # Potong jadi 6 karakter
    return result  # Return hasil

def preprocess(text):  # Pipeline lengkap preprocessing
    text = caseFolding(text)  # Langkah 1: lowercase
    text = removePunctuation(text)  # Langkah 2: hapus punctuation
    tokens = tokenize(text)  # Langkah 3: tokenisasi
    tokens = removeStopwords(tokens)  # Langkah 4: hapus stopword
    tokens = stemming(tokens)  # Langkah 5: stemming
    return ' '.join(tokens)  # Join jadi string

def preprocessing(inputCsv, outputCsv, textColumn):  # Preprocess CSV file
    with open(inputCsv, 'r', encoding='utf-8') as infile, open(outputCsv, 'w', encoding='utf-8', newline='') as outfile:  # Buka file input/output
        reader = csv.DictReader(infile)  # CSV reader
        fieldnames = reader.fieldnames + ['preprocessed']  # Tambah kolom preprocessed
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)  # CSV writer
        writer.writeheader()  # Tulis header
        for row in reader:  # Loop setiap row
            original = row[textColumn]  # Ambil text asli
            row['preprocessed'] = preprocess(original)  # Preprocess text
            writer.writerow(row)  # Tulis row baru
