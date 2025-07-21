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
from database.service import DatabaseService

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
    problem_title: str
    language: Literal["python", "java", "cpp"]
    video_type: Literal["explanation", "brute_force", "optimal"]

class VideoResponse(BaseModel):
    video_id: str
    video_url: str
    status: Literal["generating", "ready", "error"]

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "LeetCode Video Generator API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Video generation endpoint
@app.post("/api/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    """
    Generate a video for the specified LeetCode problem.
    First checks database for existing video, then generates if needed.
    """
    try:
        # Check if video already exists in database
        existing_video = DatabaseService.get_video(
            request.problem_title, 
            request.language, 
            request.video_type
        )
        
        if existing_video:
            video_id = f"{request.problem_title}_{request.language}_{request.video_type}".replace(" ", "_").lower()
            return VideoResponse(
                video_id=video_id,
                video_url=f"/api/video/{video_id}",
                status="ready"
            )
        
        # Fetch problem details from LeetCode (placeholder implementation)
        problem_details = await fetch_problem_details(request.problem_title)
        
        if not problem_details:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Generate video ID
        video_id = f"{request.problem_title}_{request.language}_{request.video_type}".replace(" ", "_").lower()
        video_path = f"videos/{video_id}.mp4"
        
        # Check if video file exists locally (fallback check)
        if os.path.exists(video_path):
            # Store in database for future reference
            DatabaseService.create_video(
                request.problem_title,
                request.language,
                request.video_type,
                video_path
            )
            return VideoResponse(
                video_id=video_id,
                video_url=f"/api/video/{video_id}",
                status="ready"
            )
        
        # For now, return generating status (actual video generation will be implemented later)
        return VideoResponse(
            video_id=video_id,
            video_url=f"/api/video/{video_id}",
            status="generating"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@app.get("/api/video/{video_id}")
async def get_video(video_id: str):
    """
    Serve the generated video file for playback.
    Returns the actual video file for direct playback in the frontend.
    """
    video_path = f"videos/{video_id}.mp4"
    
    # Check if video file exists
    if os.path.exists(video_path):
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename=f"{video_id}.mp4"
        )
    
    # If video doesn't exist, return placeholder response
    # In a real implementation, this might trigger video generation
    raise HTTPException(
        status_code=404, 
        detail="Video not found. It may still be generating or the request was invalid."
    )



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

# Create videos directory if it doesn't exist
os.makedirs("videos", exist_ok=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)