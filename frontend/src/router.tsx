import { createBrowserRouter } from "react-router-dom";

import LoginPage from "./screens/login-page";
import RegisterPage from "./screens/register-page";
import ProfilePage from "./screens/profile-page";
import NotFound from "./screens/error-page";
import ProjUserStories from "./screens/proj-history-page";
import SummaryPage from "./screens/sumary-page";
import Home from "./screens/home";
import MyProjects from "./screens/my-projects-page";

const router = createBrowserRouter([
  // Rotas públicas (sem layout)
  {
    path: "login",
    element: <LoginPage />,
  },
  {
    path: "register",
    element: <RegisterPage />,
  },

  // Rotas privadas (com HomeLayout)
  {
    path: "/",
    element: <Home />,
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
    ],
  },
]);

export default router;
