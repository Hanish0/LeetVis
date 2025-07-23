"""
Groq Cloud API client for intelligent Manim script generation.
"""

import os
from groq import Groq
from typing import Dict, Any, Optional
import json

class GroqManimScriptClient:
    """Client for generating Manim scripts using Groq Cloud API"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama3-70b-8192"  # Fast model for script generation
    
    def generate_manim_script(self, problem_data: Dict[str, Any], solution_code: str, 
                             language: str, video_type: str) -> str:
        """
        Generate Manim script using Groq API.
        
        Args:
            problem_data: Dictionary containing problem information
            solution_code: Generated solution code
            language: Programming language (python, java, cpp)
            video_type: Type of video (explanation, brute_force, optimal)
            
        Returns:
            Generated Manim script as string
        """
        try:
            prompt = self._build_prompt(problem_data, solution_code, language, video_type)
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(video_type)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.3,  # Slightly higher for creative script generation
                max_tokens=4000,  # Longer scripts need more tokens
                top_p=0.9
            )
            
            raw_response = response.choices[0].message.content.strip()
            
            # Extract Python code from markdown if present
            return self._extract_python_code(raw_response)
            
        except Exception as e:
            print(f"Groq API error: {e}")
            raise Exception(f"Failed to generate Manim script using Groq API: {str(e)}")
    
    def _get_system_prompt(self, video_type: str) -> str:
        """Get system prompt based on video type"""
        base_prompt = """
You are an expert Manim animator and coding instructor.
Generate complete, working Manim scripts for LeetCode problem explanations.

Requirements:
- Create a complete Scene class that inherits from Scene
- Use proper Manim syntax and imports
- Include engaging animations and visual elements
- Make the content educational and easy to follow
- Use appropriate colors, timing, and transitions
- Ensure the script is syntactically correct and runnable
- Include proper wait times between animations
- Use Text, Code, VGroup, and other Manim objects effectively
- For problem explanations, always visually show what the problem is asking (use diagrams, step-by-step visuals, or clear breakdowns).
- For code explanations, always dry run the code and show how data structures change at each step, with a step-by-step walkthrough of the logic.

Important Manim Guidelines:
- Always import: from manim import *
- Scene class must inherit from Scene
- Use self.play() for animations
- Use self.wait() for pauses
- Use proper Manim colors (BLUE, RED, GREEN, YELLOW, etc.)
- Format code blocks using Code() object
- Use Text() for text elements
- Use VGroup() to group related elements
- Use proper positioning with next_to(), shift(), etc.
"""
        if video_type == "explanation":
            return base_prompt + """
Create an educational explanation video:
- Start with problem title and difficulty
- Explain the problem statement clearly and visually
- Break down the approach step by step with diagrams or animations
- Show the solution code with syntax highlighting
- Include complexity analysis
- Use visual examples and diagrams where helpful
- Make it beginner-friendly
"""
        elif video_type == "brute_force":
            return base_prompt + """
Create a brute force solution video:
- Emphasize the straightforward approach
- Show why brute force works but may be inefficient
- Visualize the brute force algorithm steps
- Highlight the time complexity issues
- Compare with optimal solutions
- Use animations to show all possible combinations being checked
- Dry run the code and show how data structures change at each step
"""
        elif video_type == "optimal":
            return base_prompt + """
Create an optimal solution video:
- Focus on the optimized approach
- Explain the key insights that lead to optimization
- Show before/after complexity comparison
- Use visual elements to demonstrate efficiency gains
- Highlight clever data structures or algorithms used
- Include performance analysis
- Dry run the code and show how data structures change at each step
"""
        return base_prompt
    
    def _build_prompt(self, problem_data: Dict[str, Any], solution_code: str, 
                     language: str, video_type: str) -> str:
        """Build the user prompt with problem and solution details"""
        
        # Clean and truncate content for the prompt
        problem_content = self._clean_content(problem_data.get('content', ''))
        problem_title = problem_data.get('title', 'Unknown Problem')
        difficulty = problem_data.get('difficulty', 'Unknown')
        
        # Truncate solution code if too long
        truncated_code = self._truncate_code(solution_code)
        
        prompt = f"""
Create a complete Manim script for this LeetCode problem:

Problem Title: {problem_title}
Difficulty: {difficulty}
Language: {language}
Video Type: {video_type}

Problem Description:
{problem_content[:800]}

Solution Code:
```{language}
{truncated_code}
```

Generate a complete Manim script that:
1. Creates an engaging video explanation
2. Uses proper Manim syntax and animations
3. Includes the problem title, difficulty, and description
4. Shows the solution code with syntax highlighting using Code() object
5. Explains the approach and complexity
6. Uses appropriate visual elements and timing
7. Has a clear structure with smooth transitions

CRITICAL Manim Code Guidelines:
- Use Code(code_string=code_string, language="{language}") for code blocks, NOT Code(filename)
- NEVER use font_size parameter with Code object - it will cause errors
- Valid Code parameters ONLY: code_string, language, background, formatter_style, tab_width, add_line_numbers
- Use Text() objects with proper font_size parameter
- Use VGroup() to group related elements
- Use proper positioning with next_to(), shift(), arrange()
- Use FadeOut() and FadeIn() for scene transitions
- Keep text readable with appropriate font sizes (20-40)

CORRECT Code usage:
```python
code_string = '''
def example():
    return "hello"
'''
code_obj = Code(code_string=code_string, language="python", background="window")
```

WRONG - DO NOT USE:
```python
# This will cause TypeError - NEVER use font_size with Code
code_obj = Code(code_string=code_string, language="python", font_size=18)
```

The script should be ready to run with: manim render script.py SceneClassName

Make sure to:
- Use proper Manim imports
- Create a Scene class with a descriptive name
- Include all necessary animations and text
- Use appropriate colors and formatting
- Add proper wait times between sections
- Make the content educational and engaging
- Use Code(code_string=code_string, language=language) format for displaying code
- Don't reference external files that don't exist

IMPORTANT: Return ONLY the complete Python script starting with 'from manim import *'. 
Do not include any markdown formatting, explanations, or additional text.
The response should be ready to save as a .py file and run directly.
"""
        
        return prompt
    
    def _clean_content(self, content: str) -> str:
        """Clean HTML content for prompt"""
        import re
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', content)
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean
    
    def _truncate_code(self, code: str, max_lines: int = 30) -> str:
        """Truncate code to reasonable length for prompt"""
        lines = code.split('\n')
        if len(lines) <= max_lines:
            return code
        
        truncated_lines = lines[:max_lines]
        truncated_lines.append("# ... (code truncated for brevity)")
        return '\n'.join(truncated_lines)
    
    def _extract_python_code(self, response: str) -> str:
        """Extract Python code from markdown or mixed response"""
        import re
        
        # Look for code blocks with python or no language specified
        code_block_patterns = [
            r'```python\n(.*?)```',
            r'```\n(.*?)```',
            r'```python(.*?)```'
        ]
        
        for pattern in code_block_patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # If no code blocks found, look for lines starting with 'from manim import'
        lines = response.split('\n')
        start_idx = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('from manim import'):
                start_idx = i
                break
        
        if start_idx >= 0:
            # Extract from 'from manim import' to the end
            code_lines = lines[start_idx:]
            return '\n'.join(code_lines).strip()
        
        # If still no code found, try to find class definition
        for i, line in enumerate(lines):
            if 'class' in line and 'Scene' in line:
                # Found a scene class, extract from here
                code_lines = ['from manim import *', ''] + lines[i:]
                return '\n'.join(code_lines).strip()
        
        # Clean up common prefixes and suffixes
        cleaned = response.strip()
        
        # Remove common prefixes
        prefixes_to_remove = [
            "Here is the complete Manim script:",
            "Here's the complete Manim script:",
            "The complete Manim script is:",
            "Here is the complete Manim script for the",
            "```python",
            "```"
        ]
        
        for prefix in prefixes_to_remove:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                break
        
        # Remove trailing markdown
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
        
        # If it still doesn't start with proper import, add it
        if not cleaned.startswith('from manim import'):
            if 'class' in cleaned and 'Scene' in cleaned:
                cleaned = 'from manim import *\n\n' + cleaned
        
        # Fix common Code object parameter issues
        cleaned = self._fix_code_object_parameters(cleaned)
        
        return cleaned
    
    def _fix_code_object_parameters(self, script_content: str) -> str:
        """Fix common Code object parameter issues"""
        import re
        
        # Remove font_size parameter from Code objects
        # Pattern: Code(..., font_size=..., ...)
        pattern = r'Code\(([^)]*?)font_size\s*=\s*[^,)]+,?\s*([^)]*?)\)'
        
        def fix_code_match(match):
            before = match.group(1)
            after = match.group(2)
            
            # Clean up any double commas
            params = (before + after).strip()
            if params.endswith(','):
                params = params[:-1]
            if params.startswith(','):
                params = params[1:]
            
            return f'Code({params})'
        
        # Apply the fix
        fixed_content = re.sub(pattern, fix_code_match, script_content)
        
        # Also fix any other invalid Code parameters that might cause issues
        # Remove any other invalid parameters like font, size, etc.
        invalid_params = ['font=', 'size=', 'font_color=', 'text_size=']
        for param in invalid_params:
            pattern = rf'Code\(([^)]*?){param}[^,)]+,?\s*([^)]*?)\)'
            fixed_content = re.sub(pattern, r'Code(\1\2)', fixed_content)
        
        return fixed_content