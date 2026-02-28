import { useNavigate } from "react-router";

export default function LoginButton() {
    const navigate = useNavigate();
    return (
            <button
                onClick={() => navigate("/login")}
                className="px-8 py-3 text-base font-medium rounded-2xl 
                        bg-amber-300 text-black
                        hover:bg-violet-600 hover:text-white transition"
            >
                Login
            </button>
    );
}