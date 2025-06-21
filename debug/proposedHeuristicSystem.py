"""
PROPOSED HEURISTIC RESPONSE SYSTEM FOR ITB CHATBOT
=================================================

Template-based responses dengan fallback ke data retrieval
"""

HEURISTIC_TEMPLATES = {
    # Basic ITB Info
    "apa_itu_itb": {
        "patterns": ["apa itu itb", "itb itu apa", "pengertian itb", "definisi itb"],
        "template": """ITB adalah singkatan dari Institut Teknologi Bandung, yaitu salah satu perguruan tinggi negeri terbaik dan paling bergengsi di Indonesia yang didirikan pada tahun 1920.

ITB dikenal sebagai universitas teknik terdepan dengan berbagai fakultas unggulan seperti Teknik, MIPA, dan Seni Rupa.

Kalau kamu mau tahu lebih spesifik, misalnya soal jurusan tertentu di ITB, cara masuk, atau kehidupan kampusnya, tinggal bilang ya!""",
        "fallback_keywords": ["institut", "teknologi", "bandung", "universitas"]
    },
    
    # ITB History
    "sejarah_itb": {
        "patterns": ["sejarah itb", "awal itb", "pendirian itb", "didirikan kapan"],
        "template": """ITB didirikan pada tanggal 3 Juli 1920 dengan nama Technische Hoogeschool te Bandung (TH Bandung) sebagai sekolah tinggi teknik pertama di Hindia Belanda.

ITB memiliki sejarah panjang dalam pendidikan teknik di Indonesia dan menjadi tempat Presiden Soekarno meraih gelar insinyur sipilnya.

Mau tahu lebih detail tentang perkembangan ITB dari masa ke masa atau tokoh-tokoh penting ITB?""",
        "fallback_keywords": ["sejarah", "pendirian", "awal", "didirikan"]
    },
    
    # ITB Faculties
    "fakultas_itb": {
        "patterns": ["fakultas itb", "sekolah itb", "berapa fakultas", "fakultas apa saja"],
        "template": """ITB memiliki 12 fakultas dan sekolah, antara lain:
- STEI (Sekolah Teknik Elektro dan Informatika)
- FTSL (Fakultas Teknik Sipil dan Lingkungan) 
- FMIPA (Fakultas Matematika dan Ilmu Pengetahuan Alam)
- FSRD (Fakultas Seni Rupa dan Desain)
- Dan masih banyak lagi!

Kamu tertarik dengan fakultas yang mana? Atau mau tahu info program studi spesifik?""",
        "fallback_keywords": ["fakultas", "sekolah", "program", "studi"]
    }
}

def get_heuristic_response(user_query):
    """
    Check if query matches heuristic patterns first
    before falling back to data retrieval
    """
    query_lower = user_query.lower()
    
    for intent, config in HEURISTIC_TEMPLATES.items():
        # Check exact pattern match
        for pattern in config["patterns"]:
            if pattern in query_lower:
                return {
                    "source": "heuristic_template",
                    "intent": intent,
                    "answer": config["template"]
                }
        
        # Check keyword match
        if any(keyword in query_lower for keyword in config["fallback_keywords"]):
            return {
                "source": "heuristic_template", 
                "intent": intent,
                "answer": config["template"]
            }
    
    return None  # No heuristic match, use data retrieval

def enhanced_response_system(user_query):
    """
    Enhanced response system: Heuristic first, then data retrieval
    """
    # Try heuristic first
    heuristic_result = get_heuristic_response(user_query)
    if heuristic_result:
        return heuristic_result
    
    # Fallback to existing data retrieval
    from matching import matchIntent
    data_result = matchIntent(user_query)
    
    return {
        "source": "data_retrieval",
        "intent": "retrieved",
        "answer": data_result
    }
