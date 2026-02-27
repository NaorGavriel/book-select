import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import useAxios from "../api/useAxios";
import JobStatusPoller from "../components/JobStatusPoller";
import ResultCard from "../components/ResultCard";
import HomeButton from "../components/HomeButton";
/**
 * ResultsPage
 * -----------
 * Flow:
 * - Poll job status
 * - When completed → fetch results
 * - Display results as cards
 */
type JobResult = {
  title: string;
  authors: string[];
  decision: string;
  confidence: number;
  explanation: string;
};

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
    <div>
      <h2>Results</h2>
      
      {/* Show status while waiting */}
      {!results && <p>Status: {status}</p>}

      {/* Poller runs only until completed */}
      {!results && (
        <JobStatusPoller
          jobId={jobId}
          intervalMs={3000}
          maxAttempts={4}
          onUpdate={setStatus}
          onCompleted={() => {
            console.log("Job completed");
            fetchResults();
          }}
          onFailed={() => {
            console.error("Job failed");
            navigate("/home");
          }}
        />
      )}

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