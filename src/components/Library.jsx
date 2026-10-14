import { useMemo } from 'react';
import { PatternCard } from './ui.jsx';

const filters = ['All methods', 'Sequences', 'Structures', 'Search', 'Traversal', 'Optimization', 'Foundations', 'Learned'];

export default function Library({ patterns, learned, query, setQuery, filter, setFilter, searchRef }) {
  const matches = useMemo(() => patterns.filter(p => {
    const categoryMatches = filter === 'All methods' || p.group === filter || (filter === 'Learned' && learned.includes(p.id));
    const text = [p.name, p.summary, ...p.signals, ...p.examples.map(e => e.title)].join(' ').toLowerCase();
    return categoryMatches && text.includes(query.toLowerCase());
  }), [patterns, learned, query, filter]);
  return <>
    <section className="hero"><div className="hero-text">
      <div className="eyebrow">LESS GUESSING. MORE UNDERSTANDING.</div>
      <h1>Different problems.<br />The same <em>beautiful patterns.</em></h1>
      <p className="intro">Learn to see the algorithm hiding inside the question.<br />Explore the methods, connect the clues, and build your intuition.</p>
      <div className="stats"><div><b>{patterns.length}</b> core methods</div><div className="divider" /><div><b>{patterns.reduce((n,p)=>n+p.examples.length,0)}</b> Python examples</div><div className="divider" /><div><b>25</b> SQL exercises</div></div>
    </div><div className="hero-art" aria-hidden="true"><div className="art-ring" /><div className="art-node center">✳</div><div className="art-node a">⇆</div><div className="art-node b">⑂</div><div className="art-node c">∑</div><div className="art-node d">▦</div><div className="art-label">EVERYTHING CONNECTS</div></div></section>
    <section className="finder-banner"><span className="banner-icon">◷</span><div><h3>Preparing for tonight’s assessment?</h3><p>Follow the focused Python route, then practise under a timer.</p></div><a className="btn" href="#assessment">Open your preparation plan <span>↗</span></a></section>
    <div className="section-head"><h2>The pattern library <small>Your toolkit, one method at a time</small></h2><label className="search-box"><span aria-hidden="true">⌕</span><input ref={searchRef} aria-label="Search methods and examples" placeholder="Search a method or problem…" value={query} onChange={e => setQuery(e.target.value)} /></label></div>
    <div className="filters">{filters.map(f => <button key={f} className={`filter ${f === filter ? 'active' : ''}`} aria-pressed={f === filter} onClick={() => setFilter(f)}>{f}</button>)}</div>
    <div className="grid">{matches.length ? matches.map(p => <PatternCard key={p.id} pattern={p} learned={learned.includes(p.id)} />) : <div className="empty">No methods match yet. Try another search or choose All methods.</div>}</div>
  </>;
}
