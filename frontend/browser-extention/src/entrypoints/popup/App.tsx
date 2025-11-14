import { Routes, Route, Navigate } from 'react-router-dom';
import Auth from '../../pages/Auth';
import {useAuth } from "../../core/AuthContext";
import Home from '../../pages/protected/Home';

export default function App() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/Auth" element={<Auth />} />
      <Route
        path="/"
        element={
          user ? <Home /> : <Navigate to="/Auth" replace />
        }
        />

      <Route path="*" element={<Navigate to="/" replace />} />

    </Routes>
  );
}