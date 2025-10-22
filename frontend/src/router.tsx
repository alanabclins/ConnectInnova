import { createBrowserRouter, replace } from "react-router-dom";

import LoginPage from "./screens/login-page";
import RegisterPage from "./screens/register-page";
import ProfilePage from "./screens/profile-page";
import NotFound from "./screens/error-page";
import ProjUserStories from "./screens/proj-history-page";
import SummaryPage from "./screens/sumary-page";
import Home from "./screens/home";
import MyProjects from "./screens/my-projects-page";
import ProtectedRoute from "./components/protectedRouter";
import RootRedirect from "./components/root-redirect";
import authService from "@/services/auth.service";
import DashboardPage from "./screens/dashboard-page";

const redirectIfLoggedIn = () => {
  if (authService.isAuthenticated()) {
    return replace("/home");
  }
  return null;
};

const router = createBrowserRouter([
  // Rotas públicas
  {
    path: "/",
    element: <RootRedirect />,
    errorElement: <NotFound />,
  },
  {
    path: "login",
    element: <LoginPage />,
    loader: redirectIfLoggedIn,
    errorElement: <NotFound />,
  },
  {
    path: "register",
    element: <RegisterPage />,
    errorElement: <NotFound />,
  },

  // Rotas privadas
  {
    path: "home",
    element: (
      <ProtectedRoute>
        <Home />
      </ProtectedRoute>
    ),
    errorElement: <NotFound />,
    children: [
      {
        index: true,
        element: <MyProjects />,
      },
      {
        path: "project-stories",
        element: <ProjUserStories />,
      },
      {
        path: "profile",
        element: <ProfilePage />,
      },
      {
        path: "summary",
        element: <SummaryPage />,
      },
      {
        path: "dashboard",
        element: <DashboardPage />,
      },
    ],
  },
]);

export default router;
