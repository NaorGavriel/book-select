import { useNavigate } from "react-router-dom";

/**
 * HomeButton
 * ----------
 * Navigates the user back to the main Home page.
 */
export default function HomeButton() {
  const navigate = useNavigate();

  return (
    <button onClick={() => navigate("/home")}>
      Home
    </button>
  );
}