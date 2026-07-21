import react from '@vitejs/plugin-react';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  base: '/', // custom-domain root site (research.fasl-work.com)
  plugins: [react()],
  test: { environment: 'node', globals: true },
});
