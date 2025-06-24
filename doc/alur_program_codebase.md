# Alur Program Codebase - Chatbot ITB
## Dokumentasi Berdasarkan Implementasi Nyata

### 1. ARSITEKTUR SISTEM

Berdasarkan analisis codebase yang ada, sistem chatbot terdiri dari:

```
Frontend (React)  ←→  Backend (Flask)  ←→  Machine Learning Module
     ↓                     ↓                        ↓
- App.jsx            - app.py                - matching.py
- Chatbox.jsx        - routes/routes.py     - preprocessing.py  
- apicall.jsx        - controller/          - dataLoader.py
                     - services/            - nlpIntentDetector.py
```

### 2. ALUR REQUEST-RESPONSE SISTEM

#### 2.1 Frontend Request Flow (React)
```
User Input → InputField.jsx → QueryButton.jsx → apicall.jsx → Backend
```

**File:** `frontend/src/services/apicall.jsx`
```javascript
export async function askToBackend(question) {
  const response = await fetch('http://localhost:5000/ask', { 
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  })
  return response.json()
}
```

#### 2.2 Backend Processing Flow (Flask)
```
HTTP POST /ask → routes.py → controller.py → services.py → ML Module
```

**File:** `backend/app.py`
- Entry point aplikasi Flask
- Inisialisasi CORS untuk konektivitas frontend
- Register blueprint dari routes.py

**File:** `backend/routes/routes.py`
- Mendefinisikan endpoint `/ask` dengan method POST
- Memanggil `handle_ask()` dari controller

**File:** `backend/controller/controller.py`
- Mengambil JSON data dari request
- Extract field 'question' dari request body
- Memanggil `detectIntentService()` dari services
- Return hasil dalam format JSON

**File:** `backend/services/services.py`
- **Main orchestration layer** yang menggabungkan semua modul ML
- Import modul: `matching`, `preprocessing`, `algorithm`
- Flow processing:
  1. Preprocessing teks menggunakan `preprocessing.preprocess()`
  2. Matching menggunakan `matching.matchIntent()`
  3. Fallback ke `matching.match_with_csv_data()` jika diperlukan
  4. Return formatted response dengan fields: `intent`, `answer`, `source`

### 3. MACHINE LEARNING MODULE

#### 3.1 Data Loading Pipeline
**File:** `machinelearning/dataLoader.py`
- Load data dari file CSV yang telah diproses: `itb_chatbot_high_quality_20250621_190153.csv`
- Fallback ke file CSV asli jika processed file tidak ada:
  - `tentangITB.csv`
  - `wikipediaITB.csv` 
  - `multikampusITB.csv`
- Return structured data dengan fields: `source`, `content`, `processed_content`, `category`, `quality_score`

#### 3.2 Text Preprocessing Pipeline  
**File:** `machinelearning/preprocessing.py`

**Functions:**
- `caseFolding()` - Convert to lowercase
- `removePunctuation()` - Remove punctuation marks
- `tokenize()` - Split text into words
- `removeStopwords()` - Remove Indonesian stopwords
- `stemming()` - Improved stemming (preserve important terms like 'akreditasi', 'universitas')
- `preprocess()` - Main pipeline function

#### 3.3 Advanced Matching System
**File:** `machinelearning/matching.py` (630 lines)

**Core Algorithms Implemented:**

1. **Levenshtein Distance** (`levenshtein_distance()`)
   - Calculate edit distance between strings
   - Used for fuzzy matching and typo tolerance

2. **Soundex Algorithm** (`soundex()`)
   - Phonetic matching for similar-sounding words
   - Maps words to 4-character codes

3. **N-gram Similarity** (`n_gram_similarity()`)
   - Bigram and trigram comparison
   - Better handling of character transpositions

4. **Advanced Fuzzy Matching** (`advanced_fuzzy_similarity()`)
   - Combines multiple algorithms with weighted scoring:
     - Levenshtein (25% weight)
     - Bigram similarity (20% weight)  
     - Trigram similarity (15% weight)
     - Character frequency (15% weight)
     - Phonetic matching (10% weight)
     - Python SequenceMatcher (10% weight)
     - Pattern recognition (5% weight)

5. **Pattern Typo Recognition** (`pattern_typo_recognition()`)
   - Detects common typo patterns:
     - Repeated characters (aaa → a)
     - Missing/extra characters
     - Character insertions at start/end

6. **TF-IDF Cosine Similarity** (`tfidf_similarity()`)
   - Vector space model for semantic similarity
   - Uses scikit-learn TfidfVectorizer

**Main Matching Flow:**
```python
def match_with_csv_data(user_query, threshold=0.3, top_k=3):
    # 1. Load processed data from dataLoader
    # 2. Multiple matching strategies:
    #    - Exact substring matching (highest priority)
    #    - Enhanced word matching with advanced fuzzy support
    #    - Jaccard similarity on processed text
    #    - Basic word overlap (fallback)
    # 3. Advanced fuzzy matching as final fallback
    # 4. Sort candidates by score
    # 5. Format and return best response
```

#### 3.4 NLP Intent Detection
**File:** `machinelearning/nlpIntentDetector.py` (279 lines)

**Features:**
- Semantic word clustering for question types (what, where, when, how_many, why, who)
- Natural language understanding untuk bahasa Indonesia
- Intent classification dengan confidence scoring
- Integration dengan main matching system

#### 3.5 Algorithm Orchestration
**File:** `machinelearning/algorithm.py`

**Main Function:** `process_question(question)`
```python
def process_question(question):
    # 1. NLP-based Intent Detection
    nlp_detector = get_nlp_intent_detector()
    analysis = nlp_detector.analyze_query(question)
    
    # 2. Check predefined answers (confidence >= 0.5)
    if detected_intent and confidence >= 0.5:
        return predefined_answer
    
    # 3. Fallback to CSV data matching
    clean_text = preprocessing.preprocess(question)
    result = matching.matchIntent(question)
    
    return result
```

### 4. DATA PROCESSING PIPELINE

#### 4.1 CSV Data Structure
Data diorganisir dalam format:
- **Source files:** `database/data/` (original CSV files)
- **Processed file:** `database/processed/itb_chatbot_high_quality_20250621_190153.csv`

**Data fields:**
- `data_source`: Source identifier (tentangITB, wikipediaITB, multikampusITB)
- `content`: Original content text
- `content_cleaned`: Preprocessed content
- `category`: Content category classification
- `quality_score`: Content quality rating (0-100)
- `content_length`: Character length
- `record_id`: Unique identifier

#### 4.2 Jupyter Notebook Processing
**File:** `machinelearning/jupyter/chatbot.ipynb`
- Data exploration dan quality analysis
- Data cleaning dan preprocessing pipeline
- Export processed data untuk production use

### 5. DEPLOYMENT DAN KONFIGURASI

#### 5.1 Docker Configuration
- **Backend Dockerfile:** `backend/Dockerfile`
- **Frontend Dockerfile:** `frontend/Dockerfile`

#### 5.2 Package Management
- **Backend:** `requirement.txt` (Python dependencies)
- **Frontend:** `package.json` (Node.js dependencies)
- **Root:** `setup.py` (Python package setup)

### 6. INTERAKSI ANTAR KOMPONEN

#### 6.1 Request Flow Detail
```
1. User mengetik pertanyaan di InputField.jsx
2. QueryButton.jsx trigger onClick event
3. apicall.jsx kirim POST request ke localhost:5000/ask
4. Flask routes.py terima request di endpoint /ask
5. controller.py extract JSON dan panggil services.py
6. services.py orchestrate ML pipeline:
   - preprocessing.preprocess() untuk text cleaning
   - matching.matchIntent() untuk pencarian similarity
   - dataLoader untuk akses data CSV
   - nlpIntentDetector untuk intent classification
7. Format response dengan intent, answer, source
8. Return JSON ke frontend
9. Chatbox.jsx display response ke user
```

#### 6.2 Data Flow Architecture
```
CSV Files → dataLoader.py → matching.py → services.py → controller.py → routes.py → Frontend
     ↓           ↓              ↓            ↓             ↓            ↓         ↓
Raw Data → Structured → Similarity → Business → Request → HTTP → UI Display
           Objects      Matching     Logic     Handling   Response
```

### 7. ALGORITMA YANG DIIMPLEMENTASI

#### 7.1 String Matching Algorithms
1. **Levenshtein Distance** - Edit distance calculation
2. **Jaccard Similarity** - Set intersection/union ratio
3. **TF-IDF Cosine Similarity** - Vector space model
4. **N-gram Similarity** - Character n-gram matching
5. **Soundex** - Phonetic matching algorithm

#### 7.2 Fuzzy Matching Enhancements
1. **Pattern Typo Recognition** - Common typo detection
2. **Character Frequency Analysis** - Anagram handling
3. **Advanced Fuzzy Scoring** - Multi-algorithm combination
4. **Adaptive Distance Threshold** - Dynamic tolerance

#### 7.3 NLP Processing
1. **Text Preprocessing** - Cleaning, tokenization, stemming
2. **Stopword Removal** - Indonesian stopwords filtering  
3. **Intent Classification** - Semantic understanding
4. **Confidence Scoring** - Result reliability assessment

### 8. KONFIGURASI DAN SETUP

#### 8.1 Development Environment
- **Frontend:** Vite + React (port 3000)
- **Backend:** Flask development server (port 5000)
- **CORS:** Enabled untuk cross-origin requests

#### 8.2 File Structure Summary
```
Makalah_Chatbot/
├── frontend/src/
│   ├── App.jsx (main component)
│   ├── components/ (UI components)
│   └── services/apicall.jsx (API layer)
├── backend/
│   ├── app.py (Flask entry point)
│   ├── routes/routes.py (API endpoints)
│   ├── controller/controller.py (request handling)
│   └── services/services.py (business logic)
└── machinelearning/
    ├── matching.py (core algorithms)
    ├── preprocessing.py (text processing)
    ├── dataLoader.py (data access)
    ├── nlpIntentDetector.py (NLP analysis)
    └── algorithm.py (orchestration)
```

Dokumentasi ini berdasarkan analisis mendalam terhadap codebase yang sebenarnya, mencakup implementasi algoritma yang ada, struktur data, dan alur eksekusi program yang terjadi dalam sistem chatbot ITB.
