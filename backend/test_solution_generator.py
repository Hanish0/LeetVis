"""
Test script for the solution generation system.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from solution_generator.generator import SolutionGenerator

def test_solution_generation():
    """Test the solution generation system"""
    
    print("🚀 Testing Solution Generation System")
    print("=" * 50)
    
    # Initialize the generator
    try:
        generator = SolutionGenerator()
        print("✅ Solution generator initialized successfully")
        print("✅ Using AI for all problem generation")
            
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        print("❌ AI client is required - no fallback templates available")
        return
    
    # Test cases
    test_cases = [
        {
            "title": "Two Sum",
            "difficulty": "Easy",
            "content": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "language": "python",
            "video_type": "optimal"
        },
        {
            "title": "Unknown Problem",
            "difficulty": "Medium", 
            "content": "This is a test problem that doesn't exist in our predefined solutions.",
            "language": "python",
            "video_type": "explanation"
        },
        {
            "title": "Two Sum",
            "difficulty": "Easy",
            "content": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "language": "java",
            "video_type": "brute_force"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['title']} ({test_case['language']}, {test_case['video_type']})")
        print("-" * 40)
        
        try:
            solution = generator.generate_solution(
                test_case,
                test_case['language'],
                test_case['video_type']
            )
            
            print("✅ Solution generated successfully!")
            print(f"📄 Solution preview (first 200 chars):")
            print(solution[:200] + "..." if len(solution) > 200 else solution)
            
        except Exception as e:
            print(f"❌ Failed to generate solution: {e}")
    
    print(f"\n🎉 Solution generation testing completed!")

if __name__ == "__main__":
    test_solution_generation()