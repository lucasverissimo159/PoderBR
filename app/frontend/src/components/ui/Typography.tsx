
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function PageTitle({ children, className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h1 className={cn("text-3xl font-bold tracking-tight text-text-primary mb-4", className)} {...props}>
      {children}
    </h1>
  );
}

export function SectionTitle({ children, className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h2 className={cn("text-xl font-semibold text-text-primary mb-3", className)} {...props}>
      {children}
    </h2>
  );
}

export function Text({ children, className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p className={cn("text-base text-text-secondary mb-4 leading-relaxed", className)} {...props}>
      {children}
    </p>
  );
}
