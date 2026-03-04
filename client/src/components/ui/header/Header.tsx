import { Link } from "react-router-dom";
import { useState } from "react";
import type { ReactNode } from "react";
import { Menu } from "lucide-react";

import DesktopNav from "./DesktopNav";
import MobileMenu from "./MobileMenu";
import { NAV_LINKS } from "./navLinks";



/**
 * HeaderProps
 *
 * rightContent:
 * Content rendered on the right side of the header.
 */
type HeaderProps = {
  rightContent?: ReactNode;
};

export default function Header({ rightContent }: HeaderProps) {
  const [menuOpen, setMenuOpen] = useState(false); // Controls whether the mobile navigation menu is visible.

  return (
    <header className="sticky top-0 z-50 w-full border-b border-neutral-700 bg-neutral-900/92 backdrop-blur">
      <div className="max-w-6xl mx-auto px-6 py-4">

         {/* Top header row */}
        <div className="flex items-center justify-between">

          {/* Left section: Logo + Desktop Navigation */}
          <div className="flex items-center gap-6">

            <Link to="/" className="text-2xl font-semibold text-stone-50">
              BookSelect
            </Link>

            <DesktopNav links={NAV_LINKS} />

          </div>

          {/* Right section: Auth buttons + mobile menu toggle */}
          <div className="flex items-center gap-4">

            {/* Authentication actions (visible only on desktop) */}
            <div className="hidden md:flex">
              {rightContent}
            </div>

             {/* Mobile menu toggle button (hidden on desktop) */}
            <button
              onClick={() => setMenuOpen((prev) => !prev)}
              className="md:hidden text-stone-200"
              aria-label="Toggle navigation menu"
            >
              <Menu size={24} />
            </button>

          </div>

        </div>

        {/* Mobile navigation menu */}
        <MobileMenu
          links={NAV_LINKS}
          menuOpen={menuOpen}
          onNavigate={() => setMenuOpen(false)}
          rightContent={rightContent}
        />

      </div>
    </header>
  );
}