import { Route, Routes } from "react-router-dom";

import { PlaceholderPage } from "../../pages/Placeholder";

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<PlaceholderPage />} />
      <Route path="*" element={<PlaceholderPage />} />
    </Routes>
  );
};
