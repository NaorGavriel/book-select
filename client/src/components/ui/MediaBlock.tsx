
type MediaBlockProps = {
  src: string;
  alt: string;
  glowColor?: string;
  align?: "center" | "bottom";
};

function MediaBlock({
  src,
  alt,
  glowColor = "bg-amber-100/25",
  align = "center",
}: MediaBlockProps) {
  return (
    <div
      className={`relative w-full h-full flex ${
        align === "bottom"
          ? "items-end justify-center"
          : "items-center justify-center"
      } px-5`}
    >
      {/* Soft Glow */}
      <div
        className={`absolute ${
          align === "bottom" ? "bottom-10" : ""
        } w-[50%] h-[50%] ${glowColor} rounded-full blur-3xl`}
      />

      {/* Illustration */}
      <img
        src={src}
        alt={alt}
        className="relative z-10 max-h-[380px] w-auto"
      />
    </div>
  );
};

export default MediaBlock;