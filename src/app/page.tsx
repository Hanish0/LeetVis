'use client';

import { useState } from 'react';

export default function Home() {
  const [problemTitle, setProblemTitle] = useState('');
  const [language, setLanguage] = useState('python');
  const [showVideoButtons, setShowVideoButtons] = useState(false);

  const handleInputChange = (title: string, lang: string) => {
    setProblemTitle(title);
    setLanguage(lang);
    // Show video type buttons when both title and language are selected
    setShowVideoButtons(title.trim() !== '' && lang !== '');
  };

  const handleVideoTypeClick = (videoType: string) => {
    console.log(`Generating ${videoType} video for "${problemTitle}" in ${language}`);
    // TODO: Implement video generation logic
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
          </div>

          {/* Input Form */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
            <div className="space-y-6">
              {/* Problem Title Input */}
              <div>
                <label htmlFor="problem-title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  LeetCode Problem Title
                </label>
                <input
                  id="problem-title"
                  type="text"
                  value={problemTitle}
                  onChange={(e) => handleInputChange(e.target.value, language)}
                  placeholder="e.g., Two Sum, Valid Parentheses, etc."
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
              </div>

              {/* Language Dropdown */}
              <div>
                <label htmlFor="language" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Programming Language
                </label>
                <select
                  id="language"
                  value={language}
                  onChange={(e) => handleInputChange(problemTitle, e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  <option value="python">Python</option>
                  <option value="java">Java</option>
                  <option value="cpp">C++</option>
                </select>
              </div>
            </div>
          </div>

          {/* Video Type Buttons */}
          {showVideoButtons && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 text-center">
                Choose Video Type
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => handleVideoTypeClick('explanation')}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-4 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Problem Explanation
                </button>
                <button
                  onClick={() => handleVideoTypeClick('brute_force')}
                  className="bg-green-600 hover:bg-green-700 text-white font-medium py-4 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                >
                  Brute Force
                </button>
                <button
                  onClick={() => handleVideoTypeClick('optimal')}
                  className="bg-purple-600 hover:bg-purple-700 text-white font-medium py-4 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                >
                  Optimal Solution
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
