#!/usr/bin/env python3
"""
MASTER TEST RUNNER FOR ITB CHATBOT
==================================

Script utama untuk menjalankan semua test suite sekaligus:
1. Basic real questions test
2. Comprehensive test cases
3. Edge case robustness testing
4. Generate consolidated report

Author: ITB Chatbot Team
Date: 2025-01-21
"""

import os
import sys
import json
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from machinelearning.matching import matchIntent

class MasterTestRunner:
    def __init__(self):
        self.results = {
            "basic_test": None,
            "comprehensive_test": None,
            "edge_case_test": None
        }
        self.start_time = None
        self.end_time = None
        
    def run_basic_test(self):
        """Run basic real questions test"""
        print("🚀 RUNNING BASIC REAL QUESTIONS TEST")
        print("=" * 60)
        
        basic_questions = [
            {"question": "Apa itu ITB", "expected": ["ITB", "Institut", "Teknologi", "Bandung"]},
            {"question": "Kampus ITB dimana aja", "expected": ["Ganesha", "Jatinangor", "Cirebon"]},
            {"question": "Fakultas ITB", "expected": ["fakultas", "sekolah"]},
            {"question": "ITB itu apa sih?", "expected": ["ITB", "Institut"]},
            {"question": "berapa fakultas di ITB", "expected": ["fakultas", "jumlah"]},
            {"question": "ada berapa fakultas di ITB", "expected": ["fakultas", "jumlah"]}
        ]
        
        results = []
        for i, test in enumerate(basic_questions, 1):
            print(f"\n[{i}/{len(basic_questions)}] Testing: {test['question']}")
            try:
                answer = matchIntent(test['question'])
                is_relevant = any(keyword.lower() in answer.lower() for keyword in test['expected'])
                results.append({
                    "question": test['question'],
                    "answer": answer,
                    "expected": test['expected'],
                    "relevant": is_relevant,
                    "answer_length": len(answer)
                })
                print(f"✅ {'Relevant' if is_relevant else '❌ Not relevant'}")
            except Exception as e:
                results.append({
                    "question": test['question'],
                    "answer": "",
                    "expected": test['expected'],
                    "relevant": False,
                    "error": str(e)
                })
                print(f"❌ Error: {str(e)}")
        
        success_rate = sum(1 for r in results if r['relevant']) / len(results) * 100
        print(f"\n📊 Basic Test Success Rate: {success_rate:.1f}%")
        
        self.results["basic_test"] = {
            "success_rate": success_rate,
            "total_questions": len(results),
            "successful": sum(1 for r in results if r['relevant']),
            "details": results
        }
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite (simplified version)"""
        print("\n🚀 RUNNING COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        
        comprehensive_questions = [
            # Basic Info
            {"question": "Apa itu ITB?", "category": "basic", "difficulty": "easy"},
            {"question": "ITB didirikan kapan?", "category": "basic", "difficulty": "medium"},
            {"question": "Siapa rektor ITB sekarang?", "category": "basic", "difficulty": "hard"},
            
            # Academic
            {"question": "Fakultas apa saja yang ada di ITB?", "category": "academic", "difficulty": "medium"},
            {"question": "Berapa jumlah fakultas di ITB?", "category": "academic", "difficulty": "medium"},
            
            # Location
            {"question": "Kampus ITB ada dimana saja?", "category": "location", "difficulty": "easy"},
            {"question": "ITB Bandung alamatnya dimana?", "category": "location", "difficulty": "easy"},
            
            # History
            {"question": "Sejarah ITB singkat", "category": "history", "difficulty": "medium"},
            
            # Admission
            {"question": "Cara masuk ITB gimana?", "category": "admission", "difficulty": "medium"},
            
            # Language Variations
            {"question": "kampus itb dmn aja sih", "category": "informal", "difficulty": "medium"},
        ]
        
        results = []
        categories = {}
        
        for i, test in enumerate(comprehensive_questions, 1):
            print(f"\n[{i}/{len(comprehensive_questions)}] Testing: {test['question']}")
            print(f"Category: {test['category']}, Difficulty: {test['difficulty']}")
            
            try:
                answer = matchIntent(test['question'])
                is_relevant = "itb" in answer.lower() and len(answer) > 20
                
                # Calculate simple score
                score = 0
                if is_relevant:
                    score += 50
                    if len(answer) > 100:
                        score += 30
                    if any(word in answer.lower() for word in ["institut", "teknologi", "bandung"]):
                        score += 20
                
                results.append({
                    "question": test['question'],
                    "category": test['category'],
                    "difficulty": test['difficulty'],
                    "answer": answer,
                    "relevant": is_relevant,
                    "score": score
                })
                
                # Track by category
                if test['category'] not in categories:
                    categories[test['category']] = {"total": 0, "relevant": 0, "total_score": 0}
                categories[test['category']]["total"] += 1
                if is_relevant:
                    categories[test['category']]["relevant"] += 1
                categories[test['category']]["total_score"] += score
                
                print(f"Score: {score}/100, {'✅ Relevant' if is_relevant else '❌ Not relevant'}")
                
            except Exception as e:
                results.append({
                    "question": test['question'],
                    "category": test['category'],
                    "difficulty": test['difficulty'],
                    "answer": "",
                    "relevant": False,
                    "score": 0,
                    "error": str(e)
                })
                print(f"❌ Error: {str(e)}")
        
        # Calculate overall metrics
        total_questions = len(results)
        relevant_answers = sum(1 for r in results if r['relevant'])
        success_rate = relevant_answers / total_questions * 100
        avg_score = sum(r['score'] for r in results) / total_questions
        
        print(f"\n📊 Comprehensive Test Results:")
        print(f"   Success Rate: {success_rate:.1f}% ({relevant_answers}/{total_questions})")
        print(f"   Average Score: {avg_score:.1f}/100")
        
        print(f"\n📊 By Category:")
        for cat, stats in categories.items():
            cat_success = stats['relevant'] / stats['total'] * 100
            cat_avg_score = stats['total_score'] / stats['total']
            print(f"   {cat:12}: {cat_success:5.1f}% | Score: {cat_avg_score:5.1f}")
        
        self.results["comprehensive_test"] = {
            "success_rate": success_rate,
            "average_score": avg_score,
            "total_questions": total_questions,
            "relevant_answers": relevant_answers,
            "categories": categories,
            "details": results
        }
    
    def run_edge_case_test(self):
        """Run edge case test suite (simplified version)"""
        print("\n🚀 RUNNING EDGE CASE TEST SUITE")
        print("=" * 60)
        
        edge_cases = [
            # Ambiguous
            {"question": "ITB bagus gak?", "category": "subjective", "expected_behavior": "diplomatic"},
            {"question": "Ganesha", "category": "single_word", "expected_behavior": "context_aware"},
            {"question": "Berapa?", "category": "incomplete", "expected_behavior": "clarification"},
            
            # Typos
            {"question": "Apakah ITB puya fakultaas teknik?", "category": "typos", "expected_behavior": "tolerant"},
            {"question": "Kampuss ITB ada dimanna ya?", "category": "typos", "expected_behavior": "tolerant"},
            
            # Mixed Language
            {"question": "What is ITB dalam bahasa Inggris?", "category": "mixed_lang", "expected_behavior": "flexible"},
            {"question": "ITB faculty apa saja?", "category": "mixed_lang", "expected_behavior": "flexible"},
            
            # Complex Logic
            {"question": "Kalau saya lulusan IPA, bisa masuk fakultas apa saja di ITB?", "category": "conditional", "expected_behavior": "informative"},
            
            # Sensitive
            {"question": "Apakah ITB mahal untuk orang miskin?", "category": "sensitive", "expected_behavior": "diplomatic"},
            
            # Temporal
            {"question": "ITB tahun depan gimana?", "category": "temporal", "expected_behavior": "limitation_aware"},
        ]
        
        results = []
        categories = {}
        
        for i, test in enumerate(edge_cases, 1):
            print(f"\n[{i}/{len(edge_cases)}] Testing: {test['question']}")
            print(f"Category: {test['category']}, Expected: {test['expected_behavior']}")
            
            try:
                answer = matchIntent(test['question'])
                
                # Evaluate based on expected behavior
                handled_well = self._evaluate_edge_case(answer, test['expected_behavior'])
                
                results.append({
                    "question": test['question'],
                    "category": test['category'],
                    "expected_behavior": test['expected_behavior'],
                    "answer": answer,
                    "handled_well": handled_well,
                    "answer_length": len(answer)
                })
                
                # Track by category
                if test['category'] not in categories:
                    categories[test['category']] = {"total": 0, "handled_well": 0}
                categories[test['category']]["total"] += 1
                if handled_well:
                    categories[test['category']]["handled_well"] += 1
                
                print(f"{'✅ Handled well' if handled_well else '❌ Not handled well'}")
                
            except Exception as e:
                results.append({
                    "question": test['question'],
                    "category": test['category'],
                    "expected_behavior": test['expected_behavior'],
                    "answer": "",
                    "handled_well": False,
                    "error": str(e)
                })
                print(f"❌ Error: {str(e)}")
        
        # Calculate metrics
        total_cases = len(results)
        handled_well = sum(1 for r in results if r['handled_well'])
        robustness_rate = handled_well / total_cases * 100
        
        print(f"\n📊 Edge Case Test Results:")
        print(f"   Robustness Rate: {robustness_rate:.1f}% ({handled_well}/{total_cases})")
        
        print(f"\n📊 By Category:")
        for cat, stats in categories.items():
            cat_rate = stats['handled_well'] / stats['total'] * 100
            print(f"   {cat:12}: {cat_rate:5.1f}% ({stats['handled_well']}/{stats['total']})")
        
        self.results["edge_case_test"] = {
            "robustness_rate": robustness_rate,
            "total_cases": total_cases,
            "handled_well": handled_well,
            "categories": categories,
            "details": results
        }
    
    def _evaluate_edge_case(self, answer, expected_behavior):
        """Simple edge case evaluation"""
        if not answer or len(answer.strip()) == 0:
            return False
        
        answer_lower = answer.lower()
        
        if expected_behavior == "diplomatic":
            return "itb" in answer_lower and len(answer) > 50
        elif expected_behavior == "context_aware":
            return "ganesha" in answer_lower and "kampus" in answer_lower
        elif expected_behavior == "clarification":
            return any(word in answer_lower for word in ["maaf", "tidak", "bisa", "pertanyaan"])
        elif expected_behavior == "tolerant":
            return "itb" in answer_lower
        elif expected_behavior == "flexible":
            return "itb" in answer_lower and len(answer) > 30
        elif expected_behavior == "informative":
            return "fakultas" in answer_lower or "program" in answer_lower
        elif expected_behavior == "limitation_aware":
            return "itb" in answer_lower
        
        return "itb" in answer_lower
    
    def generate_consolidated_report(self):
        """Generate comprehensive report"""
        print("\n" + "="*80)
        print("📋 CONSOLIDATED TEST REPORT")
        print("="*80)
        
        # Overall Summary
        basic_rate = self.results["basic_test"]["success_rate"] if self.results["basic_test"] else 0
        comp_rate = self.results["comprehensive_test"]["success_rate"] if self.results["comprehensive_test"] else 0
        edge_rate = self.results["edge_case_test"]["robustness_rate"] if self.results["edge_case_test"] else 0
        
        overall_performance = (basic_rate + comp_rate + edge_rate) / 3
        
        print(f"\n🎯 OVERALL PERFORMANCE SUMMARY:")
        print(f"   Basic Questions: {basic_rate:.1f}%")
        print(f"   Comprehensive: {comp_rate:.1f}%")
        print(f"   Edge Cases: {edge_rate:.1f}%")
        print(f"   Overall Average: {overall_performance:.1f}%")
        
        # Performance Assessment
        if overall_performance >= 80:
            assessment = "✅ EXCELLENT"
        elif overall_performance >= 70:
            assessment = "👍 GOOD"
        elif overall_performance >= 60:
            assessment = "⚠️ FAIR"
        else:
            assessment = "❌ NEEDS IMPROVEMENT"
        
        print(f"\n🏆 SYSTEM ASSESSMENT: {assessment}")
        
        # Recommendations
        print(f"\n🎯 KEY RECOMMENDATIONS:")
        if edge_rate < 50:
            print("   🔧 Critical: Improve edge case handling and robustness")
        if comp_rate < 70:
            print("   📈 High: Enhance comprehensive question coverage")
        if basic_rate < 80:
            print("   ⚡ Medium: Strengthen basic question accuracy")
        
        print("   🚀 Strategic: Consider LangChain RAG implementation for 85-90% target")
        
        # Detailed breakdown
        if self.results["comprehensive_test"]:
            print(f"\n📊 COMPREHENSIVE TEST BREAKDOWN:")
            for cat, stats in self.results["comprehensive_test"]["categories"].items():
                rate = stats['relevant'] / stats['total'] * 100
                score = stats['total_score'] / stats['total']
                print(f"   {cat:12}: {rate:5.1f}% success | {score:5.1f} avg score")
        
        if self.results["edge_case_test"]:
            print(f"\n🛡️ EDGE CASE ROBUSTNESS:")
            for cat, stats in self.results["edge_case_test"]["categories"].items():
                rate = stats['handled_well'] / stats['total'] * 100
                print(f"   {cat:12}: {rate:5.1f}% handled well")
        
        # Save report
        self._save_consolidated_report(overall_performance)
        
        # Test duration
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            print(f"\n⏱️ Total Test Duration: {duration:.1f} seconds")
        
        print(f"\n{'='*80}")
        print("🎉 TESTING COMPLETED!")
        print("Check generated files for detailed results and recommendations.")
        print("="*80)
    
    def _save_consolidated_report(self, overall_performance):
        """Save consolidated report to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"master_test_report_{timestamp}.json"
        
        report_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "test_duration_seconds": (self.end_time - self.start_time) if self.start_time and self.end_time else None,
                "overall_performance": overall_performance
            },
            "summary": {
                "basic_test_success_rate": self.results["basic_test"]["success_rate"] if self.results["basic_test"] else None,
                "comprehensive_test_success_rate": self.results["comprehensive_test"]["success_rate"] if self.results["comprehensive_test"] else None,
                "edge_case_robustness_rate": self.results["edge_case_test"]["robustness_rate"] if self.results["edge_case_test"] else None,
                "overall_average": overall_performance
            },
            "detailed_results": self.results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Consolidated report saved to: {filename}")
    
    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 ITB CHATBOT MASTER TEST RUNNER")
        print("=" * 80)
        print("Running comprehensive test suite...")
        print("This will take several minutes...\n")
        
        self.start_time = time.time()
        
        try:
            # Run all test suites
            self.run_basic_test()
            self.run_comprehensive_test()
            self.run_edge_case_test()
            
            self.end_time = time.time()
            
            # Generate final report
            self.generate_consolidated_report()
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {str(e)}")
            print("Testing interrupted. Partial results may be available.")

def main():
    """Main function"""
    runner = MasterTestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main()
