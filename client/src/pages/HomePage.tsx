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
            Discover Your Next Great Book
          </h2>

          <p className="text-neutral-600 mt-2">
            Upload a photo of a bookshelf and find out which books match your reading taste.
          </p>
      </div>

      {/* Action Panels */}
      <div className="max-w-5xl mx-auto space-y-6">

        <ActionPanel
          title="Scan a Bookshelf"
          description="Upload a bookshelf photo and see which books match your taste."
          onClick={() => navigate("/upload")}
          backgroundImage={BookShelfImage}
          highlight
        />

        <ActionPanel
          title="View Recommendations"
          description="View your previous recommendations and matched books."
          onClick={() => navigate("/recommendations")}
        />

        <ActionPanel
          title="Update Your Reading History"
          description="Add books you've read to improve your recommendations."
          onClick={() => navigate("/reading-history")}
        />

      </div>
    </div>
  );
}

