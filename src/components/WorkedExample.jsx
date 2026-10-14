import {useState} from 'react';
import {CodeBlock} from './ui.jsx';
import TraceViewer from './TraceViewer.jsx';

export default function WorkedExample({example,notify,showConstraints=true}){
  const [activeLine,setActiveLine]=useState(null);
  async function copy(){try{await navigator.clipboard.writeText(example.code);notify?.('Python code copied.');}catch{notify?.('Select the code to copy it.');}}
  return <>
    <section className="lesson-contract"><h3>The problem</h3><p>{example.prompt}</p>{showConstraints&&example.constraints&&<><h4>Constraints and assumptions</h4><ul>{example.constraints.map(c=><li key={c}>{c}</li>)}</ul></>}
      <h4>Example inputs and outputs</h4><div className="io-grid">{(example.samples||[{input:example.sampleInput,output:example.sampleOutput}]).map((sample,i)=><div className="sample-box" key={i}><span>INPUT {i+1}</span><code>{sample.input}</code><span>OUTPUT</span><code>{sample.output}</code></div>)}</div>
    </section>
    {example.patternNote&&<div className="note invariant"><h3>HOW THIS EXAMPLE CONNECTS</h3><p>{example.patternNote}</p></div>}
    <section className="reference-solution"><div className="section-head"><h2>The whole solution</h2><button className="btn small" onClick={copy}>Copy code for your IDE</button></div>
      <CodeBlock code={example.code} activeLine={activeLine}/>
      {/ListNode|TreeNode/.test(example.code)&&<p className="hint">Uses LeetCode’s standard ListNode / TreeNode definitions. Node references are shown as readable lists or trees in the visual playground. <a className="text-link" href="/practice_fixtures.py" download>Get node types and sample builders for your IDE ↗</a></p>}
      <div className="insight"><strong>Why this approach works</strong>{(example.explanation||[example.insight]).map((text,i)=><p key={i}>{text}</p>)}</div>
      <h3 className="lesson-subtitle">Explain it block by block</h3><ol className="block-explanation">{example.blocks?.map((block,i)=><li key={i}><span>Lines {block.start}{block.end!==block.start?`–${block.end}`:''}</span><p>{block.text}</p></li>)}</ol>
      <div className="complexity-grid"><article className="note"><h3>TIME · {example.time}</h3><p>{example.timeReason||example.explanation?.find(t=>/time|O\(/.test(t))}</p></article><article className="note"><h3>SPACE · {example.space}</h3><p>{example.spaceReason||example.explanation?.find(t=>/space|O\(/.test(t))}</p></article></div>
      {example.optimality&&<div className="note invariant"><h3>WHY THIS IMPLEMENTATION / THE TRADEOFF</h3><p>{example.optimality}</p></div>}
      <TraceViewer example={example} onLine={setActiveLine}/>
      <div className="note"><h3>TRANSFER IT TO AN UNSEEN PROBLEM</h3><p>Predict the next playground state before advancing. Then rebuild this solution in your IDE, test a new legal input, and change one constraint. Explain whether the same pattern still applies.</p></div>
    </section>
  </>;
}
