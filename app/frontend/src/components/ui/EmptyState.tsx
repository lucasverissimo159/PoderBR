
import { Database } from "lucide-react";

interface EmptyStateProps {
  title?: string;
  message?: string;
}

export function EmptyState({ title = "No data found", message = "There is no data available for the selected parameters." }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-12 min-h-[300px] border border-border rounded-md bg-surface text-center">
      <Database className="w-10 h-10 text-text-secondary mb-4 opacity-50" aria-hidden="true" />
      <h3 className="text-lg font-semibold text-text-primary mb-2">{title}</h3>
      <p className="text-text-secondary max-w-md">{message}</p>
    </div>
  );
}
