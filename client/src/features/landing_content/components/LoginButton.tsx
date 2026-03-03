import { useNavigate } from "react-router";

export default function LoginButton() {
    const navigate = useNavigate();
    return (
            <button
                onClick={() => navigate("/login")} 
                className="px-8 py-3 text-base font-medium rounded-full border-amber-300 border-2 text-white hover:bg-zinc-700 hover:text-white transition"
            >
                Login
            </button>
    );
}