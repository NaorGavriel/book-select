import { useEffect, useState } from "react";
import useAxios from "../../api/useAxios";

export type CacheMetrics = { hits: number; misses: number; hit_rate: number };
export type JobMetrics = { total_today: number; completed: number; failed: number };
export type RecommendationMetrics = {
  total: number;
  today: number;
  this_week: number;
  avg_confidence: number;
  strong_match_pct: number;
  consider_pct: number;
  avoid_pct: number;
  top_books: { title: string; count: number }[];
  top_authors: { author: string; count: number }[];
  top_genres: { genre: string; count: number }[];
};
export type PerformanceMetrics = {
  avg_cache_lookup_latency_ms: number;
  avg_job_processing_duration_s: number;
};
export type UserMetrics = {
  total: number;
  active: number;
  new_today: number;
  reading_history_count: number;
};
export type MetricsResponse = {
  cache: CacheMetrics;
  jobs: JobMetrics;
  recommendations: RecommendationMetrics;
  performance: PerformanceMetrics;
  users: UserMetrics;
};

const POLL_INTERVAL_MS = 15_000;

/**
 * useMetrics
 * ----------
 * Fetches GET /metrics on mount and re-fetches every 15 seconds.
 * Returns the latest snapshot and an error flag.
 */
export function useMetrics(): { metrics: MetricsResponse | null; error: boolean } {
  const api = useAxios();
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [error, setError] = useState(false);

  const fetchMetrics = async () => {
    /** Request the latest metrics snapshot from the server. */
    try {
      const response = await api.get<MetricsResponse>("/metrics");
      setMetrics(response.data);
      setError(false);
    } catch {
      setError(true);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, POLL_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []);

  return { metrics, error };
}
