"""
Advanced NLP-based Intent Detection untuk pemahaman bahasa manusia yang natural
"""
import re
import nltk
import pandas as pd
import os
from collections import Counter
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Set, Optional
import math

# Download required NLTK data (jalankan sekali)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass

class NaturalLanguageIntentDetector: # detector nlp buat intent recognition
    def __init__(self): # konstruktor detector
        # Load dataset untuk link references
        self.datasetLoaded = False # flag dataset udah dimuat
        self.datasetDf = None # dataframe dataset
        self.loadDataset() # muat dataset
        
        # Semantic word embeddings (simplified)
        self.semanticClusters = { # cluster kata semantik buat grouping
            'questionWords': { # kata tanya standar
                'what': ['apa', 'apakah', 'gimana', 'bagaimana', 'seperti apa', 'macam apa'], # kata what
                'where': ['dimana', 'di mana', 'lokasi', 'alamat', 'tempat', 'berada', 'terletak'], # kata where
                'when': ['kapan', 'tanggal', 'tahun', 'waktu', 'masa'], # kata when
                'howMany': ['berapa', 'jumlah', 'banyak', 'total', 'ada berapa'], # kata how many
                'why': ['kenapa', 'mengapa', 'alasan', 'sebab'], # kata why
                'who': ['siapa', 'who', 'tokoh'] # kata who
            },
            'entities': { # entitas utama dalam query
                'itb': ['itb', 'institut teknologi bandung', 'institute', 'teknologi bandung', 'institut'], # kata itb
                'faculty': ['fakultas', 'sekolah', 'jurusan', 'program studi', 'prodi', 'departemen'], # kata fakultas
                'history': ['sejarah', 'riwayat', 'asal usul', 'latar belakang', 'berdiri', 'didirikan', 'dibentuk'], # kata sejarah
                'meaning': ['arti', 'makna', 'definisi', 'pengertian', 'maksud', 'kepanjangan', 'singkatan'], # kata arti
                'location': ['lokasi', 'alamat', 'tempat', 'posisi', 'koordinat', 'letak'] # kata lokasi
            },
            'informalPatterns': { # pola bahasa gaul/informal
                'casualAsk': ['gimana', 'bagaimana', 'ceritain', 'jelasin', 'kasih tau', 'info'], # tanya casual
                'slang': ['apaan', 'apa sih', 'gimana sih', 'kayak gimana', 'kek gimana'], # slang indo
                'polite': ['tolong', 'mohon', 'bisa', 'minta', 'bantu'] # kata sopan
            }
        }        # Intent classification rules dengan semantic understanding
        self.intentRules = { # aturan klasifikasi intent
            'jumlahFakultas': { # intent jumlah fakultas
                'mustHave': ['faculty'], # harus ada kata fakultas
                'shouldHave': [['what', 'howMany'], ['itb']], # lebih baik ada kata tanya
                'keywords': ['berapa', 'jumlah', 'banyak', 'total', 'fakultas', 'sekolah', 'apa', 'saja'], # kata kunci
                'weight': 1.0 # bobot intent
            },
            'kepanjanganItb': { # intent kepanjangan itb
                'mustHave': ['itb'], # harus ada kata itb
                'shouldHave': [['meaning'], ['what']], # lebih baik ada kata arti
                'keywords': ['arti', 'kepanjangan', 'singkatan', 'definisi', 'maksud', 'apaan'], # kata kunci
                'weight': 1.0 # bobot intent
            },
            'lokasiItb': { # intent lokasi itb
                'mustHave': ['itb'], # harus ada kata itb
                'shouldHave': [['where', 'location']], # lebih baik ada kata lokasi
                'keywords': ['dimana', 'lokasi', 'alamat', 'tempat', 'berada'], # kata kunci
                'weight': 1.0 # bobot intent
            },
            'sejarahItb': { # intent sejarah itb
                'mustHave': ['itb'], # harus ada kata itb
                'shouldHave': [['history'], ['when']], # lebih baik ada kata sejarah
                'keywords': ['sejarah', 'riwayat', 'didirikan', 'berdiri', 'kapan', 'tahun', 'asal'], # kata kunci
                'weight': 1.0 # bobot intent
            },
            'infoUmumItb': { # intent info umum itb
                'mustHave': ['itb'], # harus ada kata itb
                'shouldHave': [], # tanpa syarat khusus
                'keywords': ['tentang', 'info', 'informasi', 'cerita', 'jelasin'], # kata kunci
                'weight': 0.7 # bobot lebih rendah
            }
        }        
        # Predefined answers
        self.answers = { # jawaban predefined buat intent
            'kepanjanganItb': "ITB adalah singkatan dari Institut Teknologi Bandung, yaitu perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959.", # jawaban kepanjangan
            'jumlahFakultas': "ITB memiliki 12 fakultas dan sekolah: FTMD, FMIPA, FTSL, FTTM, FTI, SAPPK, SBM, SITH, STEI, SF, FSRD, dan FIKTM.", # jawaban jumlah fakultas
            'sejarahItb': "ITB didirikan pada 2 Maret 1959 berdasarkan PP No. 6 Tahun 1959. ITB berkembang dari Technische Hoogeschool te Bandoeng (TH Bandung) yang berdiri tahun 1920. ITB merupakan perguruan tinggi teknik pertama di Indonesia dan tempat Presiden Soekarno meraih gelar insinyur sipil.", # jawaban sejarah            'lokasiItb': "ITB berlokasi di Jalan Ganesa No. 10, Bandung, Jawa Barat. ITB juga memiliki kampus lain di Cirebon dan Jakarta untuk program tertentu.", # jawaban lokasi
            'infoUmumItb': "Institut Teknologi Bandung (ITB) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan tahun 1959. ITB memiliki 12 fakultas dengan berbagai program studi teknik dan sains, berlokasi di Bandung, Jawa Barat." # jawaban info umum
        }
    
    def loadDataset(self): # muat dataset csv buat akses link
        """Load dataset CSV untuk mencari link yang relevan"""
        try:
            # coba muat high quality dataset dulu (dari working directory ML)
            possiblePaths = [ # list path yang mungkin
                'database/processed/itb_chatbot_high_quality_20250621_190153.csv',
                '../database/processed/itb_chatbot_high_quality_20250621_190153.csv',
                '../../database/processed/itb_chatbot_high_quality_20250621_190153.csv',
                os.path.join(os.path.dirname(__file__), 'database', 'processed', 'itb_chatbot_high_quality_20250621_190153.csv'),
                os.path.join(os.path.dirname(__file__), '..', 'database', 'processed', 'itb_chatbot_high_quality_20250621_190153.csv')
            ]
            
            for highQualityPath in possiblePaths: # coba setiap path
                if os.path.exists(highQualityPath): # kalau file ada
                    self.datasetDf = pd.read_csv(highQualityPath) # muat dataset
                    self.datasetLoaded = True # set flag loaded
                    print(f"Dataset loaded from {highQualityPath}: {len(self.datasetDf)} records") # konfirmasi loaded
                    return # keluar kalau berhasil
            
            # kalau tidak ada yang cocok, coba cari di direktori processed
            processedDirs = [ # list direktori processed yang mungkin
                'database/processed/',
                '../database/processed/',
                '../../database/processed/',
                os.path.join(os.path.dirname(__file__), 'database', 'processed'),
                os.path.join(os.path.dirname(__file__), '..', 'database', 'processed')
            ]
            
            for processedDir in processedDirs: # coba setiap direktori
                if os.path.exists(processedDir): # kalau direktori ada
                    csvFiles = [f for f in os.listdir(processedDir) if f.endswith('.csv') and 'high_quality' in f] # cari file high quality
                    if csvFiles: # kalau ada file
                        latestFile = sorted(csvFiles)[-1] # ambil file terbaru
                        filePath = os.path.join(processedDir, latestFile) # gabung path
                        self.datasetDf = pd.read_csv(filePath) # muat dataset
                        self.datasetLoaded = True # set flag loaded
                        print(f"Dataset loaded from {filePath}: {len(self.datasetDf)} records") # konfirmasi loaded
                        return # keluar kalau berhasil
            
            print("No high quality dataset found in any location") # tidak ada dataset
            self.datasetLoaded = False # set flag tidak loaded
            
        except Exception as e: # handle error
            print(f"Error loading dataset: {e}") # print error
            self.datasetLoaded = False # set flag tidak loaded
    
    def findRelevantLinks(self, intent: str, query: str, topK: int = 3) -> List[Dict[str, str]]: # cari link yang relevan
        """Cari link ITB yang relevan berdasarkan intent dan query"""
        if not self.datasetLoaded or self.datasetDf is None: # kalau dataset tidak loaded
            return [] # return kosong
        
        relevantLinks = [] # list link yang relevan
        
        try:
            # filter berdasarkan kategori yang sesuai dengan intent
            categoryMapping = { # mapping intent ke kategori
                'kepanjanganItb': ['sejarah', 'umum'], # kepanjangan -> sejarah/umum
                'jumlahFakultas': ['akademik', 'fakultas'], # fakultas -> akademik
                'sejarahItb': ['sejarah'], # sejarah -> sejarah  
                'lokasiItb': ['lokasi', 'fasilitas'], # lokasi -> lokasi/fasilitas
                'infoUmumItb': ['sejarah', 'umum', 'akademik'] # umum -> semua kategori
            }
            
            targetCategories = categoryMapping.get(intent, ['umum']) # ambil kategori target
            
            # filter dataset berdasarkan kategori
            filteredDf = self.datasetDf[self.datasetDf['category'].isin(targetCategories)] # filter by category
            
            # filter yang punya link (bukan kosong)
            filteredDf = filteredDf[filteredDf['links'].notna() & (filteredDf['links'] != '')] # filter yang ada link
            
            if len(filteredDf) == 0: # kalau tidak ada data
                return [] # return kosong
            
            # scoring berdasarkan relevansi dengan query
            queryWords = self.preprocessText(query).split() # split query jadi words
            
            scores = [] # list scores
            for idx, row in filteredDf.iterrows(): # loop setiap row
                score = 0.0 # skor awal
                content = str(row['content']).lower() # content lowercase
                
                # scoring berdasarkan kecocokan kata
                for word in queryWords: # loop setiap word di query
                    if word in content: # kalau word ada di content
                        score += 1.0 # tambah skor
                
                # bonus skor berdasarkan quality_score
                qualityScore = row.get('quality_score', 0) # ambil quality score
                score += qualityScore / 100.0  # normalize quality score
                
                scores.append((idx, score)) # tambah ke list scores
            
            # sort berdasarkan score tertinggi
            scores.sort(key=lambda x: x[1], reverse=True) # sort descending
            
            # ambil top K results
            for idx, score in scores[:topK]: # ambil top K
                row = filteredDf.loc[idx] # ambil row
                links = str(row['links']) # ambil links
                
                # parse multiple links (dipisah spasi atau koma)
                linkList = re.split(r'[,\s]+', links) # split links
                linkList = [link.strip() for link in linkList if link.strip() and link.startswith('http')] # filter valid links
                
                if linkList: # kalau ada valid links
                    relevantLinks.append({ # tambah ke result
                        'content': str(row['content'])[:100] + '...' if len(str(row['content'])) > 100 else str(row['content']), # content preview
                        'links': linkList[:2], # maksimal 2 link
                        'category': row['category'], # kategori
                        'score': score # skor relevansi
                    })
            
        except Exception as e: # handle error
            print(f"Error finding relevant links: {e}") # print error
        
        return relevantLinks # return hasil
    def preprocessText(self, text: str) -> str: # preprocessing text buat normalisasi
        """Advanced text preprocessing"""
        # Convert to lowercase
        text = text.lower().strip() # lowercase dan trim whitespace
        
        # Handle common typos and variations
        typoCorrections = { # koreksi typo umum
            'gimana': 'bagaimana', # gimana -> bagaimana
            'apaan': 'apa', # apaan -> apa
            'dimana': 'di mana', # dimana -> di mana
            'napa': 'apa', # napa -> apa
            'gmana': 'bagaimana' # gmana -> bagaimana
        }        
        for typo, correct in typoCorrections.items(): # loop koreksi typo
            text = re.sub(r'\b' + typo + r'\b', correct, text) # replace typo dengan benar
          # Remove extra whitespace and punctuation
        text = re.sub(r'[^\w\s]', ' ', text) # hapus punctuation
        text = re.sub(r'\s+', ' ', text) # normalize whitespace
        
        return text.strip() # return cleaned text
    def extractSemanticFeatures(self, text: str) -> Dict[str, List[str]]: # ekstrak fitur semantik dari text
        """Extract semantic features from text"""
        features = { # dict fitur yang ditemukan
            'questionWords': [], # kata tanya
            'entities': [], # entitas
            'informalPatterns': [], # pola informal
            'keywords': [] # kata kunci
        }
        
        words = text.split() # split jadi kata-kata
        
        # Find semantic matches with exact and fuzzy matching
        for category, clusters in self.semanticClusters.items(): # loop semua kategori
            for clusterName, wordList in clusters.items(): # loop cluster dalam kategori
                for word in wordList: # loop kata dalam cluster
                    # Exact match
                    if word in text: # kalo ada exact match
                        if clusterName not in features[category]: # belum ada di features
                            features[category].append(clusterName) # tambah ke features
                        if word not in features['keywords']: # belum ada di keywords
                            features['keywords'].append(word) # tambah ke keywords
                    # Fuzzy match for typos
                    else:
                        for textWord in words: # loop kata di text
                            similarity = self.calculateSimilarity(word, textWord) # hitung similarity
                            if similarity > 0.8:  # High similarity for feature extraction
                                if clusterName not in features[category]: # belum ada di features
                                    features[category].append(clusterName) # tambah ke features
                                if textWord not in features['keywords']: # belum ada di keywords
                                    features['keywords'].append(textWord) # tambah ke keywords
        
        return features # return semua fitur
    def calculateSimilarity(self, word1: str, word2: str) -> float: # hitung similarity antar kata
        """Calculate similarity between words"""
        return SequenceMatcher(None, word1, word2).ratio() # pake sequence matcher
    
    def fuzzyMatchConcepts(self, text: str, conceptWords: List[str]) -> float: # fuzzy matching konsep
        """Fuzzy matching untuk konsep"""
        maxSimilarity = 0.0 # similarity terbesar
        textWords = text.split() # split text jadi words        
        for conceptWord in conceptWords: # loop setiap concept word
            for textWord in textWords: # loop setiap text word
                similarity = self.calculateSimilarity(conceptWord, textWord) # hitung similarity
                if similarity > 0.7:  # Threshold untuk typo tolerance
                    maxSimilarity = max(maxSimilarity, similarity) # update max similarity
        
        return maxSimilarity # return similarity terbesar
    def detectIntentNlp(self, query: str) -> Tuple[str, float, Dict]: # deteksi intent pake nlp
        """Advanced NLP-based intent detection"""
        processedQuery = self.preprocessText(query) # preprocess query dulu
        features = self.extractSemanticFeatures(processedQuery) # ekstrak fitur semantik
        
        intentScores = {} # dict skor semua intent        
        for intent, rules in self.intentRules.items(): # loop semua intent dan rules
            score = 0.0 # skor intent ini
            matchedFeatures = [] # list fitur yang match
            
            # Check must_have requirements
            mustHaveScore = 0.0 # skor must have
            for mustConcept in rules['mustHave']: # loop must have concepts
                if mustConcept in features['entities']: # ada di entities
                    mustHaveScore += 1.0 # tambah skor
                    matchedFeatures.append(f"must_have:{mustConcept}") # tambah ke matched
                else:
                    # Fuzzy matching for must_have
                    conceptWords = self.semanticClusters['entities'].get(mustConcept, []) # ambil concept words
                    fuzzyScore = self.fuzzyMatchConcepts(processedQuery, conceptWords) # fuzzy match
                    if fuzzyScore > 0.7: # threshold fuzzy
                        mustHaveScore += fuzzyScore # tambah fuzzy score
                        matchedFeatures.append(f"fuzzy_must:{mustConcept}({fuzzyScore:.2f})") # tambah ke matched
            
            # Normalize must_have score
            if rules['mustHave']: # ada must have rules
                mustHaveScore = mustHaveScore / len(rules['mustHave']) # normalize
            else:
                mustHaveScore = 1.0  # No requirements            
            # Check should_have (optional but boosts score)
            shouldHaveScore = 0.0 # skor should have
            for shouldGroup in rules['shouldHave']: # loop should have groups
                groupScore = 0.0 # skor grup ini
                for shouldConcept in shouldGroup: # loop concept dalam grup
                    if shouldConcept in features['questionWords'] or shouldConcept in features['entities']: # ada di features
                        groupScore = 1.0 # set grup score
                        matchedFeatures.append(f"should_have:{shouldConcept}") # tambah ke matched
                        break # keluar dari loop
                    else:
                        # Fuzzy matching
                        allWords = [] # list semua words buat fuzzy match
                        if shouldConcept in self.semanticClusters['questionWords']: # ada di question words
                            allWords = self.semanticClusters['questionWords'][shouldConcept] # ambil words
                        elif shouldConcept in self.semanticClusters['entities']: # ada di entities
                            allWords = self.semanticClusters['entities'][shouldConcept] # ambil words
                        
                        fuzzyScore = self.fuzzyMatchConcepts(processedQuery, allWords) # fuzzy match
                        if fuzzyScore > 0.6: # threshold fuzzy
                            groupScore = fuzzyScore # set grup score
                            matchedFeatures.append(f"fuzzy_should:{shouldConcept}({fuzzyScore:.2f})") # tambah ke matched
                            break # keluar dari loop
                
                shouldHaveScore += groupScore # tambah grup score ke total
            
            # Normalize should_have score
            if rules['shouldHave']: # ada should have rules
                shouldHaveScore = shouldHaveScore / len(rules['shouldHave']) # normalize            
            # Keyword matching with fuzzy support
            keywordScore = 0.0 # skor keyword matching
            for keyword in rules['keywords']: # loop semua keywords
                if keyword in processedQuery: # exact match keyword
                    keywordScore += 1.0 # tambah skor
                    matchedFeatures.append(f"keyword:{keyword}") # tambah ke matched
                else:
                    # Fuzzy keyword matching
                    fuzzyScore = self.fuzzyMatchConcepts(processedQuery, [keyword]) # fuzzy match keyword
                    if fuzzyScore > 0.7: # threshold fuzzy keyword
                        keywordScore += fuzzyScore # tambah fuzzy score
                        matchedFeatures.append(f"fuzzy_keyword:{keyword}({fuzzyScore:.2f})") # tambah ke matched
            
            # Normalize keyword score
            if rules['keywords']: # ada keywords
                keywordScore = keywordScore / len(rules['keywords']) # normalize
            
            # Calculate final score
            finalScore = (mustHaveScore * 0.5) + (shouldHaveScore * 0.3) + (keywordScore * 0.2) # hitung final score
            finalScore *= rules['weight'] # kali dengan weight
            
            intentScores[intent] = { # simpan ke intent scores
                'score': finalScore, # skor akhir
                'matchedFeatures': matchedFeatures, # fitur yang match
                'breakdown': { # breakdown skor
                    'mustHave': mustHaveScore, # skor must have
                    'shouldHave': shouldHaveScore, # skor should have
                    'keyword': keywordScore # skor keyword
                }
            }        
        # Find best intent
        bestIntent = max(intentScores.keys(), key=lambda x: intentScores[x]['score']) # cari intent dengan skor tertinggi
        bestScore = intentScores[bestIntent]['score'] # ambil skor terbaik
        return bestIntent, bestScore, intentScores # return hasil deteksi
    
    def getAnswer(self, intent: str, query: str = "") -> Dict[str, any]: # ambil answer berdasarkan intent
        """Get answer for detected intent dengan link yang relevan"""
        baseAnswer = self.answers.get(intent, "Maaf, saya belum bisa menjawab pertanyaan tersebut.") # jawaban dasar
        
        # cari link yang relevan
        relevantLinks = self.findRelevantLinks(intent, query) if query else [] # cari link kalau ada query
        
        result = { # struktur result
            'answer': baseAnswer, # jawaban utama
            'links': relevantLinks, # link yang relevan
            'hasLinks': len(relevantLinks) > 0 # flag ada link atau tidak
        }
        
        return result # return hasil lengkap
    
    def analyzeQuery(self, query: str) -> Dict: # analisis query buat debugging
        """Comprehensive query analysis for debugging"""
        intent, confidence, allScores = self.detectIntentNlp(query) # deteksi intent
        features = self.extractSemanticFeatures(self.preprocessText(query)) # ekstrak fitur
        
        # ambil answer dengan link
        answerData = self.getAnswer(intent, query) if confidence > 0.3 else None # ambil answer data
        
        return { # return analisis lengkap
            'originalQuery': query, # query asli
            'processedQuery': self.preprocessText(query), # query yang diproses
            'extractedFeatures': features, # fitur yang diekstrak
            'detectedIntent': intent, # intent yang terdeteksi
            'confidence': confidence, # confidence score
            'allIntentScores': allScores, # semua skor intent
            'answerData': answerData # data jawaban dengan link
        }

    def getAnswerWithLinks(self, query: str) -> Dict[str, any]: # method utama buat dapetin jawaban dengan link
        """Method utama untuk mendapatkan jawaban dengan link yang relevan"""
        intent, confidence, _ = self.detectIntentNlp(query) # deteksi intent
        
        if confidence < 0.3: # kalau confidence rendah
            return { # return default response
                'answer': "Maaf, saya kurang memahami pertanyaan Anda. Bisa tolong diperjelas?", # jawaban default
                'links': [], # tidak ada link
                'hasLinks': False, # tidak ada link
                'confidence': confidence # confidence score
            }
        
        # ambil jawaban dengan link
        result = self.getAnswer(intent, query) # ambil jawaban lengkap
        result['confidence'] = confidence # tambah confidence
        result['intent'] = intent # tambah intent
        
        return result # return hasil lengkap

# Factory function
def getNlpIntentDetector(): # factory function buat detector
    return NaturalLanguageIntentDetector() # return instance detector
