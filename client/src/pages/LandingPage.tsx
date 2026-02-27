import { useNavigate } from "react-router-dom";
/**
 * LandingPage
 * --------
 */
export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div>
      <button onClick={() => navigate("/login")}>
        Login
      </button>

      <br /><br />

      <button onClick={() => navigate("/register")}>
        Register
      </button>

      <br /><br />
    </div>
  );
}