import { createBrowserRouter } from "react-router-dom";

import Layout from "./components/layout";

import HomePage from "./screens/home";
import LoginPage from "./screens/login-page";
import RegisterPage from "./screens/register-page";
import ProfilePage from "./screens/profile-page";
import NotFound from "./screens/error-page";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />, // O Layout é o elemento pai
    errorElement: <NotFound />, // Opcional: uma página para erros
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "login",
        element: <LoginPage />,
      },
      {
        path: "register",
        element: <RegisterPage />,
      },
      {
        path: "profile",
        element: <ProfilePage />,
      },
    ],
  },
]);

export default router;
