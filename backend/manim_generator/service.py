"""
Main service for Manim video generation that integrates script generation and rendering.
"""

from typing import Dict, Any, Optional
from .script_generator import ManimScriptGenerator
from .video_renderer import ManimVideoRenderer

class ManimVideoService:
    """Main service for generating Manim videos from problem data and solutions"""
    
    def __init__(self, output_dir: str = "videos"):
        self.script_generator = ManimScriptGenerator()
        self.video_renderer = ManimVideoRenderer(output_dir)
    
    def generate_video(self, problem_data: Dict[str, Any], solution_code: str, 
                      language: str, video_type: str, video_id: str) -> str:
        """
        Generate a complete video from problem data and solution.
        
        Args:
            problem_data: Dictionary containing problem information
            solution_code: Generated solution code
            language: Programming language (python, java, cpp)
            video_type: Type of video (explanation, brute_force, optimal)
            video_id: Unique identifier for the video
            
        Returns:
            Path to the generated video file
        """
        try:
            # Generate Manim script
            script_content = self.script_generator.generate_script(
                problem_data, solution_code, language, video_type
            )
            
            # Render video from script
            video_path = self.video_renderer.render_video(
                script_content, video_id
            )
            
            return video_path
            
        except Exception as e:
            raise RuntimeError(f"Video generation failed: {str(e)}")
    
    def generate_script_only(self, problem_data: Dict[str, Any], solution_code: str, 
                           language: str, video_type: str) -> str:
        """
        Generate only the Manim script without rendering.
        Useful for testing and debugging.
        
        Args:
            problem_data: Dictionary containing problem information
            solution_code: Generated solution code
            language: Programming language (python, java, cpp)
            video_type: Type of video (explanation, brute_force, optimal)
            
        Returns:
            Generated Manim script as string
        """
        return self.script_generator.generate_script(
            problem_data, solution_code, language, video_type
        )
    
    def cleanup(self):
        """Clean up temporary files"""
        self.video_renderer.cleanup_temp_files()