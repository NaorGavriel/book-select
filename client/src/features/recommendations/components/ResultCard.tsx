/**
 * ResultCard
 * ----------
 * Displays a single book match result.
 */
type Props = {
  result: {
    title: string;
    authors: string[];
    decision: string;
    confidence: number;
    explanation: string;
  };
};

export default function ResultCard({ result }: Props) {
  return (
    <div className="bg-white border border-neutral-200 rounded-2xl shadow-md p-6 transition hover:shadow-lg">

      <h3 className="text-xl font-semibold text-neutral-800 mb-3">
        {result.title}
      </h3>

      <p className="text-sm text-neutral-600 mb-2">
        <span className="font-medium text-neutral-700">Authors:</span>{" "}
        {result.authors.join(", ")}
      </p>

      <p className="text-sm text-neutral-600 mb-2">
        <span className="font-medium text-neutral-700">Decision:</span>{" "}
        {result.decision}
      </p>

      <p className="text-sm text-neutral-600 mb-4">
        <span className="font-medium text-neutral-700">Confidence:</span>{" "}
        {(result.confidence * 100).toFixed(1)}%
      </p>

      <p className="text-sm text-neutral-700 leading-relaxed">
        {result.explanation}
      </p>
    </div>
  );
}