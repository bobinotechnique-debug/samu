import { Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "./AppLayout";
import { CollaboratorsPage } from "../../pages/CollaboratorsPage";
import { MissionDetailsPage } from "../../pages/MissionDetailsPage";
import { MissionListPage } from "../../pages/MissionListPage";
import { NotFoundPage } from "../../pages/NotFoundPage";
import { PlanningPage } from "../../pages/PlanningPage";
import { SettingsPage } from "../../pages/SettingsPage";

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/app/planning" replace />} />
      <Route path="/app" element={<AppLayout />}>
        <Route path="planning" element={<PlanningPage />} />
        <Route path="projects/:projectId/missions" element={<MissionListPage />} />
        <Route path="projects/:projectId/missions/:missionId" element={<MissionDetailsPage />} />
        <Route path="collaborators" element={<CollaboratorsPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};
