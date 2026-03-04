import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import useAxios from "../api/useAxios";
import JobStatusPoller from "../features/recommendations/JobStatusPoller";
import type { JobResult } from "../types/result";
import ResultsList from "../features/recommendations/components/ResultsList";
import ResultsLoader from "../features/recommendations/components/ResultsLoader";
import ResultsHeader from "../features/recommendations/components/ResultsHeader";
/**
 * ResultsPage
 * -----------
 * - Poll job status, fetches results when job is completed and displays each book result as card
 */
export default function ResultsPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const api = useAxios();
  
  const [status, setStatus] = useState("pending");
  const [results, setResults] = useState<JobResult[] | null>(null);
  
  if (!jobId) return <div>Invalid job</div>;
  console.log("jobId:", jobId, "results:", results);
  const fetchResults = async () => {
    try {
      const response = await api.get(`/results/${jobId}`);
      setResults(response.data);
    } catch {
      console.error("Failed to fetch results");
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-tl from-amber-100/50 via-violet-50 to-stone-50">
      <div className="max-w-4xl mx-auto">
        <ResultsHeader/>
        {/* LOADING STATE */}
        {!results && <ResultsLoader/>}

        {/* POLLER */}
        {!results && (
          <JobStatusPoller
            jobId={jobId}
            intervalMs={3000}
            maxAttempts={10}
            onUpdate={setStatus}
            onCompleted={() => {
              fetchResults();
            }}
            onFailed={() => {
              navigate("/home");
            }}
          />
        )}

        {/* RESULTS */}
        {results && <ResultsList results={results} />}
      </div>
    </div>
  );
}