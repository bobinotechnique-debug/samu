import path from "path";
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      react: path.resolve(__dirname, "node_modules/react"),
      "react-dom": path.resolve(__dirname, "node_modules/react-dom"),
      "react/jsx-runtime": path.resolve(__dirname, "node_modules/react/jsx-runtime.js"),
      "react/jsx-dev-runtime": path.resolve(__dirname, "node_modules/react/jsx-dev-runtime.js"),
      "@testing-library/react": path.resolve(
        __dirname,
        "node_modules/@testing-library/react"
      ),
      "@testing-library/jest-dom": path.resolve(
        __dirname,
        "node_modules/@testing-library/jest-dom"
      ),
      "react-router-dom": path.resolve(
        __dirname,
        "node_modules/react-router-dom"
      ),
      "@tanstack/react-query": path.resolve(
        __dirname,
        "node_modules/@tanstack/react-query"
      ),
    },
  },
  server: {
    fs: {
      allow: [".."],
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/test/setupTests.ts"],
    include: [
      "src/**/*.{test,spec}.{ts,tsx}",
      "../tests/frontend/**/*.{test,spec}.{ts,tsx}",
    ],
    deps: {
      moduleDirectories: [
        path.resolve(__dirname, "node_modules"),
        path.resolve(__dirname, "../node_modules"),
      ],
    },
  },
});
