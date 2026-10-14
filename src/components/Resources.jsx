import { PageHead } from './ui.jsx';

const resources = [
  ['NeetCode roadmap', 'A structured sequence of interview problems. Use it to practice each method and then mix topics.', 'https://neetcode.io/roadmap', 'Explore the roadmap'],
  ['Grokking companion', 'A free companion repository from Design Gurus with pattern recognition guidance and cheat sheets.', 'https://github.com/design-gurus/grokking-coding-interview', 'Open the companion'],
  ['Labuladong’s Algorithm Notes', 'Framework-oriented explanations, algorithm visualizations, and practice.', 'https://labuladong.online/en/', 'Read the notes'],
  ['Competitive Programmer’s Handbook', 'Antti Laaksonen’s free book. Extend your toolkit beyond common interview patterns.', 'https://cses.fi/book/index.php', 'Get the handbook'],
];
export default function Resources() {
  return <><PageHead eyebrow="GO A LITTLE DEEPER" description="Use these published guides alongside the Atlas. This library is a practical grouping of methods, not an exhaustive taxonomy.">Build intuition.<br /><em>Then build range.</em></PageHead>
    <div className="resource-grid">{resources.map(([title, description, url, label]) => <article className="panel" key={url}><h2>{title}</h2><p>{description}</p><a href={url} target="_blank" rel="noopener noreferrer">{label} ↗</a></article>)}</div>
    <div className="note invariant" style={{ marginTop: 25 }}><h3>A STUDY ROUTINE THAT TRANSFERS</h3><p>For each method: explain its assumptions, write its invariant, solve three variations, and revisit it in mixed practice. Broader topics include segment trees, Fenwick trees, meet-in-the-middle, and specialised dynamic programming. Recognition narrows your search; correctness still needs reasoning.</p></div>
  </>;
}
