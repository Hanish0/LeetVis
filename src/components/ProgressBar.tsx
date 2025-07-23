'use client';

import { useEffect, useState, useMemo } from 'react';

interface ProgressBarProps {
  isGenerating: boolean;
  onComplete?: () => void;
}

export default function ProgressBar({ isGenerating, onComplete }: ProgressBarProps) {
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState('');

  const steps = useMemo(() => [
    { label: 'Parsing problem...', duration: 2000 },
    { label: 'Generating solution...', duration: 3000 },
    { label: 'Creating Manim script...', duration: 2500 },
    { label: 'Rendering video...', duration: 4000 },
    { label: 'Finalizing...', duration: 1000 }
  ], []);

  useEffect(() => {
    if (!isGenerating) {
      setProgress(0);
      setCurrentStep('');
      return;
    }

    let currentStepIndex = 0;
    let totalElapsed = 0;
    const totalDuration = steps.reduce((sum, step) => sum + step.duration, 0);

    const updateProgress = () => {
      if (currentStepIndex >= steps.length) {
        setProgress(100);
        setCurrentStep('Complete!');
        onComplete?.();
        return;
      }

      const currentStepData = steps[currentStepIndex];
      setCurrentStep(currentStepData.label);

      const stepProgress = Math.min(100, (totalElapsed / totalDuration) * 100);
      setProgress(stepProgress);

      totalElapsed += 100;

      if (totalElapsed >= currentStepData.duration) {
        currentStepIndex++;
        totalElapsed = 0;
      }
    };

    const interval = setInterval(updateProgress, 100);

    return () => clearInterval(interval);
  }, [isGenerating, onComplete, steps]);

  if (!isGenerating && progress === 0) {
    return null;
  }

  return (
    <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6 mb-8">
      <div className="text-center mb-4">
        <div className="text-blue-800 dark:text-blue-200 font-medium mb-2">
          {currentStep || 'Preparing...'}
        </div>
        <div className="text-sm text-blue-600 dark:text-blue-400">
          {Math.round(progress)}% complete
        </div>
      </div>
      
      <div className="w-full bg-blue-200 dark:bg-blue-800 rounded-full h-3 mb-4">
        <div 
          className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>
      
      <div className="flex justify-center">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
      </div>
    </div>
  );
}