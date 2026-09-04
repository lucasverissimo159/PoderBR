

export interface IncomeBasisOption {
  id: string;
  name: string;
}

interface IncomeBasisSelectorProps {
  value: string;
  onChange: (value: string) => void;
  options?: IncomeBasisOption[];
}

const DEFAULT_OPTIONS: IncomeBasisOption[] = [
  { id: "minimum_wage", name: "National Minimum Wage" },
  { id: "average", name: "Average Regional Income" },
];

export function IncomeBasisSelector({ value, onChange, options = DEFAULT_OPTIONS }: IncomeBasisSelectorProps) {
  return (
    <div className="flex flex-col space-y-1.5">
      <label htmlFor="income-basis-select" className="text-sm font-medium text-text-primary">
        Income Basis
      </label>
      <select
        id="income-basis-select"
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
