import { useEffect, useState } from "react";
import useAxios from "../api/useAxios";
import type { JobResult } from "../types/result";
import ResultsList from "../features/recommendations/components/ResultsList";
import RecommendationsHeader from "../features/recommendations/components/RecommendationsHeader";

/**
 * RecommendationsPage
 * -----------
 * Displays all previous user's results.
 */
export default function RecommendationsPage() {
  const api = useAxios();
  
  const [results, setResults] = useState<JobResult[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [noResults, setNoResults] = useState(false);
  
  const fetchResults = async () => {
    try {
      const response = await api.get(`/results/`);
      setResults(response.data);
    } catch (err: any) {
      if (err?.response?.status === 404) {
        setNoResults(true);
      } else {
        console.error("Failed to fetch results");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, []);

  return (
    <div className="min-h-screen bg-linear-to-tl from-amber-100/50 via-violet-50 to-stone-50">
      <RecommendationsHeader />

      {loading && (
        <p className="text-center text-neutral-500 mt-10">
          Loading recommendations...
        </p>
      )}

      {noResults && (
        <div className="max-w-3xl mx-auto text-center py-16 text-neutral-500">
          <p className="text-lg font-medium">No recommendations yet</p>
          <p className="mt-2 text-sm">
            Upload a bookshelf photo to start discovering books you'll enjoy.
          </p>
        </div>
      )}

      {results && <ResultsList results={results} />}
    </div>
  );
}