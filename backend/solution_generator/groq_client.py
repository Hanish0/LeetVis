"""
Groq Cloud API client for intelligent solution generation.
"""

import os
from groq import Groq
from typing import Dict, Any, Optional
import json

class GroqSolutionClient:
    """Client for generating solutions using Groq Cloud API"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama3-70b-8192"  # Fast model for code generation
    
    def generate_solution(self, problem_data: Dict[str, Any], language: str, video_type: str) -> str:
        """
        Generate solution using Groq API for unknown problems.
        
        Args:
            problem_data: Parsed problem information
            language: Programming language (python, java, cpp)
            video_type: Type of solution (explanation, brute_force, optimal)
            
        Returns:
            Generated solution code
        """
        try:
            prompt = self._build_prompt(problem_data, language, video_type)
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(language, video_type)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.1,  # Low temperature for consistent code generation
                max_tokens=2000,
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Groq API error: {e}")
            # No fallback - raise the error
            raise Exception(f"Failed to generate solution using Groq API: {str(e)}")
    
    def _get_system_prompt(self, language: str, video_type: str) -> str:
        """Get system prompt based on language and video type"""
        
        base_prompt = f"""You are an expert competitive programmer and coding instructor. 
Generate clean, well-commented {language} code for LeetCode problems.

Requirements:
- Write production-quality code with proper error handling
- Include detailed comments explaining the approach
- Add time and space complexity analysis
- Include test cases and example usage
- Follow {language} best practices and conventions
"""
        
        if video_type == "explanation":
            return base_prompt + """
Focus on educational clarity:
- Step-by-step explanation in comments
- Break down the problem-solving approach
- Explain why this solution works
- Include multiple examples
"""
        elif video_type == "brute_force":
            return base_prompt + """
Implement a brute force solution:
- Straightforward, easy-to-understand approach
- May not be the most efficient
- Clearly explain the brute force logic
- Mention time complexity limitations
"""
        elif video_type == "optimal":
            return base_prompt + """
Implement the most efficient solution:
- Use optimal algorithms and data structures
- Minimize time and space complexity
- Explain optimization techniques used
- Compare with brute force approach
"""
        
        return base_prompt
    
    def _build_prompt(self, problem_data: Dict[str, Any], language: str, video_type: str) -> str:
        """Build the user prompt with problem details"""
        
        prompt = f"""
Problem Title: {problem_data.get('title', 'Unknown')}
Difficulty: {problem_data.get('difficulty', 'Unknown')}
Problem Type: {problem_data.get('problem_type', 'general')}

Problem Description:
{problem_data.get('content', 'No description available')[:1000]}

"""
        
        # Add constraints if available
        if problem_data.get('constraints'):
            prompt += f"\nConstraints:\n"
            for constraint in problem_data.get('constraints', [])[:3]:
                prompt += f"- {constraint}\n"
        
        # Add examples if available
        if problem_data.get('examples'):
            prompt += f"\nExamples:\n"
            for i, example in enumerate(problem_data.get('examples', [])[:2], 1):
                prompt += f"Example {i}:\n"
                if example.get('input'):
                    prompt += f"Input: {example['input']}\n"
                if example.get('output'):
                    prompt += f"Output: {example['output']}\n"
                if example.get('explanation'):
                    prompt += f"Explanation: {example['explanation']}\n"
                prompt += "\n"
        
        # Add algorithm hints if detected
        if problem_data.get('algorithms'):
            prompt += f"\nSuggested Algorithms: {', '.join(problem_data.get('algorithms', []))}\n"
        
        # Add data structure hints if detected
        if problem_data.get('data_structures'):
            prompt += f"Relevant Data Structures: {', '.join(problem_data.get('data_structures', []))}\n"
        
        prompt += f"""
Generate a complete {language} solution for the {video_type} approach.
Include:
1. Complete working code
2. Detailed comments
3. Time and space complexity analysis
4. Test cases
5. Example usage

Make sure the code is ready to run and follows best practices.
"""
        
        return prompt
    
