import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './style.css';

import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '@/core/AuthContext.tsx';

if (import.meta.env.DEV) {
  browser.runtime.sendMessage({ type: "get-dev-creds" }, (creds) => {
    if (creds?.access_token) {
      localStorage.setItem("token", creds.access_token);
      localStorage.setItem("user", JSON.stringify(creds.user));

      console.log("[DEV] Token + User loaded into localStorage from auth.json");
    }
  });
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
