
import { Loader2 } from "lucide-react";

interface LoadingStateProps {
  message?: string;
}

export function LoadingState({ message = "Loading data..." }: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-12 min-h-[300px]" role="status" aria-live="polite">
      <Loader2 className="w-8 h-8 text-primary animate-spin mb-4" aria-hidden="true" />
      <p className="text-text-secondary">{message}</p>
    </div>
  );
}
