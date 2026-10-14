import engine from '../lib/engine.js';
import { PageHead } from './ui.jsx';

const starters = {
  'Unique substring': 'Find the longest substring without repeating characters in a string.',
  'Exact sums': 'Count the number of contiguous subarrays whose sum equals k. Values may include negative numbers.',
  'Weighted paths': 'Find shortest paths from a starting vertex in a weighted graph with nonnegative edge costs.',
  '3Sum': 'Return all unique triplets in an unsorted array whose sum is zero.',
};

export default function ProblemMapper({ patterns, draft, setDraft, notify }) {
  function toggleSignal(id) { setDraft(d => ({ ...d, selected: d.selected.includes(id) ? d.selected.filter(x => x !== id) : [...d.selected, id] })); }
  function submit(event) {
    event.preventDefault();
    if (!draft.text.trim() && !draft.selected.length) { notify('Add a description or select a property first.'); return; }
    setDraft(d => ({ ...d, result: engine.match(d.text, d.selected, patterns), stale: false }));
  }
  return <><PageHead eyebrow="THE PROBLEM MAPPER" description="Paste your problem, add the properties you know, and explore methods that might fit. The goal is a reasoned starting point.">A clue becomes <em>a direction.</em></PageHead>
    <div className="finder-layout"><form className="panel" onSubmit={submit}>
      <h2>What are you trying to solve?</h2><p className="hint">Include the objective and constraints. Small details change the algorithm.</p>
      <label className="field-label" htmlFor="problem-text">Problem description</label><textarea id="problem-text" placeholder="Given an array of integers, count the subarrays whose sum equals k. Numbers can be negative…" value={draft.text} onChange={e => setDraft(d => ({ ...d, text: e.target.value, stale: true }))} />
      <div className="starter-links"><span className="count-label">Try one:</span>{Object.entries(starters).map(([label, text]) => <button type="button" key={label} onClick={() => setDraft({ text, selected: [], result: engine.match(text, [], patterns), stale: false })}>{label}</button>)}</div>
      <fieldset className="signal-fieldset"><legend className="field-label">Which properties do you see? <span className="count-label">Optional</span></legend><div className="signal-options">{engine.signals.map(s => <button type="button" key={s.id} className={`signal-option ${draft.selected.includes(s.id) ? 'selected' : ''}`} aria-pressed={draft.selected.includes(s.id)} onClick={() => { toggleSignal(s.id); setDraft(d => ({ ...d, stale: true })); }}>{s.label}</button>)}</div></fieldset>
      <div className="finder-actions"><button className="btn primary" type="submit">Find candidate methods ↗</button><button type="button" className="btn" onClick={() => setDraft({ text: '', selected: [], result: null, stale: false })}>Clear</button></div>
      <p className="finder-disclaimer">An explainable, rule-based guide. Check each method’s assumptions and prove your approach. Your description is processed in this browser.</p>
    </form><section className="panel" aria-live="polite">
      {!draft.result ? <div className="result-placeholder"><span className="big-icon">⌘</span><h2>Find the shape of the problem.</h2><p>Look for the structure, the objective,<br />and the condition you can maintain.</p><div className="insight">Structure → clues → candidates → proof</div></div> : <>
        <div className="eyebrow">CANDIDATE METHODS</div><h2 style={{ marginTop: 12 }}>Follow the evidence.</h2>
        {draft.stale && <p className="result-note">Your input changed. Run the mapper again to update these suggestions.</p>}
        <p className="hint">Ranked by matching clues. Some methods may work together; others are alternatives.</p>
        {!draft.result.results.length && <p className="hint">No clear match yet. Add the input structure, whether order matters, what you need to return, and any constraints. Select known properties to narrow the search.</p>}
        {draft.result.results.map((r, i) => <article className="result-card" key={r.pattern.id}><div className="result-title"><span>{r.pattern.icon} {r.pattern.name}</span><span className="rank">{i === 0 ? 'Start here' : 'Explore next'}</span></div><p>{r.pattern.use}</p><div className="evidence">{r.evidence.map(x => <div key={x}>↳ {x}</div>)}</div><p><strong>Verify:</strong> {r.pattern.pitfalls}</p><a href={`#pattern/${r.pattern.id}`}>Learn this method · 3 examples ↗</a></article>)}
        {draft.result.cautions.map(c => <p className="result-note" key={c}>{c}</p>)}
        <div className="finder-disclaimer">Next: write a brute-force solution, state an invariant or recurrence, then check that the complexity fits your input size.</div>
      </>}
    </section></div>
  </>;
}
