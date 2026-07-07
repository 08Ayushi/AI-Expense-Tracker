import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// React dev server runs on port 5173 (matches backend CORS config).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
});
