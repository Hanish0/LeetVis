try:
    from .client import db_client, VIDEOS_TABLE, PROBLEMS_TABLE
except ImportError:
    from client import db_client, VIDEOS_TABLE, PROBLEMS_TABLE
from typing import Optional, Dict, Any
from datetime import datetime

class DatabaseService:
    
    @staticmethod
    def get_video(problem_title: str, language: str, video_type: str) -> Optional[Dict[str, Any]]:
        """Check if a video already exists for the given parameters"""
        try:
            # Normalize problem_title to slug for uniqueness
            title_slug = problem_title.strip().lower().replace(" ", "_").replace("-", "_")
            response = db_client.get_client().table(VIDEOS_TABLE).select("*").eq(
                "problem_title", title_slug
            ).eq("language", language).eq("video_type", video_type).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting video: {e}")
            return None
    
    @staticmethod
    def create_video(problem_title: str, language: str, video_type: str, storage_url: str) -> Optional[Dict[str, Any]]:
        """Create a new video record in the database with Supabase Storage URL"""
        try:
            # Normalize problem_title to slug for uniqueness
            title_slug = problem_title.strip().lower().replace(" ", "_").replace("-", "_")
            video_record = {
                "problem_title": title_slug,
                "language": language,
                "video_type": video_type,
                "storage_url": storage_url,  # Store Supabase Storage URL
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
    def delete_video(problem_title: str, language: str, video_type: str) -> bool:
        """Delete a video record from the database"""
        try:
            response = db_client.get_client().table(VIDEOS_TABLE).delete().eq(
                "problem_title", problem_title
            ).eq(
                "language", language
            ).eq(
                "video_type", video_type
            ).execute()
            
            return response.data is not None
        except Exception as e:
            print(f"Error deleting video: {e}")
            return False
    

    
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
    
    @staticmethod
    def get_all_videos() -> Optional[list]:
        """Get all video records from the database"""
        try:
            response = db_client.get_client().table(VIDEOS_TABLE).select("*").order("created_at", desc=True).execute()
            
            if response.data:
                return response.data
            return []
        except Exception as e:
            print(f"Error getting all videos: {e}")
            return None
    
    @staticmethod
    def clear_all_videos() -> bool:
        """Clear all video records from the database (for testing)"""
        try:
            response = db_client.get_client().table(VIDEOS_TABLE).delete().neq("id", 0).execute()
            return True
        except Exception as e:
            print(f"Error clearing all videos: {e}")
            return False

if __name__ == "__main__":
    print("Database Service initialized successfully!")
    print(f"Videos table: {VIDEOS_TABLE}")
    print(f"Problems table: {PROBLEMS_TABLE}")
    print("Database service is ready to use.")