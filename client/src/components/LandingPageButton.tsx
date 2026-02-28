import { useNavigate } from "react-router-dom";

/**
 * LandingPageButton
 * ----------
 * Navigates the user back to the Landing page.
 */
export default function LandingPageButton() {
    const navigate = useNavigate();
    return (
        <button
                onClick={() => navigate("/")}
                className="px-8 py-3 text-base font-medium rounded-full
                        bg-amber-400 text-amber-700 
                        hover:bg-violet-200 hover:text-violet-500 transition shadow-sm"
            >
                Back
        </button>
    );
}