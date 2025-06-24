"""
Enhanced intent detection dengan sinonim dan semantic matching
"""
import re
from typing import Dict, List, Tuple, Set

class SynonymBasedIntentDetector: # detector intent berdasarkan sinonim
    def __init__(self): # konstruktor detector
        # Sinonim untuk kata-kata kunci
        self.synonyms = { # dict sinonim buat matching
            'kepanjangan': ['kepanjangan', 'singkatan', 'arti', 'maksud', 'definisi', 'pengertian'], # sinonim kepanjangan
            'berapa': ['berapa', 'jumlah', 'ada berapa', 'total', 'banyak'], # sinonim berapa
            'fakultas': ['fakultas', 'sekolah', 'jurusan', 'program studi', 'prodi'], # sinonim fakultas
            'itb': ['itb', 'institut teknologi bandung', 'institut', 'teknologi bandung'], # sinonim itb
            'sejarah': ['sejarah', 'asal usul', 'awal mula', 'riwayat', 'latar belakang'], # sinonim sejarah
            'didirikan': ['didirikan', 'berdiri', 'dibentuk', 'dibangun', 'dimulai'], # sinonim didirikan
            'lokasi': ['dimana', 'lokasi', 'alamat', 'tempat', 'berada'], # sinonim lokasi
            'kampus': ['kampus', 'universitas', 'gedung', 'tempat kuliah'] # sinonim kampus
        }        
        # Intent mapping dengan konsep yang lebih fleksibel
        self.intentConcepts = { # mapping intent ke konsep
            'kepanjanganItb': { # intent kepanjangan itb
                'requiredConcepts': [['kepanjangan', 'itb']], # konsep yang diperlukan
                'alternativeConcepts': [ # konsep alternatif
                    ['kepanjangan', 'institut'], # kepanjangan institut
                    ['arti', 'itb'], # arti itb
                    ['definisi', 'itb'] # definisi itb
                ]
            },
            'jumlahFakultas': { # intent jumlah fakultas
                'requiredConcepts': [['berapa', 'fakultas']], # konsep yang diperlukan
                'alternativeConcepts': [ # konsep alternatif
                    ['jumlah', 'fakultas'], # jumlah fakultas
                    ['fakultas', 'itb'], # fakultas itb
                    ['berapa', 'sekolah'] # berapa sekolah
                ]
            },
            'sejarahItb': { # intent sejarah itb
                'requiredConcepts': [['sejarah', 'itb']], # konsep yang diperlukan
                'alternativeConcepts': [ # konsep alternatif
                    ['didirikan', 'itb'], # didirikan itb
                    ['asal usul', 'itb'], # asal usul itb
                    ['sejarah', 'institut'] # sejarah institut
                ]
            },
            'lokasiItb': { # intent lokasi itb
                'requiredConcepts': [['lokasi', 'itb']], # konsep yang diperlukan
                'alternativeConcepts': [ # konsep alternatif
                    ['dimana', 'itb'], # dimana itb                    ['alamat', 'itb'], # alamat itb
                    ['lokasi', 'kampus'] # lokasi kampus
                ]
            },
            'infoUmumItb': { # intent info umum itb
                'requiredConcepts': [['itb']], # konsep yang diperlukan
                'alternativeConcepts': [ # konsep alternatif
                    ['institut teknologi bandung'], # institut teknologi bandung
                    ['tentang', 'itb'] # tentang itb
                ]
            }
        }        
        # Predefined answers
        self.predefinedAnswers = { # jawaban predefined buat intent
            'kepanjanganItb': "ITB adalah singkatan dari Institut Teknologi Bandung, yaitu perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959.", # jawaban kepanjangan
            'jumlahFakultas': "ITB memiliki 12 fakultas dan sekolah, antara lain FTMD (Fakultas Teknologi Mesin dan Dirgantara), FMIPA (Fakultas Matematika dan Ilmu Pengetahuan Alam), FTSL (Fakultas Teknik Sipil dan Lingkungan), FTTM (Fakultas Teknik Pertambangan dan Perminyakan), FTI (Fakultas Teknologi Industri), SAPPK (Sekolah Arsitektur, Perencanaan dan Pengembangan Kebijakan), SBM (Sekolah Bisnis dan Manajemen), SITH (Sekolah Ilmu dan Teknologi Hayati), STEI (Sekolah Teknik Elektro dan Informatika), SF (Sekolah Farmasi), dan FSRD (Fakultas Seni Rupa dan Desain).", # jawaban jumlah fakultas
            'sejarahItb': "ITB didirikan pada tanggal 2 Maret 1959 berdasarkan PP No. 6 Tahun 1959, berkembang dari Technische Hoogeschool te Bandoeng yang berdiri tahun 1920. ITB merupakan perguruan tinggi teknik pertama di Indonesia dan tempat Presiden Soekarno meraih gelar insinyur sipil.", # jawaban sejarah
            'lokasiItb': "ITB berlokasi di Jalan Ganesa No. 10, Bandung, Jawa Barat. ITB juga memiliki kampus lain di Cirebon (ITB Kampus Cirebon) dan Jakarta (untuk program tertentu).", # jawaban lokasi
            'infoUmumItb': "Institut Teknologi Bandung (ITB) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959, berlokasi di Bandung, Jawa Barat. ITB memiliki 12 fakultas dan sekolah dengan berbagai program studi teknik dan sains." # jawaban info umum
        }
    def expandQueryWithSynonyms(self, query: str) -> Set[str]: # expand query dengan sinonim
        """Expand query dengan sinonim"""
        words = set(query.lower().split()) # split query jadi kata-kata
        expandedWords = set(words) # copy ke expanded words
        
        for word in words: # loop setiap kata
            for concept, synonyms in self.synonyms.items(): # loop setiap konsep sinonim
                if word in synonyms: # kata ada di sinonim
                    expandedWords.update(synonyms) # tambah semua sinonim
        
        return expandedWords # return expanded words
    def calculateConceptMatch(self, queryWords: Set[str], conceptWords: List[str]) -> float: # hitung kecocokan konsep
        """Hitung seberapa cocok query dengan konsep"""
        conceptSet = set() # set konsep
        for word in conceptWords: # loop concept words
            if word in self.synonyms: # ada di sinonim
                conceptSet.update(self.synonyms[word]) # tambah sinonim
            else:
                conceptSet.add(word) # tambah kata asli
        
        matches = len(queryWords.intersection(conceptSet)) # hitung intersection
        return matches / len(conceptWords) if conceptWords else 0 # return ratio atau 0
    def detectIntent(self, query: str) -> Tuple[str, float]: # deteksi intent dari query
        """Detect intent menggunakan sinonim dan konsep matching"""
        queryWords = self.expandQueryWithSynonyms(query) # expand query dengan sinonim        
        bestIntent = None # intent terbaik
        bestScore = 0.0 # skor terbaik
        
        for intent, concepts in self.intentConcepts.items(): # loop semua intent
            maxConceptScore = 0.0 # skor konsep maksimal
            
            # Check required concepts
            for conceptGroup in concepts['requiredConcepts']: # loop required concepts
                score = self.calculateConceptMatch(queryWords, conceptGroup) # hitung match score
                maxConceptScore = max(maxConceptScore, score) # update max score
            
            # Check alternative concepts
            for conceptGroup in concepts.get('alternativeConcepts', []): # loop alternative concepts
                score = self.calculateConceptMatch(queryWords, conceptGroup) # hitung match score
                maxConceptScore = max(maxConceptScore, score * 0.8)  # Alternative concepts have lower weight
            
            if maxConceptScore > bestScore: # skor ini lebih baik
                bestIntent = intent # update best intent
                bestScore = maxConceptScore # update best score
        
        return bestIntent, bestScore # return hasil deteksi
    def getPredefinedAnswer(self, intent: str) -> str: # ambil predefined answer
        """Get predefined answer for detected intent"""
        return self.predefinedAnswers.get(intent, None) # return answer atau None
    
    def addSynonym(self, concept: str, newSynonyms: List[str]): # tambah sinonim baru
        """Tambah sinonim baru untuk konsep tertentu"""
        if concept in self.synonyms: # konsep sudah ada
            self.synonyms[concept].extend(newSynonyms) # extend sinonim yang ada
        else:
            self.synonyms[concept] = newSynonyms # buat entry baru
    
    def getDebugInfo(self, query: str) -> Dict: # ambil debug info
        """Get debug information untuk understanding"""
        queryWords = self.expandQueryWithSynonyms(query) # expand query
        intent, confidence = self.detectIntent(query) # deteksi intent
        
        return { # return debug info
            'originalQuery': query, # query asli
            'expandedWords': list(queryWords), # expanded words
            'detectedIntent': intent, # intent terdeteksi
            'confidence': confidence, # confidence score
            'availableSynonyms': {k: v for k, v in self.synonyms.items() if any(word in queryWords for word in v)} # sinonim yang tersedia
        }

# Factory function dengan backward compatibility
def getIntentDetector(): # factory function buat detector
    return SynonymBasedIntentDetector() # return instance detector

def enhanceCsvResponse(content: str, intent: str = None) -> str: # enhance CSV response berdasarkan intent
    """Enhance CSV response based on detected intent"""
    
    # Clean up content
    content = content.strip() # trim whitespace
    
    # Intent-specific enhancements
    if intent == 'jumlahFakultas': # intent jumlah fakultas
        # Look for faculty information
        if 'fakultas' in content.lower() or 'sekolah' in content.lower(): # ada kata fakultas/sekolah
            if not re.search(r'\d+\s+fakultas', content.lower()): # belum ada angka fakultas
                content = "ITB memiliki 12 fakultas dan sekolah. " + content # tambah info jumlah
    
    elif intent == 'kepanjanganItb': # intent kepanjangan itb
        # Ensure ITB expansion is mentioned
        if 'institut teknologi bandung' not in content.lower(): # belum ada kepanjangan
            content = "ITB (Institut Teknologi Bandung) adalah " + content.lower() # tambah kepanjangan
    
    elif intent == 'sejarahItb': # intent sejarah itb
        # For history, keep the long content but add summary
        if len(content) > 200: # content panjang
            summary = "ITB didirikan pada tahun 1959, berkembang dari TH Bandung yang berdiri tahun 1920. " # summary singkat
            content = summary + content # gabung summary dengan content
    
    # General cleanup
    if not content.endswith('.'): # belum ada titik
        content += '.' # tambah titik
    
    return content # return enhanced content
