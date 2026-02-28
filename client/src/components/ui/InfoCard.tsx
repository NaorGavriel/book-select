import React from "react";

type InfoCardProps = {
  title: string;
  description: string;
  gradientFrom: string;
  gradientVia: string;
  gradientTo: string;
  borderColor: string;
  media: React.ReactNode;
  reverse?: boolean; // optional: media on left
};

export default function InfoCard({
  title,
  description,
  gradientFrom,
  gradientVia,
  gradientTo,
  borderColor,
  media,
  reverse = false,
}: InfoCardProps) {
  return (
    <div
      className={`rounded-3xl overflow-hidden shadow-xl border ${borderColor}
                  bg-linear-to-b ${gradientFrom} ${gradientVia} ${gradientTo}`}
    >
      <div
        className={`flex flex-col lg:flex-row ${
          reverse ? "lg:flex-row-reverse" : ""
        }`}
      >
        {/* Text */}
        <div className="p-14 lg:w-1/2 flex flex-col justify-center">
          <h3 className="text-4xl font-semibold mb-8 text-neutral-900">
            {title}
          </h3>
          <p className="text-xl text-neutral-700 leading-relaxed">
            {description}
          </p>
        </div>

        {/* Media */}
        <div className="lg:w-1/2 min-h-75 lg:min-h-105">
          {media}
        </div>
      </div>
    </div>
  );
}