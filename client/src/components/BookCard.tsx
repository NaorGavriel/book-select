import type { UserBook } from "../types/book";

interface BookCardProps {
  book: UserBook;
}

/**
 * BookCard
 *
 * Renders a single book entry in the reading history.
 */
export default function BookCard({ book }: BookCardProps) {
  return (
    <div className="border rounded-lg p-4 shadow-sm bg-white">
      <h3 className="text-xl font-semibold">{book.title}</h3>

      <p className="text-sm text-gray-600">
        <strong>Authors:</strong> {book.authors.join(", ")}
      </p>

      <p className="text-sm text-gray-600">
        <strong>Genres:</strong> {book.genres.join(", ")}
      </p>

      <p className="mt-2 text-gray-800">
        {book.description}
      </p>
    </div>
  );
}