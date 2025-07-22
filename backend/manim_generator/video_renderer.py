"""
Video renderer that takes Manim scripts and generates video files.
"""

import os
import subprocess
import tempfile
from typing import Dict, Any, Optional
import uuid

class ManimVideoRenderer:
    """Handles rendering of Manim scripts to video files"""
    
    def __init__(self, output_dir: str = "videos"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def render_video(self, script_content: str, video_id: str) -> str:
        """
        Render a Manim script to a video file.
        
        Args:
            script_content: The complete Manim script as string
            video_id: Unique identifier for the video
            
        Returns:
            Path to the generated video file
        """
        # Create temporary script file
        script_filename = f"temp_script_{uuid.uuid4().hex}.py"
        script_path = os.path.join(tempfile.gettempdir(), script_filename)
        
        try:
            # Write script to temporary file
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Determine scene class name from script
            scene_class = self._extract_scene_class(script_content)
            if not scene_class:
                raise ValueError("Could not find scene class in script")
            
            # Output video path
            video_filename = f"{video_id}.mp4"
            video_path = os.path.join(self.output_dir, video_filename)
            
            # Check if video already exists
            if os.path.exists(video_path):
                return video_path
            
            # Check if manim is available
            try:
                subprocess.run(["manim", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise RuntimeError("Manim is not installed or not available in PATH")
            
            # Create temporary media directory for this render
            temp_media_dir = os.path.join(tempfile.gettempdir(), f"manim_media_{uuid.uuid4().hex}")
            os.makedirs(temp_media_dir, exist_ok=True)
            
            # Manim render command with better error handling
            cmd = [
                "manim",
                "render",
                script_path,
                scene_class,
                "-q", "m",  # medium quality
                "--output_file", video_filename,
                "--media_dir", temp_media_dir,
                "--disable_caching",  # Disable caching to avoid issues
                "--format", "mp4"
            ]
            
            # Run Manim rendering
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Unknown error"
                raise RuntimeError(f"Manim rendering failed: {error_msg}")
            
            # Find the actual output file (Manim creates subdirectories)
            actual_video_path = self._find_rendered_video_in_dir(temp_media_dir, video_filename)
            if actual_video_path and os.path.exists(actual_video_path):
                # Move to expected location
                import shutil
                shutil.move(actual_video_path, video_path)
                
                # Clean up temporary media directory
                try:
                    shutil.rmtree(temp_media_dir)
                except:
                    pass  # Ignore cleanup errors
                
                return video_path
            else:
                # List what files were actually created for debugging
                created_files = []
                if os.path.exists(temp_media_dir):
                    for root, dirs, files in os.walk(temp_media_dir):
                        for file in files:
                            if file.endswith('.mp4'):
                                created_files.append(os.path.join(root, file))
                
                error_msg = f"Rendered video file not found. Created files: {created_files}"
                raise RuntimeError(error_msg)
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Video rendering timed out (5 minutes)")
        except Exception as e:
            raise RuntimeError(f"Video rendering failed: {str(e)}")
        finally:
            # Clean up temporary script file
            if os.path.exists(script_path):
                try:
                    os.remove(script_path)
                except:
                    pass  # Ignore cleanup errors
    
    def _extract_scene_class(self, script_content: str) -> Optional[str]:
        """Extract the scene class name from the script"""
        import re
        
        # Look for class that inherits from Scene
        match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\):', script_content)
        if match:
            return match.group(1)
        return None
    
    def _find_rendered_video(self, video_id: str) -> Optional[str]:
        """Find the actual rendered video file in Manim's output structure"""
        # Manim typically creates videos in media/videos/temp_script_*/quality/
        media_dir = os.path.join(self.output_dir, "videos")
        
        if not os.path.exists(media_dir):
            return None
        
        # Search for the video file
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                if file.endswith('.mp4') and video_id in file:
                    return os.path.join(root, file)
        
        return None
    
    def _find_rendered_video_alternative(self, video_filename: str) -> Optional[str]:
        """Find the actual rendered video file in Manim's output structure"""
        # Manim typically creates videos in media/videos/temp_script_*/quality/
        media_dir = os.path.join(self.output_dir, "videos")
        
        if not os.path.exists(media_dir):
            return None
        
        # Search for the video file
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                if file.endswith('.mp4') and video_filename in file:
                    return os.path.join(root, file)
        
        return None
    
    def _find_rendered_video_in_dir(self, media_dir: str, video_filename: str) -> Optional[str]:
        """Find the actual rendered video file in a specific media directory"""
        if not os.path.exists(media_dir):
            return None
        
        # Search for the video file
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                if file.endswith('.mp4'):
                    # Return the first MP4 file found (should be our video)
                    return os.path.join(root, file)
        
        return None
    
    def cleanup_temp_files(self):
        """Clean up temporary Manim files"""
        media_dir = os.path.join(self.output_dir, "videos")
        if os.path.exists(media_dir):
            import shutil
            shutil.rmtree(media_dir)
        
        # Clean up any temp script files
        temp_dir = tempfile.gettempdir()
        for file in os.listdir(temp_dir):
            if file.startswith("temp_script_") and file.endswith(".py"):
                try:
                    os.remove(os.path.join(temp_dir, file))
                except:
                    pass  # Ignore cleanup errors