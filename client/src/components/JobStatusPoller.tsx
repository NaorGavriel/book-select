import { useEffect } from "react";
import useAxios from "../api/useAxios";

/**
 * JobStatusPoller
 * ----------------
 * Polls job status every intervalMs milliseconds.
 *
 * Props:
 * - jobId: job identifier
 * - onCompleted: called when status === completed
 * - maxAttempts: maximum polling tries before aborting
 * - onFailed: called when status === failed
 * - onUpdate: optional, called on every status update
 */
type Props = {
  jobId: string;
  intervalMs?: number;
  maxAttempts : number;
  onCompleted: () => void;
  onFailed: () => void;
  onUpdate?: (status: string) => void;
};

export default function JobStatusPoller({
  jobId,
  intervalMs,
  maxAttempts,
  onCompleted,
  onFailed,
  onUpdate,
}: Props) {
  const api = useAxios();

  useEffect(() => {
    if (!jobId) return;

    let intervalId: ReturnType<typeof setInterval>;
    let attempts = 0;
    let stopped = false;

    const poll = async () => {
        if (stopped) return;
        attempts += 1;

        try {
            const response = await api.get(`/jobs/${jobId}`);
            const data = response.data;

            // Notify caller of current status
            onUpdate?.(data.status);

            // job completed in backend
            if (data.status === "completed") {
                stopped = true;
                clearInterval(intervalId);
                onCompleted();
                return;
            }

            // job failed in backend
            if (data.status === "failed") {
                stopped = true;
                clearInterval(intervalId);
                onFailed();
                return;
            }

            // timeout: exceeded maximum attempts
            if (attempts >= maxAttempts) {
            console.error("Polling timeout");
            stopped = true;
            clearInterval(intervalId);
            onFailed();
            }
        } catch (error : any) {
            const status = error?.response?.status;
            if (status === 404) {
                console.error("Job not found");
                stopped = true;
                clearInterval(intervalId);
                onFailed();
                return;
            }
        console.error("Polling error");
        }
    };

    poll();
    intervalId = setInterval(poll, intervalMs);

    return () => {
      stopped = true;
      clearInterval(intervalId);
    };
  }, [jobId, intervalMs,maxAttempts, api, onCompleted, onFailed, onUpdate]);

  return null;
}