#!/usr/bin/env python3
"""
Test chatbot dengan pertanyaan real user - Updated with LangChain recommendation
Menguji kemampuan sistem memahami variasi pertanyaan natural
"""

from backend.services.services import detectIntentService

def test_real_user_questions():
    """Test dengan pertanyaan yang diberikan user"""
    
    print("=" * 80)
    print("🧪 TESTING CHATBOT DENGAN PERTANYAAN REAL USER")
    print("=" * 80)
    print()
    
    # Pertanyaan yang diberikan user sebagai contoh
    user_questions = [
        {
            'question': 'Apa itu ITB',
            'context': 'Pertanyaan dasar (tanpa tanda tanya)',
            'expected_content': ['Institut Teknologi Bandung', 'sejarah', 'perguruan tinggi']
        },
        {
            'question': 'Kampus ITB dimana aja',
            'context': 'Pertanyaan lokasi (bahasa informal)',
            'expected_content': ['kampus', 'Ganesha', 'Jatinangor', 'Cirebon']
        },
        {
            'question': 'Fakultas ITB',
            'context': 'Pertanyaan singkat tentang fakultas',
            'expected_content': ['fakultas', 'program studi', 'sekolah']
        },
        {
            'question': 'ITB itu apa sih?',
            'context': 'Pertanyaan casual dengan kata tanya informal',
            'expected_content': ['Institut Teknologi Bandung']
        },
        {
            'question': 'berapa fakultas di ITB',
            'context': 'Pertanyaan jumlah fakultas',
            'expected_content': ['fakultas', 'sekolah']
        },
        {
            'question': 'ada berapa fakultas di ITB',
            'context': 'Pertanyaan jumlah fakultas (variasi)',
            'expected_content': ['fakultas', 'sekolah', 'administratif']
        }
    ]
    
    successful_answers = 0
    total_questions = len(user_questions)
    
    for i, test_case in enumerate(user_questions, 1):
        question = test_case['question']
        context = test_case['context']
        expected = test_case['expected_content']
        
        print(f"🔍 Test {i}: \"{question}\"")
        print(f"📝 Context: {context}")
        print("-" * 60)
        
        try:
            # Call chatbot service
            result = detectIntentService(question)
            
            # Check if answer is found
            if result['intent'] == 'found':
                answer = result['answer'].lower()
                content_found = any(exp.lower() in answer for exp in expected)
                
                print(f"✅ Status: {result['intent']}")
                print(f"🔧 Source: {result['source']}")
                print(f"📊 Content Match: {'✅ Yes' if content_found else '❌ No'}")
                print(f"💬 Answer: {result['answer'][:200]}...")
                
                if content_found:
                    successful_answers += 1
                    print("🎯 GOOD: Answer contains expected content")
                else:
                    print("⚠️  REVIEW: Answer may not be fully relevant")
                    
            else:
                print(f"❌ Status: {result['intent']}")
                print(f"💬 Fallback: {result['answer']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
        print("=" * 80)
        print()
    
    # Summary
    success_rate = (successful_answers / total_questions) * 100
    print(f"📊 SUMMARY:")
    print(f"✅ Successful answers: {successful_answers}/{total_questions}")
    print(f"📈 Success rate: {success_rate:.1f}%")
    print()
    
    if success_rate >= 80:
        print("🎉 EXCELLENT: Chatbot handles real user questions well!")
    elif success_rate >= 60:
        print("👍 GOOD: Chatbot handles most questions, some improvements needed")
        print()
        print("🚀 RECOMMENDATION: Consider LangChain Enhancement!")
        print("📋 Benefits:")
        print("   - Semantic search instead of keyword matching")
        print("   - Vector embeddings for better understanding") 
        print("   - RAG (Retrieval-Augmented Generation) for accurate responses")
        print("   - Expected improvement: Current → 85-90% success rate")
        print("📄 See: LANGCHAIN_ENHANCEMENT_PROPOSAL.md for details")
        print("🧪 Demo: python langchain_prototype.py")
    else:
        print("⚠️  NEEDS IMPROVEMENT: Consider enhancing matching algorithms")
        print()
        print("🚀 STRONG RECOMMENDATION: Implement LangChain Enhancement!")
        print("📋 Critical benefits for low performance:")
        print("   - Complete overhaul with semantic understanding")
        print("   - Vector similarity instead of basic text matching")
        print("   - LLM-powered response generation")
        print("   - Expected major improvement to 85-90% success rate")
        print("📄 See: LANGCHAIN_ENHANCEMENT_PROPOSAL.md for implementation plan")
    
    print("=" * 80)

if __name__ == "__main__":
    test_real_user_questions()
