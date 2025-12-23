import { Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "../components/AppLayout";
import { CollaboratorsPage } from "../../pages/Collaborators";
import { HomePage } from "../../pages/Home";
import { MissionDetailsPage } from "../../pages/MissionDetails";
import { MissionsPage } from "../../pages/Missions";
import { NotFoundPage } from "../../pages/NotFound";
import { PlanningPage } from "../../pages/Planning";
import { SettingsPage } from "../../pages/Settings";

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/app/planning" replace />} />
      <Route path="/app" element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="planning" element={<PlanningPage />} />
        <Route path="projects/:projectId/missions" element={<MissionsPage />} />
        <Route path="projects/:projectId/missions/:missionId" element={<MissionDetailsPage />} />
        <Route path="collaborators" element={<CollaboratorsPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};
