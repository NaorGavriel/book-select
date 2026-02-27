import { useNavigate } from "react-router-dom";
import LogoutButton from "../components/LogoutButton";
import LandingPageButton from "../components/LandingPageButton";
/**
 * HomePage
 * --------
 * Main authenticated landing page.
 *
 * Provides navigation to core user features:
 * 1. Upload picture
 * 2. View past recommendations
 * 3. Add book to reading history
 *
 * Assumes route is protected by RequireAuth.
 */
export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div>
      <LogoutButton/>
      <LandingPageButton/>
      <h2>Home</h2>

      <button onClick={() => navigate("/upload")}>
        Upload Picture
      </button>

      <br /><br />

      <button onClick={() => navigate("/recommendations")}>
        View Past Recommendations
      </button>

      <br /><br />

      <button onClick={() => navigate("/reading-history")}>
        Add Book to Reading History
      </button>
    </div>
  );
}