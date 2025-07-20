# Free Deployment Guide

## 🆓 Render.com (Recommended - Easiest & Completely Free)

**Why Render?**
- Truly free tier (no credit card required)
- Automatic deployments from GitHub
- Built-in SSL certificates
- Easy to use dashboard

**Steps:**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Configure:
   - **Build Command**: `pip install --no-cache-dir -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
   - **Environment**: Python 3.11
6. Click "Create Web Service"
7. Your API will be live at `https://your-app-name.onrender.com`

**Note**: The requirements.txt uses `uvicorn` (not `uvicorn[standard]`) to avoid Rust compilation issues on free hosting platforms.

## 🆓 Vercel (Serverless)

**Why Vercel?**
- Completely free for personal projects
- Instant deployments
- Global CDN

**Steps:**
1. Install Vercel CLI: `npm install -g vercel`
2. In the backend directory, run: `vercel`
3. Follow the prompts:
   - Link to existing project? **N**
   - Project name: `leetcode-video-generator`
   - Directory: `./` (current)
4. Your API will be live instantly

## 🆓 PythonAnywhere

**Why PythonAnywhere?**
- Free tier with no time limits
- Traditional hosting (not serverless)
- Good for learning

**Steps:**
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Go to "Files" and upload your backend code
3. Go to "Web" → "Add a new web app"
4. Choose "Manual configuration" → Python 3.10
5. Set WSGI file to point to your `wsgi.py`
6. Install requirements in a Bash console:
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

## 🆓 Alternative Free Platforms

### Fly.io
- Free tier: 3 shared-cpu-1x VMs
- Command: `flyctl launch`

### Deta Space
- Completely free
- Good for small projects
- Easy Python deployment

### Glitch
- Free for small projects
- Web-based editor
- Instant deployment

## Testing Your Deployment

Once deployed, test your API:

```bash
# Replace YOUR_DEPLOYED_URL with your actual URL
curl https://YOUR_DEPLOYED_URL/health

# Test video generation
curl -X POST https://YOUR_DEPLOYED_URL/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{"problem_title": "Two Sum", "language": "python", "video_type": "explanation"}'
```

## Environment Variables

For production, you may want to set:
- `ENVIRONMENT=production`
- `CORS_ORIGINS=https://your-frontend-domain.com`

All these platforms allow you to set environment variables in their dashboards.