import engine from '../lib/engine.js';
import { PageHead } from './ui.jsx';

export const initialQuiz = { index: 0, choices: [], checked: false, score: 0, finished: false };

export function isCorrect(question, choices) {
  const same = answer => answer.length === choices.length && answer.every(id => choices.includes(id));
  return same(question.answers) || (question.alternatives || []).some(same);
}

export default function RecognitionPractice({ patterns, quiz, setQuiz, best, recordScore }) {
  const questions = engine.quizzes, question = questions[quiz.index];
  function toggle(id) { setQuiz(q => ({ ...q, choices: q.choices.includes(id) ? q.choices.filter(x => x !== id) : [...q.choices, id] })); }
  function next() {
    if (!quiz.checked) { setQuiz(q => ({ ...q, checked: true, score: q.score + (isCorrect(question, q.choices) ? 1 : 0) })); }
    else if (quiz.index === questions.length - 1) { recordScore(quiz.score); setQuiz(q => ({ ...q, finished: true })); }
    else setQuiz(q => ({ ...q, index: q.index + 1, choices: [], checked: false }));
  }
  const success = isCorrect(question, quiz.choices);
  return <><PageHead eyebrow="RECOGNITION PRACTICE" description="Practice without tags. Choose the best methods among the options; some questions need a combination.">Name the method.<br /><em>Explain the choice.</em></PageHead>
    <section className="panel quiz-panel">{quiz.finished ? <>
      <div className="eyebrow">SESSION COMPLETE</div><h2 className="quiz-title" style={{ marginTop: 20 }}>{quiz.score} / {questions.length} patterns recognised.</h2><p className="hint">Best session on this device: {best} / {questions.length}. Revisit the explanations, then try again.</p><button className="btn primary" onClick={() => setQuiz({ ...initialQuiz, choices: [] })}>Start another session ↗</button>
    </> : <>
      <div className="quiz-progress" aria-label={`Question ${quiz.index + 1} of ${questions.length}`}>{questions.map((_, i) => <span className={i <= quiz.index ? 'done' : ''} key={i} />)}</div>
      <div className="eyebrow">QUESTION {quiz.index + 1} OF {questions.length} · CHOOSE ALL THAT APPLY</div><h2 className="quiz-title" style={{ marginTop: 16 }}>{question.title}</h2>
      <div className="quiz-options">{question.options.map(id => {
        const p = patterns.find(p => p.id === id);
        const preferred = quiz.checked && question.answers.includes(id);
        const wrong = quiz.checked && !success && quiz.choices.includes(id) && !question.answers.includes(id);
        return <button key={id} className={`${quiz.choices.includes(id) ? 'selected' : ''} ${preferred ? 'correct' : ''} ${wrong ? 'wrong' : ''}`} aria-pressed={quiz.choices.includes(id)} disabled={quiz.checked} onClick={() => toggle(id)}>{p.icon} &nbsp; {p.name}</button>;
      })}</div>
      {quiz.checked && <div className={`quiz-feedback ${success ? '' : 'partial'}`} role="status"><strong>{success ? 'You spotted it.' : 'Here is the connection.'}</strong><br />{question.why}<div className="related">{question.answers.map(id => <a key={id} href={`#pattern/${id}`}>{patterns.find(p => p.id === id).name} ↗</a>)}</div></div>}
      <div className="quiz-bottom"><span>{quiz.score} correct so far</span><button className="btn primary" disabled={!quiz.checked && !quiz.choices.length} onClick={next}>{quiz.checked ? quiz.index === questions.length - 1 ? 'See results' : 'Next question →' : 'Check my reasoning'}</button></div>
    </>}</section>
  </>;
}
