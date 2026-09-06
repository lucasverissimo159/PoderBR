import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { MainLayout } from "./components/layout/MainLayout";
import Dashboard from "./pages/Dashboard";
import Comparison from "./pages/Comparison";

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <Dashboard />,
      },
      {
        path: "comparison",
        element: <Comparison />,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
