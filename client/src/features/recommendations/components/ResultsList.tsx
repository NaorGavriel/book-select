import type { JobResult } from "../../../types/result";
import ResultCard from "./ResultCard";

type Props = {
  results: JobResult[];
};

export default function ResultsList({ results }: Props) {
  return (
    <>
      <h2 className="text-3xl font-semibold text-neutral-800 mb-10 text-center">
        Your Results
      </h2>

      <div className="grid gap-6">
        {results.map((result, index) => (
          <div
            key={index}
            className="animate-fade-up"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <ResultCard result={result} />
          </div>
        ))}
      </div>
    </>
  );
}