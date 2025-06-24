# String Matching Module - 7 algoritma similarity terintegrasi
import os  # OS interface untuk file path
import sys  # System utilities
import re  # Regular expression
from sklearn.feature_extraction.text import TfidfVectorizer  # TF-IDF vectorizer
from sklearn.metrics.pairwise import cosine_similarity  # Cosine similarity
import numpy as np  # Numerical operations
from difflib import SequenceMatcher  # Python fuzzy matching

currentDir = os.path.dirname(os.path.abspath(__file__))  # Dapatkan direktori saat ini
sys.path.append(currentDir)  # Tambah ke Python path

from dataLoader import loadCsvData  # Import data loader

def levenshteinDistance(s1, s2):  # Hitung Levenshtein distance
    if len(s1) < len(s2):  # Pastikan s1 lebih panjang
        s1, s2 = s2, s1  # Tukar posisi
    
    if len(s2) == 0:  # Jika s2 kosong
        return len(s1)  # Return panjang s1
    
    previousRow = list(range(len(s2) + 1))  # Inisialisasi row pertama
    for i, c1 in enumerate(s1):  # Loop karakter s1
        currentRow = [i + 1]  # Inisialisasi row saat ini
        for j, c2 in enumerate(s2):  # Loop karakter s2
            insertions = previousRow[j + 1] + 1  # Cost insertion
            deletions = currentRow[j] + 1  # Cost deletion
            substitutions = previousRow[j] + (c1 != c2)  # Cost substitution
            currentRow.append(min(insertions, deletions, substitutions))  # Ambil cost minimum
        previousRow = currentRow  # Update previous row
    
    return previousRow[-1]  # Return distance

def soundex(word):  # Soundex algorithm untuk phonetic matching
    if not word:  # Cek word kosong
        return ""  # Return empty stringdef soundex(word):  # Soundex algorithm untuk phonetic matching
    if not word:  # Cek word kosong
        return ""  # Return empty string
    
    word = word.upper()  # Convert ke uppercase
    soundexMapping = {  # Mapping karakter ke angka
        'B': '1', 'F': '1', 'P': '1', 'V': '1',  # Grup 1
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',  # Grup 2
        'D': '3', 'T': '3',  # Grup 3
        'L': '4',  # Grup 4
        'M': '5', 'N': '5',  # Grup 5
        'R': '6'  # Grup 6
    }
    
    soundexCode = word[0]  # Simpan huruf pertama
    
    for char in word[1:]:  # Loop karakter setelah pertama
        if char in soundexMapping:  # Cek ada di mapping
            code = soundexMapping[char]  # Ambil code
            if not soundexCode.endswith(code):  # Hindari duplikat berturut
                soundexCode += code  # Tambah code
    
    soundexCode = (soundexCode + '000')[:4]  # Pad dengan 0, potong jadi 4 karakter
    return soundexCode  # Return soundex code

def nGramSimilarity(s1, s2, n=2):  # N-gram similarity untuk character matching
    if not s1 or not s2:  # Cek string kosong
        return 0.0  # Return 0 similarity
    
    s1 = s1.lower()  # Convert ke lowercase
    s2 = s2.lower()  # Convert ke lowercase
    
    def getNgrams(string, n):  # Generate n-grams dari string
        return set(string[i:i+n] for i in range(len(string) - n + 1))  # Set n-grams
    
    ngrams1 = getNgrams(s1, n)  # N-grams string 1
    ngrams2 = getNgrams(s2, n)  # N-grams string 2
    
    if not ngrams1 and not ngrams2:  # Kedua kosong
        return 1.0  # Perfect match
    if not ngrams1 or not ngrams2:  # Salah satu kosong
        return 0.0  # No match
    
    intersection = ngrams1 & ngrams2  # Irisan n-grams
    union = ngrams1 | ngrams2  # Gabungan n-grams
    
    return len(intersection) / len(union) if union else 0.0  # Jaccard similarity

def characterFrequencySimilarity(s1, s2): # compare character frequency distribution

    if not s1 or not s2: # cek string kosong
        return 0.0 # return 0
    
    s1Clean = ''.join(c.lower() for c in s1 if c.isalnum()) # clean s1
    s2Clean = ''.join(c.lower() for c in s2 if c.isalnum()) # clean s2
    
    if not s1Clean or not s2Clean: # cek clean string kosong
        return 0.0 # return 0
    
    # Count character frequencies
    freq1 = {} # frequency s1
    freq2 = {} # frequency s2
    
    for char in s1Clean: # loop char s1
        freq1[char] = freq1.get(char, 0) + 1 # count char
    
    for char in s2Clean: # loop char s2
        freq2[char] = freq2.get(char, 0) + 1 # count char
    
    # Calculate similarity based on frequency difference
    allChars = set(freq1.keys()) | set(freq2.keys()) # gabungan semua char
    totalDiff = 0 # total difference
    totalChars = len(s1Clean) + len(s2Clean) # total characters
    
    for char in allChars: # loop semua char
        diff = abs(freq1.get(char, 0) - freq2.get(char, 0)) # hitung difference
        totalDiff += diff # tambah total diff
    
    similarity = 1.0 - (totalDiff / totalChars) if totalChars > 0 else 0.0 # hitung similarity
    return max(0.0, similarity) # return similarity

def patternTypoRecognition(s1, s2): # recognize common typo patterns
    if not s1 or not s2: # cek string kosong
        return 0.0 # return 0
    
    s1Clean = ''.join(c.lower() for c in s1 if c.isalnum()) # clean s1
    s2Clean = ''.join(c.lower() for c in s2 if c.isalnum()) # clean s2
    
    if not s1Clean or not s2Clean: # cek clean string kosong
        return 0.0 # return 0
    
    # Remove repeated characters for comparison
    def removeRepeatedChars(s): # remove repeated chars
        result = "" # result string
        prevChar = "" # previous char
        for char in s: # loop chars
            if char != prevChar: # char berbeda dari sebelumnya
                result += char # tambah ke result
                prevChar = char # update previous
        return result # return result
    
    s1Norep = removeRepeatedChars(s1Clean) # s1 tanpa repeat
    s2Norep = removeRepeatedChars(s2Clean) # s2 tanpa repeat
    
    # Direct comparison after removing repetitions
    if s1Norep == s2Norep: # sama setelah remove repeat
        return 0.95  # High score for repeated char typos
    
    # Check if one is contained in the other (extra chars at start/end)
    if s1Norep in s2Norep or s2Norep in s1Norep: # salah satu contain yang lain
        shorterLen = min(len(s1Norep), len(s2Norep)) # panjang yang lebih pendek
        longerLen = max(len(s1Norep), len(s2Norep)) # panjang yang lebih panjang
        if shorterLen > 0: # ada panjang
            return shorterLen / longerLen * 0.9  # Good score for containment
    
    return 0.0 # no match

def advancedFuzzySimilarity(s1, s2, maxDistance=4): # enhanced fuzzy similarity gabung beberapa algoritma
    if not s1 or not s2: # cek string kosong
        return 0.0 # return 0
    
    # Normalize strings
    s1Clean = ''.join(c.lower() for c in s1 if c.isalnum()) # clean s1
    s2Clean = ''.join(c.lower() for c in s2 if c.isalnum()) # clean s2
    
    if not s1Clean or not s2Clean: # cek clean string kosong
        return 0.0 # return 0
    
    # 1. Pattern typo recognition (highest priority)
    patternScore = patternTypoRecognition(s1, s2) # pattern typo recognition
    if patternScore > 0.9: # high score
        return patternScore # return pattern score
    
    # 2. Traditional Levenshtein distance
    distance = levenshteinDistance(s1Clean, s2Clean)  # Hitung edit distance
    maxLen = max(len(s1Clean), len(s2Clean))  # Panjang maksimum
    
    # More lenient max distance for typo tolerance
    adaptiveMaxDistance = min(maxDistance, max(3, maxLen // 2))  # Adaptif threshold    
    if distance == 0:  # Jika sama persis
        return 1.0  # Perfect match
    
    levenshteinScore = 0.0  # Init score
    if distance <= adaptiveMaxDistance:  # Dalam threshold
        levenshteinScore = 1.0 - (distance / maxLen)  # Hitung score
    
    # 3. N-gram similarity (bigrams and trigrams)
    bigramScore = nGramSimilarity(s1Clean, s2Clean, 2)  # Bigram similarity
    trigramScore = nGramSimilarity(s1Clean, s2Clean, 3)  # Trigram similarity
    
    # 4. Character frequency similarity
    charFreqScore = characterFrequencySimilarity(s1, s2) # character frequency score
    
    # 5. Phonetic similarity
    phoneticScore = 0.0 # phonetic score
    try:
        if soundex(s1Clean) == soundex(s2Clean): # phonetic match
            phoneticScore = 0.8 # high phonetic score
    except:
        pass # skip error
    
    # 6. SequenceMatcher (Python's built-in fuzzy matching)
    sequenceScore = SequenceMatcher(None, s1Clean, s2Clean).ratio() # sequence matching
    
    # Combine all scores with weights
    scores = [ # combine scores dengan weights
        (levenshteinScore, 0.25),    # Traditional edit distance
        (bigramScore, 0.20),         # Bigram similarity
        (trigramScore, 0.15),        # Trigram similarity  
        (charFreqScore, 0.15),      # Character frequency
        (phoneticScore, 0.10),       # Phonetic matching
        (sequenceScore, 0.10),       # Python's fuzzy
        (patternScore, 0.05)         # Pattern recognition bonus
    ]
    
    finalScore = sum(score * weight for score, weight in scores) # final score
    
    # Length bonus for similar length words
    lengthDiff = abs(len(s1Clean) - len(s2Clean)) # length difference
    if lengthDiff <= 2: # similar length
        finalScore += 0.05 # bonus score
    
    return max(0.0, min(1.0, finalScore)) # return final score

# Keep old function for backward compatibility
def fuzzySimilarity(s1, s2, maxDistance=4): # hitung fuzzy similarity antara dua string
    """
    Calculate fuzzy similarity between two strings
    Now using advanced fuzzy similarity
    """
    return advancedFuzzySimilarity(s1, s2, maxDistance) # return advanced fuzzy similarity

def findFuzzyMatches(queryWord, contentWords, threshold=0.5): # cari fuzzy matches untuk query word
    matches = [] # list matches
    
    # Clean query word from special characters
    queryClean = ''.join(c.lower() for c in queryWord if c.isalnum()) # clean query word
    
    # Skip very short words for fuzzy matching
    if len(queryClean) < 2: # query terlalu pendek
        return matches # return empty matches
    
    for word in contentWords: # loop content words
        wordClean = ''.join(c.lower() for c in word if c.isalnum()) # clean word
        
        if len(wordClean) < 2: # word terlalu pendek
            continue # skip word
            
        similarity = advancedFuzzySimilarity(queryClean, wordClean) # hitung similarity
        if similarity >= threshold: # similarity cukup tinggi
            matches.append({ # tambah ke matches
                'word': word, # original word
                'similarity': similarity, # similarity score
                'original_query': queryWord, # original query
                'clean_query': queryClean, # clean query
                'clean_word': wordClean, # clean word
                'method': 'advanced_fuzzy' # method
            })
    
    return sorted(matches, key=lambda x: x['similarity'], reverse=True) # return sorted matches

def enhancedWordMatching(queryWords, contentWords, fuzzyThreshold=0.5): # enhanced word matching dengan advanced fuzzydef enhancedWordMatching(queryWords, contentWords, fuzzyThreshold=0.5): # enhanced word matching dengan advanced fuzzy
    exactMatches = 0 # exact matches count
    fuzzyMatches = 0 # fuzzy matches count
    totalFuzzyScore = 0.0 # total fuzzy score
    matchDetails = [] # match details list
    
    for queryWord in queryWords: # loop query words
        # Clean the query word
        queryClean = ''.join(c.lower() for c in queryWord if c.isalnum()) # clean query word
        
        # First try exact match (including original and cleaned versions)
        exactFound = False # exact match found flag
        for contentWord in contentWords: # loop content words
            contentClean = ''.join(c.lower() for c in contentWord if c.isalnum()) # clean content word
            if queryWord.lower() == contentWord.lower() or queryClean == contentClean: # exact match
                exactMatches += 1 # increment exact matches
                matchDetails.append({ # tambah match detail
                    'query_word': queryWord, # query word
                    'match_type': 'exact', # match type
                    'matched_word': contentWord, # matched word
                    'score': 1.0 # perfect score
                })
                exactFound = True # set exact found
                break # break loop
        
        if not exactFound: # no exact match found
            # Try advanced fuzzy matching
            fuzzyResults = findFuzzyMatches(queryWord, contentWords, fuzzyThreshold) # fuzzy matching
            if fuzzyResults: # ada fuzzy results
                bestFuzzy = fuzzyResults[0] # best fuzzy match
                fuzzyMatches += 1 # increment fuzzy matches
                totalFuzzyScore += bestFuzzy['similarity'] # tambah total fuzzy score
                matchDetails.append({ # tambah match detail
                    'query_word': queryWord, # query word
                    'match_type': 'advanced_fuzzy', # match type
                    'matched_word': bestFuzzy['word'], # matched word
                    'score': bestFuzzy['similarity'], # similarity score
                    'clean_query': bestFuzzy['clean_query'], # clean query
                    'clean_word': bestFuzzy['clean_word'], # clean word
                    'method': bestFuzzy.get('method', 'advanced_fuzzy') # method
                })
    
    # Calculate overall score
    totalWords = len(queryWords) # total words count
    if totalWords == 0: # no words
        return 0.0, [] # return 0 score
    
    # Weight exact matches more than fuzzy matches
    exactScore = exactMatches / totalWords # exact score
    fuzzyScore = (totalFuzzyScore / totalWords) if fuzzyMatches > 0 else 0.0 # fuzzy score
    # Combined score: 90% exact + 80% fuzzy (increased fuzzy weight for advanced matching)
    combinedScore = (exactScore * 0.9) + (fuzzyScore * 0.8) # combined score
    
    return combinedScore, matchDetails # return combined score dan details

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

def tfidfSimilarity(query, documents): # hitung similarity menggunakan TF-IDF dan cosine similarity
    """Menghitung similarity menggunakan TF-IDF dan cosine similarity"""
    if not documents: # no documents
        return [] # return empty list
    
    # Combine query with documents for TF-IDF
    allTexts = [query] + documents # combine all texts
    
    try:
        vectorizer = TfidfVectorizer(stop_words=None, lowercase=True) # TF-IDF vectorizer
        tfidfMatrix = vectorizer.fit_transform(allTexts) # transform texts
        
        # Calculate cosine similarity between query and documents
        queryVector = tfidfMatrix[0:1] # query vector
        documentVectors = tfidfMatrix[1:] # document vectors
        
        similarities = cosine_similarity(queryVector, documentVectors).flatten() # cosine similarity
        return similarities # return similarities
    except Exception as e:
        print(f"TF-IDF Error: {e}") # log error
        return [0.0] * len(documents) # return zeros

# Load data real dari CSV
_dataCache = None # cache data global

def getProcessedData(): # ambil cached processed data
    """Get cached processed data"""
    global _dataCache # pake global cache
    if _dataCache is None: # cache kosong
        try:
            _dataCache = loadCsvData()  # Load data dari CSV
            print(f"Loaded {len(_dataCache)} data entries from CSV files") # log jumlah data
        except Exception as e:
            print(f"Error loading data: {e}") # log error
            _dataCache = [] # set empty list
    return _dataCache # return cached data

# Fallback dummy intents untuk case tertentu
FALLBACK_INTENTS = [
    {"intent": "info_program_studi", "pattern": "jurusan", "answer": "ITB memiliki beberapa jurusan seperti Teknik Informatika, Arsitektur, Teknik Sipil, dan banyak lagi."},
    {"intent": "info_fakultas", "pattern": "fakultas", "answer": "ITB memiliki 12 fakultas dan sekolah, antara lain STEI, FTSL, SITH, FMIPA, dll."},
    {"intent": "info_itb", "pattern": "itb", "answer": "ITB (Institut Teknologi Bandung) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959."},
    {"intent": "info_itb", "pattern": "institut teknologi bandung", "answer": "ITB (Institut Teknologi Bandung) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959."},
]

def matchWithCsvData(userQuery, threshold=0.3, topK=3): # match user query dengan data CSV
    print(f"[MATCHING] Starting match for query: '{userQuery}'") # log start matching    
    # Get processed data
    dataEntries = getProcessedData() # ambil processed data    
    if not dataEntries: # data kosong
        print("[MATCHING] No data loaded, using fallback") # log fallback
        return matchFallbackIntents(userQuery) # return fallback match
    
    userQueryLower = userQuery.lower() # lowercase user query
    candidates = [] # list candidates
      # 1. Preprocessing query
    try:
        from preprocessing import preprocess # import preprocessing
        processedQuery = preprocess(userQuery) # preprocess query
        print(f"[MATCHING] Processed query: '{processedQuery}'") # log processed query
    except Exception as e:
        print(f"[MATCHING] Preprocessing error: {e}") # log error
        processedQuery = userQueryLower # fallback ke lowercase
    
    # Prepare query words for fuzzy matching - USE ORIGINAL WORDS FIRST
    originalQueryWords = [word for word in userQueryLower.split() if len(word) > 1] # original words
    processedQueryWords = [word for word in processedQuery.split() if len(word) > 1] # processed words
      # 2. Enhanced matching strategies with fuzzy support
    for i, entry in enumerate(dataEntries): # loop semua data entries
        content = entry['content'] # content entry
        processedContent = entry.get('processed_content', content.lower()) # processed content
        
        score = 0.0 # skor matching entry ini
        matchMethods = [] # list method yang dipakai
        
        # Strategy 1: Exact substring matching (highest priority)
        if userQueryLower in content.lower(): # exact substring match
            score += 1.0 # tambah score
            matchMethods.append("substring") # tambah method        # Strategy 2: Enhanced word matching with advanced fuzzy support
        # Use original query words for better fuzzy matching (before aggressive preprocessing)
        contentWords = [word for word in content.lower().split() if len(word) > 1] # content words
          # First try with original words for better typo tolerance
        fuzzyScore, fuzzyDetails = enhancedWordMatching(originalQueryWords, contentWords, fuzzyThreshold=0.5) # enhanced matching
        
        if fuzzyScore > 0: # ada fuzzy match
            score += fuzzyScore * 0.9  # Increased weight for fuzzy matching
            
            # Detailed logging for fuzzy matches
            fuzzyTypes = [detail['match_type'] for detail in fuzzyDetails] # ambil match types
            exactCount = fuzzyTypes.count('exact') # hitung exact matches
            advancedFuzzyCount = fuzzyTypes.count('advanced_fuzzy') # hitung advanced fuzzy
            
            methodDesc = f"enhanced_word(exact:{exactCount},fuzzy:{advancedFuzzyCount},score:{fuzzyScore:.2f})" # method description
            matchMethods.append(methodDesc) # tambah ke methods
            
            # Extra bonus for advanced fuzzy matches (typo tolerance)
            if advancedFuzzyCount > 0: # ada advanced fuzzy
                typoBonus = advancedFuzzyCount * 0.3  # Increased bonus for advanced typo handling
                score += typoBonus # tambah typo bonus
                
                fuzzyMatchInfo = [] # list fuzzy match info
                for detail in fuzzyDetails: # loop fuzzy details
                    if detail['match_type'] == 'advanced_fuzzy': # advanced fuzzy match
                        if 'clean_query' in detail and 'clean_word' in detail: # ada clean query dan word
                            fuzzyMatchInfo.append(f"{detail['clean_query']}->{detail['clean_word']}") # tambah info
                        else:
                            fuzzyMatchInfo.append(f"{detail['query_word']}->{detail['matched_word']}") # tambah info alternatif
                
                print(f"[MATCHING] Found advanced fuzzy matches for '{userQuery}': {fuzzyMatchInfo}") # log fuzzy matches
                matchMethods.append(f"advanced_typo_bonus({typoBonus:.2f})") # tambah method        
        # Fallback: try processed words if original didn't work well
        elif len(processedQueryWords) > 0: # ada processed query words
            processedContentWords = [word for word in processedContent.split() if len(word) > 1] # processed content words
            fallbackScore, fallbackDetails = enhancedWordMatching(processedQueryWords, processedContentWords, fuzzyThreshold=0.5) # fallback matching
            
            if fallbackScore > 0: # ada fallback score
                score += fallbackScore * 0.7  # Lower weight for processed fallback
                matchMethods.append(f"processed_fallback({fallbackScore:.2f})") # tambah method
        
        # Strategy 3: Jaccard similarity on processed text
        jaccardScore = jaccardSimilarity(processedQuery, processedContent) # jaccard similarity
        if jaccardScore > threshold: # di atas threshold
            score += jaccardScore * 0.5 # tambah score
            matchMethods.append(f"jaccard({jaccardScore:.2f})") # tambah method
        
        # Strategy 4: Basic word overlap (fallback)
        queryWordsSet = set(userQueryLower.split()) # set query words
        contentWordsSet = set(content.lower().split()) # set content words
        overlap = len(queryWordsSet & contentWordsSet) # hitung overlap
        if overlap > 0: # ada overlap
            overlapScore = overlap / len(queryWordsSet) # hitung overlap score
            score += overlapScore * 0.3 # tambah score
            matchMethods.append(f"overlap({overlapScore:.2f})") # tambah method
          # Strategy 4: Advanced fuzzy matching as fallback
        # Try advanced fuzzy matching for any remaining unmatched words
        for queryWord in originalQueryWords: # loop original query words
            fuzzyMatches = findFuzzyMatches(queryWord, contentWords, threshold=0.5) # fuzzy matches
            if fuzzyMatches: # ada fuzzy matches
                bestMatch = fuzzyMatches[0] # ambil best match
                if bestMatch['similarity'] > 0.7:  # High similarity threshold for fallback
                    fallbackScore = bestMatch['similarity'] * 0.4 # hitung fallback score
                    score += fallbackScore # tambah score
                    matchMethods.append(f"fallback_fuzzy({fallbackScore:.2f})") # tambah method
                    break  # Only one fallback bonus per entry
        
        if score > 0: # ada score
            candidates.append({ # tambah ke candidates
                'entry': entry, # entry data
                'score': score, # score matching
                'methods': matchMethods # methods yang dipakai
            })    
    # Sort by score
    candidates.sort(key=lambda x: x['score'], reverse=True) # sort candidates by score
    
    print(f"[MATCHING] Found {len(candidates)} candidates") # log jumlah candidates
    
    if candidates: # ada candidates
        bestMatch = candidates[0] # ambil best match
        print(f"[MATCHING] Best match: {bestMatch['entry']['content'][:100]}... (score: {bestMatch['score']:.2f}, methods: {bestMatch['methods']})") # log best match
          # Format response
        response = formatResponse(bestMatch['entry'], candidates[:topK]) # format response
        return response # return response
    
    # Fallback to simple intents
    print("[MATCHING] No good matches found, trying fallback") # log fallback
    return matchFallbackIntents(userQuery) # fallback ke simple intents

def formatResponse(bestEntry, allCandidates): # format response dari data yang ditemukan
    """Format response dari data yang ditemukan"""
    
    # Enhance the main response  
    enhancedContent = enhanceResponse(bestEntry, "") # enhance main response
    
    # If content is still too short, add info from other candidates
    if len(enhancedContent) < 80 and len(allCandidates) > 1: # content pendek dan ada candidates lain
        additionalInfo = [] # list additional info
        for candidate in allCandidates[1:3]:  # Take next 2 candidates
            additionalContent = candidate['entry']['content'] # additional content
            enhancedAdditional = enhanceResponse(candidate['entry'], "") # enhance additional
            
            if enhancedAdditional not in enhancedContent and len(enhancedAdditional) > 20: # valid additional
                additionalInfo.append(enhancedAdditional) # tambah additional info
        
        if additionalInfo: # ada additional info
            enhancedContent += " " + " ".join(additionalInfo) # gabung dengan enhanced content
    
    # Final cleanup
    enhancedContent = enhancedContent.strip() # strip whitespace
    if not enhancedContent.endswith('.'): # tidak diakhiri titik
        enhancedContent += '.' # tambah titik
    
    return enhancedContent # return enhanced content

def enhanceResponse(entry, query): # enhance response berdasarkan context dan source
    content = entry['content'] # content dari entry
    source = entry.get('source', 'ITB') # source entry
    
    # Add context prefix based on source
    if source == 'tentangITB': # source tentang ITB
        if len(content) < 30:  # Short content, likely navigation item
            content = f"ITB menyediakan informasi tentang {content.lower()}. Untuk informasi lebih detail, Anda dapat mengunjungi website resmi ITB." # enhance content
    elif source == 'wikipediaITB': # source wikipedia ITB
        if 'itb' not in content.lower() and 'institut teknologi bandung' not in content.lower(): # tidak ada mention ITB
            content = f"Menurut Wikipedia, {content}" # tambah prefix wikipedia
    elif source == 'multikampusITB': # source multikampus ITB
        if len(content) < 30: # content pendek
            content = f"ITB memiliki sistem multikampus dengan {content.lower()}. Informasi lebih lanjut tersedia di portal ITB." # enhance content
    
    # Clean up and format
    content = content.strip() # strip whitespace
    if not content.endswith('.'): # tidak diakhiri titik
        content += '.' # tambah titik
    
    return content # return enhanced content

def matchFallbackIntents(userText): # match ke fallback intents
    """Fallback ke intent sederhana jika data CSV tidak cocok"""
    userLower = userText.lower() # lowercase user text    
    # 1. Simple substring match
    for item in FALLBACK_INTENTS: # loop fallback intents
        if item['pattern'] in userLower: # pattern ada di user text
            return item['answer'] # return answer
    
    # 2. Jaccard similarity threshold
    for item in FALLBACK_INTENTS: # loop fallback intents lagi
        if jaccardSimilarity(item['pattern'], userLower) > 0.3: # jaccard similarity cukup
            return item['answer'] # return answer
    
    return None # ga ada match

def matchIntent(userText): # main matching function - entry point
    """Main matching function - entry point"""
    print(f"[MATCHING] matchIntent called with: '{userText}'") # log function call
    
    # Try matching with CSV data first
    result = matchWithCsvData(userText) # match dengan csv data
    
    if result: # ada result
        print(f"[MATCHING] Found match: {result[:100]}...") # log result
        return result # return result
    
    # Ultimate fallback
    print("[MATCHING] No matches found, returning default response") # log fallback
    return "Maaf, saya tidak dapat menemukan informasi yang sesuai dengan pertanyaan Anda. Bisa Anda coba pertanyaan lain tentang ITB?" # return default
