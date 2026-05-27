import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./AuthContext";

/**
 * RequireAdmin
 * ------------
 * Requires the authenticated user to have is_admin === true.
 * Redirects non-admins to /home.
 */
export default function RequireAdmin() {
  const { isAdmin } = useAuth();

  if (!isAdmin) {
    return <Navigate to="/home" replace />;
  }

  return <Outlet />;
}
