

interface DateSelectorProps {
  label: string;
  value?: string;
  onChange: (value: string) => void;
  id: string;
}

export function DateSelector({ label, value, onChange, id }: DateSelectorProps) {
  return (
    <div className="flex flex-col space-y-1.5">
      <label htmlFor={id} className="text-sm font-medium text-text-primary">
        {label}
      </label>
      <input
        type="date"
        id={id}
        value={value || ""}
        onChange={(e) => onChange(e.target.value)}
        className="w-full max-w-xs px-3 py-2 bg-surface border border-border rounded-md shadow-sm focus-ring text-text-primary text-sm"
      />
    </div>
  );
}
