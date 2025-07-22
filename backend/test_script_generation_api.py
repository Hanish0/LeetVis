#!/usr/bin/env python3
"""
Test script for the Manim script generation API endpoint.
"""

import requests
import json

def test_script_generation_api():
    """Test the /api/generate-script endpoint"""
    
    # Test with local backend first, then deployed
    base_urls = [
        "http://localhost:8000",
        "https://leetcode-video-generator.onrender.com"
    ]
    
    test_requests = [
        {
            "problem_title": "Two Sum",
            "language": "python",
            "video_type": "explanation"
        },
        {
            "problem_title": "Two Sum", 
            "language": "java",
            "video_type": "brute_force"
        },
        {
            "problem_title": "Add Two Numbers",
            "language": "cpp",
            "video_type": "optimal"
        }
    ]
    
    working_url = None
    
    # Find a working backend
    for url in base_urls:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                working_url = url
                print(f"✅ Found working backend: {url}")
                break
        except:
            continue
    
    if not working_url:
        print("❌ No working backend found!")
        return
    
    print(f"\n🧪 Testing script generation API at {working_url}")
    print("=" * 60)
    
    for i, test_request in enumerate(test_requests, 1):
        print(f"\nTest {i}: {test_request['problem_title']} - {test_request['language']} - {test_request['video_type']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                f"{working_url}/api/generate-script",
                json=test_request,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                script_content = data.get("script_content", "")
                
                # Validate script content
                required_elements = [
                    "from manim import *",
                    "class",
                    "Scene",
                    "def construct(self):",
                    "Text(",
                    "self.play(",
                    "self.wait("
                ]
                
                missing_elements = [elem for elem in required_elements if elem not in script_content]
                
                if missing_elements:
                    print(f"❌ FAILED - Missing elements: {missing_elements}")
                else:
                    print(f"✅ SUCCESS")
                    print(f"   Script length: {len(script_content)} characters")
                    print(f"   Problem: {data.get('problem_title')}")
                    print(f"   Language: {data.get('language')}")
                    print(f"   Video type: {data.get('video_type')}")
                    
                    # Show first few lines of script
                    lines = script_content.split('\n')[:5]
                    print(f"   Script preview:")
                    for line in lines:
                        print(f"     {line}")
                    print("     ...")
                
            else:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                print(f"❌ FAILED - Status: {response.status_code}")
                print(f"   Error: {error_data}")
                
        except Exception as e:
            print(f"❌ ERROR - {str(e)}")
    
    print("\n" + "=" * 60)
    print("Script generation API test completed!")

if __name__ == "__main__":
    test_script_generation_api()