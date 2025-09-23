import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import router from "./router";

import "./index.css";
import "./App.css";
import { ThemeProvider } from "./components/theme-provider";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Elemento 'root' não encontrado no DOM.");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <RouterProvider router={router} />
    </ThemeProvider>
  </React.StrictMode>
);
