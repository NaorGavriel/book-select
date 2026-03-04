import { useEffect, useState } from "react";
import useAxios from "../api/useAxios";
import type { JobResult } from "../types/result";
import ResultsList from "../features/recommendations/components/ResultsList";
import RecommendationsHeader from "../features/recommendations/components/RecommendationsHeader";
import SectionDivider from "../components/ui/SectionDivider";
/**
 * RecommendationsPage
 * -----------
 * Displays all previous user's results.
 */
export default function RecommendationsPage() {
  const api = useAxios();
  
  const [results, setResults] = useState<JobResult[] | null>(null);
  
  const fetchResults = async () => {
    try {
      const response = await api.get(`/results/`);
      setResults(response.data);
    } catch {
      console.error("Failed to fetch results");
    }
  };

  useEffect(() => {
    fetchResults();
  }, []);

  return (
    <div className="min-h-screen bg-linear-to-tl from-amber-100/50 via-violet-50 to-stone-50">    

      <RecommendationsHeader/>
      {/* Render result cards */}
      {results && <ResultsList results={results} />}
    </div>
  );
}