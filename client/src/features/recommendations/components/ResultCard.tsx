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
    <div style={styles.card}>
      <h3>{result.title}</h3>

      <p>
        <strong>Authors:</strong> {result.authors.join(", ")}
      </p>

      <p>
        <strong>Decision:</strong> {result.decision}
      </p>

      <p>
        <strong>Confidence:</strong> {result.confidence}
      </p>

      <p>{result.explanation}</p>
    </div>
  );
}

const styles = {
  card: {
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "12px",
    marginBottom: "12px",
  } as React.CSSProperties,
};