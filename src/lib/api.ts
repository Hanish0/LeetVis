// API service for backend communication

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface VideoRequest {
  problem_title: string;
  language: 'python' | 'java' | 'cpp';
  video_type: 'explanation' | 'brute_force' | 'optimal';
}

export interface VideoResponse {
  video_id: string;
  video_url: string;
  status: 'generating' | 'ready' | 'error';
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export const api = {
  // Health check endpoint
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new ApiError(response.status, 'Health check failed');
    }
    return response.json();
  },

  // Generate video endpoint
  async generateVideo(request: VideoRequest): Promise<VideoResponse> {
    const response = await fetch(`${API_BASE_URL}/api/generate-video`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new ApiError(response.status, errorData.detail || 'Video generation failed');
    }

    return response.json();
  },

  // Get video URL for playback
  getVideoUrl(videoId: string): string {
    return `${API_BASE_URL}/api/video/${videoId}`;
  },

  // Test backend connection
  async testConnection(): Promise<boolean> {
    try {
      await this.healthCheck();
      return true;
    } catch {
      return false;
    }
  }
};