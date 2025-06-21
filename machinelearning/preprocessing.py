# Normalisasi teks (case folding, hapus stopword, stemming, dll)
import re
import csv

# Contoh daftar stopword sederhana
STOPWORDS = set([
    'dan', 'di', 'ke', 'dari', 'yang', 'untuk', 'pada', 'dengan', 'atau', 'juga', 'sebagai', 'dalam', 'adalah', 'itu', 'ini', 'saya', 'kamu', 'kami', 'kita', 'mereka', 'akan', 'tidak', 'bisa', 'telah', 'sudah', 'belum', 'oleh', 'karena', 'agar', 'sehingga', 'supaya', 'tentang', 'pada', 'oleh', 'dengan', 'tanpa', 'setelah', 'sebelum', 'sesudah', 'sejak', 'hingga', 'sampai', 'selama', 'antara', 'bahwa', 'namun', 'tetapi', 'jadi', 'hanya', 'masih', 'lagi', 'pun', 'lah', 'punya', 'ada', 'adalah', 'itu', 'ini', 'atau', 'dan', 'di', 'ke', 'dari', 'yang', 'untuk', 'pada', 'dengan', 'atau', 'juga', 'sebagai', 'dalam', 'adalah', 'itu', 'ini', 'saya', 'kamu', 'kami', 'kita', 'mereka', 'akan', 'tidak', 'bisa', 'telah', 'sudah', 'belum', 'oleh', 'karena', 'agar', 'sehingga', 'supaya', 'tentang', 'pada', 'oleh', 'dengan', 'tanpa', 'setelah', 'sebelum', 'sesudah', 'sejak', 'hingga', 'sampai', 'selama', 'antara', 'bahwa', 'namun', 'tetapi', 'jadi', 'hanya', 'masih', 'lagi', 'pun', 'lah', 'punya', 'ada'
])

def caseFolding(text):
    return text.lower() # Mengubah teks menjadi huruf kecil

def removePunctuation(text):
    return re.sub(r'[^\w\s]', '', text) # menghapus tanda baca

def tokenize(text):
    return text.split() # Tokenisasi: memecah teks menjadi kata-kata

def removeStopwords(tokens):
    return [word for word in tokens if word not in STOPWORDS] # Menghapus stopwords dari daftar token, seperti 'dan', 'di', 'ke', dll.

def stemming(tokens): 
    # Improved stemming: keep longer words intact for better fuzzy matching
    # Only stem words longer than 6 characters to preserve important terms
    result = []
    for word in tokens:
        if len(word) <= 6:
            result.append(word)  # Keep short words as-is
        else:
            # For longer words, take 6 characters or original if important terms
            important_terms = ['akreditasi', 'universitas', 'fakultas', 'teknologi', 'bandung', 'institut', 'kampus', 'program', 'mahasiswa', 'penelitian']
            if word in important_terms or any(term in word for term in important_terms):
                result.append(word)  # Keep important terms intact
            else:
                result.append(word[:6])  # Stem to 6 chars for others
    return result

def preprocess(text):
    text = caseFolding(text)
    text = removePunctuation(text)
    tokens = tokenize(text)
    tokens = removeStopwords(tokens)
    tokens = stemming(tokens)
    return ' '.join(tokens)

# Fungsi untuk preprocessing seluruh data di CSV
def preprocessing(input_csv, output_csv, text_column):
    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['preprocessed']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            original = row[text_column]
            row['preprocessed'] = preprocess(original)
            writer.writerow(row)
