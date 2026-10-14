import itertools
import json
from collections import Counter
from pathlib import Path

all_examples={e['title']:e for p in json.loads(Path('src/data/patterns.json').read_text()) for e in p['examples']}
scope={}
for title in ['Kth Largest Element','K Closest Points to Origin','Top K Frequent Elements','Longest Increasing Subsequence','Maximum Subarray (Kadane)','Set Matrix Zeroes','Game of Life','Edit Distance','Unique Paths']:
    exec(all_examples[title]['code'],scope)
for n in range(1,7):
    for values in itertools.product([-1,0,2],repeat=n):
        for k in range(1,n+1):assert scope['kth_largest'](list(values),k)==sorted(values,reverse=True)[k-1]
        expected=max(sum(values[i:j]) for i in range(n) for j in range(i+1,n+1))
        assert scope['max_subarray'](values)==expected
        dp=[1]*n
        for i in range(n):
            for j in range(i):
                if values[j]<values[i]:dp[i]=max(dp[i],dp[j]+1)
        assert scope['lis_length'](values)==max(dp)
        counts=Counter(values)
        for k in range(len(counts)+1):
            selected=scope['top_k_frequent'](values,k)
            assert len(selected)==k and len(set(selected))==k
            if k:assert min(counts[x] for x in selected)>=sorted(counts.values(),reverse=True)[k-1]

points=[[-1,0],[0,2],[2,2]]
for n in range(1,6):
    for indexes in itertools.product(range(3),repeat=n):
        values=[points[i][:] for i in indexes]
        ordered=sorted(x*x+y*y for x,y in values)
        for k in range(n+1):
            selected=scope['k_closest']([v[:] for v in values],k)
            assert sorted(x*x+y*y for x,y in selected)==ordered[:k]

for rows,cols in [(1,3),(2,2),(2,3),(3,3)]:
    for flat in itertools.product([0,1],repeat=rows*cols):
        board=[list(flat[r*cols:(r+1)*cols]) for r in range(rows)]
        zero_rows={r for r in range(rows) if 0 in board[r]}
        zero_cols={c for c in range(cols) if any(board[r][c]==0 for r in range(rows))}
        expected=[[0 if r in zero_rows or c in zero_cols else board[r][c] for c in range(cols)] for r in range(rows)]
        assert scope['set_zeroes']([row[:] for row in board])==expected
        expected=[]
        for r in range(rows):
            line=[]
            for c in range(cols):
                neighbors=sum(board[nr][nc] for nr in range(max(0,r-1),min(rows,r+2)) for nc in range(max(0,c-1),min(cols,c+2)) if (nr,nc)!=(r,c))
                line.append(int(neighbors==3 or (board[r][c]==1 and neighbors==2)))
            expected.append(line)
        assert scope['game_of_life']([row[:] for row in board])==expected

words=[''.join(s) for n in range(4) for s in itertools.product('ab',repeat=n)]
for a in words:
    for b in words:
        dp=[[0]*(len(b)+1) for _ in range(len(a)+1)]
        for i in range(len(a)+1):dp[i][0]=i
        for j in range(len(b)+1):dp[0][j]=j
        for i in range(1,len(a)+1):
            for j in range(1,len(b)+1):dp[i][j]=dp[i-1][j-1] if a[i-1]==b[j-1] else 1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])
        assert scope['edit_distance'](a,b)==dp[-1][-1]
for m in range(1,9):
    for n in range(1,9):
        dp=[[1]*n for _ in range(m)]
        for r in range(1,m):
            for c in range(1,n):dp[r][c]=dp[r-1][c]+dp[r][c-1]
        assert scope['unique_paths'](m,n)==dp[-1][-1]
print('PASS: nine improved algorithms match independent small-input baselines, including duplicate partitions and simultaneous matrix updates.')
