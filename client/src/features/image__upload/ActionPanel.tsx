type ActionPanelProps = {
  title: string;
  description: string;
  onClick: () => void;
  highlight?: boolean;
};

export default function ActionPanel({
  title,
  description,
  onClick,
  highlight = false,
}: ActionPanelProps) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-2xl p-8 border transition-all duration-200
        ${
          highlight
            ? "bg-indigo-900 text-white border-neutral-900 hover:opacity-70 hover:-translate-y-1 hover:shadow-md"
            : "bg-indigo-100 border-neutral-200 hover:shadow-md hover:-translate-y-1"
        }
      `}
    >
      <h3 className="text-2xl font-semibold mb-3">
        {title}
      </h3>

      <p
        className={`leading-relaxed ${
          highlight ? "text-neutral-300" : "text-neutral-600"
        }`}
      >
        {description}
      </p>
    </button>
  );
}