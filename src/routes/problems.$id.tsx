import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { useState } from "react";
import { Code, Shell } from "@/components/Shell";
import { patternById, patterns, problems } from "@/lib/data";

export const Route = createFileRoute("/problems/$id")({
  loader: ({ params }) => {
    const problem = problems.find((p) => p.id === params.id);
    if (!problem) throw notFound();
    return { problem };
  },
  head: ({ loaderData }) => ({
    meta: [
      { title: loaderData ? `${loaderData.problem.title} — Pattern.py` : "Problem — Pattern.py" },
      { name: "description", content: loaderData?.problem.statement ?? "Diagnose a coding problem." },
      { property: "og:title", content: loaderData?.problem.title ?? "Problem" },
      { property: "og:description", content: "Diagnose this problem and match it to a pattern." },
    ],
  }),
  component: ProblemPage,
});

const checks = [
  "Is the input sorted?",
  "Contiguous subarray/substring?",
  "Pair/triplet or comparing ends?",
  "Need fast lookup / counts?",
  "Grid, graph or tree?",
  "'Top K' / 'Kth'?",
  "'All combinations' / generate everything?",
  "Count ways / min / max with choices?",
];

function ProblemPage() {
  const { problem } = Route.useLoaderData();
  const [ticked, setTicked] = useState<number[]>([]);
  const [guess, setGuess] = useState<string | null>(null);
  const [showSol, setShowSol] = useState(false);
  const correct = patternById(problem.pattern);

  return (
    <Shell key={problem.id}>
      <Link to="/" className="font-mono text-xs text-muted-foreground hover:text-primary">← all problems</Link>
      <h1 className="mt-3 text-3xl font-bold">{problem.title}</h1>
      <p className="font-mono text-xs text-muted-foreground">{problem.source} · {problem.difficulty}</p>
      <p className="mt-6 rounded-lg border bg-card p-5 leading-relaxed">{problem.statement}</p>

      <section className="mt-10">
        <h2 className="font-mono text-sm text-primary">01 / Diagnose</h2>
        <p className="mt-1 text-sm text-muted-foreground">Tick what applies to this problem.</p>
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {checks.map((c, i) => (
            <label key={c} className="flex cursor-pointer items-center gap-3 rounded-md border bg-card px-4 py-3 text-sm hover:bg-muted">
              <input type="checkbox" className="accent-primary" checked={ticked.includes(i)}
                onChange={() => setTicked((t) => (t.includes(i) ? t.filter((x) => x !== i) : [...t, i]))} />
              {c}
            </label>
          ))}
        </div>
      </section>

      <section className="mt-10">
        <h2 className="font-mono text-sm text-primary">02 / Pick a pattern</h2>
        <div className="mt-4 flex flex-wrap gap-2">
          {patterns.map((p) => {
            const state = guess === p.id ? (p.id === correct.id ? "border-success text-success" : "border-destructive text-destructive") : "";
            return (
              <button key={p.id} onClick={() => setGuess(p.id)}
                className={`rounded-full border px-4 py-2 text-sm transition-colors hover:bg-muted ${state}`}>
                {p.name}
              </button>
            );
          })}
        </div>
        {guess && (
          <div className="mt-5 rounded-lg border bg-card p-5">
            <p className={guess === correct.id ? "font-semibold text-success" : "font-semibold text-destructive"}>
              {guess === correct.id ? "Correct!" : `Not quite — it's ${correct.name}.`}
            </p>
            <p className="mt-3 text-sm text-muted-foreground">Clues in the problem:</p>
            <ul className="mt-1 list-disc pl-5 text-sm">
              {problem.clues.map((c) => <li key={c}>{c}</li>)}
            </ul>
            <p className="mt-3 text-sm">{correct.idea} <Link to="/patterns" hash={correct.id} className="text-primary underline">See pattern →</Link></p>
          </div>
        )}
      </section>

      <section className="mt-10">
        <h2 className="font-mono text-sm text-primary">03 / Solution</h2>
        {showSol ? (
          <div className="mt-4"><Code>{problem.solution}</Code></div>
        ) : (
          <button onClick={() => setShowSol(true)} className="mt-4 rounded-md bg-primary px-5 py-2 text-sm font-semibold text-primary-foreground hover:opacity-90">
            Reveal Python solution
          </button>
        )}
      </section>
    </Shell>
  );
}
