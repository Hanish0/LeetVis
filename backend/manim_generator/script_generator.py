"""
Manim script generator that creates animation scripts for different video types using Groq AI.
"""

import re
from typing import Dict, Any, Optional
from .groq_script_client import GroqManimScriptClient

class ManimScriptGenerator:
    """Main class for generating Manim animation scripts using AI"""
    
    def __init__(self):
        self.groq_client = GroqManimScriptClient()
    
    def generate_script(self, problem_data: Dict[str, Any], solution_code: str, 
                       language: str, video_type: str) -> str:
        """
        Generate a Manim script based on problem data and solution using Groq AI.
        
        Args:
            problem_data: Dictionary containing problem information
            solution_code: Generated solution code
            language: Programming language (python, java, cpp)
            video_type: Type of video (explanation, brute_force, optimal)
            
        Returns:
            Complete Manim script as string
        """
        # Validate inputs
        if language not in ["python", "java", "cpp"]:
            raise ValueError(f"Unsupported language: {language}")
        
        if video_type not in ["explanation", "brute_force", "optimal"]:
            raise ValueError(f"Unsupported video type: {video_type}")
        
        # Use Groq AI to generate the complete Manim script
        return self.groq_client.generate_manim_script(
            problem_data, solution_code, language, video_type
        )
