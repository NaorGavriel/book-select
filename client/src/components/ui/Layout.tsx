import Header from "./Header";
import Footer from "./Footer";
import type { ReactNode } from "react";
import { Outlet } from "react-router-dom";

type LayoutProps = {
  headerRight?: ReactNode;
};

export default function Layout({ headerRight }: LayoutProps) {
  return (
    <div className="flex flex-col min-h-screen">
      <Header rightContent={headerRight} />
      <main className="grow">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}