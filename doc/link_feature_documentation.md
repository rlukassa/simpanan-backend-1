# Dokumentasi Fitur Link ITB di Chatbot

## Overview
Fitur ini menambahkan kemampuan chatbot untuk memberikan link ITB yang relevan setelah memberikan jawaban utama. Chatbot akan menampilkan 2 bubble chat:
1. **Bubble pertama**: Jawaban utama dari pertanyaan user
2. **Bubble kedua**: Link-link ITB yang relevan (jika ada)

## Implementasi

### Backend Changes

#### 1. NLP Intent Detector (`nlpIntentDetector.py`)
- **Method `loadDataset()`**: Memuat dataset CSV high quality untuk akses link
- **Method `findRelevantLinks()`**: Mencari link yang relevan berdasarkan intent dan query
- **Method `getAnswer()`**: Modified untuk return object dengan link
- **Method `getAnswerWithLinks()`**: Method utama yang menggabungkan jawaban + link

#### 2. Services (`services.py`)
- **Modified `detectIntentService()`**: 
  - Prioritas ke NLP detector dengan link
  - Fallback ke matching tradisional
  - Return structure yang konsisten dengan `hasLinks` flag

#### 3. Response Structure
```json
{
  "intent": "kepanjanganItb",
  "answer": "ITB adalah singkatan dari Institut Teknologi Bandung...",
  "source": "nlp_intent_detector",
  "confidence": 0.95,
  "hasLinks": true,
  "links": [
    {
      "content": "Institut Teknologi Bandung (ITB) sebagai Perguruan Tinggi...",
      "links": ["https://itb.ac.id/tentang-itb", "https://itb.ac.id/sejarah"],
      "category": "sejarah",
      "score": 1.8
    }
  ]
}
```

### Frontend Changes

#### 1. App Component (`App.jsx`)
- **Modified `handleSend()`**: 
  - Tambah bubble jawaban utama
  - Tambah bubble link terpisah jika ada link
  - Handle response structure baru

#### 2. Chatbox Component (`Chatbox.jsx`)
- **Link Message Type**: Handle `msg.type === 'links'`
- **Clickable Links**: Link yang bisa diklik dan buka di tab baru
- **Hover Effects**: Animasi hover pada link
- **Responsive Design**: Layout mobile-friendly

#### 3. Styling Features
```css
.links-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.itb-link {
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.2s ease;
}

.itb-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

## Dataset Integration

### Data Source
- **File**: `itb_chatbot_high_quality_20250621_190153.csv`
- **Columns**: `category`, `content`, `links`, `quality_score`
- **Path Detection**: Multiple fallback paths untuk cross-platform compatibility

### Link Filtering
1. **Category Mapping**: Intent → Dataset Categories
   - `kepanjanganItb` → `['sejarah', 'umum']`
   - `jumlahFakultas` → `['akademik', 'fakultas']`
   - `sejarahItb` → `['sejarah']`
   - `lokasiItb` → `['lokasi', 'fasilitas']`
   - `infoUmumItb` → `['sejarah', 'umum', 'akademik']`

2. **Scoring Algorithm**:
   - Word matching dengan query
   - Quality score bonus dari dataset
   - Top K results (default: 3)

3. **Link Validation**:
   - Filter links yang valid (starts with 'http')
   - Parse multiple links per entry
   - Maximum 2 links per item

## User Experience

### Interaction Flow
1. User mengetik pertanyaan
2. Chatbot memberikan jawaban utama
3. Jika ada link relevan, muncul bubble kedua dengan gradient biru
4. User bisa hover link untuk preview
5. Klik link untuk buka di tab baru

### Visual Design
- **Gradient Background**: Blue gradient untuk bubble link
- **Link Cards**: Semi-transparent cards dengan preview content
- **Hover Animation**: Lift effect saat hover
- **Mobile Responsive**: Stack links vertically di mobile

## Testing Examples

### Test Queries
```javascript
// Query yang akan dapat link
"Apa itu ITB?"
"Sejarah ITB"
"Fakultas di ITB"
"Lokasi ITB"

// Expected Response: 2 bubbles
// 1. Jawaban utama
// 2. Bubble link dengan gradient biru
```

### Error Handling
- Dataset tidak ditemukan → Fallback ke matching tradisional
- No links available → Hanya tampil bubble jawaban
- Invalid links → Filter otomatis
- Import error → Graceful degradation

## Performance Considerations

### Optimizations
1. **Lazy Loading**: Dataset dimuat sekali saat init
2. **Link Limit**: Maksimal 3 items, 2 links per item
3. **Content Preview**: Truncate content preview (100 chars)
4. **Caching**: NLP detector instance reused

### Monitoring
- Debug logs untuk dataset loading
- Response time tracking
- Link click analytics (future enhancement)

## Future Enhancements

### Planned Features
1. **Link Preview**: Show website preview on hover
2. **Link Analytics**: Track most clicked links
3. **Dynamic Dataset**: Real-time dataset updates
4. **Smart Filtering**: ML-based link relevance scoring
5. **Link Categories**: Grouped links by type (official, news, academic)

### Configuration Options
```javascript
// Future config
{
  maxLinksPerResponse: 3,
  maxLinksPerItem: 2,
  linkPreviewEnabled: true,
  analyticsEnabled: false,
  fallbackToTraditional: true
}
```

## Maintenance

### Dataset Updates
1. Update CSV file dengan link baru
2. Restart backend untuk reload dataset
3. Test link validity
4. Monitor response quality

### Code Maintenance
- Regular lint error checking
- Frontend styling consistency
- Backend error handling robustness
- Cross-browser compatibility testing
