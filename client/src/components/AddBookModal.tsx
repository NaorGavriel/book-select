import { useState } from "react";
import useAxios from "../api/useAxios";

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
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
        <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-lg">
            <h3 className="text-xl font-bold mb-4">Add New Book</h3>

            <div className="mb-4">
            <label className="block mb-1 text-sm font-medium">
                Title
            </label>
            <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full border rounded px-3 py-2"
                placeholder="Enter book title"
            />
            </div>

            <div className="mb-4">
            <label className="block mb-1 text-sm font-medium">
                Author
            </label>
            <input
                type="text"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                className="w-full border rounded px-3 py-2"
                placeholder="Enter author name"
            />
            </div>

            <div className="flex justify-end gap-2">
            <button
                onClick={onClose}
                className="px-4 py-2 rounded border"
                disabled={submitting}
            >
                Cancel
            </button>

            <button
                onClick={handleSubmit}
                className="bg-blue-600 text-white px-4 py-2 rounded"
                disabled={submitting}
            >
                {submitting ? "Adding..." : "Add"}
            </button>
            </div>
        </div>
        </div>
    );
}