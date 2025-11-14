import { defineConfig } from 'wxt';
import fs from 'fs';

// See https://wxt.dev/api/config.html
export default defineConfig({
  modules: ['@wxt-dev/module-react'],
  srcDir: 'src',
  manifest: ({ browser, manifestVersion, mode, command }) => {
  return {
    permissions: [
      'storage'
    ]
  };
},
});

