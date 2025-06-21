#!/usr/bin/env python3
"""
Direct test script to understand how the bot answers questions
by calling matching functions directly
"""
import sys
import os

# Add paths
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ml_path = os.path.join(root_path, 'machinelearning')
sys.path.insert(0, root_path)
sys.path.insert(0, ml_path)

def test_direct_matching():
    """Test direct matching to understand bot responses"""
    try:
        # Change to machinelearning directory to import modules
        os.chdir(ml_path)
        import matching
        
        test_questions = [
            "apa itu ITB?",
            "sejarah ITB", 
            "Institut Teknologi Bandung",
            "jurusan di ITB",
            "fakultas ITB"
        ]
        
        print("=" * 60)
        print("TESTING DIRECT MATCHING MECHANISM")
        print("=" * 60)
        
        for question in test_questions:
            print(f"\n🤖 Question: '{question}'")
            print("-" * 40)
            
            # Test matchIntent function
            result = matching.matchIntent(question)
            print(f"matchIntent Result: {result}")
            print()
            
            # Test match_with_csv_data function
            csv_result = matching.match_with_csv_data(question, threshold=0.3, top_k=1)
            print(f"CSV Match Result: {csv_result}")
            
    except Exception as e:
        print(f"Error in testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_matching()
