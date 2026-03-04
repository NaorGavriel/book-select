import { Link } from "react-router-dom";

/**
 * HeaderNavLink
 *
 * Reusable navigation link used by both desktop and mobile menus.
 */
type HeaderNavLinkProps = {
   /** Target route */
  to: string;

  /** Text displayed for the link */
  label: string;

  /** click handler (used by mobile menu to close after navigation) */
  onClick?: () => void;
};

export default function HeaderNavLink({ to, label, onClick }: HeaderNavLinkProps) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className="text-xl text-stone-200 hover:text-white transition"
    >
      {label}
    </Link>
  );
}