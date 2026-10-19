import { useState } from 'react';
import pack from '../data/challenges.json';
import { PageHead, CodeBlock } from './ui.jsx';

export const challengeCount = pack.challenges.length;

// Builds a plain Python test file the learner pastes under their own solution in their IDE.
export function buildTestFile(challenge, includeHidden) {
  const cases = challenge.tests.filter(t => includeHidden || t.visible);
  const lines = [`# ${challenge.title} — paste this below your solution() and run it.`, 'import time', '', 'cases = ['];
  for (const t of cases) lines.push(`    (${JSON.stringify(t.label)}, lambda: ${t.call.replace(/^solution/, 'solution')}, ${t.expected}),`);
  lines.push(']', '', 'passed = 0', 'for label, run, expected in cases:', '    start = time.perf_counter()', '    actual = run()', '    seconds = time.perf_counter() - start',
    '    status = "PASS" if actual == expected else "FAIL"', '    if seconds > 2:', '        status += " (slow: %.2fs)" % seconds',
    '    if actual == expected:', '        passed += 1', '    print(f"{status:<6} {label}: expected {expected}, got {actual}")', 'print(f"{passed} / {len(cases)} passed")');
  return lines.join('\n');
}

export default function Challenges({ studyApi, notify }) {
  const { study, setStudy } = studyApi;
  const done = Array.isArray(study.challenges) ? study.challenges : [];
  const toggle = id => setStudy(s => { const list = Array.isArray(s.challenges) ? s.challenges : []; return { ...s, challenges: list.includes(id) ? list.filter(x => x !== id) : [...list, id] }; });
  return <>
    <PageHead eyebrow="CHALLENGE PACK" description={pack.description}>{pack.title}<br /><em>Two stories, two techniques.</em></PageHead>
    <div className="challenge-index">{pack.challenges.map(c => <a key={c.id} href={`#challenge-${c.id}`} className="problem-row" onClick={e => { e.preventDefault(); document.getElementById(`challenge-${c.id}`)?.scrollIntoView({ behavior: 'smooth' }); }}>
      <span className="pattern-icon">{c.number}</span><div><h3>{c.title}</h3><p>{c.category} · {c.difficulty}</p></div>
      <span className={`status-pill ${done.includes(c.id) ? 'green' : ''}`}>{done.includes(c.id) ? '✓ Solved' : 'Not yet'}</span></a>)}</div>
    {pack.challenges.map(c => <Challenge key={c.id} c={c} solved={done.includes(c.id)} toggle={() => toggle(c.id)} notify={notify} />)}
  </>;
}

function Challenge({ c, solved, toggle, notify }) {
  const [hints, setHints] = useState(0), [solution, setSolution] = useState(''), [reasoning, setReasoning] = useState(false);
  const copy = async (text, message) => { try { await navigator.clipboard.writeText(text); notify(message); } catch { notify('Copy is blocked here. Select the text and copy it manually.'); } };
  const hidden = c.tests.filter(t => !t.visible);
  return <section className="challenge panel" id={`challenge-${c.id}`}>
    <div className="challenge-head"><div><div className="eyebrow">CHALLENGE {c.number} · {c.category}</div><h2>{c.title}</h2></div>
      <div className="challenge-tags"><span className="status-pill">{c.difficulty}</span><span className="count-label">Target {c.time} time · {c.space} space</span></div></div>
    {c.story.map((p, i) => <p className="challenge-text" key={i}>{p}</p>)}
    <h3>Problem</h3><p className="challenge-text">{c.statement}</p>
    <CodeBlock code={c.signature} title="signature.py" />
    <h3>Examples</h3>
    <div className="challenge-examples">{c.examples.map((e, i) => <div className="challenge-example" key={i}><b>Example {i + 1}</b><code>{e.input}</code><code>→ {e.output}</code><p>{e.why}</p></div>)}</div>
    <h3>Constraints</h3><ul className="challenge-list">{c.constraints.map(x => <li key={x}>{x}</li>)}</ul>

    <h3>Test in your IDE</h3>
    <p className="challenge-text">Write <code>solution</code> in your own editor, then paste a test file below it. The full set adds {hidden.length} edge cases, including maximum-size inputs that a brute-force answer will struggle with.</p>
    <div className="challenge-actions">
      <button className="btn" onClick={() => copy(buildTestFile(c, false), 'Sample tests copied')}>Copy sample tests</button>
      <button className="btn" onClick={() => copy(buildTestFile(c, true), `All ${c.tests.length} tests copied`)}>Copy all {c.tests.length} tests</button>
    </div>
    <details className="challenge-details"><summary>See the edge cases ({hidden.length})</summary><ul className="challenge-list">{hidden.map((t, i) => <li key={i}><b>{t.label}</b> <code>{t.call}</code> → <code>{t.expected}</code><span> {t.why}</span></li>)}</ul></details>

    <h3>Hints</h3>
    {c.hints.slice(0, hints).map((h, i) => <div className="challenge-hint" key={i}><b>Hint {i + 1} · {h.title}</b><p>{h.text}</p></div>)}
    {hints < c.hints.length ? <button className="btn" onClick={() => setHints(hints + 1)}>Show hint {hints + 1} of {c.hints.length}</button> : <p className="count-label">All hints shown.</p>}

    <h3>Reference solutions</h3>
    <div className="challenge-actions">
      <button className={`btn ${solution === 'brute' ? 'primary' : ''}`} onClick={() => setSolution(solution === 'brute' ? '' : 'brute')}>{solution === 'brute' ? 'Hide' : 'Reveal'} brute force</button>
      <button className={`btn ${solution === 'optimal' ? 'primary' : ''}`} onClick={() => setSolution(solution === 'optimal' ? '' : 'optimal')}>{solution === 'optimal' ? 'Hide' : 'Reveal'} optimal</button>
    </div>
    {solution === 'brute' && <><p className="count-label">{c.bruteComplexity}</p><CodeBlock code={c.brute} title="brute_force.py" /><button className="btn small" onClick={() => copy(c.brute, 'Brute force copied')}>Copy</button></>}
    {solution === 'optimal' && <><p className="count-label">{c.pattern} · {c.time} time · {c.space} space</p><CodeBlock code={c.optimal} title="optimal.py" /><p className="challenge-text">{c.whyFast}</p><button className="btn small" onClick={() => copy(c.optimal, 'Optimal solution copied')}>Copy</button></>}

    <h3>After you solve it</h3>
    <div className="challenge-actions">
      <button className={`btn ${solved ? 'primary' : ''}`} onClick={toggle} aria-pressed={solved}>{solved ? '✓ Marked solved' : 'Mark as solved'}</button>
      <button className="btn" onClick={() => setReasoning(!reasoning)} aria-expanded={reasoning}>{reasoning ? 'Hide' : 'Show'} interview walkthrough</button>
    </div>
    {reasoning && <div className="challenge-reasoning">{c.reasoning.map(r => <div key={r.title}><b>{r.title}</b><p>{r.text}</p></div>)}</div>}
  </section>;
}
