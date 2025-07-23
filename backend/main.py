from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Literal, Dict, Any, Optional
import uvicorn
import os
import requests
import json
import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor
from database.service import DatabaseService
from database.storage import storage_service
from solution_generator.generator import SolutionGenerator
from manim_generator.service import ManimVideoService

app = FastAPI(title="LeetCode Video Generator API", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://leet-vis.vercel.app"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class VideoRequest(BaseModel):
    problem_title: str  # Raw title from user
    @property
    def title_slug(self) -> str:
        # Normalize to lowercase, replace spaces and hyphens with underscores
        return self.problem_title.strip().lower().replace(" ", "_").replace("-", "_")
    language: Literal["python", "java", "cpp"]
    video_type: Literal["explanation", "brute_force", "optimal"]

class VideoResponse(BaseModel):
    video_id: str
    video_url: str
    status: Literal["generating", "ready", "error"]
    error_message: Optional[str] = None

# Global dictionary to track video generation status
video_generation_status: Dict[str, Dict[str, Any]] = {}

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "LeetCode Video Generator API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Thread pool for background video generation
executor = ThreadPoolExecutor(max_workers=2)

def generate_video_background(video_id: str, problem_details: Dict[str, Any], 
                            request: VideoRequest) -> None:
    """Background function to generate video with proper error handling and storage"""
    try:
        title_slug = request.title_slug
        
        # Update status to generating
        video_generation_status[video_id] = {
            "status": "generating",
            "progress": 0,
            "message": "Starting video generation..."
        }
        print(f"Starting video generation for: {video_id}")
        
        # Generate solution code
        video_generation_status[video_id]["progress"] = 20
        video_generation_status[video_id]["message"] = "Generating solution code..."
        
        try:
            solution_code = solution_generator.generate_solution(
                problem_details,
                request.language,
                request.video_type
            )
            print(f"Solution code generated successfully for: {video_id}")
        except Exception as e:
            print(f"Solution generation failed for {video_id}: {e}")
            video_generation_status[video_id] = {
                "status": "error",
                "progress": 0,
                "message": "We couldn't generate a solution for this problem. Please check the problem title and try again."
            }
            return
        
        # Generate and render video
        video_generation_status[video_id]["progress"] = 50
        video_generation_status[video_id]["message"] = "Creating video animation..."
        
        try:
            video_path = manim_service.generate_video(
                problem_details, 
                solution_code, 
                request.language, 
                request.video_type,
                video_id
            )
            print(f"Video rendered successfully at: {video_path}")
        except Exception as e:
            print(f"Video rendering failed for {video_id}: {e}")
            video_generation_status[video_id] = {
                "status": "error",
                "progress": 0,
                "message": "Sorry, we couldn't create the video animation. Please try again later."
            }
            return
        
        # Verify video file was created
        if not os.path.exists(video_path):
            print(f"Video file not found after generation: {video_path}")
            video_generation_status[video_id] = {
                "status": "error",
                "progress": 0,
                "message": "Video generation completed but file not found. Please try again."
            }
            return
        
        video_generation_status[video_id]["progress"] = 70
        video_generation_status[video_id]["message"] = "Uploading video to storage..."
        
        # Upload video to Supabase Storage
        storage_url = None
        try:
            storage_url = storage_service.upload_video(
                video_path,
                title_slug,  # Use normalized title_slug
                request.language,
                request.video_type
            )
            
            if not storage_url:
                raise Exception("Upload returned no URL")
            
            print(f"Video uploaded to storage successfully: {storage_url}")
                
        except Exception as e:
            print(f"Storage upload failed for {video_id}: {e}")
            video_generation_status[video_id] = {
                "status": "error",
                "progress": 0,
                "message": "Video was created but couldn't be saved to storage. Please try again."
            }
            return
        
        video_generation_status[video_id]["progress"] = 90
        video_generation_status[video_id]["message"] = "Saving video record to database..."
        
        # Store video record in database with storage URL
        try:
            video_record = DatabaseService.create_video(
                title_slug,  # Use normalized title_slug
                request.language,
                request.video_type,
                storage_url
            )
            
            if video_record:
                print(f"Video record saved to database successfully: {video_record}")
            else:
                print(f"Warning: Video record creation returned None for {video_id}")
                
        except Exception as e:
            print(f"Database save failed for {video_id}: {e}")
            # Video is uploaded to storage but not in database - still usable
            print("Video uploaded to storage but database record failed - video still accessible")
        
        video_generation_status[video_id]["progress"] = 95
        video_generation_status[video_id]["message"] = "Cleaning up temporary files..."
        
        # Clean up local file after uploading to storage
        try:
            if os.path.exists(video_path):
                os.remove(video_path)
                print(f"Local video file cleaned up: {video_path}")
        except Exception as e:
            print(f"Cleanup failed for {video_path}: {e}")
            # Not critical, continue
        
        # Mark as complete
        video_generation_status[video_id] = {
            "status": "ready",
            "progress": 100,
            "message": "Your video is ready!",
            "storage_url": storage_url
        }
        
        print(f"Video generation completed successfully for: {video_id}")
        
    except Exception as e:
        print(f"Unexpected error in video generation for {video_id}: {e}")
        video_generation_status[video_id] = {
            "status": "error",
            "progress": 0,
            "message": "Something went wrong while creating your video. Our team has been notified."
        }

@app.post("/api/generate-video")
async def generate_video(request: VideoRequest):
    """
    Generate a video for the given problem, language, and video type.
    Returns immediately with a video_id and status, while video generation happens in background.
    Implements proper video caching by checking database before generation.
    """
    try:
        # Use normalized slug for all DB and ID operations
        title_slug = request.title_slug
        video_id = f"{title_slug}_{request.language}_{request.video_type}"
        
        # STEP 1: Check if video already exists in database (caching)
        print(f"Checking database for existing video: {title_slug}, {request.language}, {request.video_type}")
        existing_video = DatabaseService.get_video(
            title_slug,
            request.language,
            request.video_type
        )
        
        if existing_video:
            print(f"Found existing video in database: {existing_video}")
            storage_url = existing_video.get('storage_url')
            if storage_url:
                # Video exists and has valid storage URL - return immediately
                print(f"Returning cached video with storage URL: {storage_url}")
                return VideoResponse(
                    video_id=video_id,
                    video_url=storage_url,
                    status="ready"
                )
            else:
                # Video record exists but no storage URL - clean up and regenerate
                print("Video record exists but no storage URL - cleaning up")
                DatabaseService.delete_video(title_slug, request.language, request.video_type)

        # STEP 2: Check if video is currently being generated
        if video_id in video_generation_status:
            current_status = video_generation_status[video_id]
            if current_status["status"] == "generating":
                print(f"Video is currently being generated: {video_id}")
                return VideoResponse(
                    video_id=video_id,
                    video_url=f"/api/video-status/{video_id}",
                    status="generating"
                )
            elif current_status["status"] == "ready" and "storage_url" in current_status:
                # Generation completed but not yet stored in DB
                print(f"Video generation completed, returning storage URL: {current_status['storage_url']}")
                return VideoResponse(
                    video_id=video_id,
                    video_url=current_status["storage_url"],
                    status="ready"
                )

        # STEP 3: Fetch problem details before starting generation
        print(f"Fetching problem details for: {request.problem_title}")
        problem_details = await fetch_problem_details(request.problem_title)
        if not problem_details:
            raise HTTPException(status_code=404, detail="Problem not found")

        # STEP 4: Start background video generation
        print(f"Starting background video generation for: {video_id}")
        executor.submit(generate_video_background, video_id, problem_details, request)
        
        return VideoResponse(
            video_id=video_id,
            video_url=f"/api/video-status/{video_id}",
            status="generating"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Unexpected error in generate_video: {e}")
        
        # Return user-friendly error message
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="The requested problem could not be found. Please check the problem title and try again.")
        elif "storage" in str(e).lower() or "upload" in str(e).lower():
            raise HTTPException(status_code=503, detail="Our video storage service is temporarily unavailable. Please try again in a few minutes.")
        elif "database" in str(e).lower():
            raise HTTPException(status_code=503, detail="Our database is temporarily unavailable. Please try again in a few minutes.")
        else:
            raise HTTPException(status_code=500, detail="We're experiencing technical difficulties. Please try again later or contact support if the problem persists.")

@app.get("/api/video/{video_id}")
async def get_video(video_id: str):
    """
    Serve the generated video file for playback.
    Returns redirect to Supabase storage URL with proper caching logic.
    """
    from fastapi.responses import RedirectResponse
    
    try:
        # Parse video_id to get problem details
        parts = video_id.split("_")
        if len(parts) < 3:
            raise HTTPException(status_code=400, detail="Invalid video ID format")
        
        # Extract problem title, language, and video type from video_id
        # Format: "problem_title_language_videotype"
        video_type = parts[-1]
        language = parts[-2]
        title_slug = "_".join(parts[:-2])  # Keep as slug format
        
        print(f"Looking for video: title_slug={title_slug}, language={language}, video_type={video_type}")
        
        # Get video record from database (primary source)
        video_record = DatabaseService.get_video(title_slug, language, video_type)
        
        if video_record and video_record.get('storage_url'):
            storage_url = video_record['storage_url']
            print(f"Found video in database with storage URL: {storage_url}")
            
            # Check if it's a full URL (public bucket) or just filename (private bucket)
            if storage_url.startswith('http'):
                # Public bucket - redirect directly
                return RedirectResponse(url=storage_url)
            else:
                # Private bucket - generate signed URL
                try:
                    signed_url = storage_service.get_signed_url(storage_url, expires_in=3600)
                    if signed_url:
                        return RedirectResponse(url=signed_url)
                    else:
                        print(f"Failed to generate signed URL for: {storage_url}")
                        raise HTTPException(status_code=500, detail="Failed to generate video access URL")
                except Exception as e:
                    print(f"Error generating signed URL: {e}")
                    raise HTTPException(status_code=500, detail="Failed to generate video access URL")
        
        # Check if video is currently being generated
        if video_id in video_generation_status:
            status_info = video_generation_status[video_id]
            if status_info["status"] == "ready" and "storage_url" in status_info:
                # Video generation completed but may not be in database yet
                storage_url = status_info["storage_url"]
                print(f"Found video in generation status with storage URL: {storage_url}")
                return RedirectResponse(url=storage_url)
            elif status_info["status"] == "generating":
                raise HTTPException(
                    status_code=202, 
                    detail="Video is still being generated. Please check status endpoint."
                )
            elif status_info["status"] == "error":
                raise HTTPException(
                    status_code=500, 
                    detail="Video generation failed. Please try generating again."
                )
        
        # Video not found anywhere
        raise HTTPException(
            status_code=404, 
            detail="Video not found. It may still be generating or the request was invalid."
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Unexpected error in get_video: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving video")

@app.get("/api/video-status/{video_id}")
async def get_video_status(video_id: str):
    """
    Get the current status of video generation with proper caching logic.
    Returns progress information for ongoing generations or cached video status.
    """
    try:
        # Check if video is currently being generated
        if video_id in video_generation_status:
            status_info = video_generation_status[video_id]
            response = {
                "video_id": video_id,
                "status": status_info["status"],
                "progress": status_info["progress"],
                "message": status_info["message"]
            }
            
            # Include storage URL if video is ready
            if status_info["status"] == "ready" and "storage_url" in status_info:
                response["video_url"] = status_info["storage_url"]
            
            return response
        
        # Parse video_id to check database for existing video
        parts = video_id.split("_")
        if len(parts) >= 3:
            video_type = parts[-1]
            language = parts[-2]
            title_slug = "_".join(parts[:-2])  # Keep as slug format
            
            print(f"Checking database for video status: {title_slug}, {language}, {video_type}")
            
            existing_video = DatabaseService.get_video(title_slug, language, video_type)
            if existing_video:
                print(f"Found existing video in database: {existing_video}")
                response = {
                    "video_id": video_id,
                    "status": "ready",
                    "progress": 100,
                    "message": "Video is ready for playback (cached)"
                }
                
                # Include storage URL if available
                storage_url = existing_video.get('storage_url')
                if storage_url:
                    response["video_url"] = storage_url
                else:
                    # Video record exists but no storage URL - mark as error
                    response["status"] = "error"
                    response["progress"] = 0
                    response["message"] = "Video record found but storage URL missing"
                
                return response
        
        # Video not found in generation status or database
        return {
            "video_id": video_id,
            "status": "not_found",
            "progress": 0,
            "message": "Video not found or generation not started"
        }
        
    except Exception as e:
        print(f"Error in get_video_status for {video_id}: {e}")
        return {
            "video_id": video_id,
            "status": "error",
            "progress": 0,
            "message": "Error checking video status"
        }



# LeetCode API configuration
LEETCODE_URL = "https://leetcode.com/graphql"
client = httpx.AsyncClient()

async def fetch_problem_details_by_title_slug(title_slug: str) -> Dict[str, Any]:
    """
    Fetch problem details directly from LeetCode based on the title slug.
    """
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            content
            likes
            dislikes
            difficulty
            isPaidOnly
            solution { canSeeDetail content }
            hasSolution
            hasVideoSolution
        }
    }
    """
    
    query_payload = {
        "query": query,
        "variables": {"titleSlug": title_slug}
    }
    
    try:
        response = await client.post(LEETCODE_URL, json=query_payload)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and data["data"].get("question"):
                return data["data"]["question"]
            else:
                raise HTTPException(status_code=404, detail="Problem data not found")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data from LeetCode")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

def convert_title_to_slug(title: str) -> str:
    """
    Convert a problem title to a LeetCode slug format.
    Example: "Two Sum" -> "two-sum"
    """
    return title.lower().replace(" ", "-")

async def fetch_problem_details(problem_title: str) -> Optional[Dict[str, Any]]:
    """
    Fetch problem details from database first, then from LeetCode API if not found.
    Stores fetched problems in the database for future use.
    """
    # First check database for existing problem by title
    existing_problem = DatabaseService.get_problem_by_title(problem_title)
    if existing_problem:
        return {
            "title": existing_problem["title"],
            "difficulty": existing_problem["difficulty"],
            "content": existing_problem["content"]
        }
    
    # If not found in database, try to fetch from LeetCode API
    try:
        # Convert title to slug format for LeetCode API
        title_slug = convert_title_to_slug(problem_title)
        
        # Check if we have the problem by slug in the database
        existing_problem_by_slug = DatabaseService.get_problem_by_title_slug(title_slug)
        if existing_problem_by_slug:
            return {
                "title": existing_problem_by_slug["title"],
                "difficulty": existing_problem_by_slug["difficulty"],
                "content": existing_problem_by_slug["content"]
            }
        
        # Fetch from LeetCode API
        leetcode_data = await fetch_problem_details_by_title_slug(title_slug)
        
        # Store in database for future use
        if leetcode_data:
            DatabaseService.create_problem_from_leetcode(leetcode_data, title_slug)
            
            return {
                "title": leetcode_data["title"],
                "difficulty": leetcode_data["difficulty"],
                "content": leetcode_data["content"]
            }
        
        return None
    except Exception as e:
        print(f"Error fetching problem from LeetCode: {e}")
        
        # Fallback to mock problems if LeetCode API fails
        mock_problems = {
            "two sum": {
                "title": "Two Sum",
                "difficulty": "Easy",
                "content": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
            },
            "add two numbers": {
                "title": "Add Two Numbers", 
                "difficulty": "Medium",
                "content": "You are given two non-empty linked lists representing two non-negative integers."
            }
        }
        
        # Normalize the problem title for lookup
        normalized_title = problem_title.lower().strip()
        return mock_problems.get(normalized_title)

@app.get("/api/problem/{title}", tags=["Problems"])
async def get_problem_by_title(title: str):
    """
    Get details of a problem by its title.
    First checks the database, then fetches from LeetCode if not found.
    """
    problem_details = await fetch_problem_details(title)
    if not problem_details:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Add URL to the problem details
    title_slug = convert_title_to_slug(title)
    problem_details["url"] = f"https://leetcode.com/problems/{title_slug}/"
    
    return problem_details

@app.delete("/api/video/{video_id}")
async def delete_video(video_id: str):
    """
    Delete a video from both Supabase storage and database.
    """
    try:
        # Parse video_id to get problem details
        parts = video_id.replace("_", " ").split(" ")
        if len(parts) < 3:
            raise HTTPException(status_code=400, detail="Invalid video ID format")
        
        video_type = parts[-1]
        language = parts[-2]
        problem_title = " ".join(parts[:-2]).title()
        
        # Get video record to get storage URL
        video_record = DatabaseService.get_video(problem_title, language, video_type)
        
        if not video_record:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Delete from Supabase storage if storage URL exists
        storage_url = video_record.get('storage_url')
        if storage_url:
            storage_service.delete_video(storage_url)
        
        # Delete from database
        success = DatabaseService.delete_video(problem_title, language, video_type)
        
        if success:
            return {"message": "Video deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete video from database")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video deletion failed: {str(e)}")

@app.get("/api/videos")
async def list_videos():
    """
    List all videos stored in database with caching information.
    """
    try:
        # Get videos from storage service
        storage_videos = storage_service.list_videos()
        
        # Get videos from database
        db_videos = DatabaseService.get_all_videos()
        
        return {
            "storage_videos": storage_videos,
            "database_videos": db_videos,
            "total_cached": len(db_videos) if db_videos else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list videos: {str(e)}")

@app.get("/api/cache/stats")
async def get_cache_stats():
    """
    Get statistics about video caching.
    """
    try:
        db_videos = DatabaseService.get_all_videos()
        
        stats = {
            "total_cached_videos": len(db_videos) if db_videos else 0,
            "videos_by_language": {},
            "videos_by_type": {},
            "recent_videos": []
        }
        
        if db_videos:
            # Count by language
            for video in db_videos:
                lang = video.get('language', 'unknown')
                stats["videos_by_language"][lang] = stats["videos_by_language"].get(lang, 0) + 1
            
            # Count by video type
            for video in db_videos:
                vtype = video.get('video_type', 'unknown')
                stats["videos_by_type"][vtype] = stats["videos_by_type"].get(vtype, 0) + 1
            
            # Get recent videos (last 10)
            sorted_videos = sorted(db_videos, key=lambda x: x.get('created_at', ''), reverse=True)
            stats["recent_videos"] = sorted_videos[:10]
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cache stats: {str(e)}")

@app.post("/api/cache/clear")
async def clear_cache():
    """
    Clear video cache (for testing purposes).
    WARNING: This will delete all video records from database but not from storage.
    """
    try:
        success = DatabaseService.clear_all_videos()
        if success:
            return {"message": "Video cache cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear cache")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")

@app.post("/api/generate-script", tags=["Testing"])
async def generate_script_only(request: VideoRequest):
    """
    Generate only the Manim script without rendering video.
    Useful for testing and debugging the script generation.
    """
    try:
        # Fetch problem details
        problem_details = await fetch_problem_details(request.problem_title)
        
        if not problem_details:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Generate placeholder solution code
        solution_code = f"""
def solution():
    # Placeholder solution for {request.problem_title}
    # Language: {request.language}
    # Type: {request.video_type}
    pass
"""
        
        # Generate Manim script
        script_content = manim_service.generate_script_only(
            problem_details, 
            solution_code, 
            request.language, 
            request.video_type
        )
        
        return {
            "problem_title": request.problem_title,
            "language": request.language,
            "video_type": request.video_type,
            "script_content": script_content
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")

# Initialize services
solution_generator = SolutionGenerator()
manim_service = ManimVideoService()

# Create videos directory if it doesn't exist
os.makedirs("videos", exist_ok=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)