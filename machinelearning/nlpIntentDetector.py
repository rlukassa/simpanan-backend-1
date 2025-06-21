"""
Advanced NLP-based Intent Detection untuk pemahaman bahasa manusia yang natural
"""
import re
import nltk
from collections import Counter
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Set
import math

# Download required NLTK data (jalankan sekali)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass

class NaturalLanguageIntentDetector:
    def __init__(self):
        # Semantic word embeddings (simplified)
        self.semantic_clusters = {
            'question_words': {
                'what': ['apa', 'apakah', 'gimana', 'bagaimana', 'seperti apa', 'macam apa'],
                'where': ['dimana', 'di mana', 'lokasi', 'alamat', 'tempat', 'berada', 'terletak'],
                'when': ['kapan', 'tanggal', 'tahun', 'waktu', 'masa'],
                'how_many': ['berapa', 'jumlah', 'banyak', 'total', 'ada berapa'],
                'why': ['kenapa', 'mengapa', 'alasan', 'sebab'],
                'who': ['siapa', 'who', 'tokoh']
            },
            'entities': {
                'itb': ['itb', 'institut teknologi bandung', 'institute', 'teknologi bandung', 'institut'],
                'faculty': ['fakultas', 'sekolah', 'jurusan', 'program studi', 'prodi', 'departemen'],
                'history': ['sejarah', 'riwayat', 'asal usul', 'latar belakang', 'berdiri', 'didirikan', 'dibentuk'],
                'meaning': ['arti', 'makna', 'definisi', 'pengertian', 'maksud', 'kepanjangan', 'singkatan'],
                'location': ['lokasi', 'alamat', 'tempat', 'posisi', 'koordinat', 'letak']
            },
            'informal_patterns': {
                'casual_ask': ['gimana', 'bagaimana', 'ceritain', 'jelasin', 'kasih tau', 'info'],
                'slang': ['apaan', 'apa sih', 'gimana sih', 'kayak gimana', 'kek gimana'],
                'polite': ['tolong', 'mohon', 'bisa', 'minta', 'bantu']
            }
        }
          # Intent classification rules dengan semantic understanding
        self.intent_rules = {
            'jumlah_fakultas': {
                'must_have': ['faculty'],
                'should_have': [['what', 'how_many'], ['itb']],
                'keywords': ['berapa', 'jumlah', 'banyak', 'total', 'fakultas', 'sekolah', 'apa', 'saja'],
                'weight': 1.0
            },
            'kepanjangan_itb': {
                'must_have': ['itb'],
                'should_have': [['meaning'], ['what']],
                'keywords': ['arti', 'kepanjangan', 'singkatan', 'definisi', 'maksud', 'apaan'],
                'weight': 1.0
            },
            'lokasi_itb': {
                'must_have': ['itb'],
                'should_have': [['where', 'location']],
                'keywords': ['dimana', 'lokasi', 'alamat', 'tempat', 'berada'],
                'weight': 1.0
            },
            'sejarah_itb': {
                'must_have': ['itb'],
                'should_have': [['history'], ['when']],
                'keywords': ['sejarah', 'riwayat', 'didirikan', 'berdiri', 'kapan', 'tahun', 'asal'],
                'weight': 1.0
            },
            'info_umum_itb': {
                'must_have': ['itb'],
                'should_have': [],
                'keywords': ['tentang', 'info', 'informasi', 'cerita', 'jelasin'],
                'weight': 0.7
            }
        }
        
        # Predefined answers
        self.answers = {
            'kepanjangan_itb': "ITB adalah singkatan dari Institut Teknologi Bandung, yaitu perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959.",
            'jumlah_fakultas': "ITB memiliki 12 fakultas dan sekolah: FTMD, FMIPA, FTSL, FTTM, FTI, SAPPK, SBM, SITH, STEI, SF, FSRD, dan FIKTM.",
            'sejarah_itb': "ITB didirikan pada 2 Maret 1959 berdasarkan PP No. 6 Tahun 1959. ITB berkembang dari Technische Hoogeschool te Bandoeng (TH Bandung) yang berdiri tahun 1920. ITB merupakan perguruan tinggi teknik pertama di Indonesia dan tempat Presiden Soekarno meraih gelar insinyur sipil.",
            'lokasi_itb': "ITB berlokasi di Jalan Ganesa No. 10, Bandung, Jawa Barat. ITB juga memiliki kampus lain di Cirebon dan Jakarta untuk program tertentu.",
            'info_umum_itb': "Institut Teknologi Bandung (ITB) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan tahun 1959. ITB memiliki 12 fakultas dengan berbagai program studi teknik dan sains, berlokasi di Bandung, Jawa Barat."
        }
    
    def preprocess_text(self, text: str) -> str:
        """Advanced text preprocessing"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Handle common typos and variations
        typo_corrections = {
            'gimana': 'bagaimana',
            'apaan': 'apa',
            'dimana': 'di mana',
            'napa': 'apa',
            'gmana': 'bagaimana'
        }
        
        for typo, correct in typo_corrections.items():
            text = re.sub(r'\b' + typo + r'\b', correct, text)
          # Remove extra whitespace and punctuation
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_semantic_features(self, text: str) -> Dict[str, List[str]]:
        """Extract semantic features from text"""
        features = {
            'question_words': [],
            'entities': [],
            'informal_patterns': [],
            'keywords': []
        }
        
        words = text.split()
        
        # Find semantic matches with exact and fuzzy matching
        for category, clusters in self.semantic_clusters.items():
            for cluster_name, word_list in clusters.items():
                for word in word_list:
                    # Exact match
                    if word in text:
                        if cluster_name not in features[category]:
                            features[category].append(cluster_name)
                        if word not in features['keywords']:
                            features['keywords'].append(word)
                    # Fuzzy match for typos
                    else:
                        for text_word in words:
                            similarity = self.calculate_similarity(word, text_word)
                            if similarity > 0.8:  # High similarity for feature extraction
                                if cluster_name not in features[category]:
                                    features[category].append(cluster_name)
                                if text_word not in features['keywords']:
                                    features['keywords'].append(text_word)
        
        return features
    
    def calculate_similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity between words"""
        return SequenceMatcher(None, word1, word2).ratio()
    
    def fuzzy_match_concepts(self, text: str, concept_words: List[str]) -> float:
        """Fuzzy matching untuk konsep"""
        max_similarity = 0.0
        text_words = text.split()
        
        for concept_word in concept_words:
            for text_word in text_words:
                similarity = self.calculate_similarity(concept_word, text_word)
                if similarity > 0.7:  # Threshold untuk typo tolerance
                    max_similarity = max(max_similarity, similarity)
        
        return max_similarity
    
    def detect_intent_nlp(self, query: str) -> Tuple[str, float, Dict]:
        """Advanced NLP-based intent detection"""
        processed_query = self.preprocess_text(query)
        features = self.extract_semantic_features(processed_query)
        
        intent_scores = {}
        
        for intent, rules in self.intent_rules.items():
            score = 0.0
            matched_features = []
            
            # Check must_have requirements
            must_have_score = 0.0
            for must_concept in rules['must_have']:
                if must_concept in features['entities']:
                    must_have_score += 1.0
                    matched_features.append(f"must_have:{must_concept}")
                else:
                    # Fuzzy matching for must_have
                    concept_words = self.semantic_clusters['entities'].get(must_concept, [])
                    fuzzy_score = self.fuzzy_match_concepts(processed_query, concept_words)
                    if fuzzy_score > 0.7:
                        must_have_score += fuzzy_score
                        matched_features.append(f"fuzzy_must:{must_concept}({fuzzy_score:.2f})")
            
            # Normalize must_have score
            if rules['must_have']:
                must_have_score = must_have_score / len(rules['must_have'])
            else:
                must_have_score = 1.0  # No requirements
            
            # Check should_have (optional but boosts score)
            should_have_score = 0.0
            for should_group in rules['should_have']:
                group_score = 0.0
                for should_concept in should_group:
                    if should_concept in features['question_words'] or should_concept in features['entities']:
                        group_score = 1.0
                        matched_features.append(f"should_have:{should_concept}")
                        break
                    else:
                        # Fuzzy matching
                        all_words = []
                        if should_concept in self.semantic_clusters['question_words']:
                            all_words = self.semantic_clusters['question_words'][should_concept]
                        elif should_concept in self.semantic_clusters['entities']:
                            all_words = self.semantic_clusters['entities'][should_concept]
                        
                        fuzzy_score = self.fuzzy_match_concepts(processed_query, all_words)
                        if fuzzy_score > 0.6:
                            group_score = fuzzy_score
                            matched_features.append(f"fuzzy_should:{should_concept}({fuzzy_score:.2f})")
                            break
                
                should_have_score += group_score
            
            # Normalize should_have score
            if rules['should_have']:
                should_have_score = should_have_score / len(rules['should_have'])
            
            # Keyword matching with fuzzy support
            keyword_score = 0.0
            for keyword in rules['keywords']:
                if keyword in processed_query:
                    keyword_score += 1.0
                    matched_features.append(f"keyword:{keyword}")
                else:
                    # Fuzzy keyword matching
                    fuzzy_score = self.fuzzy_match_concepts(processed_query, [keyword])
                    if fuzzy_score > 0.7:
                        keyword_score += fuzzy_score
                        matched_features.append(f"fuzzy_keyword:{keyword}({fuzzy_score:.2f})")
            
            # Normalize keyword score
            if rules['keywords']:
                keyword_score = keyword_score / len(rules['keywords'])
            
            # Calculate final score
            final_score = (must_have_score * 0.5) + (should_have_score * 0.3) + (keyword_score * 0.2)
            final_score *= rules['weight']
            
            intent_scores[intent] = {
                'score': final_score,
                'matched_features': matched_features,
                'breakdown': {
                    'must_have': must_have_score,
                    'should_have': should_have_score,
                    'keyword': keyword_score
                }
            }
        
        # Find best intent
        best_intent = max(intent_scores.keys(), key=lambda x: intent_scores[x]['score'])
        best_score = intent_scores[best_intent]['score']
        
        return best_intent, best_score, intent_scores
    
    def get_answer(self, intent: str) -> str:
        """Get answer for detected intent"""
        return self.answers.get(intent, "Maaf, saya belum bisa menjawab pertanyaan tersebut.")
    
    def analyze_query(self, query: str) -> Dict:
        """Comprehensive query analysis for debugging"""
        intent, confidence, all_scores = self.detect_intent_nlp(query)
        features = self.extract_semantic_features(self.preprocess_text(query))
        
        return {
            'original_query': query,
            'processed_query': self.preprocess_text(query),
            'extracted_features': features,
            'detected_intent': intent,
            'confidence': confidence,
            'all_intent_scores': all_scores,
            'answer': self.get_answer(intent) if confidence > 0.3 else None
        }

# Factory function
def get_nlp_intent_detector():
    return NaturalLanguageIntentDetector()
