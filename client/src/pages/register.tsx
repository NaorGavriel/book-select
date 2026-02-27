import { useState } from "react";
import api from "../api/axios";
import { useNavigate } from "react-router";
import LandingPageButton from "../components/LandingPageButton";

/**
 * RegisterPage
 * ------------
 * Creates a new user account.
 * - Sends email and password to POST /register
 * - On success, redirects user to /login
 * - On failure, displays backend error message
 */
export default function RegisterPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async () => {
    setError("");

    try {
      await api.post("/register", {
        email,
        password,
      });

      // After successful registration routing to login
      navigate("/login");

    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div>
      <LandingPageButton/>
      <h2>Register</h2>

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleRegister}>
        Register
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}