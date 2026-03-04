import type { JobResult } from "../../../types/result";
import ResultCard from "./ResultCard";

type Props = {
  results: JobResult[];
};

export default function ResultsList({ results }: Props) {
  if (results.length === 0) {
    return (
      <div className="max-w-3xl mx-auto text-center py-16 text-neutral-500">
        <p className="text-lg font-medium">
          No recommendations yet
        </p>
        <p className="mt-2 text-sm">
          Upload a bookshelf photo to start getting book matches.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto grid gap-6 sm:grid-cols-2 pb-5 pl-4 pr-4">
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
  );
}