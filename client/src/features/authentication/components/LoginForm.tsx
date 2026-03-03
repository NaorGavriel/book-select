import { useState, useEffect } from "react";
import api from "../../../api/axiosPrivate";
import { useAuth } from "../AuthContext";
import { useNavigate, useLocation } from "react-router-dom";

/**
  * LoginForm
  * ---------
  * Authenticates the user and initializes the session.
  * Sends credentials to /token, access token saved in memory inside AuthContext
  * refresh token stored as cookie
  */
export default function LoginForm() {
    const { accessToken, setAccessToken } = useAuth();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/home";

    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    useEffect(() => {
        if (accessToken) {
            navigate(from, {replace : true}); // navigating to the previous route /home if there isn't one
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
        <div className="space-y-6">
        <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
            Email
            </label>
            <input
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-lg border border-neutral-300 px-4 py-3
                        focus:outline-none focus:ring-2 focus:ring-emerald-500
                        focus:border-transparent transition"
            />
        </div>
        
        <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
            Password
            </label>
            <input
            placeholder="••••••••"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-lg border border-neutral-300 px-4 py-3
                        focus:outline-none focus:ring-2 focus:ring-emerald-500
                        focus:border-transparent transition"
            />
        </div>
        

        <button onClick={handleLogin}
            className="w-full rounded-full bg-emerald-600 text-white
                    py-3 font-medium hover:bg-emerald-700
                    transition shadow-sm">
            Sign In
        </button>


        {/* Register Link */}
        <p className="text-center text-sm text-neutral-600">
            Don’t have an account?{" "}
            <button
            type="button"
            onClick={() => navigate("/register")}
            className="text-emerald-600 hover:underline font-medium"
            >
            Create one
            </button>
        </p>
        
        </div>
    );
}