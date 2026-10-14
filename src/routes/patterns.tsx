import { createFileRoute, Link } from "@tanstack/react-router";
import { Code, Shell } from "@/components/Shell";
import { patterns, problems } from "@/lib/data";

export const Route = createFileRoute("/patterns")({
  head: () => ({
    meta: [
      { title: "Coding Patterns Cheat Sheet (Python) — Pattern.py" },
      { name: "description", content: "Signals, ideas and Python templates for the core LeetCode/HackerRank patterns." },
      { property: "og:title", content: "Coding Patterns Cheat Sheet (Python)" },
      { property: "og:description", content: "How to recognise each pattern, with Python templates." },
    ],
  }),
  component: PatternsPage,
});

function PatternsPage() {
  return (
    <Shell>
      <h1 className="text-4xl font-bold tracking-tight">Patterns</h1>
      <p className="mt-3 text-muted-foreground">Learn the signals — that's how you recognise the pattern fast.</p>
      <div className="mt-10 space-y-10">
        {patterns.map((p) => (
          <article key={p.id} id={p.id} className="scroll-mt-6 rounded-lg border bg-card p-6">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <h2 className="text-2xl font-bold">{p.name}</h2>
              <span className="font-mono text-xs text-accent">{p.complexity}</span>
            </div>
            <p className="mt-2 text-muted-foreground">{p.idea}</p>
            <h3 className="mt-4 font-mono text-sm text-primary">Signals</h3>
            <ul className="mt-1 list-disc pl-5 text-sm">{p.signals.map((s) => <li key={s}>{s}</li>)}</ul>
            <h3 className="mt-4 mb-2 font-mono text-sm text-primary">Python template</h3>
            <Code>{p.template}</Code>
            <div className="mt-4 flex flex-wrap gap-2 text-sm">
              {problems.filter((x) => x.pattern === p.id).map((x) => (
                <Link key={x.id} to="/problems/$id" params={{ id: x.id }} className="rounded-full border px-3 py-1 hover:bg-muted">{x.title}</Link>
              ))}
            </div>
          </article>
        ))}
      </div>
    </Shell>
  );
}
