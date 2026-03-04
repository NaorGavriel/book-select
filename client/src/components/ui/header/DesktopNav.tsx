import HeaderNavLink from "./HeaderNavLink";

/**
 * DesktopNav
 *
 * Renders the navigation links displayed in the header on desktop screens.
 * Hidden on small screens; the MobileMenu component is used instead.
 */
type Props = {
    /** Navigation links to render */
  links: { to: string; label: string }[];
};

export default function DesktopNav({ links }: Props) {
  return (
    <nav className="hidden md:flex items-center gap-5">
      {links.map((link) => (
        <HeaderNavLink key={link.to} {...link} />
      ))}
    </nav>
  );
}