import { useState } from "react";
import type { UserBook } from "../../../types/book";

interface BookCardProps {
  book: UserBook;
}

export default function BookCard({ book }: BookCardProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="group bg-white border border-neutral-200 rounded-2xl p-8
                border-l-4 border-l-indigo-400 hover:border-l-indigo-600
                transition-all duration-200 hover:shadow-lg hover:-translate-y-1 ">

      {/* Title */}
      <h3 className="text-xl font-semibold tracking-tight text-neutral-900">
        {book.title}
      </h3>

      {/* Metadata */}
      <div className="mt-2 text-sm text-neutral-600 flex flex-wrap gap-x-4 gap-y-1">
        <span>
          <span className="font-medium text-neutral-800">Author:</span>{" "}
          {book.authors.join(", ")}
        </span>

        <span>
          <span className="font-medium text-neutral-800">Genres:</span>{" "}
          {book.genres.join(", ")}
        </span>
      </div>

      {/* Divider */}
      {book.description && (
        <>
          <div className="my-4 h-px bg-neutral-200" />

          {/* Description */}
          <p
            className={`text-neutral-600 leading-relaxed text-sm ${
              expanded ? "" : "line-clamp-3"
            }`}
          >
            {book.description}
          </p>

          <button
            onClick={() => setExpanded(!expanded)}
            className="mt-2 text-sm font-medium text-indigo-600 hover:underline"
          >
            {expanded ? "Show less" : "Read more"}
          </button>
        </>
      )}
    </div>
  );
}