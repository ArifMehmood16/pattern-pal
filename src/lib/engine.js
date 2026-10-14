/* Deterministic suggestions: evidence, not an AI prediction or a proof. */
const AtlasEngine = (() => {
  const signals = [
    {id:'contiguous',label:'Contiguous range',methods:['window','prefix']},
    {id:'sorted',label:'Sorted input',methods:['pointers','binary']},
    {id:'exact',label:'Exact subarray sum',methods:['prefix','hash']},
    {id:'negative',label:'Negative values',methods:['prefix']},
    {id:'topk',label:'Top K / streaming',methods:['heap']},
    {id:'all',label:'All combinations',methods:['backtrack']},
    {id:'ways',label:'Count ways / repeated states',methods:['dp']},
    {id:'tree',label:'Tree or grid',methods:['dfs','bfs']},
    {id:'equal',label:'Equal-cost minimum moves',methods:['bfs']},
    {id:'weighted',label:'Nonnegative weighted edges',methods:['graph','heap']},
    {id:'dependencies',label:'Dependencies',methods:['graph']},
    {id:'overlap',label:'Overlapping intervals',methods:['intervals','sort']},
    {id:'next',label:'Next greater / smaller',methods:['stack']},
    {id:'prefix',label:'Dictionary / prefix lookup',methods:['trie']},
    {id:'nodes',label:'Linked nodes',methods:['linked','fast']},
    {id:'bits',label:'XOR / bitmask',methods:['bits']},
    {id:'feasible',label:'Monotonic feasibility',methods:['binary']},
    {id:'proof',label:'Provable local choice',methods:['greedy']},
    {id:'extrema',label:'Window maximum / minimum',methods:['deque','window']},
  ];
  function match(text, selected, patterns) {
    const t = text.toLowerCase();
    const map = new Map(patterns.map(p=>[p.id,{pattern:p,score:0,evidence:[]}]));
    function add(id, score, evidence) { const r=map.get(id); if(!r)return; r.score+=score; if(!r.evidence.includes(evidence))r.evidence.push(evidence); }
    for(const p of patterns) for(const phrase of p.signals) {
      const escaped=phrase.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
      if(new RegExp('\\b'+escaped+'\\b','i').test(t))add(p.id,2,`“${phrase}” in your description`);
    }
    for(const s of signals)if(selected.includes(s.id))for(const id of s.methods)add(id,5,s.label);
    if(/\b(subarray|subarrays)\b/.test(t)&&/\b(sum|summing)\b/.test(t)&&/\b(equals?|exact|count|number of)\b/.test(t)){
      add('prefix',7,'Exact subarray sums can be expressed as differences of prefixes');
      add('hash',6,'Count prior prefix sums with a frequency map');
    }
    if(/\b(substring|substrings)\b/.test(t)&&/\b(unique|distinct|repeat|repeating|longest)\b/.test(t)){
      add('window',6,'Maintain validity of a contiguous substring');add('hash',3,'Track character counts or last positions');
    }
    if(/\b(prerequisites?|dependencies|dependency|course schedule)\b/.test(t))add('graph',7,'Model dependencies as directed edges; check for cycles');
    if(/\b(3sum|three sum|triplets?)\b/.test(t)){add('pointers',7,'Fix one value and search for a pair');add('sort',5,'Sorting makes directional pointer moves possible');}
    const weighted=selected.includes('weighted')||/\bweighted\b|\bdifferent (edge )?costs\b/.test(t);
    const negative=selected.includes('negative')||/\bnegatives?\b/.test(t);
    const path=/\b(shortest paths?|shortest distances?|minimum costs?|network delay)\b/.test(t);
    if(path&&weighted){add('graph',8,'Weighted paths need a cost-aware algorithm');add('heap',4,'Dijkstra uses a priority queue for nonnegative weights');map.get('bfs').score-=6;}
    if(path&&!weighted){add('bfs',3,'BFS is a candidate if all transitions have equal cost');}
    if(/\b(window|windows)\b/.test(t)&&/\b(maximum|minimum|max|min)\b/.test(t)){add('deque',6,'Maintain ordered candidates and expire old indices');}
    const sumRange=/\b(sum|summing)\b/.test(t)&&/\b(subarray|subarrays|contiguous)\b/.test(t);
    const cautions=[];
    if(negative&&sumRange){map.get('window').score-=8;add('prefix',4,'Negative values can break the usual sum-window monotonicity');cautions.push('Negative values: a standard sum-based sliding window may fail. Exact sums often use prefix sums + hashing; shortest sum-at-least-K can need a prefix sum + monotonic deque.');}
    if(negative&&weighted)cautions.push('Negative edge weights: do not use Dijkstra. Consider Bellman–Ford, or topological relaxation if the graph is a DAG.');
    if(weighted&&!negative)cautions.push('For Dijkstra, verify that every edge weight is nonnegative. Ordinary BFS only gives shortest distances when edge costs are equal.');
    if(map.get('binary').score>0)cautions.push('Binary search requires sorted structure or a proven monotonic predicate. “Find the minimum” alone is insufficient.');
    if(map.get('greedy').score>0)cautions.push('Before using greedy, prove that the local choice preserves an optimum.');
    const results=[...map.values()].filter(r=>r.score>0).sort((a,b)=>b.score-a.score).slice(0,4);
    return {results,cautions};
  }
  function trace(s) {
    const steps=[{left:0,right:-1,best:0,counts:{},note:'Start with an empty window and an empty frequency map.',line:2}];
    let left=0,best=0;const counts={};
    for(let right=0;right<s.length;right++){
      const c=s[right];counts[c]=(counts[c]||0)+1;
      steps.push({left,right,best,counts:{...counts},note:`Expand right to ${right}: add “${c}”. ${counts[c]>1?'This creates a duplicate; the window needs to shrink.':'The window has no duplicates.'}`,line:5});
      while(counts[c]>1){const old=s[left];counts[old]--;left++;steps.push({left,right,best,counts:{...counts},note:`Remove “${old}” from the left. ${counts[c]>1?'There is still a duplicate, so continue shrinking.':'All characters are unique again.'}`,line:9});}
      best=Math.max(best,right-left+1);steps.push({left,right,best,counts:{...counts},note:`Valid window “${s.slice(left,right+1)}” has length ${right-left+1}. Best length so far: ${best}.`,line:10});
    }
    return steps;
  }
  const quizzes=[
    {title:'Find the longest substring without repeating characters.',answers:['window','hash'],options:['window','hash','binary','heap'],why:'The region is contiguous. Grow and shrink a window while a map tracks character frequencies. Both techniques work together.'},
    {title:'Count subarrays whose sum equals K. Values may be negative.',answers:['prefix','hash'],options:['window','prefix','hash','greedy'],why:'Each valid subarray is a difference of two prefix sums. A frequency map counts matching earlier prefixes. Negative values break the usual sum-window rule.'},
    {title:'Return all unique triplets that sum to zero.',answers:['sort','pointers'],options:['sort','pointers','bfs','dp'],why:'Sort the values, fix one value, then search the remaining suffix with two pointers. Skip duplicates to keep triplets unique.'},
    {title:'Find the fewest moves between two cells. Each legal move costs one.',answers:['bfs'],options:['bfs','greedy','binary','heap'],why:'Model cells as vertices and moves as edges. BFS discovers cells in increasing move count because all edges have equal cost.'},
    {title:'Courses have prerequisites. Can you complete every course?',answers:['graph'],options:['graph','window','trie','bits'],why:'Build a directed dependency graph. A topological sort completes all nodes precisely when no directed cycle remains. DFS cycle detection is another valid approach.'},
    {title:'Find the first strictly warmer day after each day in a temperature list.',answers:['stack'],options:['stack','heap','binary','prefix'],why:'A decreasing stack stores unresolved day indices. A warmer day resolves cooler entries at the top. Each index is pushed and popped at most once.'},
    {title:'Generate every subset of distinct values.',answers:['backtrack'],options:['backtrack','greedy','heap','intervals'],why:'Enumerate a decision tree of include/skip choices. Copy the current path at a leaf. Bitmask enumeration is also possible, but is not among these choices.'},
    {title:'Find the fewest coins making an amount with arbitrary positive denominations and unlimited reuse.',answers:['dp'],options:['dp','greedy','bfs','pointers'],why:'DP is a standard fit: dp[a] is the minimum over final-coin choices. Greedy can fail, for example with [1,3,4] and amount 6. BFS can also solve this as a state graph; accept it as an alternative if selected alone.',alternatives:[['bfs']]},
    {title:'Find the maximum of every window of K values.',answers:['deque'],options:['deque','trie','fast','linked'],why:'A decreasing deque retains undominated candidate indices. Expire indices outside the window and read the maximum at the front.'},
    {title:'Find shortest paths in a graph with nonnegative, unequal edge weights.',answers:['graph','heap'],options:['graph','heap','bfs','window'],why:'Dijkstra combines graph relaxation with a min-heap. Ordinary BFS cannot account for unequal weights.'},
    {title:'Support exact dictionary word lookup and prefix lookup.',answers:['trie'],options:['trie','prefix','stack','intervals'],why:'Trie edges represent characters and share prefix paths. Prefix sums are a different technique; similar names do not imply the same use.'},
    {title:'Find the smallest integer capacity that can ship all packages within D days, preserving order.',answers:['binary'],options:['binary','backtrack','fast','bits'],why:'As capacity increases, required days never increase. Binary search finds the first feasible capacity; a left-to-right packing pass implements the predicate.'},
  ];
  return {signals,match,trace,quizzes};
})();

export default AtlasEngine;
