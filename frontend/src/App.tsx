import { Route, Routes } from "react-router-dom";
import { DbStatusBanner } from "./components/layout/DbStatusBanner";
import { NavBar } from "./components/layout/NavBar";
import { HomePage } from "./pages/HomePage";
import { PeoplePage } from "./pages/PeoplePage";
import { PersonDetailPage } from "./pages/PersonDetailPage";
import { ProjectDetailPage } from "./pages/ProjectDetailPage";
import { ProjectsPage } from "./pages/ProjectsPage";
import { StaffingPage } from "./pages/StaffingPage";

export default function App() {
  return (
    <div className="app-shell">
      <NavBar />
      <DbStatusBanner />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/people" element={<PeoplePage />} />
        <Route path="/people/:personId" element={<PersonDetailPage />} />
        <Route path="/projects" element={<ProjectsPage />} />
        <Route path="/projects/:projectId" element={<ProjectDetailPage />} />
        <Route path="/staffing" element={<StaffingPage />} />
      </Routes>
    </div>
  );
}
