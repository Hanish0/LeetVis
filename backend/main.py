from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Literal
import uvicorn
import os
import requests
import json

app = FastAPI(title="LeetCode Video Generator API", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
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
    First fetches problem details, then generates the video.
    """
    try:
        # Fetch problem details from LeetCode (placeholder implementation)
        problem_details = await fetch_problem_details(request.problem_title)
        
        if not problem_details:
            raise HTTPException(status_code=404, detail="Problem not found")
        
        # Generate video ID
        video_id = f"{request.problem_title}_{request.language}_{request.video_type}".replace(" ", "_").lower()
        
        # Check if video already exists (placeholder - would check database)
        video_path = f"videos/{video_id}.mp4"
        
        if os.path.exists(video_path):
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

async def fetch_problem_details(problem_title: str):
    """
    Fetch problem details from LeetCode or other source.
    This is a placeholder implementation that would normally:
    1. Query LeetCode API or scrape problem details
    2. Return problem description, constraints, examples, etc.
    """
    # Placeholder implementation - in reality would fetch from LeetCode
    mock_problems = {
        "two sum": {
            "title": "Two Sum",
            "difficulty": "Easy",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "examples": [
                {
                    "input": "nums = [2,7,11,15], target = 9",
                    "output": "[0,1]",
                    "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
                }
            ]
        },
        "add two numbers": {
            "title": "Add Two Numbers", 
            "difficulty": "Medium",
            "description": "You are given two non-empty linked lists representing two non-negative integers.",
            "examples": []
        }
    }
    
    # Normalize the problem title for lookup
    normalized_title = problem_title.lower().strip()
    
    return mock_problems.get(normalized_title)

if __name__ == "__main__":
    # Create videos directory if it doesn't exist
    os.makedirs("videos", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)