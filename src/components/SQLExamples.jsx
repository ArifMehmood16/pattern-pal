import {useState} from 'react';
import sql from '../data/sql-lessons.json';
import {PageHead,CodeBlock} from './ui.jsx';
import {DataTable} from './TraceViewer.jsx';

const work={
  Filtering:'A full scan examines N rows. A useful index may reduce access work, but OR predicates and selectivity affect the chosen plan. The final ORDER BY may require a sort.',
  Joins:'Join cost depends on access paths: an unindexed nested-loop join can examine N×M pairs; indexed lookups or a hash join can reduce that. Preserve the intended one-to-many row multiplicity.',
  Grouping:'A hash aggregation can scan N rows with expected O(N) grouping work and storage proportional to distinct groups; a sort-based plan can cost O(N log N). The database chooses its plan.',
  Subqueries:'Compute the scalar aggregate once, then filter and aggregate the outer rows. Confirm that the optimizer does not repeat work unnecessarily; indexes may accelerate extrema.',
  Ranking:'Ranking commonly requires sorting rows within each partition, bounded by O(N log N) comparison work without an already useful order. Ranking then scans the sorted rows. Sort memory depends on the execution plan.',
  'Window functions':'Aggregate first when the desired grain is one row per day, then evaluate the window. Sorting the resulting K rows can cost O(K log K); keeping fewer rows reduces later work and storage.',
  'Conditional aggregation':'One grouped pass accumulates numerator and denominator together. Avoid joining unrelated one-to-many tables into that pass because it multiplies both work and counts.',
  Dates:'Join/filter on the required calendar relation, not merely neighboring available rows. Useful date and entity indexes can reduce searches; date conversions may affect index use. Confirm the plan in the target database.',
  CTEs:'The CTE names a grouped intermediate result. It is not automatically a performance optimization: materialization and join strategy depend on the database. Grouping before a many-to-one join prevents repeated aggregate work.',
  'Set operations':'UNION must deduplicate complete result rows, typically using hashing or sorting. UNION ALL can concatenate when duplicates are allowed and avoids that deduplication cost.',
};

export default function SQLExamples({index,notify}){
  const i=Math.max(0,Math.min(sql.lessons.length-1,Math.trunc(Number(index))||0)),lesson=sql.lessons[i];
  const [dialect,setDialect]=useState('SQLite');
  const code=dialect==='SQLite'?lesson.code:lesson.postgres;
  async function copy(){try{await navigator.clipboard.writeText(code);notify?.('SQL query copied.');}catch{notify?.('Select the query to copy it.');}}
  return <><PageHead eyebrow="SQL · WORKED EXAMPLES" description="Twenty-five queries with complete input tables, expected output, and step-by-step explanations. Read here and practise in your own database or IDE.">Understand the rows.<br/><em>Understand the query.</em></PageHead>
    <div className="lesson-selector"><label>Choose an example<select value={i} onChange={e=>{window.location.hash=`sql/${e.target.value}`;}}>{sql.lessons.map((q,index)=><option key={q.title} value={index}>{index+1}. {q.title} · {q.category}</option>)}</select></label><span className="status-pill">{lesson.priority}</span></div>
    <section className="panel"><h2>{lesson.title}</h2><p className="intro">{lesson.prompt}</p>
      <details className="reference-card" open><summary>Input tables · every sample row</summary><div className="input-tables">{lesson.inputs.map(table=><DataTable key={table.name} table={table} label={table.name}/>)}</div></details>
      <DataTable table={lesson.expected} label="Expected output · the exercise specifies this row order"/>
      <section className="reference-solution"><div className="section-head"><h2>The whole query</h2><div className="action-row" style={{margin:0}}><select aria-label="Reference SQL dialect" value={dialect} onChange={e=>setDialect(e.target.value)}><option>SQLite</option><option>PostgreSQL</option></select><button className="btn small" onClick={copy}>Copy query</button></div></div><CodeBlock title="solution.sql" language={dialect} code={code}/>
        <p className="hint">Sample dates are ISO text. The PostgreSQL variant uses explicit date casts where required. The sample outputs were verified with SQLite; PostgreSQL references are provided for use in your own database.</p>
        <h3 className="lesson-subtitle">How the data changes</h3><ol className="block-explanation">{lesson.steps.map((step,i)=><li key={i}><span>Stage {i+1}</span><p>{step}</p></li>)}</ol>
        {lesson.stages?.map(table=><DataTable key={table.name} table={table} label={table.name}/>)}
        <div className="note invariant"><h3>REASON ABOUT THE QUERY’S WORK</h3><p>{work[lesson.category]}</p><p>SQL has no universal time/space bound from query text alone. Table cardinalities, indexes, statistics, join algorithms and sort memory determine its physical cost. Use EXPLAIN in your target database to check those assumptions.</p></div>
        <div className="result-note"><b>Common mistake:</b> {lesson.trap}</div>
      </section>
      <details className="reference-card"><summary>Sample schema and rows for your IDE</summary><CodeBlock title="setup.sql" language="SQLite" code={lesson.setup}/></details>
    </section>
    <details className="reference-card" open><summary>SQL foundations · {sql.foundations.length} essentials</summary><div className="pitfall-grid">{sql.foundations.map(([title,text])=><article className="note" key={title}><h3>{title}</h3><p>{text}</p></article>)}</div><p className="hint">Official references: {sql.sources.map(([title,url])=><a className="text-link" href={url} key={url} target="_blank" rel="noreferrer">{title} ↗ </a>)}</p></details>
  </>;
}
