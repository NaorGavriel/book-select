import type { ReactNode } from "react";

type HeaderProps = {
  rightContent?: ReactNode;
};

export default function Header({ rightContent }: HeaderProps) {
  return (
    <header className="w-full bg-neutral-900">
      <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
        
        <h1 className="text-xl sm:text-2xl font-semibold tracking-tight text-neutral-200">
          BookSelect
        </h1>

        {rightContent && (
          <div className="flex items-center">
            {rightContent}
          </div>
        )}

      </div>
    </header>
  );
}