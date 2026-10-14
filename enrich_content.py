import ast
import json
import sys
from pathlib import Path
from collections import deque
import practice_fixtures

TONIGHT = {
    'Contains Duplicate','Valid Anagram','Two Sum','Valid Palindrome','Longest Unique Substring',
    'Product of Array Except Self','Subarray Sum Equals K','Merge Intervals','Lower Bound',
    'First and Last Position of Element','Valid Parentheses','Maximum Subarray (Kadane)',
    'Best Time to Buy and Sell Stock','Group Anagrams','Minimum Size Subarray Sum',
    'Max Consecutive Ones III','Reverse Linked List','Binary Tree Level Order',
    'Maximum Tree Depth','Number of Islands','House Robber','Coin Change',
}
STRETCH = {'Trapping Rain Water','Minimum Window Substring','Largest Rectangle in Histogram',
           'Shortest Subarray With Sum at Least K','Word Ladder','Edit Distance','Game of Life'}

def serial(value, seen=None):
    seen = set() if seen is None else seen
    if value is None or isinstance(value, (bool,int,float,str)):
        if isinstance(value,float) and (value == float('inf') or value == float('-inf')): return str(value)
        return value
    if callable(value): return '<function>'
    if id(value) in seen: return '<same object / cycle>'
    seen.add(id(value))
    if isinstance(value,(list,tuple,deque)): return [serial(x,seen.copy()) for x in value]
    if isinstance(value,set): return sorted([serial(x,seen.copy()) for x in value],key=str)
    if isinstance(value,dict): return {('<word-end>' if type(k) is object else str(k)):serial(v,seen.copy()) for k,v in value.items()}
    if isinstance(value,practice_fixtures.ListNode):
        values, node, visited = [], value, set()
        while node is not None and id(node) not in visited:
            visited.add(id(node));values.append(node.val);node=node.next
        return {'list':values,'cycle':node is not None}
    if hasattr(value,'__dict__'): return {k:serial(v,seen.copy()) for k,v in vars(value).items()}
    return f'<{type(value).__name__}>'

def generic_blocks(code, insight):
    blocks=[]
    for node in ast.parse(code).body:
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            blocks.append({'start':node.lineno,'end':node.end_lineno,'text':f'Import {ast.unparse(node)}. Use this standard-library tool rather than recreating its data structure.'})
        elif isinstance(node,(ast.FunctionDef,ast.ClassDef)):
            for part in node.body:
                src=ast.unparse(part)
                if isinstance(part,ast.Return): text=f'Return {ast.unparse(part.value) if part.value else "None"}. This is the function’s output; it does not print automatically.'
                elif isinstance(part,(ast.For,ast.While)):
                    condition=ast.unparse(part.iter if isinstance(part,ast.For) else part.test)
                    text=f'Process {condition}. {insight} The complete trace below shows every executed iteration and each resulting state.'
                elif isinstance(part,ast.If): text=f'Check {ast.unparse(part.test)} before taking the branch. Review both branches in the whole code; boundary conditions decide which work is legal.'
                elif isinstance(part,(ast.Assign,ast.AnnAssign,ast.AugAssign)): text=f'Execute {src}. Python evaluates the right-hand expression before storing its result; tuple assignments use the previous values for every right-hand component.'
                elif isinstance(part,ast.FunctionDef): text=f'Define helper {part.name}({ast.unparse(part.args)}). It captures outer variables used in its body. Each recursive invocation has its own local variables.'
                else: text=f'Execute {src}. This operation updates the current state before the next block.'
                blocks.append({'start':part.lineno,'end':part.end_lineno,'text':text})
    return blocks

def enrich(patterns):
    directory=Path('public/traces');directory.mkdir(parents=True,exist_ok=True)
    for p in patterns:
        for index,e in enumerate(p['examples']):
            tree=ast.parse(e['code']);imports=[ast.unparse(n) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom))]
            starter=[]
            for n in tree.body:
                if isinstance(n,ast.FunctionDef): starter.append(f'def {n.name}({ast.unparse(n.args)}):\n    # Write your solution here.\n    pass')
                elif isinstance(n,ast.ClassDef):
                    methods=[f'    def {m.name}({ast.unparse(m.args)}):\n        pass' for m in n.body if isinstance(m,ast.FunctionDef)]
                    starter.append(f'class {n.name}:\n'+'\n'.join(methods))
            e['starter']='\n\n'.join(imports+starter)
            parsed=ast.parse(e['check'],mode='eval').body
            checks=parsed.values if isinstance(parsed,ast.BoolOp) and isinstance(parsed.op,ast.And) else [parsed]
            e['tests']=[ast.unparse(c) for c in checks]
            e['priority']='Tonight' if e['title'] in TONIGHT else 'Stretch' if e['title'] in STRETCH else 'Next'
            e['blocks']=generic_blocks(e['code'],e['insight'])
            if e.get('teaching'):
                e['explanation']=e['teaching']
            else: e['explanation']=[e['insight'],p['invariant'],p['pitfalls']]
            e['traceUrl']=f'/traces/{p["id"]}-{index}.json'
            filename=f'<atlas:{p["id"]}:{index}>'
            e['samples']=[];e['traces']=[]
            names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)}
            for case,check in enumerate(checks):
                scope={k:v for k,v in vars(practice_fixtures).items() if not k.startswith('__')}
                exec(compile(e['code'],filename,'exec'),scope)
                if isinstance(check,ast.Compare): expression=check.left
                elif isinstance(check,ast.UnaryOp) and isinstance(check.op,ast.Not): expression=check.operand
                else: expression=check
                # Show the solution's real result, not a len()/sorted() verification wrapper.
                core=next((n for n in ast.walk(expression) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in names),None)
                if core is not None:expression=core
                events=[];frame_ids={};previous={}
                def tracing(frame,event,arg):
                    if frame.f_code.co_filename != filename: return tracing
                    if event not in ('line','return'): return tracing
                    fid=frame_ids.setdefault(frame,len(frame_ids)+1)
                    state={k:serial(v) for k,v in frame.f_locals.items() if not callable(v)}
                    changed=[k for k in set(state)|set(previous.get(fid,{})) if state.get(k)!=previous.get(fid,{}).get(k)]
                    previous[fid]=state
                    depth=0;parent=frame.f_back
                    while parent:
                        if parent.f_code.co_filename==filename:depth+=1
                        parent=parent.f_back
                    events.append({'line':frame.f_lineno,'event':event,'function':frame.f_code.co_name,'call':fid,'depth':depth,'state':state,'changed':sorted(changed),'result':serial(arg) if event=='return' else None})
                    return tracing
                sys.settrace(tracing)
                try: result=eval(compile(ast.Expression(expression),'<sample>','eval'),scope)
                finally: sys.settrace(None)
                rendered=serial(result)
                input_text=ast.unparse(expression)
                output_text=repr(result) if result is None or isinstance(result,(str,bool,int,float,list,tuple,dict)) else json.dumps(rendered,ensure_ascii=False)
                if case==0 and ('→' in e['sampleInput'] or e['title'] in ['Min Stack','Moving Average From a Stream','Implement a Trie','Lowest Common Ancestor']):
                    input_text,output_text=e['sampleInput'],e['sampleOutput']
                url=e['traceUrl'] if case==0 else f'/traces/{p["id"]}-{index}-case-{case}.json'
                e['samples'].append({'input':input_text,'output':output_text})
                e['traces'].append({'label':f'Example {case+1}','url':url})
                trace={'input':input_text,'expression':ast.unparse(expression),'result':rendered,'steps':events,'semantics':'Each line snapshot is taken BEFORE the highlighted line executes. A later event in the same call shows its resulting state. Return events show the return value; nested calls have separate call numbers. No executed source-line events are sampled or omitted.'}
                if e['title'] in ['Unique Paths','Edit Distance','Longest Common Subsequence'] and core is not None:
                    args=[ast.literal_eval(a) for a in core.args]
                    if e['title']=='Unique Paths':
                        m,n=args;matrix=[[1]*n for _ in range(m)]
                        for r in range(1,m):
                            for c in range(1,n):matrix[r][c]=matrix[r-1][c]+matrix[r][c-1]
                        label='Conceptual DP matrix · the primary obstacle-free code uses a combinatorial count instead'
                    else:
                        a,b=args;matrix=[[0]*(len(b)+1) for _ in range(len(a)+1)]
                        if e['title']=='Edit Distance':
                            for r in range(len(a)+1):matrix[r][0]=r
                            for c in range(len(b)+1):matrix[0][c]=c
                        for r in range(1,len(a)+1):
                            for c in range(1,len(b)+1):
                                if e['title']=='Edit Distance':matrix[r][c]=matrix[r-1][c-1] if a[r-1]==b[c-1] else 1+min(matrix[r-1][c],matrix[r][c-1],matrix[r-1][c-1])
                                else:matrix[r][c]=matrix[r-1][c-1]+1 if a[r-1]==b[c-1] else max(matrix[r-1][c],matrix[r][c-1])
                        label='Full conceptual DP matrix · primary code retains only dependency rows'
                    assert matrix[-1][-1]==result
                    trace['conceptMatrix']={'name':label,'columns':['r / c',*range(len(matrix[0]))],'values':[[r,*row] for r,row in enumerate(matrix)]}
                Path('public'+url).write_text(json.dumps(trace,ensure_ascii=False))
