import type { ReactNode } from "react";
import { Link } from "react-router-dom";

type HeaderProps = {
  rightContent?: ReactNode;
};

export default function Header({ rightContent }: HeaderProps) {
  return (
    <header className="w-full bg-neutral-900">
      <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
        
        {/* Clickable Logo */}
        <Link
          to="/"
          className="text-xl sm:text-2xl font-semibold tracking-tight text-neutral-200 hover:text-white transition"
        >
          BookSelect
        </Link>

        {rightContent && (
          <div className="flex items-center">
            {rightContent}
          </div>
        )}

      </div>
    </header>
  );
}