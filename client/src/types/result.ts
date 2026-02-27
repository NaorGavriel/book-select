/**
 * Represents a single recommendation / job result
 */export type JobResult = {
  title: string;
  authors: string[];
  decision: string;
  confidence: number;
  explanation: string;
};