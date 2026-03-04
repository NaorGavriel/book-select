import { useNavigate } from "react-router-dom";

/**
 * HomeButton
 * ----------
 * Navigates the user back to the main Home page.
 */
export default function HomeButton() {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate("/home")}
      className="mt-4 px-5 py-2.5 rounded-lg bg-neutral-800 text-white 
                 font-medium hover:bg-neutral-700 transition"
    >
      Go to Home
    </button>
  );
}