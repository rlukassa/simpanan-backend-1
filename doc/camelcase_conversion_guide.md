# Konversi Codebase ke camelCase - Panduan Implementasi

## 📋 **PROGRESS KONVERSI**

### ✅ **Files Sudah Dikonversi:**

#### **Backend Layer:**
1. **`backend/app.py`** ✅
   - Flask app initialization dengan comment singkat
   - Variable: `app`, `apiBp` (camelCase)

2. **`backend/routes/routes.py`** ✅  
   - Function: `askEndpoint()` (camelCase)
   - Variable: `apiBp` (camelCase)

3. **`backend/controller/controller.py`** ✅
   - Function: `handleAskRequest()` (camelCase)
   - Variables: `requestData`, `userQuestion`, `serviceResult` (camelCase)

4. **`backend/services/services.py`** ✅
   - Function: `detectIntentService(userQuestion)` (camelCase)
   - Variables: `rootPath`, `cleanedText`, `matchedResult` (camelCase)

#### **Machine Learning Layer:**
5. **`machinelearning/preprocessing.py`** ✅
   - Functions: `caseFolding()`, `removePunctuation()`, `removeStopwords()` (camelCase)
   - Variables: `importantTerms`, `inputCsv`, `outputCsv`, `textColumn` (camelCase)

6. **`machinelearning/dataLoader.py`** ✅
   - Functions: `loadCsvData()`, `loadOriginalCsvData()`, `getSampleData()` (camelCase)
   - Variables: `currentDir`, `processedFile`, `allData`, `csvFiles`, `dataDir` (camelCase)

7. **`machinelearning/algorithm.py`** ✅
   - Functions: `processQuestion()`, `processQuestionWithDebug()` (camelCase)
   - Variables: `nlpDetector`, `detectedIntent`, `predefinedAnswer`, `cleanText` (camelCase)

8. **`machinelearning/matching.py`** ⚠️ **Partial**
   - Functions dikonversi: `levenshteinDistance()`, `nGramSimilarity()` (camelCase)
   - Masih perlu: Function calls dan variable names dalam file besar ini

#### **Frontend Layer:**
9. **`frontend/src/services/apicall.jsx`** ✅
   - Function: `askToBackend(question)` (camelCase) 

### 🔄 **Files Perlu Dikonversi:**

#### **Frontend Components:**
- `frontend/src/App.jsx`
- `frontend/src/components/Chatbox.jsx`
- `frontend/src/components/InputField.jsx`
- `frontend/src/components/QueryButton.jsx`

#### **Machine Learning (Lanjutan):**
- `machinelearning/nlpIntentDetector.py` (279 lines)
- Sisa function calls di `machinelearning/matching.py` (608 lines)

---

## 🎯 **PATTERN KONVERSI YANG DITERAPKAN**

### **1. Function Names:**
```python
# BEFORE (snake_case)
def detect_intent_service(user_question):
def load_csv_data():
def process_question_with_debug():

# AFTER (camelCase) 
def detectIntentService(userQuestion):  # Parameter juga camelCase
def loadCsvData():
def processQuestionWithDebug():
```

### **2. Variable Names:**
```python
# BEFORE (snake_case)
root_path = os.path.abspath(...)
cleaned_text = preprocessing.preprocess(question)
matched_result = matching.matchIntent(question)

# AFTER (camelCase)
rootPath = os.path.abspath(...)  # Path ke root project
cleanedText = preprocessing.preprocess(question)  # Text yang dibersihkan
matchedResult = matching.matchIntent(question)  # Hasil matching
```

### **3. Comment Pattern:**
```python
# BEFORE (verbose)
# Import modul yang diperlukan setelah cleanup
# This will load the CSV data and process it through ML pipeline

# AFTER (singkat, 1 baris, bahasa Indonesia)
import sys  # Sistem parameter untuk path
cleanedText = preprocessing.preprocess(userQuestion)  # Bersihkan text
```

### **4. Import Statement Updates:**
```python
# BEFORE
from dataLoader import load_csv_data
from controller.controller import handle_ask

# AFTER 
from dataLoader import loadCsvData  # Import data loader
from controller.controller import handleAskRequest  # Import request handler
```

---

## 🚀 **LANGKAH SELANJUTNYA**

### **Priority 1: Machine Learning Completion**
```bash
# Files yang perlu diselesaikan:
1. machinelearning/matching.py (sisa function calls)
   - Update semua snake_case function calls
   - Update variable names dalam 608 baris
   
2. machinelearning/nlpIntentDetector.py (279 lines)
   - Convert class methods dan variables
   - Update semantic_clusters dictionary keys
```

### **Priority 2: Frontend Components**
```bash
# Files frontend yang perlu dikonversi:
1. App.jsx - Main component state dan functions
2. Chatbox.jsx - Message display logic
3. InputField.jsx - Input handling
4. QueryButton.jsx - Button interactions
```

### **Priority 3: Integration Testing**
```bash
# Setelah konversi, test:
1. Backend API endpoints (/ask)
2. ML pipeline functionality
3. Frontend-backend communication
4. Error handling flows
```

---

## 📝 **CONTOH IMPLEMENTASI PATTERN**

### **Untuk Functions dengan Many Parameters:**
```python
# BEFORE
def match_with_csv_data(user_query, threshold=0.3, top_k=3):

# AFTER
def matchWithCsvData(userQuery, threshold=0.3, topK=3):  # CamelCase parameters
```

### **Untuk Complex Variable Assignments:**
```python
# BEFORE
processed_file = os.path.join(os.path.dirname(__file__), 'database', 'processed', 'file.csv')

# AFTER
processedFile = os.path.join(  # Path ke file processed
    os.path.dirname(__file__), 
    'database', 
    'processed', 
    'itb_chatbot_high_quality_20250621_190153.csv'
)
```

### **Untuk Error Handling:**
```python
# BEFORE
except ImportError as e:
    print(f"DEBUG: Import error = {e}")

# AFTER
except ImportError as importError:  # CamelCase exception variable
    print(f"DEBUG: Import gagal = {importError}")  # Bahasa Indonesia
```

---

## 🎯 **TESTING EXAMPLES dengan Typos**

### **Input Test Cases:**
```python
# Test cases dengan typo seperti tulisan manusia:
testQueries = [
    "apa itu itb?",           # Normal
    "infromasi fakultas",     # Typo: infromasi -> informasi  
    "akreditas kampus",       # Typo: akreditas -> akreditasi
    "tekknologi informasi",   # Typo: tekknologi -> teknologi
    "jurusan tkerik sipil",   # Typo: tkerik -> teknik
    "biayya kuliah",          # Typo: biayya -> biaya
    "lokasi kamppus"          # Typo: kamppus -> kampus
]

# Expected behavior:
# Fuzzy matching algorithms akan detect dan correct typos
# Advanced algorithms: Levenshtein, Soundex, n-gram similarity
```

### **Response Format:**
```json
{
    "intent": "found",
    "answer": "ITB (Institut Teknologi Bandung) adalah...",
    "source": "machine_learning", 
    "processedQuery": "informasi fakultas"  // Typo corrected
}
```

---

## 🔧 **TOOLS UNTUK KONVERSI MASS**

### **Find & Replace Patterns:**
```bash
# Pattern 1: Function calls
find: "(\w+)\.(\w+_\w+)"
replace: "$1.$2" (manual camelCase conversion needed)

# Pattern 2: Variable assignments  
find: "(\w+_\w+) = "
replace: "camelCaseVersion = "

# Pattern 3: Function definitions
find: "def (\w+_\w+)\("
replace: "def camelCaseVersion("
```

Dokumentasi ini memberikan blueprint lengkap untuk menyelesaikan konversi codebase ke camelCase dengan pattern yang konsisten dan maintainable.
