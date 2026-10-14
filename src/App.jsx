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
    <aside className="sidebar"><a className="brand" href="#library"><span className="brand-mark">✳</span><span>pattern<span className="brand-light">pal</span><small>YOUR ALGORITHM SIDEKICK</small></span></a>
      <div className="sidebar-label">STUDY WORKSPACE</div><nav aria-label="Main navigation">{navigation.map(([route, icon, label]) => <a href={`#${route}`} className={active === route ? 'active' : ''} aria-current={active === route ? 'page' : undefined} key={route}><span>{icon}</span>{label}{route === 'library' && <i>{patterns.length}</i>}{route === 'sql' && <i>25</i>}</a>)}</nav>
      <div className="sidebar-bottom"><div className="journey-head">Your learning journey <span>{progress.learned.length} / {patterns.length}</span></div><div className="progress-track" role="progressbar" aria-label="Methods learned" aria-valuemin={0} aria-valuemax={patterns.length} aria-valuenow={progress.learned.length}><div style={{ width: `${progress.learned.length / patterns.length * 100}%` }} /></div><a href="#resources" className="resource-link">↗ Guides & resources</a><div className="local-note">◌ {storageAvailable ? 'Progress saved on this device' : 'Progress kept for this session'}</div></div>
    </aside>
    <div className="workspace"><header className="topbar"><div><span className="top-icon">⌘</span>Workspace / {view === 'resources' ? 'Guides & resources' : names[active] || 'Pattern library'}</div><div className="top-right"><span className="python-badge">● Python + SQL</span><button className="key-button" aria-label="Search patterns" onClick={focusSearch}>⌕ <kbd>⌘ K</kbd></button></div></header>
      <main id="main" tabIndex={-1}>{page}</main><footer>Made for the moment a problem starts to make sense.<span>21 methods · 107 coding examples · 25 SQL exercises</span></footer>
    </div><div id="toast" className={toast ? 'show' : ''} role="status" aria-live="polite">{toast}</div>
  </>;
}
