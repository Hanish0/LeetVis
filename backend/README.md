# LeetCode Video Generator Backend

FastAPI backend for generating LeetCode problem explanation videos with Supabase database integration.

## Features

- **Video Generation**: Generates videos for LeetCode problems based on user input
- **Database Integration**: Uses Supabase for storing video metadata and problem details
- **LeetCode API Integration**: Fetches real problem details from LeetCode GraphQL API
- **Smart Caching**: Checks database first, then fetches from LeetCode API if needed
- **Problem Storage**: Automatically stores fetched problems in database for future use
- **Video Serving**: Serves generated videos directly for playback in the frontend
- **Video Caching**: Checks database for existing videos to avoid regeneration

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

### GET /api/problem/{title}
Get details of a problem by its title. First checks the database, then fetches from LeetCode if not found.

**Response:**
```json
{
  "title": "Two Sum",
  "difficulty": "Easy",
  "content": "Given an array of integers nums and an integer target...",
  "url": "https://leetcode.com/problems/two-sum/"
}
```



## Database Setup

This backend uses Supabase as the database. Follow these steps to set up:

1. **Create a Supabase project:**
   - Go to [supabase.com](https://supabase.com) and create a free account
   - Create a new project

2. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Supabase URL and anon key from your project settings

3. **Create database tables:**
   - Run the initialization script to see the SQL commands:
   ```bash
   python -m database.init
   ```
   - Copy and run the SQL commands in your Supabase SQL Editor

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

## Deployment (100% Free Options)

### Option 1: Render (Recommended - Completely Free)
1. Go to [render.com](https://render.com) and sign up
2. Connect your GitHub repository
3. Create a new "Web Service"
4. Render will automatically detect the `render.yaml` configuration
5. Deploy with 0 cost on the free tier

### Option 2: Vercel (Serverless)
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the backend directory
3. Follow the prompts to deploy
4. Uses the `vercel.json` configuration

### Option 3: PythonAnywhere (Free Tier)
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your code to their file system
3. Configure a web app using the `wsgi.py` file
4. Free tier includes 512MB storage and limited CPU

### Option 4: Heroku (Free Alternative)
Use platforms like:
- **Fly.io** (free tier available)
- **Deta Space** (completely free)
- **Glitch** (free for small projects)

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── database/            # Database package
│   ├── __init__.py     # Package initialization
│   ├── client.py       # Supabase client configuration
│   ├── service.py      # Database service operations
│   └── init.py         # Database initialization script
├── render.yaml         # Render deployment config (free)
├── vercel.json         # Vercel deployment config (free)
├── wsgi.py             # PythonAnywhere WSGI config (free)
└── videos/             # Generated video storage (created automatically)
```