type AuthHeaderProps = {
  title: string;
  subtitle: string;
};

export default function AuthHeader({ title, subtitle }: AuthHeaderProps) {
  return (
    <div className="text-center mb-10">
      <h2 className="text-3xl sm:text-4xl font-semibold tracking-tight">
        {title}
      </h2>
      <p className="mt-4 text-neutral-600">
        {subtitle}
      </p>
    </div>
  );
}