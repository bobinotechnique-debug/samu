import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { AppShell } from "../../frontend/src/app/AppShell";
import { QueryProvider } from "../../frontend/src/app/providers/QueryProvider";

describe("AppShell (cross-repo)", () => {
  it("renders the placeholder heading", () => {
    render(
      <MemoryRouter>
        <QueryProvider>
          <AppShell />
        </QueryProvider>
      </MemoryRouter>
    );

    expect(screen.getByText(/Org context console/i)).toBeInTheDocument();
  });
});
