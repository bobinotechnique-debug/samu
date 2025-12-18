import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import { AppShell } from "./app/AppShell";
import { QueryProvider } from "./app/providers/QueryProvider";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <BrowserRouter>
      <QueryProvider>
        <AppShell />
      </QueryProvider>
    </BrowserRouter>
  </React.StrictMode>
);
