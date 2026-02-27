import { useEffect, useState } from "react";
import useAxios from "../api/useAxios";
import HomeButton from "../components/HomeButton";
import AddBookModal from "../components/AddBookModal";
import BookCard from "../components/BookCard";
import type { UserBook } from "../types/book";

/**
 * ReadingHistoryPage
 *
 * Displays the user's reading history.
 * Allows adding new books via a modal.
 * Fetches data from `/user_books/` on mount.
 */
export default function ReadingHistoryPage() {
  const [books, setBooks] = useState<UserBook[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const showAddButton = !isModalOpen;

  const api = useAxios();

  /**
   * Fetches the user's reading history from the backend..
   */
  const fetchBooks = async () => {
    try {
      const response = await api.get<UserBook[]>("/user_books/");
      setBooks(response.data);
      setError(null);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setBooks([]);
        setError("No books found in reading history.");
      } else {
        setError("Failed to fetch books.");
      }
    } finally {
      setLoading(false);
    }
  };

  /**
  * Fetch reading history once on initial mount.
  */
  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <div className="p-6">
      <HomeButton />

      <h2 className="text-2xl font-bold mb-4">
                  Reading History
      </h2>

      {/* Modal for adding a new book */}
      <AddBookModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onBookAdded={() => {
          setLoading(true);
          fetchBooks();
        }}
      />
  
      {/* Show Add button only when modal is closed */}
      {showAddButton && (
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded mb-6"
        >
          Add Book
        </button>
      )}

      {loading && <p>Loading books...</p>} {/* Loading state */}
      {error && <p className="text-red-500">{error}</p>} {/* Error state */}

      {/* Render books when data is available */}
      {!loading && !error && (
        <div className="grid gap-4">
          {books.map((book, index) => (
            <BookCard key={index} book={book} />
          ))}
        </div>
      )}

    </div>
  );
}