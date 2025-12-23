import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

import { AppShell } from "./AppShell";
import { QueryProvider } from "./providers/QueryProvider";

describe("AppShell", () => {
  it("renders placeholder page", () => {
    render(
      <BrowserRouter>
        <QueryProvider>
          <AppShell />
        </QueryProvider>
      </BrowserRouter>
    );

    expect(screen.getByText(/Org context console/)).toBeInTheDocument();
  });
});
