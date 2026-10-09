import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
export default defineConfig({
  site: 'https://insidelabs.cl',
  output: 'static',
  integrations: [react()],
  trailingSlash: 'never',
  server: { host: '0.0.0.0', port: 3000 },
});
