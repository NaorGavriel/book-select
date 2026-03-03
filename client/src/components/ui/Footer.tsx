export default function Footer() {
  return (
    <footer className="w-full bg-neutral-950 text-neutral-400">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          
          <p className="text-sm">
            {new Date().getFullYear()} BookSelect
          </p>

          <div className="flex gap-6 text-sm">
          </div>

        </div>
      </div>
    </footer>
  );
}