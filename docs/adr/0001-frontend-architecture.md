# ADR 0001: Frontend Architecture and Design System

## Status
Accepted

## Context
PoderBR is a public analytics platform aimed at explaining how income and prices affect purchasing power. The product demands an analytical-first interface prioritizing readability, data transparency, and strict accessibility standards (WCAG 2.2 AA). The MVP requires presenting data visualizations (charts) and tabular data with configurable controls for geography, date, and income basis.

The architecture must support:
- Deterministic and rerunnable transformations (via backend APIs).
- Progressive disclosure of methodologies and data provenance.
- Handling data gaps explicitly (no silent interpolations).
- Complex state management for filters and asynchronous API calls.

## Decision

We will implement a minimal, coherent frontend stack based on the following tools:

### 1. Structure: React + Vite + TypeScript
- **React**: Provides a robust, component-driven UI paradigm.
- **Vite**: Offers extremely fast cold starts, hot module replacement, and a leaner build process compared to Webpack or Create React App.
- **TypeScript**: Ensures type safety across the frontend-backend boundary, directly mapping to the JSON schemas defined in `FRONTEND_BACKEND_CONTRACT.md`.

### 2. Styling & Layout: Tailwind CSS
- **Tailwind CSS**: Utility-first CSS framework allows rapid prototyping and guarantees consistency in layout, typography, and spacing without maintaining separate CSS files. We will build semantic utility classes mapping to our design constraints.

### 3. Data Fetching & Cache: React Query (TanStack Query)
- **React Query**: Handles asynchronous state, caching, background updates, and error handling seamlessly. Since data updates infrequently (relying heavily on HTTP caching), React Query simplifies fetching from our synchronous FastAPI backend while cleanly managing loading/error/partial data states.

### 4. Charting: Recharts
- **Recharts**: A composable charting library built on React components. It is declarative, supports responsive containers, and allows easy customization of tooltips and axes to handle edge cases like missing data points (null values) natively, aligning with our strict "no interpolation" rule.

### 5. Routing: React Router
- **React Router**: Essential for managing URL state (e.g., sharing links to specific geographic views or historical periods). We will use a minimal routing setup to map URLs to specific dashboard configurations.

### 6. Accessibility (a11y) & Design System Strategy
To meet WCAG 2.2 AA requirements:
- **Semantic Structure**: Proper use of `<main>`, `<nav>`, `<header>`, and `<footer>`.
- **Keyboard Navigation**: All interactive elements (selectors, buttons) will be focusable and operable via keyboard.
- **Accessible Charts**: Recharts outputs SVG, which is inherently inaccessible to screen readers. We will implement an `<AccessibleChart />` wrapper convention. Every chart will be paired with a visually hidden (or togglable) semantic HTML `<table />` containing the exact same data.
- **Focus & Contrast**: Custom Tailwind variants for focus states (`focus-visible:ring`) and strict adherence to a high-contrast color palette.
- **Forms/State**: Use native HTML forms elements with explicit `<label>` associations for controls (Geography, Income Basis).
- **Reduced Motion**: Respect `@media (prefers-reduced-motion)` for any transitions or chart animations.

## Consequences
- **Positive**: High developer velocity, type safety across the stack, and strict adherence to accessibility from day one.
- **Negative**: Adds a build step and JS dependency overhead compared to a purely server-rendered template approach, but necessary for the highly interactive and chart-heavy nature of the analytics dashboard.
