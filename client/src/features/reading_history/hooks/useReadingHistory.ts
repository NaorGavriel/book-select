import { useEffect, useState } from "react";
import useAxios from "../../../api/useAxios";
import type { UserBook } from "../../../types/book";

export function useReadingHistory() {
  const [books, setBooks] = useState<UserBook[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const api = useAxios();

  const fetchBooks = async () => {
    try {
      const response = await api.get<UserBook[]>("/user_books/");
      setBooks(response.data);
      setError(null);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setBooks([]);
        setError(null);
      } else {
        setError("Failed to fetch books.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  return { books, loading, error, refresh: fetchBooks };
}