import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import router from "./router";

import "./index.css";
import "./App.css";
import { ThemeProvider } from "./components/theme-provider";
import { AuthProvider } from "./auth/authContext";
import { Toaster } from "./components/ui/sonner";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Elemento 'root' não encontrado no DOM.");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <AuthProvider>
        <RouterProvider router={router} />
        <Toaster />
      </AuthProvider>
    </ThemeProvider>
  </React.StrictMode>
);
