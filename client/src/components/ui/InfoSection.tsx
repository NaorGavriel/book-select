import type { ReactNode } from "react";

type InfoSectionProps = {
  title: string;
  description: string;
  background: string;
  isDark?: boolean;
  media: ReactNode;
  reverse?: boolean;
};

export default function InfoSection({
  title,
  description,
  background,
  isDark = false,
  media,
  reverse = false,
}: InfoSectionProps) {
  return (
    <section className={`w-full ${background} py-32`}>
      <div
        className={`max-w-6xl mx-auto px-6 flex flex-col lg:flex-row ${
          reverse ? "lg:flex-row-reverse" : ""
        }`}
      >
        {/* Text */}
        <div className="lg:w-1/2 flex flex-col justify-center lg:pr-16">
          <h3
            className={`text-4xl sm:text-5xl font-semibold mb-8 ${
              isDark ? "text-white" : "text-neutral-900"
            }`}
          >
            {title}
          </h3>

          <p
            className={`text-xl leading-relaxed ${
              isDark ? "text-neutral-300" : "text-neutral-700"
            }`}
          >
            {description}
          </p>
        </div>

        {/* Media */}
        <div className="lg:w-1/2 mt-12 lg:mt-0 min-h-[350px] lg:min-h-[500px]">
          {media}
        </div>
      </div>
    </section>
  );
}