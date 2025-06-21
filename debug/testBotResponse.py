#!/usr/bin/env python3
"""
Test script to understand how the bot answers questions
"""
import sys
import os

# Add paths
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if root_path not in sys.path:
    sys.path.append(root_path)

backend_path = os.path.join(root_path, 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

def test_bot_responses():
    """Test how the bot responds to different types of questions"""
    try:
        # Direct import with full path
        services_path = os.path.join(root_path, 'backend', 'services')
        sys.path.insert(0, services_path)
        
        from backend import services
        detectIntentService = services.detectIntentService
        
        test_questions = [
            "apa itu ITB?",
            "sejarah ITB",
            "jurusan di ITB",
            "fakultas ITB",
            "tentang Institut Teknologi Bandung"
        ]
        
        print("=" * 60)
        print("TESTING BOT RESPONSE MECHANISM")
        print("=" * 60)
        
        for question in test_questions:
            print(f"\n🤖 Question: '{question}'")
            print("-" * 40)
            
            result = detectIntentService(question)
            
            print(f"Intent: {result.get('intent', 'N/A')}")
            print(f"Source: {result.get('source', 'N/A')}")
            print(f"Answer: {result.get('answer', 'N/A')}")
            
    except Exception as e:
        print(f"Error in testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_bot_responses()
