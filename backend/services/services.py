# Logika layanan backend (memanggil fungsi ML/matching) 
# Memanggil modul algorithm / intentClassifier
# 
# UPDATE AFTER CLEANUP (Dec 2024):
# - Removed references to deleted intentClassifier module
# - Updated imports to use cleaned-up module structure
# - Improved error handling and debugging
# - Uses matchIntent function from matching.py as primary method
# - Fallback to match_with_csv_data if needed
# - Added source field to response for better tracking

import sys
import os

# Tambahkan path ke root project agar bisa import machinelearning
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

def detectIntentService(question):
    """
    Menerima pertanyaan user, melakukan preprocessing, matching, dan intent classification,
    lalu mengembalikan intent dan jawaban.
    """
    # Import modul yang diperlukan setelah cleanup
    try:
        from machinelearning import matching
        from machinelearning import preprocessing
        from machinelearning import algorithm
    except ImportError as e:
        print(f"DEBUG: Import error = {e}")
        return {
            "intent": None,
            "answer": "Maaf, sistem sedang mengalami masalah. Silakan coba lagi nanti."
        }

    # 1. Preprocessing teks
    try:
        if hasattr(preprocessing, 'preprocess'):
            clean_text = preprocessing.preprocess(question)
            print(f"DEBUG: Preprocessed text = {clean_text}")
        else:
            clean_text = question
    except Exception as e:
        print(f"DEBUG: Preprocessing error = {e}")
        clean_text = question

    # 2. Matching menggunakan algoritma yang tersedia
    try:
        # Gunakan fungsi matchIntent dari matching.py
        if hasattr(matching, 'matchIntent'):
            matched_result = matching.matchIntent(question)
            print(f"DEBUG: Matching result = {matched_result}")
        # Alternatif: gunakan match_with_csv_data
        elif hasattr(matching, 'match_with_csv_data'):
            matched_result = matching.match_with_csv_data(question, threshold=0.3, top_k=1)
            print(f"DEBUG: CSV matching result = {matched_result}")
        else:
            print("DEBUG: No matching function found")
            matched_result = None
    except Exception as e:
        print(f"DEBUG: Matching error = {e}")
        matched_result = None

    # 3. Format respons
    if matched_result:
        return {
            "intent": "found",
            "answer": matched_result,
            "source": "machine_learning"
        }
    else:
        return {
            "intent": "not_found",
            "answer": "Maaf, saya belum bisa menjawab pertanyaan tersebut. Silakan coba dengan kata kunci yang berbeda.",
            "source": "fallback"
        }

