import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    watch: {
      usePolling: true, // Ensures file changes are detected inside Docker
    },
    host: "0.0.0.0", // Allows access from outside the container
    strictPort: true,
    port: 5173,
  },
});
