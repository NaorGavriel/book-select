import useAxios from "../../../api/useAxios";
import { useAuth } from "../AuthContext";
import { useNavigate } from "react-router-dom";

/**
 * LogoutButton
 *
 * - sends logout request to backend,
 * - clears access token from client state,
 * - redirects user to login page.
 */
export default function LogoutButton() {
  const api = useAxios();
  const { setAccessToken } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      // Invalidate refresh cookie server-side
      await api.post("/logout");
    } catch (err) {

    } finally {
      // Clear access token from memory
      setAccessToken(null);
      navigate("/");
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="bg-red-600 text-white px-4 py-2 rounded"
    >
      Logout
    </button>
  );
}