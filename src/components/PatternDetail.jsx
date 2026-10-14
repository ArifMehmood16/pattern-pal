import { useEffect, useRef, useState } from 'react';
import { RelatedMethods, PageHead } from './ui.jsx';
import Exercise from './WorkedExample.jsx';

export default function PatternDetail({ id, initialIndex, patterns, progress, toggleLearned, toggleSaved, notify, studyApi }) {
  const pattern = patterns.find(p => p.id === id);
  const [index, setIndex] = useState(0);
  const tabsRef = useRef([]);
  useEffect(() => { setIndex(Number.isInteger(initialIndex) && initialIndex >= 0 && initialIndex < (pattern?.examples.length||0) ? initialIndex : 0); }, [id, initialIndex, pattern]);
  if (!pattern) return <><PageHead eyebrow="NOT FOUND" description="Return to the library to choose a method.">That pattern is not here.</PageHead><a className="btn primary" href="#library">Open the library</a></>;
  const safeIndex=Math.min(index,pattern.examples.length-1);
  const example = pattern.examples[safeIndex], key = `${id}:${safeIndex}`, learned = progress.learned.includes(id), saved = progress.saved.includes(key);
  function tabKey(event, position) {
    let next;
    if (event.key === 'ArrowRight') next = (position + 1) % pattern.examples.length;
    if (event.key === 'ArrowLeft') next = (position + pattern.examples.length - 1) % pattern.examples.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = pattern.examples.length - 1;
    if (next !== undefined) { event.preventDefault(); setIndex(next); tabsRef.current[next]?.focus(); }
  }
  return <>
    <a className="back-link" href="#library">← Back to the library</a>
    <div className="detail-head"><div><span className="pattern-icon">{pattern.icon}</span><div className="eyebrow">{pattern.group} · METHOD {String(patterns.indexOf(pattern) + 1).padStart(2, '0')}</div><h1>{pattern.name}</h1><p className="intro">{pattern.summary}</p></div><button className={`btn ${learned ? '' : 'primary'}`} onClick={() => toggleLearned(id)}>{learned ? '✓ Learned · undo' : 'Mark as learned'}</button></div>
    <section className="pattern-definition"><h2>What this pattern means</h2><p>{pattern.definition}</p><h3>Why and when it helps</h3><p>{pattern.reasoning}</p><div className="insight"><b>A concrete example</b><p>{pattern.concreteExample}</p></div></section>
    <div className="overview-grid"><div className="note"><h3>WHEN TO REACH FOR IT</h3><p>{pattern.use}</p></div><div className="note invariant"><h3>THE INVARIANT · WHAT STAYS TRUE</h3><p>{pattern.invariant}</p></div></div>
    <div className="note caution"><h3>CHECK BEFORE YOU CODE</h3><p>{pattern.pitfalls}</p></div>
    <div className="section-head"><h2>From idea to implementation <small>{pattern.examples.length} worked Python examples · explain, trace, rebuild</small></h2></div>
    <div className="example-layout"><div className="example-menu" role="tablist" aria-label="Code examples">{pattern.examples.map((e, i) => <button key={e.title} ref={node => { tabsRef.current[i] = node; }} id={`example-tab-${i}`} className={`example-tab ${i === index ? 'active' : ''}`} role="tab" aria-selected={i === index} aria-controls="example-panel" tabIndex={i === index ? 0 : -1} onKeyDown={event => tabKey(event, i)} onClick={() => setIndex(i)}>{String(i + 1).padStart(2, '0')} · {e.title}<small>{e.difficulty} · {e.time}</small></button>)}</div>
      <section className="example-panel" id="example-panel" role="tabpanel" aria-labelledby={`example-tab-${index}`}>
        <div className="example-toolbar"><button className="btn small" onClick={() => toggleSaved(key)}>{saved ? '✓ Saved' : '♧ Save'}</button><span className="status-pill">{example.priority}</span></div>
        <h2>{example.title}</h2><Exercise key={`${id}:${safeIndex}`} example={example} exerciseKey={`algorithm:${id}:${safeIndex}`} title={example.title} studyApi={studyApi} notify={notify}/>
      </section>
    </div><RelatedMethods ids={pattern.related} patterns={patterns} />
  </>;
}
