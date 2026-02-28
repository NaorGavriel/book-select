type ActionPanelProps = {
  title: string;
  description: string;
  onClick: () => void;
  highlight?: boolean;
  backgroundImage?: string;
};

export default function ActionPanel({
  title,
  description,
  onClick,
  highlight = false,
  backgroundImage,
}: ActionPanelProps) {
  return (
    <button
      onClick={onClick}
      className={`relative w-full text-left rounded-2xl overflow-hidden transition-all duration-300
        ${
          highlight
            ? "border border-neutral-900 hover:shadow-lg hover:-translate-y-1"
            : "border border-neutral-200 hover:shadow-lg hover:-translate-y-1"
        }
      `}
    >
      {/* Background Image */}
      {backgroundImage && (
        <>
          <img
            src={backgroundImage}
            alt=""
            className="absolute inset-0 w-full h-full object-cover blur-xs scale-105"
          />
          <div className="absolute inset-0 bg-black/75" />
        </>
      )}

      {/* Content */}
      <div
        className={`relative z-10 p-8 ${
          backgroundImage
            ? "text-white"
            : highlight
            ? "bg-neutral-900 text-white"
            : "bg-white text-neutral-900"
        }`}
      >
        <h3 className="text-2xl font-semibold mb-3">
          {title}
        </h3>

        <p
          className={`leading-relaxed ${
            backgroundImage || highlight
              ? "text-neutral-200"
              : "text-neutral-600"
          }`}
        >
          {description}
        </p>
      </div>
    </button>
  );
}