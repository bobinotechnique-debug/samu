import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { AppRoutes } from "./index";

describe("AppRoutes", () => {
  it("redirects root to planning", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <AppRoutes />
      </MemoryRouter>
    );

    expect(screen.getByRole("heading", { name: /planning/i })).toBeInTheDocument();
  });

  it("renders mission details route", () => {
    render(
      <MemoryRouter initialEntries={["/app/projects/demo/missions/mission-42"]}>
        <AppRoutes />
      </MemoryRouter>
    );

    expect(screen.getByRole("heading", { name: /mission details/i })).toBeInTheDocument();
    expect(screen.getByText(/mission-42/i)).toBeInTheDocument();
  });

  it("renders not found for unknown routes", () => {
    render(
      <MemoryRouter initialEntries={["/unknown"]}>
        <AppRoutes />
      </MemoryRouter>
    );

    expect(screen.getByRole("heading", { name: /page not found/i })).toBeInTheDocument();
  });
});
