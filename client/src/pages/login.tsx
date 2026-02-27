import { useState, useEffect } from "react";
import api from "../api/axios";
import { useAuth } from "../features/authentication/AuthContext";
import { useNavigate } from "react-router-dom";
import LandingPageButton from "../components/LandingPageButton";
  /**
  * LoginPage
  * ---------
  * Authenticates the user and initializes the session.
  * Sends credentials to /token, access token saved in memory inside AuthContext
  * refresh token stored as cookie
  */
export default function LoginPage() {
  const { accessToken, setAccessToken } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    if (accessToken) {
      navigate("/home", { replace: true });
    }
  }, [accessToken]);

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(
        "/token",
        formData,
        { headers: { "Content-Type": "application/x-www-form-urlencoded", }
        ,});

      const { access_token } = response.data;

      // store token
      setAccessToken(access_token);
      
      console.log("Logged in!");
    } catch (err) {
      console.error("Login failed");
    }
  };

  return (
    <div>
      <LandingPageButton/>
      <h2>Login</h2>

      <input
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        placeholder="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>
    </div>
  );
}