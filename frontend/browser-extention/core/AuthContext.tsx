import React, { createContext, useContext, useState, useEffect } from "react";
import { registerUser, loginUser } from "@/services/AuthService";



type User = { id: string; email: string };

type AuthContextType = {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: {
    name: string;
    email: string;
    password: string;
    location: string;
    phone: string;
  }) => Promise<void>;

  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");
    
    if (savedToken && savedUser){
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
  }, []);

  
  // Login function
  const login = async(email: string, password: string) => {
    const { access_token, user } = await loginUser({
      username: email,
      password: password,
     });
    localStorage.setItem("token", access_token);
    localStorage.setItem("user", JSON.stringify(user));
    setToken(access_token);
    setUser(user);
  };

  // Register function
  const register = async(data: {
    name: string;
    email: string;
    password: string;
    location: string;
    phone: string;
  }) => {
    await registerUser(data);
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    setToken(null);
  };


  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
