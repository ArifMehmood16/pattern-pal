import { createFileRoute, Link } from "@tanstack/react-router";
import { Shell } from "@/components/Shell";
import { problems } from "@/lib/data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Pattern.py — Python Coding Interview Pattern Practice" },
      { name: "description", content: "Read a LeetCode/HackerRank problem, diagnose it, and match it to the right solving pattern in Python." },
      { property: "og:title", content: "Pattern.py — Diagnose problems, match patterns" },
      { property: "og:description", content: "Practice recognising coding interview patterns in Python." },
    ],
  }),
  component: Index,
});

const diffColor = { Easy: "text-success", Medium: "text-accent", Hard: "text-destructive" };

function Index() {
  return (
    <Shell>
      <h1 className="text-4xl font-bold tracking-tight">Read. Diagnose. <span className="text-primary">Pattern.</span></h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Pick a problem, guess which pattern solves it, then check your reasoning and the Python solution.
      </p>
      <ul className="mt-10 divide-y rounded-lg border bg-card">
        {problems.map((p) => (
          <li key={p.id}>
            <Link to="/problems/$id" params={{ id: p.id }} className="flex items-center justify-between px-5 py-4 hover:bg-muted">
              <span className="font-medium">{p.title}</span>
              <span className="flex gap-4 font-mono text-xs">
                <span className="text-muted-foreground">{p.source}</span>
                <span className={diffColor[p.difficulty]}>{p.difficulty}</span>
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </Shell>
  );
}
