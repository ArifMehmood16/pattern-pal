import React, {useEffect, useRef} from 'react';

export function PageHead({ eyebrow, children, description }) {
  return <div className="page-lead"><div className="eyebrow">{eyebrow}</div><h1>{children}</h1><p className="intro">{description}</p></div>;
}

export function PatternCard({ pattern, learned }) {
  return <a className="pattern-card" href={`#pattern/${pattern.id}`}>
    <div className="card-top"><span className="pattern-icon">{pattern.icon}</span><span className="group-tag">{pattern.group}</span></div>
    <h3>{pattern.name}</h3><p>{pattern.summary}</p>
    <div className="card-foot"><span>⌘ {pattern.examples.length} code examples</span>{learned && <span className="learned-dot">✓ Learned</span>}<span className="arrow">↗</span></div>
  </a>;
}

export function CodeBlock({ code, title = 'solution.py', activeLine, language='Python 3', followLine=false }) {
  const preRef=useRef(null);
  useEffect(()=>{
    if(!followLine)return;
    const pre=preRef.current, line=pre?.querySelector('.highlight');
    if(!line)return;
    // Scroll only this code pane; never move the page or the visual stage.
    const offset=line.getBoundingClientRect().top-pre.getBoundingClientRect().top;
    if(offset<12||offset+line.offsetHeight>pre.clientHeight-12){
      pre.scrollTop+=offset-pre.clientHeight/2+line.offsetHeight/2;
    }
  },[activeLine,followLine,code]);
  return <div className="code-shell"><div className="code-top"><span>{title}</span><span>{language}</span></div>
    <pre ref={preRef}><code>{code.split('\n').map((line, index) => {
      const expression=language==='Python 3'?/(#[^\n]*|'[^'\n]*'|"[^"\n]*"|\b(?:def|class|return|if|else|elif|for|while|in|not|and|or|is|None|True|False|from|import|break|continue)\b|\b\d+\b)/g:/(--[^\n]*|'[^'\n]*'|"[^"\n]*"|\b(?:select|join|left|on|where|group|by|having|order|with|as|distinct|over|partition|case|when|then|end|union|rows|between|preceding|current|null|desc|from|and|or|is|not)\b|\b\d+\b)/gi;
      const parts = line.split(expression);
      return <span className={`code-line ${activeLine === index + 1 ? 'highlight' : ''}`} key={index}>
        <span className="line-no" aria-hidden="true">{index + 1}</span>
        {parts.map((part, i) => {
          if (i % 2 === 0) return <React.Fragment key={i}>{part}</React.Fragment>;
          const kind = part.startsWith('#')||part.startsWith('--') ? 'comment' : /^['"]/.test(part) ? 'string' : /^\d/.test(part) ? 'number' : 'keyword';
          return <span className={`token-${kind}`} key={i}>{part}</span>;
        })}{line ? '' : ' '}
      </span>;
    })}</code></pre>
  </div>;
}

export function RelatedMethods({ ids, patterns }) {
  return <div className="related"><span>CONNECT THIS METHOD WITH</span>{ids.map(id => {
    const pattern = patterns.find(p => p.id === id);
    return pattern && <a key={id} href={`#pattern/${id}`}>{pattern.name} ↗</a>;
  })}</div>;
}
