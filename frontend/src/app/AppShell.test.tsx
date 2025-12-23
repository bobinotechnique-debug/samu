import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";

import { AppShell } from "./AppShell";
import { QueryProvider } from "./providers/QueryProvider";

describe("AppShell", () => {
  it("renders planning page by default", () => {
    render(
      <BrowserRouter>
        <QueryProvider>
          <AppShell />
        </QueryProvider>
      </BrowserRouter>
    );

    expect(screen.getByRole("heading", { name: /planning/i })).toBeInTheDocument();
  });
});
