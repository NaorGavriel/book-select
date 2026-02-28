import type{ ReactNode } from "react";

type AuthCardProps = {
  children: ReactNode;
};

export default function AuthCard({ children }: AuthCardProps) {
  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 sm:p-10 border border-neutral-200">
      {children}
    </div>
  );
}