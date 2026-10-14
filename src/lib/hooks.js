import { useEffect, useState } from 'react';

export function useHashRoute() {
  const [hash, setHash] = useState(() => window.location.hash.slice(1) || 'assessment');
  useEffect(() => {
    const onHashChange = () => {
      setHash(window.location.hash.slice(1) || 'assessment');
      window.scrollTo(0, 0);
    };
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);
  return hash.split('/');
}

export function useProgress(patterns) {
  const [progress, setProgress] = useState(() => {
    const fallback = { learned: [], saved: [], quizBest: 0 };
    try {
      const stored = JSON.parse(localStorage.getItem('pattern-atlas-v1'));
      if (!stored) return fallback;
      return {
        learned: Array.isArray(stored.learned) ? [...new Set(stored.learned.filter(id => patterns.some(p => p.id === id)))] : [],
        saved: Array.isArray(stored.saved) ? [...new Set(stored.saved.filter(key => patterns.some(p => p.examples.some((_, i) => key === `${p.id}:${i}`))))] : [],
        quizBest: Math.max(0, Math.min(12, Number(stored.quizBest) || 0)),
      };
    } catch { return fallback; }
  });
  const [storageAvailable, setStorageAvailable] = useState(true);
  useEffect(() => {
    try { localStorage.setItem('pattern-atlas-v1', JSON.stringify(progress)); setStorageAvailable(true); }
    catch { setStorageAvailable(false); }
  }, [progress]);
  const toggleLearned = id => setProgress(p => ({ ...p, learned: p.learned.includes(id) ? p.learned.filter(x => x !== id) : [...p.learned, id] }));
  const toggleSaved = key => setProgress(p => ({ ...p, saved: p.saved.includes(key) ? p.saved.filter(x => x !== key) : [...p.saved, key] }));
  const recordScore = score => setProgress(p => ({ ...p, quizBest: Math.max(p.quizBest, score) }));
  return { progress, toggleLearned, toggleSaved, recordScore, storageAvailable };
}
