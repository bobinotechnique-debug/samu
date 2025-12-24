import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { AppShell } from "./AppShell";
import { QueryProvider } from "./providers/QueryProvider";

describe("AppShell", () => {
  it("renders planning page by default", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <QueryProvider>
          <AppShell />
        </QueryProvider>
      </MemoryRouter>
    );

    expect(screen.getByRole("heading", { name: /planning/i })).toBeInTheDocument();
  });
});
