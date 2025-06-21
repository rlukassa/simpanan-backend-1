# matching.py
# Modul untuk string matching (Jaccard, Fuzzy, dsb) dengan integrasi data CSV
# Enhanced with phonetic matching, n-gram similarity, and typo pattern recognition

import os
import sys
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from difflib import SequenceMatcher

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from dataLoader import load_csv_data

def levenshtein_distance(s1, s2):
    """
    Calculate Levenshtein distance between two strings
    For fuzzy matching and typo tolerance
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    if len(s2) == 0:
        return len(s1)
    
    # Create matrix
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions and substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def soundex(word):
    """
    Simple Soundex algorithm for phonetic matching
    Maps similar-sounding words to same code
    """
    if not word:
        return ""
    
    word = word.upper()
    soundex_mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2',
        'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    
    # Keep first letter
    soundex_code = word[0]
    
    # Convert remaining letters
    for char in word[1:]:
        if char in soundex_mapping:
            code = soundex_mapping[char]
            # Avoid consecutive duplicates
            if not soundex_code.endswith(code):
                soundex_code += code
    
    # Pad with zeros or truncate to 4 characters
    soundex_code = (soundex_code + '000')[:4]
    return soundex_code

def n_gram_similarity(s1, s2, n=2):
    """
    Calculate n-gram similarity between two strings
    Better for handling character transpositions and insertions
    """
    if not s1 or not s2:
        return 0.0
    
    s1 = s1.lower()
    s2 = s2.lower()
    
    # Generate n-grams
    def get_ngrams(string, n):
        return set(string[i:i+n] for i in range(len(string) - n + 1))
    
    ngrams1 = get_ngrams(s1, n)
    ngrams2 = get_ngrams(s2, n)
    
    if not ngrams1 and not ngrams2:
        return 1.0
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2
    
    return len(intersection) / len(union) if union else 0.0

def character_frequency_similarity(s1, s2):
    """
    Compare character frequency distribution
    Good for handling repeated characters and anagrams
    """
    if not s1 or not s2:
        return 0.0
    
    s1_clean = ''.join(c.lower() for c in s1 if c.isalnum())
    s2_clean = ''.join(c.lower() for c in s2 if c.isalnum())
    
    if not s1_clean or not s2_clean:
        return 0.0
    
    # Count character frequencies
    freq1 = {}
    freq2 = {}
    
    for char in s1_clean:
        freq1[char] = freq1.get(char, 0) + 1
    
    for char in s2_clean:
        freq2[char] = freq2.get(char, 0) + 1
    
    # Calculate similarity based on frequency difference
    all_chars = set(freq1.keys()) | set(freq2.keys())
    total_diff = 0
    total_chars = len(s1_clean) + len(s2_clean)
    
    for char in all_chars:
        diff = abs(freq1.get(char, 0) - freq2.get(char, 0))
        total_diff += diff
    
    similarity = 1.0 - (total_diff / total_chars) if total_chars > 0 else 0.0
    return max(0.0, similarity)

def pattern_typo_recognition(s1, s2):
    """
    Recognize common typo patterns
    - Repeated characters (aaa -> a)
    - Missing characters
    - Extra characters at start/end
    """
    if not s1 or not s2:
        return 0.0
    
    s1_clean = ''.join(c.lower() for c in s1 if c.isalnum())
    s2_clean = ''.join(c.lower() for c in s2 if c.isalnum())
    
    if not s1_clean or not s2_clean:
        return 0.0
    
    # Remove repeated characters for comparison
    def remove_repeated_chars(s):
        result = ""
        prev_char = ""
        for char in s:
            if char != prev_char:
                result += char
                prev_char = char
        return result
    
    s1_norep = remove_repeated_chars(s1_clean)
    s2_norep = remove_repeated_chars(s2_clean)
    
    # Direct comparison after removing repetitions
    if s1_norep == s2_norep:
        return 0.95  # High score for repeated char typos
    
    # Check if one is contained in the other (extra chars at start/end)
    if s1_norep in s2_norep or s2_norep in s1_norep:
        shorter_len = min(len(s1_norep), len(s2_norep))
        longer_len = max(len(s1_norep), len(s2_norep))
        if shorter_len > 0:
            return shorter_len / longer_len * 0.9  # Good score for containment
    
    return 0.0

def advanced_fuzzy_similarity(s1, s2, max_distance=4):
    """
    Enhanced fuzzy similarity combining multiple algorithms
    - Levenshtein distance
    - N-gram similarity
    - Character frequency
    - Phonetic matching
    - Pattern recognition
    """
    if not s1 or not s2:
        return 0.0
    
    # Normalize strings
    s1_clean = ''.join(c.lower() for c in s1 if c.isalnum())
    s2_clean = ''.join(c.lower() for c in s2 if c.isalnum())
    
    if not s1_clean or not s2_clean:
        return 0.0
    
    # 1. Pattern typo recognition (highest priority)
    pattern_score = pattern_typo_recognition(s1, s2)
    if pattern_score > 0.9:
        return pattern_score
    
    # 2. Traditional Levenshtein distance
    distance = levenshtein_distance(s1_clean, s2_clean)
    max_len = max(len(s1_clean), len(s2_clean))
    
    # More lenient max distance for typo tolerance
    adaptive_max_distance = min(max_distance, max(3, max_len // 2))
    
    if distance == 0:
        return 1.0
    
    levenshtein_score = 0.0
    if distance <= adaptive_max_distance:
        levenshtein_score = 1.0 - (distance / max_len)
    
    # 3. N-gram similarity (bigrams and trigrams)
    bigram_score = n_gram_similarity(s1_clean, s2_clean, 2)
    trigram_score = n_gram_similarity(s1_clean, s2_clean, 3)
    
    # 4. Character frequency similarity
    char_freq_score = character_frequency_similarity(s1, s2)
    
    # 5. Phonetic similarity
    phonetic_score = 0.0
    try:
        if soundex(s1_clean) == soundex(s2_clean):
            phonetic_score = 0.8
    except:
        pass
    
    # 6. SequenceMatcher (Python's built-in fuzzy matching)
    sequence_score = SequenceMatcher(None, s1_clean, s2_clean).ratio()
    
    # Combine all scores with weights
    scores = [
        (levenshtein_score, 0.25),    # Traditional edit distance
        (bigram_score, 0.20),         # Bigram similarity
        (trigram_score, 0.15),        # Trigram similarity  
        (char_freq_score, 0.15),      # Character frequency
        (phonetic_score, 0.10),       # Phonetic matching
        (sequence_score, 0.10),       # Python's fuzzy
        (pattern_score, 0.05)         # Pattern recognition bonus
    ]
    
    final_score = sum(score * weight for score, weight in scores)
    
    # Length bonus for similar length words
    length_diff = abs(len(s1_clean) - len(s2_clean))
    if length_diff <= 2:
        final_score += 0.05
    
    return max(0.0, min(1.0, final_score))

# Keep old function for backward compatibility
def fuzzy_similarity(s1, s2, max_distance=4):
    """
    Calculate fuzzy similarity between two strings
    Now using advanced fuzzy similarity
    """
    return advanced_fuzzy_similarity(s1, s2, max_distance)

def find_fuzzy_matches(query_word, content_words, threshold=0.5):
    """
    Find fuzzy matches for a query word in content words
    Returns list of matches with similarity scores
    Lowered threshold further for better typo tolerance with advanced algorithms
    """
    matches = []
    
    # Clean query word from special characters
    query_clean = ''.join(c.lower() for c in query_word if c.isalnum())
    
    # Skip very short words for fuzzy matching
    if len(query_clean) < 2:
        return matches
    
    for word in content_words:
        word_clean = ''.join(c.lower() for c in word if c.isalnum())
        
        if len(word_clean) < 2:
            continue
            
        similarity = advanced_fuzzy_similarity(query_clean, word_clean)
        if similarity >= threshold:
            matches.append({
                'word': word,
                'similarity': similarity,
                'original_query': query_word,
                'clean_query': query_clean,
                'clean_word': word_clean,
                'method': 'advanced_fuzzy'
            })
    
    return sorted(matches, key=lambda x: x['similarity'], reverse=True)

def enhanced_word_matching(query_words, content_words, fuzzy_threshold=0.5):
    """
    Enhanced word matching with advanced fuzzy support
    Returns match score and details
    Lowered threshold further for better typo coverage with advanced algorithms
    """
    exact_matches = 0
    fuzzy_matches = 0
    total_fuzzy_score = 0.0
    match_details = []
    
    for query_word in query_words:
        # Clean the query word
        query_clean = ''.join(c.lower() for c in query_word if c.isalnum())
        
        # First try exact match (including original and cleaned versions)
        exact_found = False
        for content_word in content_words:
            content_clean = ''.join(c.lower() for c in content_word if c.isalnum())
            if query_word.lower() == content_word.lower() or query_clean == content_clean:
                exact_matches += 1
                match_details.append({
                    'query_word': query_word,
                    'match_type': 'exact',
                    'matched_word': content_word,
                    'score': 1.0
                })
                exact_found = True
                break
        
        if not exact_found:
            # Try advanced fuzzy matching
            fuzzy_results = find_fuzzy_matches(query_word, content_words, fuzzy_threshold)
            if fuzzy_results:
                best_fuzzy = fuzzy_results[0]
                fuzzy_matches += 1
                total_fuzzy_score += best_fuzzy['similarity']
                match_details.append({
                    'query_word': query_word,
                    'match_type': 'advanced_fuzzy',
                    'matched_word': best_fuzzy['word'],
                    'score': best_fuzzy['similarity'],
                    'clean_query': best_fuzzy['clean_query'],
                    'clean_word': best_fuzzy['clean_word'],
                    'method': best_fuzzy.get('method', 'advanced_fuzzy')
                })
    
    # Calculate overall score
    total_words = len(query_words)
    if total_words == 0:
        return 0.0, []
    
    # Weight exact matches more than fuzzy matches
    exact_score = exact_matches / total_words
    fuzzy_score = (total_fuzzy_score / total_words) if fuzzy_matches > 0 else 0.0
      # Combined score: 90% exact + 80% fuzzy (increased fuzzy weight for advanced matching)
    combined_score = (exact_score * 0.9) + (fuzzy_score * 0.8)
    
    return combined_score, match_details

def jaccardSimilarity(a, b):
    if not a or not b:
        return 0.0
    set_a = set(a.split())
    set_b = set(b.split())
    intersection = set_a & set_b
    union = set_a | set_b
    if not union:
        return 0.0
    return len(intersection) / len(union)

def tfidf_similarity(query, documents):
    """Menghitung similarity menggunakan TF-IDF dan cosine similarity"""
    if not documents:
        return []
    
    # Combine query with documents for TF-IDF
    all_texts = [query] + documents
    
    try:
        vectorizer = TfidfVectorizer(stop_words=None, lowercase=True)
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Calculate cosine similarity between query and documents
        query_vector = tfidf_matrix[0:1]
        document_vectors = tfidf_matrix[1:]
        
        similarities = cosine_similarity(query_vector, document_vectors).flatten()
        return similarities
    except Exception as e:
        print(f"TF-IDF Error: {e}")
        return [0.0] * len(documents)

# Load data real dari CSV
_data_cache = None

def get_processed_data():
    """Get cached processed data"""
    global _data_cache
    if _data_cache is None:
        try:
            _data_cache = load_csv_data()
            print(f"Loaded {len(_data_cache)} data entries from CSV files")
        except Exception as e:
            print(f"Error loading data: {e}")
            _data_cache = []
    return _data_cache

# Fallback dummy intents untuk case tertentu
FALLBACK_INTENTS = [
    {"intent": "info_program_studi", "pattern": "jurusan", "answer": "ITB memiliki beberapa jurusan seperti Teknik Informatika, Arsitektur, Teknik Sipil, dan banyak lagi."},
    {"intent": "info_fakultas", "pattern": "fakultas", "answer": "ITB memiliki 12 fakultas dan sekolah, antara lain STEI, FTSL, SITH, FMIPA, dll."},
    {"intent": "info_itb", "pattern": "itb", "answer": "ITB (Institut Teknologi Bandung) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959."},
    {"intent": "info_itb", "pattern": "institut teknologi bandung", "answer": "ITB (Institut Teknologi Bandung) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959."},
]

def match_with_csv_data(user_query, threshold=0.3, top_k=3):
    """
    Match user query dengan data dari CSV menggunakan multiple algorithms
    Enhanced with fuzzy matching for typo tolerance
    """
    print(f"[MATCHING] Starting match for query: '{user_query}'")
    
    # Get processed data
    data_entries = get_processed_data()
    
    if not data_entries:
        print("[MATCHING] No data loaded, using fallback")
        return match_fallback_intents(user_query)
    
    user_query_lower = user_query.lower()
    candidates = []
      # 1. Preprocessing query
    try:
        from preprocessing import preprocess
        processed_query = preprocess(user_query)
        print(f"[MATCHING] Processed query: '{processed_query}'")
    except Exception as e:
        print(f"[MATCHING] Preprocessing error: {e}")
        processed_query = user_query_lower
    
    # Prepare query words for fuzzy matching - USE ORIGINAL WORDS FIRST
    original_query_words = [word for word in user_query_lower.split() if len(word) > 1]
    processed_query_words = [word for word in processed_query.split() if len(word) > 1]
    
    # 2. Enhanced matching strategies with fuzzy support
    for i, entry in enumerate(data_entries):
        content = entry['content']
        processed_content = entry.get('processed_content', content.lower())
        
        score = 0.0
        match_methods = []
        
        # Strategy 1: Exact substring matching (highest priority)
        if user_query_lower in content.lower():
            score += 1.0
            match_methods.append("substring")        # Strategy 2: Enhanced word matching with advanced fuzzy support
        # Use original query words for better fuzzy matching (before aggressive preprocessing)
        content_words = [word for word in content.lower().split() if len(word) > 1]
        
        # First try with original words for better typo tolerance
        fuzzy_score, fuzzy_details = enhanced_word_matching(original_query_words, content_words, fuzzy_threshold=0.5)
        
        if fuzzy_score > 0:
            score += fuzzy_score * 0.9  # Increased weight for fuzzy matching
            
            # Detailed logging for fuzzy matches
            fuzzy_types = [detail['match_type'] for detail in fuzzy_details]
            exact_count = fuzzy_types.count('exact')
            advanced_fuzzy_count = fuzzy_types.count('advanced_fuzzy')
            
            method_desc = f"enhanced_word(exact:{exact_count},fuzzy:{advanced_fuzzy_count},score:{fuzzy_score:.2f})"
            match_methods.append(method_desc)
            
            # Extra bonus for advanced fuzzy matches (typo tolerance)
            if advanced_fuzzy_count > 0:
                typo_bonus = advanced_fuzzy_count * 0.3  # Increased bonus for advanced typo handling
                score += typo_bonus
                
                fuzzy_match_info = []
                for detail in fuzzy_details:
                    if detail['match_type'] == 'advanced_fuzzy':
                        if 'clean_query' in detail and 'clean_word' in detail:
                            fuzzy_match_info.append(f"{detail['clean_query']}->{detail['clean_word']}")
                        else:
                            fuzzy_match_info.append(f"{detail['query_word']}->{detail['matched_word']}")
                
                print(f"[MATCHING] Found advanced fuzzy matches for '{user_query}': {fuzzy_match_info}")
                match_methods.append(f"advanced_typo_bonus({typo_bonus:.2f})")
        
        # Fallback: try processed words if original didn't work well
        elif len(processed_query_words) > 0:
            processed_content_words = [word for word in processed_content.split() if len(word) > 1]
            fallback_score, fallback_details = enhanced_word_matching(processed_query_words, processed_content_words, fuzzy_threshold=0.5)
            
            if fallback_score > 0:
                score += fallback_score * 0.7  # Lower weight for processed fallback
                match_methods.append(f"processed_fallback({fallback_score:.2f})")
        
        # Strategy 3: Jaccard similarity on processed text
        jaccard_score = jaccardSimilarity(processed_query, processed_content)
        if jaccard_score > threshold:
            score += jaccard_score * 0.5
            match_methods.append(f"jaccard({jaccard_score:.2f})")
        
        # Strategy 4: Basic word overlap (fallback)
        query_words_set = set(user_query_lower.split())
        content_words_set = set(content.lower().split())
        overlap = len(query_words_set & content_words_set)
        if overlap > 0:
            overlap_score = overlap / len(query_words_set)
            score += overlap_score * 0.3
            match_methods.append(f"overlap({overlap_score:.2f})")
          # Strategy 4: Advanced fuzzy matching as fallback
        # Try advanced fuzzy matching for any remaining unmatched words
        for query_word in original_query_words:
            fuzzy_matches = find_fuzzy_matches(query_word, content_words, threshold=0.5)
            if fuzzy_matches:
                best_match = fuzzy_matches[0]
                if best_match['similarity'] > 0.7:  # High similarity threshold for fallback
                    fallback_score = best_match['similarity'] * 0.4
                    score += fallback_score
                    match_methods.append(f"fallback_fuzzy({fallback_score:.2f})")
                    break  # Only one fallback bonus per entry
        
        if score > 0:
            candidates.append({
                'entry': entry,
                'score': score,
                'methods': match_methods
            })
    
    # Sort by score
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"[MATCHING] Found {len(candidates)} candidates")
    
    if candidates:
        best_match = candidates[0]
        print(f"[MATCHING] Best match: {best_match['entry']['content'][:100]}... (score: {best_match['score']:.2f}, methods: {best_match['methods']})")
        
        # Format response
        response = format_response(best_match['entry'], candidates[:top_k])
        return response
    
    # Fallback to simple intents
    print("[MATCHING] No good matches found, trying fallback")
    return match_fallback_intents(user_query)

def format_response(best_entry, all_candidates):
    """Format response dari data yang ditemukan"""
    
    # Enhance the main response  
    enhanced_content = enhance_response(best_entry, "")
    
    # If content is still too short, add info from other candidates
    if len(enhanced_content) < 80 and len(all_candidates) > 1:
        additional_info = []
        for candidate in all_candidates[1:3]:  # Take next 2 candidates
            additional_content = candidate['entry']['content']
            enhanced_additional = enhance_response(candidate['entry'], "")
            
            if enhanced_additional not in enhanced_content and len(enhanced_additional) > 20:
                additional_info.append(enhanced_additional)
        
        if additional_info:
            enhanced_content += " " + " ".join(additional_info)
    
    # Final cleanup
    enhanced_content = enhanced_content.strip()
    if not enhanced_content.endswith('.'):
        enhanced_content += '.'
    
    return enhanced_content

def enhance_response(entry, query):
    """Enhance response berdasarkan context dan source"""
    content = entry['content']
    source = entry.get('source', 'ITB')
    
    # Add context prefix based on source
    if source == 'tentangITB':
        if len(content) < 30:  # Short content, likely navigation item
            content = f"ITB menyediakan informasi tentang {content.lower()}. Untuk informasi lebih detail, Anda dapat mengunjungi website resmi ITB."
    elif source == 'wikipediaITB':
        if 'itb' not in content.lower() and 'institut teknologi bandung' not in content.lower():
            content = f"Menurut Wikipedia, {content}"
    elif source == 'multikampusITB':
        if len(content) < 30:
            content = f"ITB memiliki sistem multikampus dengan {content.lower()}. Informasi lebih lanjut tersedia di portal ITB."
    
    # Clean up and format
    content = content.strip()
    if not content.endswith('.'):
        content += '.'
    
    return content

def match_fallback_intents(user_text):
    """Fallback ke intent sederhana jika data CSV tidak cocok"""
    user_lower = user_text.lower()
    
    # 1. Simple substring match
    for item in FALLBACK_INTENTS:
        if item['pattern'] in user_lower:
            return item['answer']
    
    # 2. Jaccard similarity threshold
    for item in FALLBACK_INTENTS:
        if jaccardSimilarity(item['pattern'], user_lower) > 0.3:
            return item['answer']
    
    return None

def matchIntent(user_text):
    """Main matching function - entry point"""
    print(f"[MATCHING] matchIntent called with: '{user_text}'")
    
    # Try matching with CSV data first
    result = match_with_csv_data(user_text)
    
    if result:
        print(f"[MATCHING] Found match: {result[:100]}...")
        return result
    
    # Ultimate fallback
    print("[MATCHING] No matches found, returning default response")
    return "Maaf, saya tidak dapat menemukan informasi yang sesuai dengan pertanyaan Anda. Bisa Anda coba pertanyaan lain tentang ITB?"
