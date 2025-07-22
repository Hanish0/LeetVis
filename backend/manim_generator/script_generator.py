"""
Manim script generator that creates animation scripts for different video types.
"""

import re
from typing import Dict, Any, Optional
from .templates import ManimTemplates

class ManimScriptGenerator:
    """Main class for generating Manim animation scripts"""
    
    def __init__(self):
        self.templates = ManimTemplates()
    
    def generate_script(self, problem_data: Dict[str, Any], solution_code: str, 
                       language: str, video_type: str) -> str:
        """
        Generate a Manim script based on problem data and solution.
        
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
        
        # Extract key information from problem and solution
        problem_title = problem_data.get("title", "Unknown Problem")
        problem_content = problem_data.get("content", "")
        difficulty = problem_data.get("difficulty", "Unknown")
        
        # Parse solution code to extract key components
        code_components = self._parse_solution_code(solution_code, language)
        
        # Generate script based on video type
        if video_type == "explanation":
            return self.templates.generate_explanation_script(
                problem_title, problem_content, difficulty, code_components, language
            )
        elif video_type == "brute_force":
            return self.templates.generate_brute_force_script(
                problem_title, problem_content, code_components, language
            )
        elif video_type == "optimal":
            return self.templates.generate_optimal_script(
                problem_title, problem_content, code_components, language
            )
    
    def _parse_solution_code(self, solution_code: str, language: str) -> Dict[str, Any]:
        """
        Parse solution code to extract key components for animation.
        
        Args:
            solution_code: The solution code string
            language: Programming language
            
        Returns:
            Dictionary with parsed code components
        """
        components = {
            "main_function": "",
            "variables": [],
            "loops": [],
            "conditions": [],
            "return_statement": "",
            "time_complexity": "",
            "space_complexity": "",
            "raw_code": solution_code
        }
        
        if language == "python":
            components.update(self._parse_python_code(solution_code))
        elif language == "java":
            components.update(self._parse_java_code(solution_code))
        elif language == "cpp":
            components.update(self._parse_cpp_code(solution_code))
        
        return components
    
    def _parse_python_code(self, code: str) -> Dict[str, Any]:
        """Parse Python code to extract components"""
        components = {}
        
        # Extract function definition
        func_match = re.search(r'def\s+(\w+)\s*\([^)]*\):', code)
        if func_match:
            components["main_function"] = func_match.group(1)
        
        # Extract variable assignments
        var_matches = re.findall(r'(\w+)\s*=\s*([^=\n]+)', code)
        components["variables"] = [{"name": var, "value": val.strip()} for var, val in var_matches]
        
        # Extract loops
        loop_matches = re.findall(r'for\s+([^:]+):|while\s+([^:]+):', code)
        components["loops"] = [match[0] or match[1] for match in loop_matches]
        
        # Extract conditions
        if_matches = re.findall(r'if\s+([^:]+):', code)
        components["conditions"] = if_matches
        
        # Extract return statement
        return_match = re.search(r'return\s+([^\n]+)', code)
        if return_match:
            components["return_statement"] = return_match.group(1).strip()
        
        return components
    
    def _parse_java_code(self, code: str) -> Dict[str, Any]:
        """Parse Java code to extract components"""
        components = {}
        
        # Extract method definition
        method_match = re.search(r'public\s+\w+\s+(\w+)\s*\([^)]*\)', code)
        if method_match:
            components["main_function"] = method_match.group(1)
        
        # Extract variable declarations
        var_matches = re.findall(r'(\w+)\s+(\w+)\s*=\s*([^;]+);', code)
        components["variables"] = [{"name": var[1], "type": var[0], "value": var[2].strip()} 
                                 for var in var_matches]
        
        # Extract loops
        loop_matches = re.findall(r'for\s*\([^)]+\)|while\s*\([^)]+\)', code)
        components["loops"] = loop_matches
        
        # Extract conditions
        if_matches = re.findall(r'if\s*\([^)]+\)', code)
        components["conditions"] = if_matches
        
        # Extract return statement
        return_match = re.search(r'return\s+([^;]+);', code)
        if return_match:
            components["return_statement"] = return_match.group(1).strip()
        
        return components
    
    def _parse_cpp_code(self, code: str) -> Dict[str, Any]:
        """Parse C++ code to extract components"""
        components = {}
        
        # Extract function definition
        func_match = re.search(r'\w+\s+(\w+)\s*\([^)]*\)', code)
        if func_match:
            components["main_function"] = func_match.group(1)
        
        # Extract variable declarations
        var_matches = re.findall(r'(\w+)\s+(\w+)\s*=\s*([^;]+);', code)
        components["variables"] = [{"name": var[1], "type": var[0], "value": var[2].strip()} 
                                 for var in var_matches]
        
        # Extract loops
        loop_matches = re.findall(r'for\s*\([^)]+\)|while\s*\([^)]+\)', code)
        components["loops"] = loop_matches
        
        # Extract conditions
        if_matches = re.findall(r'if\s*\([^)]+\)', code)
        components["conditions"] = if_matches
        
        # Extract return statement
        return_match = re.search(r'return\s+([^;]+);', code)
        if return_match:
            components["return_statement"] = return_match.group(1).strip()
        
        return components