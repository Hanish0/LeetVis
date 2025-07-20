# LeetCode Video Generator Backend

FastAPI backend for generating LeetCode problem explanation videos.

## Features

- **Video Generation**: Generates videos for LeetCode problems based on user input
- **Problem Fetching**: Automatically fetches problem details when given a problem title
- **Video Serving**: Serves generated videos directly for playback in the frontend
- **Caching**: Checks for existing videos to avoid regeneration

## API Endpoints

### POST /api/generate-video
Generate a video for a LeetCode problem.

**Request Body:**
```json
{
  "problem_title": "Two Sum",
  "language": "python",
  "video_type": "explanation"
}
```

**Response:**
```json
{
  "video_id": "two_sum_python_explanation",
  "video_url": "/api/video/two_sum_python_explanation",
  "status": "generating"
}
```

### GET /api/video/{video_id}
Retrieve and stream a generated video file for direct playback.

**Response:** Video file (MP4) for direct playback in browser

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Deployment

This backend is configured for deployment on Railway:

1. Connect your GitHub repository to Railway
2. Railway will automatically detect the Python project
3. The `Procfile` and `railway.json` configure the deployment settings
4. Environment variables can be set in Railway dashboard

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Procfile            # Railway deployment config
├── railway.json        # Railway deployment settings
└── videos/             # Generated video storage (created automatically)
```