type Decision = "strong_match" | "consider" | "avoid";

const decisionStyles: Record<Decision, string> = {
  "strong_match": "bg-green-100 text-green-800",
  "consider": "bg-yellow-100 text-yellow-800",
  "avoid": "bg-red-100 text-red-800",
};

const decisionLabels: Record<Decision, string> = {
  strong_match: "Good Match",
  consider: "Maybe",
  avoid: "Avoid",
};

type Props = {
  result: {
    title: string;
    authors: string[];
    decision: Decision;
    confidence: number;
    explanation: string;
  };
};

export default function ResultCard({ result }: Props) {
  const decisionStyle = decisionStyles[result.decision];
  const decisionText = decisionLabels[result.decision];

  return (
    <div className="bg-white border border-neutral-300 items-center text-center rounded-2xl shadow-md p-6 transition hover:shadow-lg">

      <h3 className="text-2xl font-semibold text-neutral-800 mb-3">
        {result.title}
      </h3>

      {/* Authors */}
      <p className="text-sm text-neutral-600 items-center text-center mb-6">
        <span className="font-medium text-neutral-700">Authors:</span>{" "}
        {result.authors.join(", ")}
      </p>

      <div className="flex flex-col items-center text-center mb-6">
        <div className={`px-8 py-4 rounded-xl text-3xl font-bold ${decisionStyle}`}>
          {decisionText}
        </div>
      </div>

      <p className="text-base text-neutral-700 leading-relaxed text-center">
        {result.explanation}
      </p>

    </div>
  );
}

