# Implementasi algoritma KMP, BM, Rabin-Karp, atau Jaccard
# Logika utama kombinasi semua metode dengan NLP-based intent detection

import preprocessing
import matching
from nlpIntentDetector import get_nlp_intent_detector

def process_question(question):
    """
    Fungsi utama yang menggabungkan NLP-based intent detection, preprocessing dan matching
    """
    print(f"DEBUG: Processing question = {question}")  # Debug
    
    # 1. NLP-based Intent Detection terlebih dahulu
    nlp_detector = get_nlp_intent_detector()
    analysis = nlp_detector.analyze_query(question)
    
    detected_intent = analysis['detected_intent']
    confidence = analysis['confidence']
    
    print(f"DEBUG: Detected intent = {detected_intent}, confidence = {confidence}")  # Debug
      # 2. Cek apakah ada predefined answer dengan confidence tinggi
    if detected_intent and confidence >= 0.5:  # Raised threshold from 0.3 to 0.5
        predefined_answer = analysis['answer']
        if predefined_answer:
            print(f"DEBUG: Using NLP predefined answer for intent {detected_intent}")  # Debug
            return predefined_answer
    
    # 3. Fallback ke system matching dengan CSV data
    print("DEBUG: Falling back to CSV data matching")  # Debug
    
    # Preprocessing (opsional) bersihkan kata
    clean_text = preprocessing.preprocess(question)
    print(f"DEBUG: Clean text = {clean_text}")  # Debug
    
    # Coba matching dengan text asli dulu
    result = matching.matchIntent(question)
    print(f"DEBUG: Matching result (raw) = {result}")  # Debug
    
    # Jika gagal, coba dengan text yang sudah di-preprocessing
    if not result:
        result = matching.matchIntent(clean_text)
        print(f"DEBUG: Matching result (clean) = {result}")  # Debug
    
    return result

def process_question_with_debug(question):
    """
    Fungsi dengan debug info lengkap untuk menunjukkan cara kerja NLP system
    """
    print(f"DEBUG: Processing question = {question}")  # Debug
    
    # 1. NLP-based Intent Detection dengan debug info
    nlp_detector = get_nlp_intent_detector()
    debug_info = nlp_detector.analyze_query(question)
    
    print(f"DEBUG: Original query: {debug_info['original_query']}")
    print(f"DEBUG: Processed query: {debug_info['processed_query']}")
    print(f"DEBUG: Extracted features: {debug_info['extracted_features']}")
    print(f"DEBUG: Detected intent: {debug_info['detected_intent']}")
    print(f"DEBUG: Confidence: {debug_info['confidence']}")
    
    detected_intent = debug_info['detected_intent']
    confidence = debug_info['confidence']
    
    # 2. Cek apakah ada predefined answer dengan confidence tinggi
    if detected_intent and confidence >= 0.3:
        predefined_answer = debug_info['answer']
        if predefined_answer:
            print(f"DEBUG: Using NLP predefined answer for intent {detected_intent}")  # Debug
            return predefined_answer
    
    # 3. Fallback ke sistem lama
    return process_question(question)