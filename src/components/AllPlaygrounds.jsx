import {useState} from 'react';
import drills from '../data/python-drills.json';
import {CodeBlock,PageHead} from './ui.jsx';
import TraceViewer from './TraceViewer.jsx';

export default function AllPlaygrounds({patterns}){
  const [selected,setSelected]=useState('window:0'),[line,setLine]=useState(null);
  const [id,index]=selected.split(':');
  const method=patterns.find(p=>p.id===id);
  const example=id==='python'?drills[Number(index)]:method.examples[Number(index)];
  return <><PageHead eyebrow="A PLAYGROUND FOR EVERY EXAMPLE" description="Choose any coding example or Python refresher. See its complete execution, all before/after variables, array positions, object references and matrix cells.">Watch the data.<br/><em>Explain every change.</em></PageHead>
    <div className="lesson-selector playground-selector"><label>Choose a visual example<select aria-label="Playground example" value={selected} onChange={e=>{setSelected(e.target.value);setLine(null);}}>{patterns.map(p=><optgroup key={p.id} label={p.name}>{p.examples.map((e,i)=><option key={e.title} value={`${p.id}:${i}`}>{e.title}</option>)}</optgroup>)}<optgroup label="Python refresh">{drills.map((e,i)=><option key={e.title} value={`python:${i}`}>{e.title}</option>)}</optgroup></select></label></div>
    <div className="note invariant" style={{marginBottom:22}}><h3>{example.title}</h3><p>{example.prompt}</p><p>{example.insight}</p></div>
    <div className="global-playground"><TraceViewer key={selected} example={example} onLine={setLine}/><section className="playground-code"><CodeBlock code={example.code} activeLine={line}/><div className="note" style={{marginTop:18}}><h3>TIME · {example.time}</h3><p>{example.timeReason||example.explanation?.find(t=>/time|O\(/.test(t))}</p><h3 style={{marginTop:20}}>SPACE · {example.space}</h3><p>{example.spaceReason||example.explanation?.find(t=>/space|O\(/.test(t))}</p></div><a className="btn" style={{marginTop:18}} href={id==='python'?`#python/${index}`:`#pattern/${id}/${index}`}>Open the full explanation ↗</a></section></div>
  </>;
}
