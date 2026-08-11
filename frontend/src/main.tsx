import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { AppStatusProvider } from "./context/AppStatusContext";
import "./styles/index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <AppStatusProvider>
        <App />
      </AppStatusProvider>
    </BrowserRouter>
  </StrictMode>,
);
