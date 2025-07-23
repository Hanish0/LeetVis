'use client';

import { useState, useRef, useEffect } from 'react';

interface VideoPlayerProps {
    videoUrl: string;
    title?: string;
    onError?: (error: string) => void;
}

export default function VideoPlayer({ videoUrl, title, onError }: VideoPlayerProps) {
    const [isLoading, setIsLoading] = useState(true);
    const [hasError, setHasError] = useState(false);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [volume, setVolume] = useState(1);
    const [isMuted, setIsMuted] = useState(false);
    const videoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        const video = videoRef.current;
        if (!video) return;

        const handleLoadStart = () => setIsLoading(true);
        const handleCanPlay = () => setIsLoading(false);
        const handleError = () => {
            setHasError(true);
            setIsLoading(false);
            onError?.('Failed to load video');
        };
        const handleTimeUpdate = () => setCurrentTime(video.currentTime);
        const handleDurationChange = () => setDuration(video.duration);
        const handlePlay = () => setIsPlaying(true);
        const handlePause = () => setIsPlaying(false);

        video.addEventListener('loadstart', handleLoadStart);
        video.addEventListener('canplay', handleCanPlay);
        video.addEventListener('error', handleError);
        video.addEventListener('timeupdate', handleTimeUpdate);
        video.addEventListener('durationchange', handleDurationChange);
        video.addEventListener('play', handlePlay);
        video.addEventListener('pause', handlePause);

        return () => {
            video.removeEventListener('loadstart', handleLoadStart);
            video.removeEventListener('canplay', handleCanPlay);
            video.removeEventListener('error', handleError);
            video.removeEventListener('timeupdate', handleTimeUpdate);
            video.removeEventListener('durationchange', handleDurationChange);
            video.removeEventListener('play', handlePlay);
            video.removeEventListener('pause', handlePause);
        };
    }, [onError]);

    const togglePlay = () => {
        const video = videoRef.current;
        if (!video) return;

        if (isPlaying) {
            video.pause();
        } else {
            video.play();
        }
    };

    const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
        const video = videoRef.current;
        if (!video) return;

        const newTime = (parseFloat(e.target.value) / 100) * duration;
        video.currentTime = newTime;
        setCurrentTime(newTime);
    };

    const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const video = videoRef.current;
        if (!video) return;

        const newVolume = parseFloat(e.target.value) / 100;
        video.volume = newVolume;
        setVolume(newVolume);
        setIsMuted(newVolume === 0);
    };

    const toggleMute = () => {
        const video = videoRef.current;
        if (!video) return;

        if (isMuted) {
            video.volume = volume;
            setIsMuted(false);
        } else {
            video.volume = 0;
            setIsMuted(true);
        }
    };

    const formatTime = (time: number) => {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };

    if (hasError) {
        return (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-8 text-center">
                <div className="text-red-600 dark:text-red-400 mb-4">
                    ❌ Failed to load video
                </div>
                <div className="text-sm text-red-500 dark:text-red-300">
                    Please check your connection and try again.
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
            {title && (
                <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {title}
                    </h3>
                </div>
            )}

            <div className="relative">
                {isLoading && (
                    <div className="absolute inset-0 bg-gray-100 dark:bg-gray-700 flex items-center justify-center z-10">
                        <div className="text-center">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
                            <div className="text-sm text-gray-600 dark:text-gray-400">Loading video...</div>
                        </div>
                    </div>
                )}

                <video
                    ref={videoRef}
                    src={videoUrl}
                    className="w-full aspect-video bg-black"
                    preload="metadata"
                />

                {/* Custom Controls */}
                <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
                    {/* Progress Bar */}
                    <div className="mb-3">
                        <input
                            type="range"
                            min="0"
                            max="100"
                            value={duration ? (currentTime / duration) * 100 : 0}
                            onChange={handleSeek}
                            className="w-full h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer hover:bg-gray-500 transition-colors"
                            style={{
                                background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${duration ? (currentTime / duration) * 100 : 0}%, #4b5563 ${duration ? (currentTime / duration) * 100 : 0}%, #4b5563 100%)`
                            }}
                        />
                    </div>

                    {/* Control Buttons */}
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <button
                                onClick={togglePlay}
                                className="text-white hover:text-blue-400 transition-colors"
                                disabled={isLoading}
                            >
                                {isPlaying ? (
                                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                                    </svg>
                                ) : (
                                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                                    </svg>
                                )}
                            </button>

                            <div className="text-white text-sm">
                                {formatTime(currentTime)} / {formatTime(duration)}
                            </div>
                        </div>

                        <div className="flex items-center space-x-3">
                            <button
                                onClick={toggleMute}
                                className="text-white hover:text-blue-400 transition-colors"
                            >
                                {isMuted ? (
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.793L4.828 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.828l3.555-3.793A1 1 0 019.383 3.076zM12.293 7.293a1 1 0 011.414 0L15 8.586l1.293-1.293a1 1 0 111.414 1.414L16.414 10l1.293 1.293a1 1 0 01-1.414 1.414L15 11.414l-1.293 1.293a1 1 0 01-1.414-1.414L13.586 10l-1.293-1.293a1 1 0 010-1.414z" clipRule="evenodd" />
                                    </svg>
                                ) : (
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.793L4.828 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.828l3.555-3.793A1 1 0 019.383 3.076zM12 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm4-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                                    </svg>
                                )}
                            </button>

                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={isMuted ? 0 : volume * 100}
                                onChange={handleVolumeChange}
                                className="w-20 h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer hover:bg-gray-500 transition-colors"
                                style={{
                                    background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${isMuted ? 0 : volume * 100}%, #4b5563 ${isMuted ? 0 : volume * 100}%, #4b5563 100%)`
                                }}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}