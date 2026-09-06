
import { Link, Outlet } from "react-router-dom";

export function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-surface border-b border-border shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="focus-ring rounded-sm">
              <h1 className="text-xl font-bold text-primary">PoderBR</h1>
            </Link>
            <nav aria-label="Main Navigation" className="flex space-x-4">
              <Link
                to="/"
                className="text-text-secondary hover:text-primary font-medium focus-ring rounded-sm px-2 py-1"
              >
                Dashboard
              </Link>
              <Link
                to="/comparison"
                className="text-text-secondary hover:text-primary font-medium focus-ring rounded-sm px-2 py-1"
              >
                Comparison
              </Link>
            </nav>
          </div>
        </div>
      </header>

      <main id="main-content" className="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      <footer className="bg-surface border-t border-border mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-sm text-text-secondary text-center">
            PoderBR is an analytical platform for measuring purchasing power in Brazil.
          </p>
        </div>
      </footer>
    </div>
  );
}
