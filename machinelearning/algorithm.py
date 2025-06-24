# Algorithm Orchestrator - koordinasi semua metode NLP dan matching
import preprocessing  # Import text preprocessing
import matching  # Import similarity matching
from nlpIntentDetector import getNlpIntentDetector  # Import NLP detector

def processQuestion(question):  # Fungsi utama proses pertanyaan
    print(f"DEBUG: Processing question = {question}")  # Log pertanyaan masuk
    
    # 1. NLP-based Intent Detection terlebih dahulu
    nlpDetector = getNlpIntentDetector()  # Dapatkan NLP detector instance
    analysis = nlpDetector.analyzeQuery(question)  # Analisis query dengan NLP
    
    detectedIntent = analysis['detected_intent']  # Ambil intent terdeteksi
    confidence = analysis['confidence']  # Ambil confidence score
    
    print(f"DEBUG: Intent = {detectedIntent}, confidence = {confidence}")  # Log hasil NLP
    
    # 2. Cek apakah ada predefined answer dengan confidence tinggi
    if detectedIntent and confidence >= 0.5:  # Threshold confidence tinggi
        predefinedAnswer = analysis['answer']  # Ambil jawaban predefined
        if predefinedAnswer:  # Jika ada jawaban
            print(f"DEBUG: Using NLP answer for intent {detectedIntent}")  # Log penggunaan NLP
            return predefinedAnswer  # Return jawaban NLP
    
    # 3. Fallback ke system matching dengan CSV data
    print("DEBUG: Fallback to CSV matching")  # Log fallback
    
    cleanText = preprocessing.preprocess(question)  # Preprocessing text
    print(f"DEBUG: Clean text = {cleanText}")  # Log text bersih
    
    result = matching.matchIntent(question)  # Coba matching dengan text asli
    print(f"DEBUG: Matching result (raw) = {result}")  # Log hasil raw
    
    if not result:  # Jika gagal dengan text asli
        result = matching.matchIntent(cleanText)  # Coba dengan text bersih
        print(f"DEBUG: Matching result (clean) = {result}")  # Log hasil clean
    
    return result  # Return hasil matching

def processQuestionWithDebug(question):  # Fungsi dengan debug lengkap
    print(f"DEBUG: Processing question = {question}")  # Log pertanyaan
    
    nlpDetector = getNlpIntentDetector()  # Dapatkan NLP detector
    debugInfo = nlpDetector.analyzeQuery(question)  # Analisis dengan debug info
    
    print(f"DEBUG: Original query: {debugInfo['original_query']}")  # Log query asli
    print(f"DEBUG: Processed query: {debugInfo['processed_query']}")  # Log query processed
    print(f"DEBUG: Features: {debugInfo['extracted_features']}")  # Log features
    print(f"DEBUG: Intent: {debugInfo['detected_intent']}")  # Log intent
    print(f"DEBUG: Confidence: {debugInfo['confidence']}")  # Log confidence
    
    detectedIntent = debugInfo['detected_intent']  # Ambil intent
    confidence = debugInfo['confidence']  # Ambil confidence
    
    if detectedIntent and confidence >= 0.3:  # Threshold rendah untuk debug
        predefinedAnswer = debugInfo['answer']  # Ambil jawaban
        if predefinedAnswer:  # Jika ada
            print(f"DEBUG: Using NLP answer for intent {detectedIntent}")  # Log NLP
            return predefinedAnswer  # Return jawaban NLP
    
    return processQuestion(question)  # Fallback ke proses normal