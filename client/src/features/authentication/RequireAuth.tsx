import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./AuthContext";

/**
 * RequireAuth
 * -----------
 * If user is not authenticated redirect to /login 
 * If authenticated renders the protected route
 */
export default function RequireAuth() {
  const { accessToken } = useAuth();

  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}