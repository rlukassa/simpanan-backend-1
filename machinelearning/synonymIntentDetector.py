"""
Enhanced intent detection dengan sinonim dan semantic matching
"""
import re
from typing import Dict, List, Tuple, Set

class SynonymBasedIntentDetector:
    def __init__(self):
        # Sinonim untuk kata-kata kunci
        self.synonyms = {
            'kepanjangan': ['kepanjangan', 'singkatan', 'arti', 'maksud', 'definisi', 'pengertian'],
            'berapa': ['berapa', 'jumlah', 'ada berapa', 'total', 'banyak'],
            'fakultas': ['fakultas', 'sekolah', 'jurusan', 'program studi', 'prodi'],
            'itb': ['itb', 'institut teknologi bandung', 'institut', 'teknologi bandung'],
            'sejarah': ['sejarah', 'asal usul', 'awal mula', 'riwayat', 'latar belakang'],
            'didirikan': ['didirikan', 'berdiri', 'dibentuk', 'dibangun', 'dimulai'],
            'lokasi': ['dimana', 'lokasi', 'alamat', 'tempat', 'berada'],
            'kampus': ['kampus', 'universitas', 'gedung', 'tempat kuliah']
        }
        
        # Intent mapping dengan konsep yang lebih fleksibel
        self.intent_concepts = {
            'kepanjangan_itb': {
                'required_concepts': [['kepanjangan', 'itb']],
                'alternative_concepts': [
                    ['kepanjangan', 'institut'],
                    ['arti', 'itb'],
                    ['definisi', 'itb']
                ]
            },
            'jumlah_fakultas': {
                'required_concepts': [['berapa', 'fakultas']],
                'alternative_concepts': [
                    ['jumlah', 'fakultas'],
                    ['fakultas', 'itb'],
                    ['berapa', 'sekolah']
                ]
            },
            'sejarah_itb': {
                'required_concepts': [['sejarah', 'itb']],
                'alternative_concepts': [
                    ['didirikan', 'itb'],
                    ['asal usul', 'itb'],
                    ['sejarah', 'institut']
                ]
            },
            'lokasi_itb': {
                'required_concepts': [['lokasi', 'itb']],
                'alternative_concepts': [
                    ['dimana', 'itb'],
                    ['alamat', 'itb'],
                    ['lokasi', 'kampus']
                ]
            },
            'info_umum_itb': {
                'required_concepts': [['itb']],
                'alternative_concepts': [
                    ['institut teknologi bandung'],
                    ['tentang', 'itb']
                ]
            }
        }
        
        # Predefined answers
        self.predefined_answers = {
            'kepanjangan_itb': "ITB adalah singkatan dari Institut Teknologi Bandung, yaitu perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959.",
            'jumlah_fakultas': "ITB memiliki 12 fakultas dan sekolah, antara lain FTMD (Fakultas Teknologi Mesin dan Dirgantara), FMIPA (Fakultas Matematika dan Ilmu Pengetahuan Alam), FTSL (Fakultas Teknik Sipil dan Lingkungan), FTTM (Fakultas Teknik Pertambangan dan Perminyakan), FTI (Fakultas Teknologi Industri), SAPPK (Sekolah Arsitektur, Perencanaan dan Pengembangan Kebijakan), SBM (Sekolah Bisnis dan Manajemen), SITH (Sekolah Ilmu dan Teknologi Hayati), STEI (Sekolah Teknik Elektro dan Informatika), SF (Sekolah Farmasi), dan FSRD (Fakultas Seni Rupa dan Desain).",
            'sejarah_itb': "ITB didirikan pada tanggal 2 Maret 1959 berdasarkan PP No. 6 Tahun 1959, berkembang dari Technische Hoogeschool te Bandoeng yang berdiri tahun 1920. ITB merupakan perguruan tinggi teknik pertama di Indonesia dan tempat Presiden Soekarno meraih gelar insinyur sipil.",
            'lokasi_itb': "ITB berlokasi di Jalan Ganesa No. 10, Bandung, Jawa Barat. ITB juga memiliki kampus lain di Cirebon (ITB Kampus Cirebon) dan Jakarta (untuk program tertentu).",
            'info_umum_itb': "Institut Teknologi Bandung (ITB) adalah perguruan tinggi teknik terkemuka di Indonesia yang didirikan pada tahun 1959, berlokasi di Bandung, Jawa Barat. ITB memiliki 12 fakultas dan sekolah dengan berbagai program studi teknik dan sains."
        }
    
    def expand_query_with_synonyms(self, query: str) -> Set[str]:
        """Expand query dengan sinonim"""
        words = set(query.lower().split())
        expanded_words = set(words)
        
        for word in words:
            for concept, synonyms in self.synonyms.items():
                if word in synonyms:
                    expanded_words.update(synonyms)
        
        return expanded_words
    
    def calculate_concept_match(self, query_words: Set[str], concept_words: List[str]) -> float:
        """Hitung seberapa cocok query dengan konsep"""
        concept_set = set()
        for word in concept_words:
            if word in self.synonyms:
                concept_set.update(self.synonyms[word])
            else:
                concept_set.add(word)
        
        matches = len(query_words.intersection(concept_set))
        return matches / len(concept_words) if concept_words else 0
    
    def detect_intent(self, query: str) -> Tuple[str, float]:
        """Detect intent menggunakan sinonim dan konsep matching"""
        query_words = self.expand_query_with_synonyms(query)
        
        best_intent = None
        best_score = 0.0
        
        for intent, concepts in self.intent_concepts.items():
            max_concept_score = 0.0
            
            # Check required concepts
            for concept_group in concepts['required_concepts']:
                score = self.calculate_concept_match(query_words, concept_group)
                max_concept_score = max(max_concept_score, score)
            
            # Check alternative concepts
            for concept_group in concepts.get('alternative_concepts', []):
                score = self.calculate_concept_match(query_words, concept_group)
                max_concept_score = max(max_concept_score, score * 0.8)  # Alternative concepts have lower weight
            
            if max_concept_score > best_score:
                best_intent = intent
                best_score = max_concept_score
        
        return best_intent, best_score
    
    def get_predefined_answer(self, intent: str) -> str:
        """Get predefined answer for detected intent"""
        return self.predefined_answers.get(intent, None)
    
    def add_synonym(self, concept: str, new_synonyms: List[str]):
        """Tambah sinonim baru untuk konsep tertentu"""
        if concept in self.synonyms:
            self.synonyms[concept].extend(new_synonyms)
        else:
            self.synonyms[concept] = new_synonyms
    
    def get_debug_info(self, query: str) -> Dict:
        """Get debug information untuk understanding"""
        query_words = self.expand_query_with_synonyms(query)
        intent, confidence = self.detect_intent(query)
        
        return {
            'original_query': query,
            'expanded_words': list(query_words),
            'detected_intent': intent,
            'confidence': confidence,
            'available_synonyms': {k: v for k, v in self.synonyms.items() if any(word in query_words for word in v)}
        }

# Factory function dengan backward compatibility
def get_intent_detector():
    return SynonymBasedIntentDetector()

def enhance_csv_response(content: str, intent: str = None) -> str:
    """Enhance CSV response based on detected intent"""
    
    # Clean up content
    content = content.strip()
    
    # Intent-specific enhancements
    if intent == 'jumlah_fakultas':
        # Look for faculty information
        if 'fakultas' in content.lower() or 'sekolah' in content.lower():
            if not re.search(r'\d+\s+fakultas', content.lower()):
                content = "ITB memiliki 12 fakultas dan sekolah. " + content
    
    elif intent == 'kepanjangan_itb':
        # Ensure ITB expansion is mentioned
        if 'institut teknologi bandung' not in content.lower():
            content = "ITB (Institut Teknologi Bandung) adalah " + content.lower()
    
    elif intent == 'sejarah_itb':
        # For history, keep the long content but add summary
        if len(content) > 200:
            summary = "ITB didirikan pada tahun 1959, berkembang dari TH Bandung yang berdiri tahun 1920. "
            content = summary + content
    
    # General cleanup
    if not content.endswith('.'):
        content += '.'
    
    return content
