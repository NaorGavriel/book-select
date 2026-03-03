import { useState } from "react";
import api from "../../../api/axiosPrivate";
import { useNavigate } from "react-router";

/**
 * RegisterForm
 * ------------
 * Creates a new user account.
 * - Sends email and password to POST /register
 * - On success, redirects user to /login
 * - On failure, displays backend error message
 */
export default function RegisterForm() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async () => {
    setError("");

    try {
      await api.post("/users/", {
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
        <div className="space-y-6">
            <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                    Email
                </label>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full rounded-lg border border-neutral-300 px-4 py-3
                                focus:outline-none focus:ring-2 focus:ring-emerald-500
                                focus:border-transparent transition disabled:opacity-50"
                    placeholder="you@example.com"
                />
            </div>
            
        <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">
                Confirm Password
            </label>
            <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-neutral-300 px-4 py-3
                            focus:outline-none focus:ring-2 focus:ring-emerald-500
                            focus:border-transparent transition disabled:opacity-50"
            />
        </div>
      

      <button   onClick={handleRegister}
                className="w-full rounded-full bg-emerald-600 text-white
                            py-3 font-medium hover:bg-emerald-700
                            transition shadow-sm flex items-center justify-center
                            disabled:opacity-70 disabled:cursor-not-allowed">
        Create Account
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
    );
}