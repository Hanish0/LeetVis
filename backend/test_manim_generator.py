#!/usr/bin/env python3
"""
Test script for Manim script generation functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from manim_generator.service import ManimVideoService

def test_script_generation():
    """Test the Manim script generation for different video types"""
    
    # Initialize the service
    manim_service = ManimVideoService()
    
    # Sample problem data
    problem_data = {
        "title": "Two Sum",
        "difficulty": "Easy",
        "content": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
    }
    
    # Sample solution code
    solution_code = """
def twoSum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hash_map:
            return [hash_map[complement], i]
        hash_map[num] = i
    return []
"""
    
    # Test different video types
    video_types = ["explanation", "brute_force", "optimal"]
    languages = ["python", "java", "cpp"]
    
    print("Testing Manim script generation...")
    print("=" * 50)
    
    for language in languages:
        for video_type in video_types:
            try:
                print(f"\nTesting {language} - {video_type}...")
                
                script = manim_service.generate_script_only(
                    problem_data, 
                    solution_code, 
                    language, 
                    video_type
                )
                
                # Check if script contains expected elements
                expected_elements = [
                    "from manim import *",
                    "class",
                    "Scene",
                    "def construct(self):",
                    "Text(",
                    "self.play(",
                    "self.wait("
                ]
                
                missing_elements = []
                for element in expected_elements:
                    if element not in script:
                        missing_elements.append(element)
                
                if missing_elements:
                    print(f"  ❌ FAILED - Missing elements: {missing_elements}")
                else:
                    print(f"  ✅ SUCCESS - Script generated successfully")
                    print(f"     Script length: {len(script)} characters")
                
            except Exception as e:
                print(f"  ❌ ERROR - {str(e)}")
    
    print("\n" + "=" * 50)
    print("Script generation test completed!")

def test_individual_components():
    """Test individual components of the script generator"""
    
    print("\nTesting individual components...")
    print("-" * 30)
    
    from manim_generator.script_generator import ManimScriptGenerator
    
    generator = ManimScriptGenerator()
    
    # Test code parsing
    test_code = """
def twoSum(nums, target):
    hash_map = {}
    for i, num in enumerate(nums):
        if target - num in hash_map:
            return [hash_map[target - num], i]
        hash_map[num] = i
    return []
"""
    
    try:
        components = generator._parse_solution_code(test_code, "python")
        print("✅ Code parsing successful")
        print(f"   Main function: {components.get('main_function', 'Not found')}")
        print(f"   Variables found: {len(components.get('variables', []))}")
        print(f"   Loops found: {len(components.get('loops', []))}")
        print(f"   Conditions found: {len(components.get('conditions', []))}")
        
    except Exception as e:
        print(f"❌ Code parsing failed: {str(e)}")
    
    # Test template methods
    from manim_generator.templates import ManimTemplates
    
    templates = ManimTemplates()
    
    try:
        # Test helper methods
        test_content = "<p>This is a <strong>test</strong> with HTML tags.</p>"
        cleaned = templates._clean_html_content(test_content)
        print(f"✅ HTML cleaning successful: '{cleaned}'")
        
        truncated = templates._truncate_text("This is a very long text that should be truncated", 20)
        print(f"✅ Text truncation successful: '{truncated}'")
        
    except Exception as e:
        print(f"❌ Template helper methods failed: {str(e)}")

if __name__ == "__main__":
    test_script_generation()
    test_individual_components()