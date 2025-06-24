# Business Logic Service Layer
import sys  # Sistem parameter untuk path
import os   # Interface OS untuk file path

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Dapatkan path root project
if rootPath not in sys.path:  # Cek apakah path sudah ada
    sys.path.append(rootPath)  # Tambah ke Python path

def detectIntentService(userQuestion):  # Fungsi utama deteksi intent
    try:  # Coba import modul ML
        from machinelearning import matching  # Import algoritma matching
        from machinelearning import preprocessing  # Import text preprocessing
        from machinelearning import algorithm  # Import orchestrator
        from machinelearning.nlpIntentDetector import getNlpIntentDetector  # Import NLP detector
    except ImportError as importError:  # Tangkap error import
        print(f"DEBUG: Import gagal = {importError}")  # Log error
        return {  # Return fallback response
            "intent": None,
            "answer": "Maaf, sistem bermasalah. Coba lagi nanti.",
            "source": "import_error"
        }

    try:  # Coba preprocessing text
        if hasattr(preprocessing, 'preprocess'):  # Cek fungsi ada
            cleanedText = preprocessing.preprocess(userQuestion)  # Bersihkan text
            print(f"DEBUG: '{userQuestion}' → '{cleanedText}'")  # Log hasil
        else:  # Jika preprocess tidak ada
            cleanedText = userQuestion  # Pakai text asli
    except Exception as preprocessError:  # Tangkap error preprocessing
        print(f"DEBUG: Preprocessing gagal = {preprocessError}")  # Log error
        cleanedText = userQuestion  # Fallback ke text asli

    # Coba NLP Intent Detector dengan link terlebih dahulu
    try:
        nlpDetector = getNlpIntentDetector()  # Buat instance NLP detector
        nlpResult = nlpDetector.getAnswerWithLinks(userQuestion)  # Deteksi dengan link
        print(f"DEBUG: NLP result = {nlpResult}")  # Log hasil NLP
        
        if nlpResult and nlpResult.get('confidence', 0) > 0.3:  # Kalau confidence cukup
            response = {  # Response structure
                "intent": nlpResult.get('intent', 'nlp_detected'),
                "answer": nlpResult.get('answer', ''),
                "source": "nlp_intent_detector",
                "processedQuery": cleanedText,
                "confidence": nlpResult.get('confidence', 0)
            }
            
            # Tambahkan link jika ada
            if nlpResult.get('hasLinks', False) and nlpResult.get('links'):
                response['links'] = nlpResult['links']  # Tambah link ke response
                response['hasLinks'] = True  # Flag ada link
            else:
                response['hasLinks'] = False  # Tidak ada link
                
            return response  # Return hasil NLP
            
    except Exception as nlpError:  # Handle error NLP
        print(f"DEBUG: NLP detection gagal = {nlpError}")  # Log error
        # Lanjut ke fallback matching
      # Fallback ke matching tradisional jika NLP gagal
    try:  # Coba matching intent
        if hasattr(matching, 'matchIntent'):  # Cek fungsi matchIntent ada
            matchedResult = matching.matchIntent(userQuestion)  # Cari match
            print(f"DEBUG: Match = {matchedResult[:100] if matchedResult else 'None'}...")  # Log hasil
        elif hasattr(matching, 'match_with_csv_data'):  # Alternatif fungsi
            matchedResult = matching.match_with_csv_data(userQuestion, threshold=0.3, topK=1)  # Match CSV
            print(f"DEBUG: CSV match = {matchedResult[:100] if matchedResult else 'None'}...")  # Log hasil
        else:  # Tidak ada fungsi matching
            print("DEBUG: Tidak ada fungsi matching")  # Log info
            matchedResult = None  # Set None
    except Exception as matchingError:  # Tangkap error matching
        print(f"DEBUG: Matching gagal = {matchingError}")  # Log error
        matchedResult = None  # Set None
    
    # Cek hasil matching
    if matchedResult and len(str(matchedResult).strip()) > 0:  # Cek hasil valid
        return {  # Return sukses
            "intent": "found",
            "answer": str(matchedResult).strip(),
            "source": "machine_learning",
            "processedQuery": cleanedText,
            "hasLinks": False  # Matching tradisional tidak ada link
        }
    else:  # Tidak ada hasil
        return {  # Return tidak ditemukan
            "intent": "not_found",
            "answer": "Maaf, belum bisa jawab. Coba kata kunci lain seperti 'fakultas', 'jurusan', 'akreditas'.",
            "source": "fallback",
            "processedQuery": cleanedText,
            "hasLinks": False  # Fallback tidak ada link
        }

