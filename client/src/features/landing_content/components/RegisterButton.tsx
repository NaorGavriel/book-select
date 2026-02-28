import { useNavigate } from "react-router";

export default function RegisterButton() {
    const navigate = useNavigate();
    return (
        <button
                onClick={() => navigate("/register")}
                className="px-8 py-3 text-base font-medium rounded-full 
                        bg-violet-600 text-white border border-slate-100
                        hover:bg-amber-300 transition shadow-sm"
            >
                Get Started
        </button>
    );
}