/**
 * Represents a single recommendation / job result
 */
import type { Decision } from "./decision";

export interface JobResult {
  title: string;
  authors: string[];
  decision: Decision;
  confidence: number;
  explanation: string;
}