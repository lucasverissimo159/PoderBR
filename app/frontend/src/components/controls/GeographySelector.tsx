

export interface GeographyOption {
  id: string;
  name: string;
}

interface GeographySelectorProps {
  value: string;
  onChange: (value: string) => void;
  options?: GeographyOption[];
}

const DEFAULT_OPTIONS: GeographyOption[] = [
  { id: "BR", name: "Brazil (National)" },
  { id: "SP", name: "São Paulo" },
];

export function GeographySelector({ value, onChange, options = DEFAULT_OPTIONS }: GeographySelectorProps) {
  return (
    <div className="flex flex-col space-y-1.5">
      <label htmlFor="geography-select" className="text-sm font-medium text-text-primary">
        Geography
      </label>
      <select
        id="geography-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full max-w-xs px-3 py-2 bg-surface border border-border rounded-md shadow-sm focus-ring text-text-primary text-sm"
      >
        {options.map((opt) => (
          <option key={opt.id} value={opt.id}>
            {opt.name}
          </option>
        ))}
      </select>
    </div>
  );
}
