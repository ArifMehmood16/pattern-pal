import { PageHead } from './ui.jsx';

export default function SavedExamples({ saved, patterns, toggleSaved }) {
  return <><PageHead eyebrow="YOUR COLLECTION" description="Save reference implementations as you explore. Your collection stays in this browser on this device.">Good ideas, <em>kept close.</em></PageHead>
    {saved.length ? saved.map(key => {
      const [id, index] = key.split(':'), p = patterns.find(p => p.id === id), example = p?.examples[Number(index)];
      if (!example) return null;
      return <article className="saved-card" key={key}><span className="pattern-icon">{p.icon}</span><div><h3>{example.title}</h3><p>{p.name} · {example.difficulty}</p></div><a className="btn small" href={`#pattern/${id}/${index}`}>Open example ↗</a><button className="btn small" aria-label={`Remove ${example.title}`} onClick={() => toggleSaved(key)}>Remove</button></article>;
    }) : <div className="empty">Your collection is ready for its first idea.<br /><br /><a className="btn primary" href="#library">Explore the library ↗</a></div>}
  </>;
}
