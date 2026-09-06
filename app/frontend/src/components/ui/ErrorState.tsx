
import { AlertCircle } from "lucide-react";

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export function ErrorState({ title = "Something went wrong", message = "We encountered an error loading this data.", onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-12 min-h-[300px] bg-error-bg border border-error/20 rounded-md" role="alert">
      <AlertCircle className="w-10 h-10 text-error mb-4" aria-hidden="true" />
      <h3 className="text-lg font-semibold text-error mb-2">{title}</h3>
      <p className="text-error/80 text-center mb-6 max-w-md">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-error text-white rounded-md font-medium focus-ring hover:bg-error/90 transition-colors"
        >
          Try Again
        </button>
      )}
    </div>
  );
}
