import React from "react";

interface CircularStepIndicatorProps {
  currentStep: number;
  totalSteps: number;
}

export const CircularStepIndicator: React.FC<CircularStepIndicatorProps> = ({
  currentStep,
  totalSteps,
}) => {
  const progress = (currentStep / totalSteps) * 100;
  const circumference = 2 * Math.PI * 26; // radius of 26
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative w-20 h-20">
      <svg
        className="w-full h-full -rotate-90"
        viewBox="0 0 60 60"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Background circle */}
        <circle
          cx="30"
          cy="30"
          r="26"
          stroke="hsl(var(--muted))"
          strokeWidth="3"
          fill="hsl(var(--step-indicator-bg))"
        />
        {/* Progress circle */}
        <circle
          cx="30"
          cy="30"
          r="26"
          stroke="hsl(var(--step-indicator-progress))"
          strokeWidth="3"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          className="transition-all duration-500 ease-out"
        />
      </svg>
      {/* Step number */}
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-foreground font-medium text-lg">
          {currentStep.toString().padStart(2, "0")}
        </span>
      </div>
    </div>
  );
};
