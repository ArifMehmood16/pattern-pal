import json
import practice_fixtures
patterns = json.load(open('src/data/patterns.json'))
for p in patterns:
    for e in p['examples']:
        scope = {k:v for k,v in vars(practice_fixtures).items() if not k.startswith('__')}
        exec(compile(e['code'], e['title'], 'exec'), scope)
        assert eval(e['check'], scope), f'{p["name"]}: {e["title"]}'
print('PASS: all 107 Python implementations compile and pass their sample / boundary assertions.')

# Independent exhaustive checks for the trickier interval and window algorithms.
import itertools
scope = {}
exec(next(p for p in patterns if p['id']=='deque')['examples'][2]['code'], scope)
for length in range(1, 6):
    for nums in itertools.product([-2, 0, 2], repeat=length):
        for target in [-1, 1, 3]:
            candidates = [j-i for i in range(length) for j in range(i+1, length+1) if sum(nums[i:j]) >= target]
            expected = min(candidates, default=-1)
            assert scope['shortest_subarray'](list(nums),target) == expected
scope = {}
exec(next(p for p in patterns if p['id']=='stack')['examples'][2]['code'], scope)
for length in range(6):
    for heights in itertools.product([0, 1, 3], repeat=length):
        expected = max((min(heights[i:j])*(j-i) for i in range(length) for j in range(i+1,length+1)), default=0)
        assert scope['largest_rectangle'](list(heights)) == expected
print('PASS: shortest-subarray and histogram algorithms agree with brute force on exhaustive small inputs.')
