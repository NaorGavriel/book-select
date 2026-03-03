import type { UserBook } from "../../../types/book";

interface BookCardProps {
  book: UserBook;
}

export default function BookCard({ book }: BookCardProps) {
  return (
    <div className="group bg-white border border-indigo-300 rounded-2xl p-8
                    transition-all duration-200 hover:shadow-lg hover:-translate-y-1">

      {/* Title */}
      <h3 className="text-2xl font-semibold tracking-tight mb-4">
        {book.title}
      </h3>

      {/* Metadata Row */}
      <div className="flex flex-wrap gap-4 text-sm text-neutral-600 mb-6">
        <span>
          <span className="font-medium text-neutral-800">Authors:</span>{" "}
          {book.authors.join(", ")}
        </span>

        <span>
          <span className="font-medium text-neutral-800">Genres:</span>{" "}
          {book.genres.join(", ")}
        </span>
      </div>

      {/* Description */}
      {book.description && (
        <p className="text-neutral-600 leading-relaxed">
          {book.description}
        </p>
      )}

    </div>
  );
}