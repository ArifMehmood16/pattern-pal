import { useCallback, useEffect, useRef, useState } from 'react';
import { useHashRoute, useProgress } from './lib/hooks.js';
import Library from './components/Library.jsx';
import PatternDetail from './components/PatternDetail.jsx';
import ProblemMapper from './components/ProblemMapper.jsx';
import VisualPlayground from './components/AllPlaygrounds.jsx';
import RecognitionPractice, { initialQuiz } from './components/RecognitionPractice.jsx';
import SavedExamples from './components/SavedExamples.jsx';
import Resources from './components/Resources.jsx';
import { useJourney } from './lib/journey.js';
import { PreparationHub, PythonRefresh, ProblemBank } from './components/Preparation.jsx';
import SQLExamples from './components/SQLExamples.jsx';

const navigation = [
  ['assessment','◷','Tonight’s plan'], ['python','⌘','Python refresh'], ['problems','≋','Coding problems'],
  ['library', '▦', 'Pattern library'], ['sql','▤','SQL examples'],
  ['finder', '⌕', 'Problem mapper'], ['lab', '◉', 'Visual playground'],
  ['practice', '◇', 'Recognition practice'], ['saved', '♧', 'Saved examples'],
];
const names = Object.fromEntries(navigation.map(([id, , label]) => [id, label]));

export default function App(){
  const [patterns,setPatterns]=useState(null),[error,setError]=useState('');
  useEffect(()=>{const controller=new AbortController();fetch('/patterns.json',{signal:controller.signal}).then(r=>{if(!r.ok)throw new Error('Could not load the learning content. Restart npm run dev and reload.');return r.json();}).then(setPatterns).catch(e=>{if(e.name!=='AbortError')setError(e.message);});return()=>controller.abort();},[]);
  if(error)return <main><h1>Content could not load</h1><p>{error}</p></main>;
  if(!patterns)return <main><div className="eyebrow">PATTERNPAL</div><h1>Opening your field guide…</h1></main>;
  return <Workspace patterns={patterns}/>;
}

function Workspace({patterns}) {
  const [view, id, index] = useHashRoute();
  const { progress, toggleLearned, toggleSaved, recordScore, storageAvailable } = useProgress(patterns);
  const studyApi=useJourney();
  const [query, setQuery] = useState(''), [filter, setFilter] = useState('All methods');
  const [draft, setDraft] = useState({ text: '', selected: [], result: null, stale: false });
  const [quiz, setQuiz] = useState({ ...initialQuiz, choices: [] });
  const [toast, setToast] = useState('');
  const searchRef = useRef(null), focusPending = useRef(false);
  const notify = useCallback(message => setToast(message), []);
  useEffect(() => { if (!toast) return; const timer = setTimeout(() => setToast(''), 2800); return () => clearTimeout(timer); }, [toast]);
  const focusSearch = useCallback(() => {
    if (view !== 'library') { focusPending.current = true; window.location.hash = 'library'; }
    else searchRef.current?.focus();
  }, [view]);
  useEffect(() => { if (view === 'library' && focusPending.current) { searchRef.current?.focus(); focusPending.current = false; } }, [view]);
  useEffect(() => {
    const keydown = e => { if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); focusSearch(); } };
    document.addEventListener('keydown', keydown);
    return () => document.removeEventListener('keydown', keydown);
  }, [focusSearch]);
  const active = view === 'pattern' ? 'library' : view;
  let page;
  switch (view) {
    case 'pattern': page = <PatternDetail key={id} id={id} initialIndex={Number(index) || 0} patterns={patterns} progress={progress} toggleLearned={toggleLearned} toggleSaved={toggleSaved} notify={notify} studyApi={studyApi}/>; break;
    case 'assessment': page=<PreparationHub patterns={patterns} studyApi={studyApi}/>;break;
    case 'python': page=<PythonRefresh index={id} studyApi={studyApi} notify={notify}/>;break;
    case 'problems': page=<ProblemBank patterns={patterns} studyApi={studyApi}/>;break;
    case 'sql': page=<SQLExamples key={id||'0'} index={id} notify={notify}/>;break;
    case 'finder': page = <ProblemMapper patterns={patterns} draft={draft} setDraft={setDraft} notify={notify} />; break;
    case 'lab': page = <VisualPlayground patterns={patterns} />; break;
    case 'practice': page = <RecognitionPractice patterns={patterns} quiz={quiz} setQuiz={setQuiz} best={progress.quizBest} recordScore={recordScore} />; break;
    case 'saved': page = <SavedExamples saved={progress.saved} patterns={patterns} toggleSaved={toggleSaved} />; break;
    case 'resources': page = <Resources />; break;
    default: page = <Library patterns={patterns} learned={progress.learned} query={query} setQuery={setQuery} filter={filter} setFilter={setFilter} searchRef={searchRef} />;
  }
  return <>
    <a className="skip-link" href="#main" onClick={e => { e.preventDefault(); document.getElementById('main')?.focus(); }}>Skip to content</a>
    <aside className="sidebar"><a className="brand" href="#library"><span className="brand-mark" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><g fill="none" stroke="#7561cf" stroke-width="2.5" opacity=".5"><rect x="25" y="5" width="14" height="14" rx="4.5"/><rect x="45" y="5" width="14" height="14" rx="4.5"/><rect x="45" y="25" width="14" height="14" rx="4.5"/><rect x="5" y="45" width="14" height="14" rx="4.5"/><rect x="25" y="45" width="14" height="14" rx="4.5"/></g><g fill="#7561cf"><rect x="8" y="17" width="8" height="11"/><rect x="18" y="28" width="11" height="8"/><rect x="5" y="5" width="16" height="16" rx="5"/><rect x="5" y="25" width="16" height="16" rx="5"/><rect x="25" y="25" width="16" height="16" rx="5"/><rect x="44" y="44" width="16" height="16" rx="5"/><path d="M34 34L51 51" stroke="#7561cf" stroke-width="7"/></g></svg></span><span>pattern<span className="brand-light">pal</span><small>YOUR ALGORITHM SIDEKICK</small></span></a>
      <div className="sidebar-label">STUDY WORKSPACE</div><nav aria-label="Main navigation">{navigation.map(([route, icon, label]) => <a href={`#${route}`} className={active === route ? 'active' : ''} aria-current={active === route ? 'page' : undefined} key={route}><span>{icon}</span>{label}{route === 'library' && <i>{patterns.length}</i>}{route === 'sql' && <i>25</i>}</a>)}</nav>
      <div className="sidebar-bottom"><div className="journey-head">Your learning journey <span>{progress.learned.length} / {patterns.length}</span></div><div className="progress-track" role="progressbar" aria-label="Methods learned" aria-valuemin={0} aria-valuemax={patterns.length} aria-valuenow={progress.learned.length}><div style={{ width: `${progress.learned.length / patterns.length * 100}%` }} /></div><a href="#resources" className="resource-link">↗ Guides & resources</a><div className="local-note">◌ {storageAvailable ? 'Progress saved on this device' : 'Progress kept for this session'}</div></div>
    </aside>
    <div className="workspace"><header className="topbar"><div><span className="top-icon">⌘</span>Workspace / {view === 'resources' ? 'Guides & resources' : names[active] || 'Pattern library'}</div><div className="top-right"><span className="python-badge">● Python + SQL</span><button className="key-button" aria-label="Search patterns" onClick={focusSearch}>⌕ <kbd>⌘ K</kbd></button></div></header>
      <main id="main" tabIndex={-1}>{page}</main>
      <footer>
        <div className="footer-note">Made for the moment a problem starts to make sense.<span>21 methods · 107 coding examples · 25 SQL exercises</span></div>
        <div className="footer-author">
          <span className="footer-by">Built by <b>Arif Mehmood</b></span>
          <span className="footer-links">
            <a className="footer-link" href="https://github.com/ArifMehmood16" target="_blank" rel="noreferrer noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>GitHub</a>
            <a className="footer-link" href="https://www.linkedin.com/in/aarif9516" target="_blank" rel="noreferrer noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>LinkedIn</a>
          </span>
          <span className="footer-copy">© {new Date().getFullYear()} Arif Mehmood · All rights reserved</span>
        </div>
      </footer>
    </div><div id="toast" className={toast ? 'show' : ''} role="status" aria-live="polite">{toast}</div>
  </>;
}
