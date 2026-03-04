type AddBookPanelProps = {
  onClick: () => void;
};

export default function AddBookPanel({ onClick }: AddBookPanelProps) {
  return (
    <div className="max-w-5xl mx-auto mb-8">
      <button
        onClick={onClick}
        className="w-full text-left bg-indigo-950 text-white
                   rounded-2xl p-6 transition-all duration-200
                   hover:opacity-95"
      >
        <h3 className="text-xl font-semibold">
          Add a Book
        </h3>
        <p className="text-neutral-300 mt-2">
          Add books you've read to improve your future recommendations.
        </p>
      </button>
    </div>
  );
}