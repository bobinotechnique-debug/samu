import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { AppRoutes } from "../routes";

const renderWithRouter = (initialEntry: string) =>
  render(
    <MemoryRouter initialEntries={[initialEntry]}>
      <AppRoutes />
    </MemoryRouter>
  );

describe("AppRoutes", () => {
  it("renders planning page by default", () => {
    renderWithRouter("/");

    expect(screen.getByRole("heading", { name: /planning/i })).toBeInTheDocument();
  });

  it("renders mission details route", () => {
    renderWithRouter("/app/projects/demo/missions/123");

    expect(screen.getByRole("heading", { name: /mission details/i })).toBeInTheDocument();
  });

  it("renders not found for unknown routes", () => {
    renderWithRouter("/unknown");

    expect(screen.getByRole("heading", { name: /page not found/i })).toBeInTheDocument();
  });
});
