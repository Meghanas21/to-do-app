import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Dev server runs on port 5173 by default — this MUST match one of the
// origins listed in the backend's CORS_ORIGINS env var.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
