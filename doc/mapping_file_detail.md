# Mapping File dan Fungsi - Chatbot ITB
## Dokumentasi Detail Interaksi Antar File

### 1. ENTRY POINTS DAN INITIALIZATION

#### 1.1 Frontend Entry Point
**File:** `frontend/src/main.jsx`
```jsx
// Entry point React application
import App from './App.jsx'
// Render App component ke DOM
```

**File:** `frontend/src/App.jsx`
```jsx
// Main application component
// Contains: Logo, Chatbox, InputField, QueryButton
// State management untuk conversation history  
// Import dan render semua child components
```

#### 1.2 Backend Entry Point  
**File:** `backend/app.py`
```python
from flask import Flask
from flask_cors import CORS
from routes.routes import api_bp

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests
app.register_blueprint(api_bp)  # Register API routes

if __name__ == '__main__':
    app.run(debug=True)  # Start Flask server
```

### 2. API LAYER MAPPING

#### 2.1 Frontend API Service
**File:** `frontend/src/services/apicall.jsx`
```jsx
export async function askToBackend(question) {
  // POST request ke http://localhost:5000/ask
  // Headers: Content-Type: application/json
  // Body: { question: "user input" }
  // Return: JSON response dari backend
}
```

**Called by:** 
- `frontend/src/components/QueryButton.jsx`
- `frontend/src/components/InputField.jsx` (on Enter key)

#### 2.2 Backend Route Definition
**File:** `backend/routes/routes.py`
```python
from flask import Blueprint
from controller.controller import handle_ask

api_bp = Blueprint('api', __name__)

@api_bp.route('/ask', methods=['POST'])
def ask():
    return handle_ask()  # Delegate to controller
```

**Imported by:** `backend/app.py`

#### 2.3 Request Controller
**File:** `backend/controller/controller.py`
```python
from flask import request, jsonify
from services.services import detectIntentService

def handle_ask():
    data = request.get_json()          # Parse JSON request
    question = data.get('question', '') # Extract question field
    result = detectIntentService(question)  # Call business logic
    return jsonify(result)             # Return JSON response
```

**Called by:** `backend/routes/routes.py`
**Calls:** `backend/services/services.py`

### 3. BUSINESS LOGIC LAYER

#### 3.1 Main Service Orchestrator
**File:** `backend/services/services.py`
```python
# Main business logic coordinator
def detectIntentService(question):
    # Import ML modules
    from machinelearning import matching
    from machinelearning import preprocessing  
    from machinelearning import algorithm
    
    # 1. Text preprocessing
    clean_text = preprocessing.preprocess(question)
    
    # 2. Intent matching
    matched_result = matching.matchIntent(question)
    # Alternative: matching.match_with_csv_data(question)
    
    # 3. Format response
    return {
        "intent": "found" or "not_found",
        "answer": matched_result,
        "source": "machine_learning" or "fallback"
    }
```

**Called by:** `backend/controller/controller.py`
**Calls:** All machine learning modules

### 4. MACHINE LEARNING MODULES

#### 4.1 Algorithm Orchestrator
**File:** `machinelearning/algorithm.py`
```python
import preprocessing
import matching
from nlpIntentDetector import get_nlp_intent_detector

def process_question(question):
    # 1. NLP Intent Detection
    nlp_detector = get_nlp_intent_detector()
    analysis = nlp_detector.analyze_query(question)
    
    # 2. Check confidence threshold (>= 0.5)
    if detected_intent and confidence >= 0.5:
        return predefined_answer
    
    # 3. Fallback to CSV matching
    clean_text = preprocessing.preprocess(question)
    result = matching.matchIntent(question)
    return result
```

**Function:** `process_question_with_debug()` - Enhanced debugging version

#### 4.2 Text Preprocessing Module
**File:** `machinelearning/preprocessing.py`
```python
# Complete preprocessing pipeline
def preprocess(text):
    text = caseFolding(text)      # lowercase
    text = removePunctuation(text) # remove punctuation
    tokens = tokenize(text)        # split to words
    tokens = removeStopwords(tokens) # remove Indonesian stopwords
    tokens = stemming(tokens)      # intelligent stemming
    return ' '.join(tokens)

# Individual functions:
- caseFolding() 
- removePunctuation()
- tokenize()
- removeStopwords() # Indonesian stopwords
- stemming() # Preserve important terms like 'akreditasi', 'universitas'
```

**Called by:** 
- `machinelearning/algorithm.py`
- `backend/services/services.py`

#### 4.3 Core Matching Engine
**File:** `machinelearning/matching.py` (630 lines)

**Main Functions:**
```python
def matchIntent(user_text):
    # Entry point function
    # Try CSV data matching first
    # Ultimate fallback if no matches
    
def match_with_csv_data(user_query, threshold=0.3, top_k=3):
    # Main matching algorithm
    # Multiple strategies:
    # 1. Exact substring matching
    # 2. Enhanced fuzzy word matching  
    # 3. Jaccard similarity
    # 4. Basic word overlap
    # 5. Advanced fuzzy fallback
    
def advanced_fuzzy_similarity(s1, s2, max_distance=4):
    # Multi-algorithm fuzzy matching:
    # - Levenshtein distance (25%)
    # - N-gram similarity (35% combined) 
    # - Character frequency (15%)
    # - Phonetic matching (10%)
    # - SequenceMatcher (10%)
    # - Pattern recognition (5%)
```

**Algorithm Functions:**
- `levenshtein_distance()` - Edit distance calculation
- `soundex()` - Phonetic matching 
- `n_gram_similarity()` - Bigram/trigram comparison
- `character_frequency_similarity()` - Anagram detection
- `pattern_typo_recognition()` - Common typo patterns
- `find_fuzzy_matches()` - Fuzzy match finder
- `enhanced_word_matching()` - Word-level matching
- `jaccardSimilarity()` - Set similarity
- `tfidf_similarity()` - Vector space model

**Called by:**
- `backend/services/services.py`
- `machinelearning/algorithm.py`

#### 4.4 Data Access Layer
**File:** `machinelearning/dataLoader.py`
```python
def load_csv_data():
    # Try processed high-quality CSV first:
    # 'itb_chatbot_high_quality_20250621_190153.csv'
    
    # Fallback to original CSV files:
    # - tentangITB.csv
    # - wikipediaITB.csv  
    # - multikampusITB.csv
    
    # Return structured data:
    # {
    #   'source': data_source,
    #   'content': original_content,
    #   'processed_content': cleaned_content,
    #   'category': category,
    #   'quality_score': score,
    #   'content_length': length
    # }

def load_original_csv_data():
    # Fallback method for original CSV files
```

**Called by:** `machinelearning/matching.py`

#### 4.5 NLP Intent Detection
**File:** `machinelearning/nlpIntentDetector.py` (279 lines)
```python
class NaturalLanguageIntentDetector:
    def __init__(self):
        # Semantic word clustering
        self.semantic_clusters = {
            'question_words': {
                'what': ['apa', 'apakah', 'gimana', ...],
                'where': ['dimana', 'di mana', 'lokasi', ...], 
                'when': ['kapan', 'tanggal', 'tahun', ...],
                # ... more clusters
            }
        }
    
    def analyze_query(self, query):
        # Natural language understanding
        # Intent classification
        # Confidence scoring
        return {
            'original_query': query,
            'processed_query': processed,
            'detected_intent': intent,
            'confidence': confidence,
            'answer': predefined_answer
        }

def get_nlp_intent_detector():
    # Factory function untuk NLP detector instance
```

**Called by:** `machinelearning/algorithm.py`

### 5. UI COMPONENT MAPPING

#### 5.1 Main App Component
**File:** `frontend/src/App.jsx`
```jsx
// State management:
- messages (conversation history)
- isLoading (request status)

// Child components:
- Logo component (ITB logo)
- Chatbox component (message display)
- InputField component (user input)
- QueryButton component (predefined queries)

// Functions:
- handleSendMessage() // Process user input
- addMessage() // Add to conversation
```

#### 5.2 Chat Display Component
**File:** `frontend/src/components/Chatbox.jsx`
```jsx
// Props: messages, isLoading
// Renders conversation history
// Message types: user, bot
// Loading indicator during processing
// Auto-scroll to latest message
```

#### 5.3 Input Component
**File:** `frontend/src/components/InputField.jsx`
```jsx
// Props: onSendMessage, isLoading
// State: inputValue
// Events:
- onChange (update input)
- onKeyPress (Enter to send)
- onSubmit (form submission)
// Calls: apicall.askToBackend()
```

#### 5.4 Quick Query Component  
**File:** `frontend/src/components/QueryButton.jsx`
```jsx
// Props: queries, onQuerySelect
// Renders predefined query buttons
// Quick access untuk common questions
// Triggers same flow as manual input
```

### 6. COMPLETE DATA FLOW MAPPING

#### 6.1 User Query Flow
```
User Input (InputField.jsx)
    ↓
handleSendMessage (App.jsx)
    ↓  
askToBackend (apicall.jsx)
    ↓
POST /ask (routes.py)
    ↓
handle_ask (controller.py)
    ↓
detectIntentService (services.py)
    ↓
[ML Processing Pipeline]
    ↓
JSON Response
    ↓
Display in Chatbox (Chatbox.jsx)
```

#### 6.2 ML Processing Pipeline Detail
```
detectIntentService (services.py)
    ↓
preprocess (preprocessing.py)
    ↓
matchIntent (matching.py)
    ↓ 
match_with_csv_data (matching.py)
    ↓
get_processed_data (dataLoader.py)
    ↓
load_csv_data (dataLoader.py)
    ↓
[Multiple Matching Algorithms]
    ↓
format_response (matching.py)
    ↓
Return to services.py
```

#### 6.3 Error Handling Flow
```
Exception in ML modules
    ↓
Caught by services.py
    ↓  
Return fallback response:
{
  "intent": "not_found",
  "answer": "Maaf, saya belum bisa menjawab...",
  "source": "fallback"
}
    ↓
Display error message to user
```

### 7. CONFIGURATION FILES

#### 7.1 Build Configuration
- `package.json` - Node.js dependencies dan scripts
- `vite.config.js` - Vite build configuration  
- `eslint.config.js` - Code linting rules

#### 7.2 Python Configuration
- `requirement.txt` - Python dependencies
- `setup.py` - Package setup configuration

#### 7.3 Docker Configuration
- `backend/Dockerfile` - Backend container setup
- `frontend/Dockerfile` - Frontend container setup

### 8. DEBUGGING DAN LOGGING

#### 8.1 Debug Points
```python
# services.py
print(f"DEBUG: Import error = {e}")
print(f"DEBUG: Preprocessed text = {clean_text}")
print(f"DEBUG: Matching result = {matched_result}")

# matching.py  
print(f"[MATCHING] Starting match for query: '{user_query}'")
print(f"[MATCHING] Found {len(candidates)} candidates")
print(f"[MATCHING] Best match: {best_match['entry']['content'][:100]}...")

# algorithm.py
print(f"DEBUG: Processing question = {question}")
print(f"DEBUG: Detected intent = {detected_intent}, confidence = {confidence}")
```

#### 8.2 Error Handling Points
- Import errors dalam services.py
- CSV file loading errors dalam dataLoader.py  
- Network errors dalam apicall.jsx
- Processing errors dalam matching.py

### 9. INTERAKSI SUMMARY TABLE

| From File | Function | To File | Function | Purpose |
|-----------|----------|---------|----------|---------|
| App.jsx | handleSendMessage | apicall.jsx | askToBackend | Send user query |
| apicall.jsx | fetch POST | routes.py | ask() | HTTP API call |
| routes.py | ask() | controller.py | handle_ask() | Route request |
| controller.py | handle_ask() | services.py | detectIntentService() | Process request |
| services.py | detectIntentService | preprocessing.py | preprocess() | Clean text |
| services.py | detectIntentService | matching.py | matchIntent() | Find answers |
| matching.py | match_with_csv_data | dataLoader.py | load_csv_data() | Get data |
| algorithm.py | process_question | nlpIntentDetector.py | analyze_query() | NLP analysis |

Dokumentasi ini memberikan panduan lengkap tentang bagaimana setiap file berinteraksi dalam sistem chatbot ITB, berdasarkan analisis mendalam terhadap implementasi yang sebenarnya ada di codebase.
