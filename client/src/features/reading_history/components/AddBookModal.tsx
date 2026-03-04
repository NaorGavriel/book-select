import { useState } from "react";
import useAxios from "../../../api/useAxios";

interface AddBookModalProps {
  isOpen: boolean;
  onClose: () => void;
  onBookAdded: () => void;
}

/**
 * AddBookModal
 *
 * Modal component for manually adding a book
 * to the user's reading history.
 *
 * Sends a POST request to `/user_books/` and
 * notifies the parent component on success.
 */
export default function AddBookModal({
    isOpen,
    onClose,
    onBookAdded,
}: AddBookModalProps) {

    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const api = useAxios();

    
    // not rendering modal if not open.
    if (!isOpen) return null;

    // Submits new book data to backend.
    const handleSubmit = async () => {
        if (!title.trim() || !author.trim()) return;

        try {
            setSubmitting(true);

            await api.post("/user_books/", {
                title,
                author,
            });
            
            // Reset form fields
            setTitle("");
            setAuthor("");

            onBookAdded(); // notify parent component
            onClose();
        } catch (err) {
            console.error("Failed to add book", err);
        } finally {
            setSubmitting(false);
        }
    };

    return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm px-4">
      <div className="w-full max-w-md rounded-2xl bg-white shadow-xl border border-neutral-200 p-8 animate-fade-in">

        {/* Header */}
        <div className="mb-6">
          <h3 className="text-2xl font-semibold text-neutral-800">
            Add a Book
          </h3>
          <p className="text-sm text-neutral-500 mt-1">
            Enter the book title and author.
          </p>
        </div>

        {/* Title Field */}
        <div className="mb-5">
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Title
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Atomic Habits"
            className="w-full rounded-lg border border-neutral-300 bg-neutral-50 px-4 py-2.5 
                       focus:outline-none focus:ring-2 focus:ring-neutral-400 
                       focus:border-neutral-400 transition"
          />
        </div>

        {/* Author Field */}
        <div className="mb-8">
          <label className="block text-sm font-medium text-neutral-700 mb-2">
            Author
          </label>
          <input
            type="text"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            placeholder="James Clear"
            className="w-full rounded-lg border border-neutral-300 bg-neutral-50 px-4 py-2.5 
                       focus:outline-none focus:ring-2 focus:ring-neutral-400 
                       focus:border-neutral-400 transition"
          />
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-3">
          <button
            onClick={onClose}
            disabled={submitting}
            className="rounded-lg px-4 py-2 text-sm font-medium text-neutral-600 
                       hover:bg-neutral-100 transition disabled:opacity-50"
          >
            Cancel
          </button>

          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="rounded-lg bg-neutral-800 text-white px-5 py-2 text-sm font-medium 
                       hover:bg-neutral-700 transition disabled:opacity-50"
          >
            {submitting ? "Adding..." : "Add Book"}
          </button>
        </div>
      </div>
    </div>
  );
}