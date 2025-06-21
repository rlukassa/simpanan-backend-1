<div align="center">

# 🤖✨ **ITB CHATBOT** ✨🤖
### *Implementasi Normalisasi Teks, Regex, dan Algoritma String Matching dalam Chatbot Informasi Khusus Institut Teknologi Bandung untuk Sistem Deteksi Intent Pengguna*

<img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&size=35&duration=3000&pause=500&color=00FFFF&center=true&vCenter=true&multiline=true&width=800&height=100&lines=%F0%9F%9A%80+INTELLIGENT+CHATBOT;%E2%9A%A1+FUZZY+MATCHING+POWER;%F0%9F%92%8E+NEON+TECH+STACK" alt="Typing SVG" />

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

[![Python](https://img.shields.io/badge/Python-3.8+-00FF00?style=for-the-badge&logo=python&logoColor=black)](https://python.org)
[![React](https://img.shields.io/badge/React-18.2+-FF00FF?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-00FFFF?style=for-the-badge&logo=flask&logoColor=black)](https://flask.palletsprojects.com)
[![MIT License](https://img.shields.io/badge/License-MIT-FFFF00?style=for-the-badge)](LICENSE)

<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400">

</div>

---

## 🌟 **PENJELASAN UMUM PROGRAM**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284087-bbe7e430-757e-4901-90bf-4cd2ce3e1852.gif" width="100">
</div>

**ITB Chatbot** adalah sistem **cerdas berbasis AI** yang dirancang khusus untuk menjawab pertanyaan seputar **Institut Teknologi Bandung (ITB)**. Program ini menggunakan **Advanced Fuzzy Matching** dengan toleransi typo yang sangat tinggi, memungkinkan pengguna bertanya dengan bahasa natural tanpa khawatir salah ketik.

### 🎯 **Key Features:**
- 🧠 **Advanced Fuzzy Matching** - Toleransi typo hingga 90%
- ⚡ **Real-time Response** - Jawaban instan < 1 detik
- 🌐 **Full Stack** - Web interface + REST API
- 📊 **382+ Data Entries** - Comprehensive ITB information
- 🔍 **Multi-Algorithm** - Levenshtein, N-gram, TF-IDF, Soundex
- 🎨 **Modern UI** - React + Vite dengan neon styling

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284136-03988914-d42b-4505-b9d4-f13b444d6e7a.gif" width="600">
</div>

---

## 📚 **TEORI SINGKAT**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284094-e50ceae2-de86-4dd6-a90c-78bcb3a926c0.gif" width="100">
</div>

### 🧮 **String Matching Algorithms**

Program ini mengimplementasikan multiple algoritma untuk mencapai akurasi tinggi:

#### **1. 🎯 Levenshtein Distance**
```
Edit distance untuk menghitung perbedaan karakter
Contoh: "itb" ↔ "ITB" = distance 0
        "fakultaas" ↔ "fakultas" = distance 1
```

#### **2. 🔤 N-Gram Similarity** 
```
Membandingkan substring dengan panjang n
Bigram: "itb" → ["it", "tb"]
Trigram: "itb" → ["itb"]
```

#### **3. 🔊 Soundex Phonetic Matching**
```
Mencocokkan berdasarkan bunyi kata
"teknologi" ↔ "teknoloji" → Same soundex code
```

#### **4. 📊 TF-IDF + Cosine Similarity**
```
Vector space model untuk semantic matching
Query vector vs Document vectors
```

### 🏗️ **Architecture Pattern**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284119-fbfd994d-8c2a-4c3d-9966-b43e43e20bca.gif" width="500">
</div>

```
User Query → Preprocessing → Multi-Algorithm Matching → Response Ranking → Best Answer
```

### ⚠️ **DISCLAIMER & LIMITATIONS**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="400">
</div>

> **📌 Important Note:** Chatbot ini **BUKAN** seperti ChatGPT atau Large Language Model (LLM) pada umumnya!

#### 🎯 **Perbedaan Fundamental:**

| **ITB Chatbot** | **ChatGPT/LLM** |
|-----------------|------------------|
| 🔍 **Rule-based + String Matching** | 🧠 **Neural Network Generation** |
| 📊 **Pre-defined Dataset** (382 entries) | 🌐 **Massive Training Data** (Billions) |
| 🎯 **Specific Domain** (ITB only) | 🌍 **General Knowledge** |
| ⚡ **Fast & Deterministic** | 🤔 **Creative but Unpredictable** |
| 💾 **Lightweight** (~50MB) | 🏗️ **Resource Heavy** (GBs) |

#### 🚫 **Keterbatasan Utama:**

- **📚 Limited Knowledge**: Hanya tahu tentang ITB berdasarkan dataset yang tersedia
- **🤖 No Conversation Context**: Tidak mengingat percakapan sebelumnya
- **❌ No Creative Generation**: Tidak bisa membuat jawaban baru, hanya matching dari database
- **🎯 Domain Specific**: Tidak bisa menjawab pertanyaan di luar topik ITB
- **📝 Static Responses**: Jawaban terbatas pada data yang sudah diproses

#### ✅ **Keunggulan:**

- **⚡ Ultra Fast**: Response time < 1 detik vs 5-10 detik ChatGPT
- **🎯 High Accuracy**: 76.7% untuk domain ITB vs general LLM yang mungkin hallucination
- **💰 Cost Effective**: Tidak butuh API subscription atau cloud computing
- **🔒 Privacy**: Data tidak dikirim ke server eksternal
- **📱 Offline Ready**: Bisa jalan tanpa internet connection

> **🎓 Academic Purpose:** Chatbot ini dibuat untuk mendemonstrasikan implementasi algoritma string matching dan fuzzy matching dalam konteks NLP, bukan untuk menggantikan general-purpose AI assistant.

---

## 💻 **TECH STACK**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284145-bf2c01a8-c448-4f1a-b911-996024c84606.gif" width="100">
</div>

### 🐍 **Backend Technologies**
<div align="center">

| Technology | Version | Purpose |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3.8+-00FF00?style=flat-square&logo=python&logoColor=black) | 3.8+ | Core Language |
| ![Flask](https://img.shields.io/badge/Flask-2.3+-00FFFF?style=flat-square&logo=flask&logoColor=black) | 2.3+ | Web Framework |
| ![Pandas](https://img.shields.io/badge/Pandas-1.5+-FF00FF?style=flat-square&logo=pandas&logoColor=white) | 1.5+ | Data Processing |
| ![NumPy](https://img.shields.io/badge/NumPy-1.21+-FFFF00?style=flat-square&logo=numpy&logoColor=black) | 1.21+ | Numerical Computing |
| ![Scikit](https://img.shields.io/badge/Scikit--Learn-1.3+-FF6600?style=flat-square&logo=scikit-learn&logoColor=white) | 1.3+ | Machine Learning |
| ![NLTK](https://img.shields.io/badge/NLTK-3.8+-00FF66?style=flat-square&logo=python&logoColor=black) | 3.8+ | NLP Processing |

</div>

### 🟢 **Frontend Technologies**
<div align="center">

| Technology | Version | Purpose |
|------------|---------|---------|
| ![React](https://img.shields.io/badge/React-18.2+-FF00FF?style=flat-square&logo=react&logoColor=white) | 18.2+ | UI Framework |
| ![Vite](https://img.shields.io/badge/Vite-5.0+-00FFFF?style=flat-square&logo=vite&logoColor=black) | 5.0+ | Build Tool |
| ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-FFFF00?style=flat-square&logo=javascript&logoColor=black) | ES6+ | Frontend Logic |
| ![CSS3](https://img.shields.io/badge/CSS3-Neon-FF00FF?style=flat-square&logo=css3&logoColor=white) | 3 | Neon Styling |
| ![HTML5](https://img.shields.io/badge/HTML5-5-00FF00?style=flat-square&logo=html5&logoColor=black) | 5 | Structure |

</div>

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284152-00e03c25-8c5c-4fe4-8df6-5c8e8d22f29e.gif" width="400">
</div>

---

## 📁 **STRUKTUR DIREKTORI**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284111-1a8912e8-b298-40e3-a1b0-3cbe90ed9f3a.gif" width="100">
</div>

```
🤖 ITB_Chatbot/
├── 📊 backend/                     # Python Backend
│   ├── 🚀 app.py                   # Flask Application Entry
│   ├── 🎮 controller/              # Request Controllers  
│   ├── 🛤️  routes/                 # API Routes
│   └── ⚙️  services/               # Business Logic
│
├── 🌐 frontend/                    # React Frontend
│   ├── 📂 public/                  # Static Assets
│   ├── 🎨 src/                     # Source Code
│   │   ├── 🧩 components/          # React Components
│   │   ├── 🔧 services/            # API Calls
│   │   └── 🎯 utils/               # Utilities
│   └── 📄 Dockerfile               # Container Config
│
├── 🧠 machinelearning/             # AI/ML Core
│   ├── 🔍 matching.py              # Fuzzy Matching Algorithms
│   ├── 📝 preprocessing.py         # Text Processing
│   ├── 📊 dataLoader.py            # Data Management
│   └── 🗃️  database/               # Data Storage
│       ├── 📋 data/                # Raw CSV Files
│       └── ✨ processed/           # Processed Data
│
├── 🧪 debug/                       # Testing & Debug
│   ├── 🎯 masterTestRunner.py      # Main Test Suite
│   ├── 🔬 testDirectMatching.py    # Unit Tests
│   └── 📈 *TestReports.json        # Test Results
│
├── 📚 docs/                        # Documentation
│   ├── 📖 README.md                # This File
│   ├── 🚀 INSTALLATION_GUIDE.md    # Setup Guide
│   └── 📊 *_REPORT.md              # Analysis Reports
│
├── ⚙️  setup.py                    # Automated Installer
├── 📦 package.json                 # npm Dependencies
├── 📋 requirement.txt              # Python Dependencies
└── 🔧 vite.config.js               # Vite Configuration
```

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8c7-6851-477b-90d6-1a9e7ac63e1e.gif" width="600">
</div>

---

## 🔄 **ALUR PROGRAM**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284103-b0a2e8f2-0e2e-4c3b-9eeb-aa85ce9d8898.gif" width="100">
</div>

### 🌊 **Data Flow Architecture**

```mermaid
flowchart TD
    A[👤 User Input] -->|"apa itu ITB?"| B[🔍 Preprocessing]
    B --> C[🧹 Text Cleaning]
    C --> D[🎯 Multi-Algorithm Matching]
    
    D --> E[📊 Levenshtein Distance]
    D --> F[🔤 N-Gram Similarity] 
    D --> G[🔊 Soundex Matching]
    D --> H[📈 TF-IDF Cosine]
    
    E --> I[⚖️ Score Combination]
    F --> I
    G --> I  
    H --> I
    
    I --> J[🏆 Best Match Selection]
    J --> K[📝 Response Formatting]
    K --> L[💬 User Response]
    
    style A fill:#00ffff,stroke:#ff00ff,stroke-width:3px
    style L fill:#00ff00,stroke:#ffff00,stroke-width:3px
    style D fill:#ff00ff,stroke:#00ffff,stroke-width:2px
```

### ⚡ **Processing Pipeline**

<div align="center">

| Step | Process | Input Example | Output Example |
|------|---------|---------------|----------------|
| 1️⃣ | **Input** | `"apakah ITB puya fakultaas teknik?"` | Raw query |
| 2️⃣ | **Preprocessing** | Text cleaning | `"apakah itb puya fakultas teknik"` |
| 3️⃣ | **Fuzzy Matching** | Query vs 382 entries | Similarity scores |
| 4️⃣ | **Ranking** | Score calculation | Best matches ranked |
| 5️⃣ | **Response** | Top match | ITB faculty information |

</div>

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284137-6fa6cc3a-6b1c-4075-b50b-4a43fcf74c40.gif" width="500">
</div>

---

## 👥 **USER JOURNEY**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284107-024ff8a4-db94-49d0-b3b7-b83c502d144c.gif" width="100">
</div>

### 🌟 **Persona 1: ITB Student**

```
🎓 "Mahasiswa ITB mencari info fakultas"

Step 1: 💻 Buka web chatbot
Step 2: 💬 Ketik "fakultas apa saja di ITB?"  
Step 3: ⚡ Bot response dalam <1 detik
Step 4: 📚 Dapat info lengkap 12 fakultas
Step 5: 🔍 Follow-up question: "jurusan teknik informatika"
Step 6: ✅ Satisfied dengan detailed answer
```

### 🌟 **Persona 2: Calon Mahasiswa**

```
🏫 "Calon mahasiswa dengan banyak typo"

Step 1: 📱 Akses via mobile browser
Step 2: 💬 Ketik "bagimana cara masuk ITB?" (typo: bagimana)
Step 3: 🤖 Fuzzy matching deteksi maksud "bagaimana"
Step 4: 📋 Dapat panduan lengkap admission process
Step 5: 💡 Tertarik dengan advanced typo tolerance
Step 6: 🎯 Explore lebih banyak features
```

### 🌟 **Persona 3: Developer/Researcher**

```
👨‍💻 "Developer testing API capabilities"

Step 1: 📖 Baca documentation
Step 2: 🔧 Setup environment dengan `python setup.py dev`
Step 3: 🚀 Start backend: `python app.py`
Step 4: 🧪 Test API: POST /ask endpoint
Step 5: 📊 Analyze fuzzy matching performance
Step 6: 🔬 Run comprehensive test suite
Step 7: ✨ Impressed dengan 76.7% overall accuracy
```

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284149-af43e5a9-4dd3-4b5d-ba88-9b3c6b1e15e8.gif" width="400">
</div>

---

## 🎬 **HOW TO DEMO**

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284104-4a2c9c1b-8a4c-4ad4-9db2-68de19d09752.gif" width="100">
</div>

### 🚀 **Quick Start Demo (5 minutes)**

#### **1️⃣ One-Command Setup**
```bash
# 🔥 Automated installation
python setup.py install

# ⏱️ Expected time: 2-3 minutes
# ✅ Will install Python + npm dependencies
# ✅ Will build frontend for production  
# ✅ Will verify all components
```

#### **2️⃣ Start Services**
```bash
# 🐍 Terminal 1: Backend
cd backend && python app.py
# 🟢 Server starts on http://localhost:5000

# 🌐 Terminal 2: Frontend  
npm run preview
# 🟢 Frontend serves on http://localhost:4173
```

#### **3️⃣ Demo Script**
```bash
# 💬 Open browser: http://localhost:4173

# 🎯 Demo Questions:
1. "apa itu ITB?"
   ➜ Shows basic ITB information

2. "apakah ITB puya fakultaas teknik?" (heavy typos)
   ➜ Demonstrates fuzzy matching power

3. "sejarah institut teknologi bandung"  
   ➜ Shows comprehensive historical data

4. "jurusan di ITB"
   ➜ Lists available programs

5. "cara masuk itb gimana sih?"
   ➜ Admission process information
```

### 🧪 **Advanced Demo (10 minutes)**

#### **4️⃣ Testing Suite Demo**
```bash
# 🔬 Run comprehensive tests
python debug/masterTestRunner.py

# 📊 Expected results:
# ✅ Basic Questions: 50.0%
# ✅ Comprehensive: 100.0%  
# ✅ Edge Cases: 80.0%
# 🏆 Overall: 76.7% GOOD
```

#### **5️⃣ API Demo**
```bash
# 🔌 Test REST API directly
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "fakultas ITB"}'

# 📈 Response time: <1 second
# 📋 JSON response with ITB faculty info
```

#### **6️⃣ Fuzzy Matching Demo**
```bash
# 🎯 Heavy typo tolerance test
python debug/testDirectMatching.py

# 💪 Test cases:
# ✅ "apakah ITB puya fakultaas teknik?" → ✅ Match
# ✅ "sejrah institut teknolgi bandng?" → ✅ Match  
# ✅ "gmna cara msuk ITB yah?" → ✅ Match
```

### 🎥 **Demo Highlights**

<div align="center">

| Feature | Demo Time | Wow Factor |
|---------|-----------|------------|
| 🚀 **One-Command Setup** | 30 seconds | ⭐⭐⭐⭐⭐ |
| 💬 **Web Interface** | 1 minute | ⭐⭐⭐⭐ |
| 🤖 **Fuzzy Matching** | 2 minutes | ⭐⭐⭐⭐⭐ |
| 🧪 **Testing Suite** | 2 minutes | ⭐⭐⭐⭐ |
| 🔌 **API Integration** | 1 minute | ⭐⭐⭐ |

</div>

### 🎨 **Demo Script Template**

```
🎤 "Selamat datang di demo ITB Chatbot!"

🔥 "Ini adalah chatbot AI dengan fuzzy matching advanced 
    yang bisa mengerti typo berat sekalipun!"

🚀 "Mari kita mulai dengan one-command setup..."
    [Run: python setup.py install]

💻 "Sekarang kita start backend dan frontend..."
    [Start services]

💬 "Mari kita test dengan pertanyaan normal dulu..."
    [Type: "apa itu ITB?"]

🤯 "Sekarang yang menarik - typo berat!"
    [Type: "apakah ITB puya fakultaas teknik?"]

⚡ "Lihat! Bot masih bisa memahami meskipun banyak typo!"

🧪 "Terakhir, mari kita lihat comprehensive testing..."
    [Run: python debug/masterTestRunner.py]

🎉 "Dan voila! ITB Chatbot dengan accuracy 76.7%!"
```

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284126-dd9ca0b4-94a7-4b6e-9bf1-7a48e6e4b7cc.gif" width="600">

### 🌟 **Ready to Experience the Future of ITB Information?** 🌟

[![Get Started](https://img.shields.io/badge/🚀_GET_STARTED-NOW-00FFFF?style=for-the-badge&logo=rocket)](setup.py)
[![Demo](https://img.shields.io/badge/🎬_LIVE_DEMO-AVAILABLE-FF00FF?style=for-the-badge&logo=play)](http://localhost:4173)
[![API](https://img.shields.io/badge/🔌_API_DOCS-EXPLORE-00FF00?style=for-the-badge&logo=swagger)](http://localhost:5000)

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">

**Made with ⚡ by Lukas Raja Agripa | 13523158 | ITB - Informatika**

**Licensed under the [MIT License](LICENSE).**

</div>
