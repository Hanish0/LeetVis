"""
Solution generator that creates code solutions for LeetCode problems using AI.
"""

import re
from typing import Dict, Any, Optional
from .groq_client import GroqSolutionClient

class SolutionGenerator:
    """Main class for generating solutions based on problem data using AI only"""
    
    def __init__(self):
        # Initialize Groq client - required for all problem generation
        self.groq_client = GroqSolutionClient()  # Will raise exception if fails
    
    def generate_solution(self, problem_data: Dict[str, Any], language: str, video_type: str) -> str:
        """
        Generate a solution using AI for any problem.
        
        Args:
            problem_data: Dictionary containing problem information
            language: Programming language (python, java, cpp)
            video_type: Type of solution (explanation, brute_force, optimal)
            
        Returns:
            Generated solution code as string
        """
        # Validate language support
        if language not in ["python", "java", "cpp"]:
            raise ValueError(f"Unsupported language: {language}")
        
        # Use AI to generate solution for all problems
        return self.groq_client.generate_solution(problem_data, language, video_type)
