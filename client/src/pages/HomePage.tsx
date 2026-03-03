import { useNavigate } from "react-router-dom";
import ActionPanel from "../components/ui/ActionPanel";
import BookShelfImage from "../assets/marialaura-gionfriddo-50G3FvyQxX0-unsplash.jpg"
/**
 * HomePage
 * --------
 * Main authenticated landing page.
 *
 * Provides navigation to core user features:
 * 1. Upload picture
 * 2. View past recommendations
 * 3. Add book to reading history
 */
export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-linear-to-t from-violet-300 from-0% via-amber-100 via-50% to-stone-100 to-80% px-6 py-16">
      
      {/* Header */}
      <div className="max-w-5xl mx-auto mb-16">
        <h2 className="text-4xl font-semibold tracking-tight text-black">
          Welcome back
        </h2>
      </div>

      {/* Action Panels */}
      <div className="max-w-5xl mx-auto space-y-6">

        <ActionPanel
          title="Upload Picture"
          description="Upload a photo of books you're considering and receive intelligent, tailored recommendations."
          onClick={() => navigate("/upload")}
          backgroundImage={BookShelfImage}
          highlight
        />

        <ActionPanel
          title="View Past Recommendations"
          description="Revisit previously generated suggestions and explore your recommendation history."
          onClick={() => navigate("/recommendations")}
        />

        <ActionPanel
          title="Add Book to Reading History"
          description="Log books you've read to continuously improve your recommendation accuracy."
          onClick={() => navigate("/reading-history")}
        />

      </div>
    </div>
  );
}

