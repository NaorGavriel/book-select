import BookCard from "./BookCard";
import type { UserBook } from "../../../types/book";

type BookListProps = {
  books: UserBook[];
};

export default function BookList({ books }: BookListProps) {
  return (
    <div className="max-w-5xl mx-auto grid gap-6 sm:grid-cols-2">
      {books.map((book, index) => (
        <BookCard key={index} book={book} />
      ))}
    </div>
  );
}