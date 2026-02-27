import { useEffect, useState } from "react";
import useAxios from "../api/useAxios";
import ResultCard from "../components/ResultCard";
import HomeButton from "../components/HomeButton";
import type { JobResult } from "../types/result";

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
    <div>
      <h2>Results</h2>
      
      {/* Render result cards */}
      <div>
        <HomeButton/>
      </div>
      {results && (
        <div>
          {results.map((result, index) => (
            <ResultCard key={index} result={result} />
          ))}
        </div>
      )}
    </div>
  );
}