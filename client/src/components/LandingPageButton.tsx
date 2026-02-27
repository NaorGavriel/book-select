import { useNavigate } from "react-router-dom";

/**
 * LandingPageButton
 * ----------
 * Navigates the user back to the Landing page.
 */
export default function LandingPageButton() {
  const navigate = useNavigate();

  return (
    <button onClick={() => navigate("/")}>
      Back
    </button>
  );
}