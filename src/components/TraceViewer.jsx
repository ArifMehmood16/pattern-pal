import {useEffect, useId, useMemo, useRef, useState} from 'react';
import {createPortal} from 'react-dom';
import {CodeBlock} from './ui.jsx';

const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const display=value=>value===undefined?'Not defined yet':JSON.stringify(value,null,2);
const compact=value=>value===undefined?'Not defined yet':JSON.stringify(value);

export function DataTable({table,label,previous}) {
  return <div className="data-table-scroll"><table className="data-table"><caption>{label}</caption><thead><tr>{table.columns.map((column,i)=><th key={i}>{column}</th>)}</tr></thead><tbody>{table.values.length?table.values.map((row,i)=><tr key={i}>{row.map((value,j)=><td key={j} className={previous&&j>0&&!same(value,previous[i]?.[j-1])?'value-changed':''}>{value===null?<em>NULL</em>:String(value)}</td>)}</tr>):<tr><td colSpan={table.columns.length}>No rows</td></tr>}</tbody></table></div>;
}

function Value({value,previous,markers={}}) {
  if(value===undefined)return <span className="count-label">Not defined yet</span>;
  if(Array.isArray(value)&&value.length&&value.every(Array.isArray)){
    const width=Math.max(...value.map(row=>row.length));
    return <DataTable label="Matrix · row and column indices" previous={previous} table={{columns:['r / c',...Array.from({length:width},(_,i)=>i)],values:value.map((row,i)=>[i,...row.map(v=>typeof v==='object'?JSON.stringify(v):v)])}}/>;
  }
  if(Array.isArray(value))return <div className="trace-array">{value.length?value.map((v,i)=><div key={i} className={previous&&!same(v,previous[i])?'value-changed':''}><small>index {i}</small><code>{typeof v==='object'?JSON.stringify(v):String(v)}</code>{Object.entries(markers).filter(([,position])=>position===i).map(([name])=><span className="index-marker" key={name}>{name}</span>)}</div>):<code>[]</code>}</div>;
  return <pre className="state-value">{display(value)}</pre>;
}

function Inspector({kind,side,onMove,onDrag,onDragMove,onDragEnd,children}){
  const title=kind==='code'?'Complete Python code':'Variables & objects';
  return <aside className={`trace-inspector inspector-${kind}`} aria-label={title}>
    <header className="inspector-head">
      <button className="inspector-grip" aria-label={`Move ${kind} panel. Drag to the other side or press Enter to swap.`} title="Drag to the other side · Enter to swap" onPointerDown={onDrag} onPointerMove={onDragMove} onPointerUp={onDragEnd} onPointerCancel={onDragEnd} onClick={e=>{if(e.detail===0)onMove();}}>⠿ <span>{title}</span></button>
      <button className="inspector-swap" aria-label={`Move ${kind} panel ${side==='left'?'right':'left'}`} title="Swap panel sides" onClick={onMove}>{side==='left'?'⇥':'⇤'}</button>
    </header>
    {children}
  </aside>;
}

export default function TraceViewer({example,onLine}){
  const [data,setData]=useState(null),[error,setError]=useState(''),[index,setIndex]=useState(0),[all,setAll]=useState(false),[sample,setSample]=useState(0);
  const [focused,setFocused]=useState(false),[playing,setPlaying]=useState(false),[speed,setSpeed]=useState(1000),[follow,setFollow]=useState(true),[codeSide,setCodeSide]=useState('left'),[dropSide,setDropSide]=useState(null),[selected,setSelected]=useState(''),[copied,setCopied]=useState(false);
  const panelRef=useRef(null),boardRef=useRef(null),focusButton=useRef(null),exitButton=useRef(null),dragRef=useRef(null),titleId=useId();
  const traceUrl=example.traces?.[sample]?.url||example.traceUrl;
  useEffect(()=>{
    const controller=new AbortController();setData(null);setError('');setIndex(0);setPlaying(false);setSelected('');setAll(false);setCopied(false);
    fetch(traceUrl,{signal:controller.signal}).then(r=>{if(!r.ok)throw new Error('Trace file unavailable. Run npm run content:generate.');return r.json();}).then(setData).catch(e=>{if(e.name!=='AbortError')setError(e.message);});
    return()=>controller.abort();
  },[traceUrl]);
  const step=data?.steps[index];
  useEffect(()=>{onLine?.(step?.line);},[step?.line,onLine]);
  useEffect(()=>{
    if(!playing||!data)return;
    if(index>=data.steps.length-1){setPlaying(false);return;}
    const timer=setTimeout(()=>setIndex(i=>Math.min(i+1,data.steps.length-1)),speed);
    return()=>clearTimeout(timer);
  },[playing,index,speed,data]);
  useEffect(()=>{
    if(!focused)return;
    const previousFocus=document.activeElement,root=document.getElementById('root'),wasInert=root?.inert,overflow=document.body.style.overflow;
    if(root)root.inert=true;
    document.body.style.overflow='hidden';exitButton.current?.focus();
    const keydown=e=>{
      if(e.key==='Escape'){e.preventDefault();setFocused(false);setPlaying(false);}
      if(e.key!=='Tab')return;
      const nodes=[...panelRef.current?.querySelectorAll('button:not(:disabled), select, input, a[href], summary')||[]].filter(el=>el.getClientRects().length);
      const first=nodes[0],last=nodes.at(-1);
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus();}
    };
    document.addEventListener('keydown',keydown);
    return()=>{
      document.removeEventListener('keydown',keydown);document.body.style.overflow=overflow;
      if(root)root.inert=wasInert;
      if(previousFocus?.isConnected)previousFocus.focus();else focusButton.current?.focus();
    };
  },[focused]);
  useEffect(()=>{
    if(focused&&!panelRef.current?.contains(document.activeElement))exitButton.current?.focus();
  },[focused,data,error]);
  const nextSameCall=useMemo(()=>data?.steps.slice(index+1).find(s=>s.call===step?.call),[data,index,step?.call]);
  function jump(next){setPlaying(false);setIndex(next);}
  function swap(){setCodeSide(side=>side==='left'?'right':'left');setDropSide(null);}
  function dragStart(event,kind,side){
    if(event.button!==0)return;
    event.currentTarget.setPointerCapture(event.pointerId);
    dragRef.current={kind,side,startX:event.clientX,startY:event.clientY,moved:false,target:side};
  }
  function closestDock(event){
    const docks=['left','right'].map(side=>{
      const rect=boardRef.current.querySelector(`.dock-${side}`).getBoundingClientRect();
      return {side,distance:Math.hypot(event.clientX-(rect.left+rect.width/2),event.clientY-(rect.top+rect.height/2))};
    });
    return docks.sort((a,b)=>a.distance-b.distance)[0].side;
  }
  function dragMove(event){
    const drag=dragRef.current;if(!drag||!boardRef.current)return;
    if(Math.hypot(event.clientX-drag.startX,event.clientY-drag.startY)<6)return;
    drag.moved=true;drag.target=closestDock(event);setDropSide(drag.target);
  }
  function dragEnd(event){
    const drag=dragRef.current;if(!drag)return;
    if(event.type!=='pointercancel'&&Math.hypot(event.clientX-drag.startX,event.clientY-drag.startY)>=6&&closestDock(event)!==drag.side)swap();
    dragRef.current=null;setDropSide(null);
  }
  async function copy(){try{await navigator.clipboard.writeText(example.code);setCopied(true);}catch{setCopied(false);}}
  if(error||!data||!step){
    const status=<section ref={panelRef} className={`trace-panel ${focused?'trace-focus':''}`} role={focused?'dialog':undefined} aria-modal={focused||undefined} aria-label="Playground status"><p className="hint">{error||(!data?'Loading the complete trace…':'This sample has no recorded function steps.')}</p>{focused&&<button ref={exitButton} className="btn" onClick={()=>setFocused(false)}>↙ Exit focus</button>}</section>;
    return focused?createPortal(status,document.body):status;
  }
  const before=step.state,after=step.event==='return'?before:nextSameCall?.state||before;
  const names=[...new Set([...Object.keys(before),...Object.keys(after)])];
  const changed=names.filter(name=>!same(before[name],after[name]));
  const visualName=names.includes(selected)?selected:names.find(name=>typeof(after[name]??before[name])==='object'&&(after[name]??before[name])!==null)||names[0];
  const markers=state=>Object.fromEntries(Object.entries(state).filter(([name,value])=>/^(i|j|k|l|r|left|right|lo|hi|start|end|slow|fast)$/.test(name)&&Number.isInteger(value)));
  function inspector(kind,side){return <div className={`inspector-dock dock-${side} ${dropSide===side?'dock-target':''}`}>
    <Inspector kind={kind} side={side} onMove={swap} onDrag={e=>dragStart(e,kind,side)} onDragMove={dragMove} onDragEnd={dragEnd}>
      {kind==='code'?<>
        <div className="inspector-code-body"><CodeBlock code={example.code} activeLine={step.line} followLine={follow}/></div>
        <div className="inspector-foot"><label><input type="checkbox" checked={follow} onChange={e=>setFollow(e.target.checked)}/> Follow line</label><button onClick={copy}>{copied?'Copied ✓':'Copy code'}</button></div>
      </>:<>
        <div className="variable-legend"><span className="change-dot"/> {changed.length} changed · click a variable to visualise</div>
        <div className="inspector-variable-body">{names.map(name=><button key={name} className={`variable-card ${typeof before[name]!=='object'&&typeof after[name]!=='object'?'variable-scalar':''} ${changed.includes(name)?'variable-changed':''} ${visualName===name?'variable-selected':''}`} onClick={()=>setSelected(name)} aria-pressed={visualName===name}>
          <span className="variable-name"><b>{name}</b><small>{changed.includes(name)?'changed':'unchanged'}</small></span>
          <span className="variable-snapshot"><small>BEFORE</small><code>{compact(before[name])}</code></span>
          <span className="variable-snapshot"><small>AFTER</small><code>{compact(after[name])}</code></span>
        </button>)}</div>
        <div className="inspector-foot"><span>Call {step.call} · depth {step.depth}</span><span>{names.length} locals</span></div>
      </>}
    </Inspector>
  </div>;}
  const view=<section ref={panelRef} className={`trace-panel trace-workspace ${focused?'trace-focus':''}`} role={focused?'dialog':undefined} aria-modal={focused||undefined} aria-labelledby={titleId}>
    <div className="trace-toolbar"><div><div className="eyebrow">VISUAL PLAYGROUND</div><h2 id={titleId}>{focused?example.title:'See every state change'}</h2></div><div className="trace-toolbar-actions"><button className="btn small" onClick={()=>{setCodeSide('left');setDropSide(null);}}>Reset panels</button>{focused?<button ref={exitButton} className="btn small" onClick={()=>{setFocused(false);setPlaying(false);}}>↙ Exit focus</button>:<button ref={focusButton} className="btn primary small" onClick={()=>setFocused(true)}>⛶ Focus playground</button>}</div></div>
    <div className="trace-casebar">{example.traces?.length>1&&<label>Input case<select aria-label="Trace input example" value={sample} onChange={e=>setSample(Number(e.target.value))}>{example.traces.map((s,i)=><option value={i} key={s.url}>{s.label}</option>)}</select></label>}<span><b>{data.expression}</b><span className="case-result">Result: {JSON.stringify(data.result)}</span></span></div>
    <div className="trace-playback"><button className="btn small" disabled={index===0} onClick={()=>jump(index-1)}>← Previous</button><button className={`btn small ${playing?'':'primary'}`} onClick={()=>{if(!playing&&index===data.steps.length-1)setIndex(0);setPlaying(v=>!v);}}>{playing?'Ⅱ Pause':'▶ Play'}</button><button className="btn small" disabled={index===data.steps.length-1} onClick={()=>jump(index+1)}>Next →</button><input aria-label="Execution trace step" type="range" min={0} max={data.steps.length-1} value={index} onChange={e=>jump(Number(e.target.value))}/><span className="step-counter">{index+1} / {data.steps.length}</span><select aria-label="Playback speed" value={speed} onChange={e=>setSpeed(Number(e.target.value))}><option value={2000}>0.5×</option><option value={1000}>1×</option><option value={500}>2×</option></select></div>
    <div className="trace-board" ref={boardRef}>
      {inspector(codeSide==='left'?'code':'variables','left')}
      <div className="trace-stage" role="region" aria-label="Data visualisation">
        <div className="stage-heading"><span className="stage-live-dot"/><b>{step.event==='return'?'Return event':`Execute line ${step.line}`}</b><span>{step.function} · depth {step.depth}</span></div>
        <div className="stage-scroll">
          <div className="stage-source"><code>{example.code.split('\n')[step.line-1]}</code>{step.event==='return'&&<p>Return value: <strong>{JSON.stringify(step.result)}</strong></p>}</div>
          {visualName&&<><label className="visual-variable-label">Visualise<select aria-label="Visualised variable" value={visualName} onChange={e=>setSelected(e.target.value)}>{names.map(name=><option key={name}>{name}</option>)}</select></label>
            <div className="visual-states"><section className="visual-state"><div className="visual-state-label"><span>01</span> Before this line</div><Value value={before[visualName]} markers={markers(before)}/></section>
            <section className={`visual-state visual-after ${changed.includes(visualName)?'visual-state-changed':''}`}><div className="visual-state-label"><span>02</span> After this line</div><Value value={after[visualName]} previous={before[visualName]} markers={markers(after)}/></section></div>
            <div className="state-transition">→ <span>{changed.length?`${changed.length} variable${changed.length===1?'':'s'} changed`:'No local value changed'}{step.event==='return'?' · function returns':''}</span></div>
          </>}
          <p className="stage-semantics">{step.event==='return'?'This is the final state of this function call.':`After = next recorded event in call ${step.call}. Recursive calls complete before their caller’s next snapshot.`} Tuple assignments update together; green cells and variables changed.</p>
          <details className="trace-detail"><summary>Time & space reasoning</summary><h3>TIME · {example.time}</h3><p>{example.timeReason}</p><h3>SPACE · {example.space}</h3><p>{example.spaceReason}</p></details>
          <details className="trace-detail"><summary>How these snapshots work</summary><p>{data.semantics}</p></details>
          {data.conceptMatrix&&<details className="trace-detail"><summary>Recurrence explanation matrix</summary><DataTable table={data.conceptMatrix} label={data.conceptMatrix.name}/><p>This explains the recurrence. The execution states show the efficient storage used by the code.</p></details>}
        </div>
        <div className="stage-footer">Code & variables stay beside the visualisation.</div>
      </div>
      {inspector(codeSide==='right'?'code':'variables','right')}
    </div>
    <div className="trace-bottom"><span>⠿ Drag headers to swap panels. Each panel scrolls independently.</span><button className="btn small" onClick={()=>setAll(v=>!v)}>{all?'Hide full history':'Show full history'}</button></div>
    {all&&<div className="full-history data-table-scroll"><table className="data-table"><thead><tr><th>Event</th><th>Call / function</th><th>Line</th><th>All local state before the line / at return</th></tr></thead><tbody>{data.steps.map((s,i)=><tr key={i} className={i===index?'changed-row':''}><td><button className="history-step" onClick={()=>jump(i)}>{i+1} · {s.event}</button></td><td>{s.call} · {s.function}<br/>Depth {s.depth}</td><td>{s.line}</td><td><pre className="state-value">{JSON.stringify(s.state,null,2)}{s.event==='return'?'\nReturn: '+JSON.stringify(s.result):''}</pre></td></tr>)}</tbody></table></div>}
  </section>;
  return focused?createPortal(view,document.body):view;
}
