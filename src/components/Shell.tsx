import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";

export function Shell({ children }: { children: ReactNode }) {
  const cls = "text-muted-foreground hover:text-foreground transition-colors";
  const active = { className: "text-primary" };
  return (
    <div className="min-h-screen">
      <header className="border-b">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <Link to="/" className="font-mono font-bold text-primary">{"> pattern.py"}</Link>
          <nav className="flex gap-6 text-sm">
            <Link to="/" className={cls} activeProps={active} activeOptions={{ exact: true }}>Problems</Link>
            <Link to="/patterns" className={cls} activeProps={active}>Patterns</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-6 py-10">{children}</main>
    </div>
  );
}

export function Code({ children }: { children: string }) {
  return (
    <pre className="overflow-x-auto rounded-lg border bg-code p-4 font-mono text-sm leading-relaxed text-foreground">
      <code>{children}</code>
    </pre>
  );
}
