from .client import db_client, VIDEOS_TABLE, PROBLEMS_TABLE
from typing import Optional, Dict, Any
from datetime import datetime

class DatabaseService:
    
    @staticmethod
    def get_video(problem_title: str, language: str, video_type: str) -> Optional[Dict[str, Any]]:
        """Check if a video already exists for the given parameters"""
        try:
            response = db_client.get_client().table(VIDEOS_TABLE).select("*").eq(
                "problem_title", problem_title
            ).eq(
                "language", language
            ).eq(
                "video_type", video_type
            ).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting video: {e}")
            return None
    
    @staticmethod
    def create_video(problem_title: str, language: str, video_type: str, video_data: bytes) -> Optional[Dict[str, Any]]:
        """Create a new video record in the database with binary video data"""
        try:
            import base64
            
            # Convert binary video data to base64 for storage
            video_base64 = base64.b64encode(video_data).decode('utf-8')
            
            video_record = {
                "problem_title": problem_title,
                "language": language,
                "video_type": video_type,
                "video_data": video_base64,  # Store actual video data, not path
                "created_at": datetime.utcnow().isoformat()
            }
            
            response = db_client.get_client().table(VIDEOS_TABLE).insert(video_record).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating video: {e}")
            return None
    
    @staticmethod
    def get_video_data(problem_title: str, language: str, video_type: str) -> Optional[bytes]:
        """Get the actual video binary data from database"""
        try:
            import base64
            
            response = db_client.get_client().table(VIDEOS_TABLE).select("video_data").eq(
                "problem_title", problem_title
            ).eq(
                "language", language
            ).eq(
                "video_type", video_type
            ).execute()
            
            if response.data and len(response.data) > 0:
                video_base64 = response.data[0].get("video_data")
                if video_base64:
                    # Convert base64 back to binary data
                    return base64.b64decode(video_base64)
            return None
        except Exception as e:
            print(f"Error getting video data: {e}")
            return None
    
    @staticmethod
    def get_problem_by_title_slug(title_slug: str) -> Optional[Dict[str, Any]]:
        """Get a problem by title slug"""
        try:
            response = db_client.get_client().table(PROBLEMS_TABLE).select("*").eq(
                "title_slug", title_slug
            ).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting problem by title slug: {e}")
            return None
    
    @staticmethod
    def get_problem_by_title(title: str) -> Optional[Dict[str, Any]]:
        """Get a problem by title"""
        try:
            response = db_client.get_client().table(PROBLEMS_TABLE).select("*").ilike(
                "title", f"%{title}%"
            ).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting problem by title: {e}")
            return None
    
    @staticmethod
    def create_problem_from_leetcode(leetcode_data: Dict[str, Any], title_slug: str) -> Optional[Dict[str, Any]]:
        """Create a new problem record from LeetCode API data - only essential fields"""
        try:
            problem_data = {
                "title": leetcode_data.get("title", ""),
                "title_slug": title_slug,
                "content": leetcode_data.get("content", ""),
                "difficulty": leetcode_data.get("difficulty", "")
            }
            
            response = db_client.get_client().table(PROBLEMS_TABLE).insert(problem_data).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error creating problem from LeetCode data: {e}")
            return None