import type { ReactNode } from "react";
import HeaderNavLink from "./HeaderNavLink";

/**
 * MobileMenu
 *
 * Collapsible mobile navigation menu displayed below the header.
 * Hidden on desktop screens and toggled via the header menu button.
 */
type Props = {
  links: { to: string; label: string }[];
  menuOpen: boolean;
  onNavigate: () => void;
  rightContent?: ReactNode;
};

export default function MobileMenu({
  links, /** Navigation links to render */
  menuOpen,
  onNavigate,
  rightContent, /** Optional content shown at the bottom of the menu (e.g. Login / Logout button) */
}: Props) {
  return (
    <div
      className={`md:hidden overflow-hidden transition-all duration-300 ${
        menuOpen ? "max-h-60 opacity-100 mt-4" : "max-h-0 opacity-0"
      }`}
    >
      <div className="flex flex-col gap-3 text-stone-200">

        {links.map((link) => (
          <HeaderNavLink
            key={link.to}
            {...link}
            onClick={onNavigate}
          />
        ))}

        <div className="border-t border-neutral-700 pt-3 mt-2">
          {rightContent}
        </div>

      </div>
    </div>
  );
}