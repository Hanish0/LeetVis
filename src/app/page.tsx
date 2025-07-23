'use client';

import { useState, useEffect } from 'react';
import { api, VideoRequest, VideoResponse, ApiError } from '@/lib/api';
import ProgressBar from '@/components/ProgressBar';
import VideoPlayer from '@/components/VideoPlayer';

export default function Home() {
  const [problemTitle, setProblemTitle] = useState('');
  const [selectedVideoType, setSelectedVideoType] = useState<'explanation' | 'brute_force' | 'optimal' | null>(null);
  const [language, setLanguage] = useState<'python' | 'java' | 'cpp'>('python');
  const [isGenerating, setIsGenerating] = useState(false);
  const [videoResponse, setVideoResponse] = useState<VideoResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null);

  // Test backend connection on component mount
  useEffect(() => {
    const testBackend = async () => {
      const connected = await api.testConnection();
      setBackendConnected(connected);
    };
    testBackend();
  }, []);

  const handleProblemTitleChange = (title: string) => {
    setProblemTitle(title);
    // Clear previous results when input changes
    setVideoResponse(null);
    setError(null);
    // Reset video type selection when problem changes
    setSelectedVideoType(null);
  };

  const handleVideoTypeSelect = (videoType: 'explanation' | 'brute_force' | 'optimal') => {
    setSelectedVideoType(videoType);
    setError(null);
    setVideoResponse(null);
  };

  const handleLanguageChange = (lang: 'python' | 'java' | 'cpp') => {
    setLanguage(lang);
  };

  const canGenerateVideo = () => {
    if (!problemTitle.trim()) return false;
    if (!selectedVideoType) return false;
    // For explanation, no language needed. For others, language is required.
    if (selectedVideoType !== 'explanation' && !language) return false;
    return true;
  };

  const pollVideoStatus = async (videoId: string) => {
    const maxAttempts = 60; // Poll for up to 5 minutes (60 * 5 seconds)
    let attempts = 0;

    const poll = async (): Promise<void> => {
      try {
        attempts++;
        const statusResponse = await api.checkVideoStatus(videoId);
        setVideoResponse(statusResponse);

        if (statusResponse.status === 'ready') {
          setIsGenerating(false);
          return;
        }

        if (statusResponse.status === 'error') {
          setError('Video generation failed during processing.');
          setIsGenerating(false);
          return;
        }

        // Continue polling if still generating and haven't exceeded max attempts
        if (statusResponse.status === 'generating' && attempts < maxAttempts) {
          setTimeout(poll, 5000); // Poll every 5 seconds
        } else if (attempts >= maxAttempts) {
          setError('Video generation is taking longer than expected. Please try again later.');
          setIsGenerating(false);
        }
      } catch (err) {
        console.error('Error polling video status:', err);
        if (attempts < maxAttempts) {
          setTimeout(poll, 5000); // Retry polling
        } else {
          setError('Failed to check video generation status.');
          setIsGenerating(false);
        }
      }
    };

    // Start polling after a short delay
    setTimeout(poll, 2000);
  };

  const handleGenerateVideo = async () => {
    if (!canGenerateVideo()) {
      setError('Please fill in all required fields');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setVideoResponse(null);

    try {
      const request: VideoRequest = {
        problem_title: problemTitle.trim(),
        language: selectedVideoType === 'explanation' ? 'python' : language,
        video_type: selectedVideoType!
      };

      const response = await api.generateVideo(request);
      setVideoResponse(response);

      if (response.status === 'error') {
        setError('Video generation failed. Please check your input or try again later.');
        setIsGenerating(false);
      } else if (response.status === 'generating') {
        // Start polling for status updates
        pollVideoStatus(response.video_id);
      } else if (response.status === 'ready') {
        // Video is already ready
        setIsGenerating(false);
      }
    } catch (err: unknown) {
      if (err instanceof ApiError) {
        // Show more details and suggest retry for server/network errors
        if (err.status >= 500) {
          setError(`Server error (${err.status}): ${err.message}. Please try again.`);
        } else if (err.status === 429) {
          setError(`Rate limit exceeded. Please wait and try again.`);
        } else if (err.status === 400) {
          setError(`Bad request: ${err.message}. Please check your input.`);
        } else {
          setError(`Error ${err.status}: ${err.message}`);
        }
      } else {
        setError('Failed to connect to backend. Please check your network and try again.');
      }
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              LeetCode Video Generator
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Enter a LeetCode problem and get an AI-generated video explanation
            </p>

            {/* Backend Connection Status */}
            <div className="mt-4">
              {backendConnected === null ? (
                <div className="text-sm text-gray-500">Testing backend connection...</div>
              ) : backendConnected ? (
                <div className="text-sm text-green-600 dark:text-green-400">
                  ✅ Backend connected
                </div>
              ) : (
                <div className="text-sm text-red-600 dark:text-red-400">
                  ❌ Backend not connected - Please check your backend deployment
                </div>
              )}
            </div>
          </div>

          {/* Step 1: Problem Title Input */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
            <div className="space-y-6">
              <div>
                <label htmlFor="problem-title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Enter LeetCode Problem Title
                </label>
                <input
                  id="problem-title"
                  type="text"
                  value={problemTitle}
                  onChange={(e) => handleProblemTitleChange(e.target.value)}
                  placeholder="e.g., Two Sum, Valid Parentheses, etc."
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
              </div>
            </div>
          </div>

          {/* Step 2: Video Type Selection */}
          {problemTitle.trim() && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                Choose Video Type
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => handleVideoTypeSelect('explanation')}
                  className={`${selectedVideoType === 'explanation'
                      ? 'bg-blue-700 ring-2 ring-blue-500'
                      : 'bg-blue-600 hover:bg-blue-700'
                    } text-white font-medium py-4 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`}
                >
                  Problem Explanation
                  
                </button>
                <button
                  onClick={() => handleVideoTypeSelect('brute_force')}
                  className={`${selectedVideoType === 'brute_force'
                      ? 'bg-green-700 ring-2 ring-green-500'
                      : 'bg-green-600 hover:bg-green-700'
                    } text-white font-medium py-4 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2`}
                >
                  Brute Force Solution
                  
                </button>
                <button
                  onClick={() => handleVideoTypeSelect('optimal')}
                  className={`${selectedVideoType === 'optimal'
                      ? 'bg-purple-700 ring-2 ring-purple-500'
                      : 'bg-purple-600 hover:bg-purple-700'
                    } text-white font-medium py-4 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2`}
                >
                  Optimal Solution
                  
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Language Selection (only for brute_force and optimal) */}
          {selectedVideoType && selectedVideoType !== 'explanation' && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                Choose Programming Language
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => handleLanguageChange('python')}
                  className={`${language === 'python'
                      ? 'bg-yellow-600 ring-2 ring-yellow-500'
                      : 'bg-gray-600 hover:bg-yellow-600'
                    } text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2`}
                >
                  Python
                </button>
                <button
                  onClick={() => handleLanguageChange('java')}
                  className={`${language === 'java'
                      ? 'bg-orange-600 ring-2 ring-orange-500'
                      : 'bg-gray-600 hover:bg-orange-600'
                    } text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2`}
                >
                  Java
                </button>
                <button
                  onClick={() => handleLanguageChange('cpp')}
                  className={`${language === 'cpp'
                      ? 'bg-indigo-600 ring-2 ring-indigo-500'
                      : 'bg-gray-600 hover:bg-indigo-600'
                    } text-white font-medium py-3 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2`}
                >
                  C++
                </button>
              </div>
            </div>
          )}

          {/* Generate Video Button */}
          {canGenerateVideo() && !isGenerating && (
            <div className="text-center mb-8">
              <button
                onClick={handleGenerateVideo}
                disabled={!backendConnected}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed text-white font-bold py-4 px-8 rounded-lg text-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 shadow-lg"
              >
                🎬 Generate Video
              </button>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-8">
              <div className="text-red-800 dark:text-red-200">
                <strong>Error:</strong> {error}
                {error.includes('try again') && (
                  <button
                    className="ml-4 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                    onClick={() => handleGenerateVideo()}
                  >
                    Retry
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Progress Bar */}
          <ProgressBar 
            isGenerating={isGenerating} 
            onComplete={() => {
              // Progress bar completed, but we still need to wait for actual API response
              console.log('Progress simulation completed');
            }}
          />



          {/* Video Response */}
          {videoResponse && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
                Video Result
              </h2>

              {videoResponse.status === 'ready' && (
                <div>
                  <div className="text-center mb-4">
                    <div className="text-green-600 dark:text-green-400 mb-4">
                      ✅ Video is ready!
                    </div>
                  </div>
                  <VideoPlayer
                    videoUrl={api.getVideoUrl(videoResponse.video_id)}
                    title={`${problemTitle} - ${selectedVideoType?.replace('_', ' ').toUpperCase()} (${language?.toUpperCase()})`}
                    onError={(error) => setError(`Video playback error: ${error}`)}
                  />
                </div>
              )}

              {videoResponse.status === 'generating' && (
                <div className="text-center">
                  <div className="text-blue-600 dark:text-blue-400 mb-4">
                    🔄 Video is being generated...
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Video ID: {videoResponse.video_id}
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                    This is a placeholder response. In the full implementation,
                    the system will generate actual videos.
                  </div>
                </div>
              )}

              {videoResponse.status === 'error' && (
                <div className="text-center">
                  <div className="text-red-600 dark:text-red-400">
                    ❌ Video generation failed
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
