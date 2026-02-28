import { useState } from "react";
import AddBookModal from "../features/reading_history/components/AddBookModal";
import ReadingHistoryHeader from "../features/reading_history/components/ReadingHistoryHeader";
import { useReadingHistory } from "../features/reading_history/hooks/useReadingHistory";
import AddBookPanel from "../features/reading_history/components/AddBookPanel";
import SectionDivider from "../components/ui/SectionDivider";
import BookList from "../features/reading_history/components/BookList";
/**
 * ReadingHistoryPage
 *
 * Displays the user's reading history.
 * Allows adding new books via a modal.
 * Fetches data from `/user_books/` on mount.
 */
export default function ReadingHistoryPage() {
  const { books, loading, error, refresh } = useReadingHistory();
  const [isModalOpen, setIsModalOpen] = useState(false);


  return (
       <div className="min-h-[calc(100vh-140px)] bg-linear-to-b from-neutral-100 to-slate-100 px-6 py-16">

      <ReadingHistoryHeader />

      <AddBookPanel onClick={() => setIsModalOpen(true)} />

      <SectionDivider />

      {loading && <p className="text-center">Loading books...</p>}
      {error && <p className="text-center text-red-500">{error}</p>}

      {!loading && !error && <BookList books={books} />}

      <AddBookModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onBookAdded={refresh}
      />
    </div>
  );
}