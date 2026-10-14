"""Structured, independent preparation exercises and a realistic study sequence."""
import json
from pathlib import Path
from enrich_content import enrich

drills=[]
def D(title,minutes,topic,prompt,code,check,hints,explanation):
    drills.append(dict(title=title,minutes=minutes,topic=topic,prompt=prompt,code=code,check=check,
                       difficulty='Python refresh',insight=explanation[0],time='See the explanation for this exercise',
                       space='See the explanation for this exercise',sampleInput='',sampleOutput='',teaching=explanation,hints=hints))

D('Maximum value and its first index',12,'Functions & loops','Return (maximum, first_index). For empty input return (None,-1). Avoid max() and list.index() for this exercise.', '''def maximum_and_index(nums):
    if not nums:
        return None, -1
    best, index = nums[0], 0
    for i, value in enumerate(nums):
        if value > best:
            best, index = value, i
    return best, index''','maximum_and_index([-4,-1,-1,-3])==(-1,1) and maximum_and_index([])==(None,-1) and maximum_and_index([7])==(7,0)', ['Initialise from the first value so all-negative inputs work.','Use > rather than ≥ if the first occurrence must win.'],['Define the empty-input contract before indexing.','best and index are updated together only on a strict improvement. Equal values keep the earlier index.','The return tuple contains both outputs. The scan is O(n) time and O(1) auxiliary space.'])
D('Reverse words',10,'Strings & lists','Reverse word order. Treat any whitespace as a separator and emit one space between words.', '''def reverse_words(text):
    words = text.split()
    words.reverse()
    return ' '.join(words)''', 'reverse_words("  hello   world  ")=="world hello" and reverse_words("")==""',['split() without an argument collapses whitespace.','list.reverse() mutates the list and returns None.'],['split constructs the word list.','reverse changes that list in place; do not assign its return value.','join creates the output string. O(number of characters) time and space.'])
D('Palindrome with slicing',8,'Strings & slicing','Determine whether a string exactly matches its reverse; this exercise does not ignore case or punctuation.', '''def exact_palindrome(text):
    reversed_text = text[::-1]
    return text == reversed_text''', 'exact_palindrome("abba") and not exact_palindrome("Abba") and exact_palindrome("")',['A slice step of −1 visits positions backwards.'],['Create the reversed copy using slicing.','Compare the two complete strings.','This is O(n) time and O(n) extra space; the two-pointer library example avoids the extra copy.'])
D('First unique character',12,'Dictionaries','Return the index of the first character appearing exactly once, or −1. Index zero is a valid answer.', '''def first_unique(text):
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    for i,char in enumerate(text):
        if counts[char] == 1:
            return i
    return -1''', 'first_unique("leetcode")==0 and first_unique("loveleetcode")==2 and first_unique("aabb")==-1',['Count in one pass, then scan the original order.','Do not write if index: when index can be zero.'],['get(char,0) handles a missing key without KeyError.','The second pass preserves input order and returns the earliest unique character.','Return −1 only after scanning every character. O(n) time and O(alphabet size) space.'])
D('Frequency counts with Counter',8,'Counter','Return a normal dictionary of character counts, including spaces and case as written.', '''from collections import Counter

def character_counts(text):
    return dict(Counter(text))''', 'character_counts("aab")=={"a":2,"b":1} and character_counts("")=={}',['Counter counts iterable values; it is a mapping.'],['Counter creates counts for every character.','dict converts the Counter into an ordinary dictionary.','Counting takes O(n) time with O(distinct characters) space.'])
D('Group records with defaultdict',10,'defaultdict','Input records are (category,value) tuples. Group values by category, preserving their arrival order.', '''from collections import defaultdict

def group_records(records):
    groups = defaultdict(list)
    for category,value in records:
        groups[category].append(value)
    return dict(groups)''', 'group_records([("a",1),("b",2),("a",3)])=={"a":[1,3],"b":[2]} and group_records([])=={}',['defaultdict(list) constructs a fresh list for each missing key.'],['A missing category automatically receives an empty list.','Tuple unpacking names both fields, then append preserves input order.','Return a normal dict. O(n) time and O(n) total stored values.'])
D('Sort records by two keys',10,'Sorting & tuples','Records are (name,score). Sort highest score first, then name alphabetically for ties. Return a new list.', '''def sort_records(records):
    return sorted(records, key=lambda record: (-record[1], record[0]))''', 'sort_records([("Zoe",9),("Ali",9),("Bea",7)])==[("Ali",9),("Zoe",9),("Bea",7)] and sort_records([])==[]',['Tuples compare left to right. A negative numeric score reverses its order.'],['The key tuple ranks score first, then name.','sorted returns a new list and leaves the input order unchanged.','O(n log n) time; O(n) output space. list.sort would mutate input and return None.'])
D('Dot product with zip',8,'zip & comprehensions','For two equal-length numeric lists, return the sum of pairwise products.', '''def dot_product(a, b):
    return sum(x * y for x,y in zip(a,b))''', 'dot_product([1,2,3],[4,5,6])==32 and dot_product([],[])==0',['zip pairs items by position; normally it stops at the shorter input.'],['zip creates position-wise pairs.','The generator computes products lazily, and sum accumulates them.','This contract requires equal lengths. O(n) time and O(1) auxiliary space.'])
D('Missing values with a set',10,'Sets','Given integers, return which values in the inclusive range 1..n are absent, in ascending order.', '''def missing_values(nums, n):
    present = set(nums)
    return [value for value in range(1,n+1) if value not in present]''', 'missing_values([1,1,3],4)==[2,4] and missing_values([],0)==[]',['range stops before its second argument.'],['A set removes duplicate values and supports expected constant-time membership.','range(1,n+1) includes n.','The comprehension preserves ascending iteration order. O(len(nums)+n) expected time.'])
D('Stack with append and pop',12,'Stacks','Validate bracket-only input containing (),[] and {}. Return a boolean.', '''def balanced_brackets(text):
    stack = []
    matching = {')':'(', ']':'[', '}':'{'}
    for char in text:
        if char in matching:
            if not stack or stack.pop() != matching[char]:
                return False
        else:
            stack.append(char)
    return not stack''', 'balanced_brackets("([])") and not balanced_brackets("([)]") and not balanced_brackets("]")',['A closing bracket must match the most recent opener.'],['append pushes onto the right, and pop removes the newest entry.','Guard an empty stack before popping. Short-circuit or avoids the invalid pop.','After the scan, no unmatched openers may remain. O(n) time and O(n) space.'])
D('Fixed window with deque',12,'deque','Return the sum of every length-k contiguous window. Require 1 ≤ k ≤ len(nums).', '''from collections import deque

def fixed_window_sums(nums, k):
    window, total, result = deque(), 0, []
    for value in nums:
        window.append(value)
        total += value
        if len(window) > k:
            total -= window.popleft()
        if len(window) == k:
            result.append(total)
    return result''', 'fixed_window_sums([1,2,3,4],2)==[3,5,7] and fixed_window_sums([-2,3],1)==[-2,3]',['deque.popleft is efficient; list.pop(0) shifts later elements.'],['Add each value to the queue and total.','If capacity is exceeded, remove the oldest value from both states.','Emit a sum only when the window is full. O(n) time, O(k) auxiliary space plus output.'])
D('Top three using heapq',10,'heapq','Return up to three largest values in descending order, counting duplicates.', '''import heapq

def largest_three(nums):
    return heapq.nlargest(3, nums)''', 'largest_three([5,1,8,8,2])==[8,8,5] and largest_three([1])==[1]',['Python’s basic heap is a min-heap; nlargest handles selection for you.'],['nlargest keeps the best candidates without requiring a full sort.','Duplicate values count independently in this exercise.','O(n log 3), effectively O(n) for this fixed size; O(3) selection space.'])
D('Independent matrix rows',10,'Matrices','Return an n×n zero matrix with only [0][0] set to 1; n ≥ 1. Other rows must stay zero.', '''def independent_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    matrix[0][0] = 1
    return matrix''', 'independent_matrix(2)==[[1,0],[0,0]] and independent_matrix(1)==[[1]]',['Do not use [[0]*n]*n: that repeats references to one row.'],['The comprehension constructs a new inner list for every row.','Only the first row’s first cell changes.','O(n²) allocation time and space. The full trace makes the row mutation visible.'])
D('Binary search boundaries',15,'Binary search','Return target’s index in a sorted list of distinct integers, or −1.', '''def binary_search(nums, target):
    left, right = 0, len(nums)-1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1''', 'binary_search([1,3,5,7],1)==0 and binary_search([1,3,5,7],6)==-1 and binary_search([],2)==-1',['Keep one consistent interval convention. Here both endpoints are inclusive.'],['Use // so mid remains an integer index.','Discard mid itself after a nonmatching comparison; otherwise the interval may fail to shrink.','left<=right allows the final singleton candidate. O(log n) time and O(1) space.'])
D('Prefix range sums',12,'Prefix sums','Given values and inclusive queries (left,right), return the sum for each query.', '''def query_sums(nums, queries):
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    return [prefix[right+1]-prefix[left] for left,right in queries]''', 'query_sums([2,-1,3],[(0,2),(1,1)])==[4,-1] and query_sums([],[])==[]',['The prefix has length n+1; entry i includes values before i.'],['Leading zero represents the empty prefix.','For an inclusive right endpoint, read prefix[right+1].','Subtract the prefix before left. O(n+queries) time and O(n) extra space plus output.'])
D('Parse whitespace-separated input',10,'Input/output','Given text containing whitespace-separated integers, return their sum. Empty text returns zero.', '''def sum_input(text):
    values = [int(token) for token in text.split()]
    return sum(values)''', 'sum_input("1  2\\n-3 4")==4 and sum_input("")==0',['Whitespace may include spaces and newlines.'],['split without an explicit separator handles arbitrary whitespace.','Convert every token to int, then sum.','O(number of characters + values) time. For the real editor, follow its exact function or stdin contract; the assessment’s contract is not known here.'])

import ast
costs=[
 ('O(n)','O(1)','One pass visits each value once; each comparison and tuple update is constant work.','Only a maximum and its first index are stored.'),
 ('O(L)','O(L)','split, reverse and join each process at most L input characters overall.','Words and the returned string retain O(L) total character storage.'),
 ('O(n)','O(n)','Creating and comparing the reversed slice each process n characters.','text[::-1] allocates an n-character copy.'),
 ('O(n)','O(alphabet size)','One counting pass plus one ordered scan is 2n expected-constant-time mapping operations.','The frequency dictionary contains one count per distinct character.'),
 ('O(n)','O(alphabet size)','Counter consumes each character once. Converting its distinct keys to dict is at most another O(n) pass.','One mapping entry is kept for each distinct character.'),
 ('O(n)','O(n) output','Each record is unpacked and appended once, using expected constant-time dictionary access.','The grouped output stores all n values, with one list per category.'),
 ('O(n log n)','O(n) output / sort storage','Python comparison sorting uses O(n log n) comparisons in the general case. The two-field key is constant-sized.','sorted creates an n-record list and sorting can use O(n) temporary storage.'),
 ('O(n)','O(1) auxiliary','zip yields each pair once; the generator multiplies and sum adds once per pair.','The generator does not allocate a product list; only current pair and total are needed.'),
 ('O(len(nums) + n)','O(distinct input + output)','Build the set once, then perform n expected-constant-time membership checks.','The set holds distinct input values and the returned list holds missing values.'),
 ('O(n)','O(n)','Each bracket is visited once and pushed or popped at most once.','All n characters could be unclosed openers, so the stack can grow linearly.'),
 ('O(n)','O(k) auxiliary + output','Every value enters once and can leave the deque once; sums are updated instead of recomputed.','The queue holds at most k values; output contains n−k+1 sums.'),
 ('O(n)','O(1) selection space','Selecting the top fixed count 3 requires O(n log 3), which is O(n).','Only three heap candidates need to be retained, independent of n.'),
 ('O(n²)','O(n²) output','Allocate n independent rows each with n cells, then perform one cell update.','The returned matrix has n² cells; only loop/allocation state is auxiliary.'),
 ('O(log n)','O(1)','Each comparison halves the inclusive candidate interval; at most logarithmically many rounds are needed.','Three integer indices are sufficient; no subarray copies are created.'),
 ('O(n + q)','O(n) auxiliary + O(q) output','Build n prefix sums, then answer q queries with constant work each.','The prefix list has n+1 entries; result holds q sums.'),
 ('O(L)','O(L)','split and integer conversion process the L-character text, then sum visits each parsed value.','The token list and integer list retain storage proportional to the input size under ordinary bounded-integer assumptions.'),
]
for d in drills:
    node=ast.parse(d['check'],mode='eval').body
    if isinstance(node,ast.BoolOp):node=node.values[0]
    if isinstance(node,ast.Compare):d['sampleInput'],d['sampleOutput']=ast.unparse(node.left),ast.unparse(node.comparators[0])
    else:d['sampleInput'],d['sampleOutput']=ast.unparse(node),'True'
    d['priority']='Tonight'
for d,(time,space,time_reason,space_reason) in zip(drills,costs):
    d.update(time=time,space=space,timeReason=time_reason,spaceReason=space_reason,optimality='This is a focused Python-language example. Its allocation and copying costs are explicit; the pattern library shows space-saving alternatives when they matter.')
enrich([dict(id='python',examples=drills,invariant='The maintained state represents exactly the values processed so far.',pitfalls='Check empty input, zero indices, negative values, duplicates, boundaries and return values.')])
Path('src/data/python-drills.json').write_text(json.dumps(drills,ensure_ascii=False,indent=2))

blocks=[
    dict(title='Python fundamentals',minutes=40,description='Functions, loops, conditions, range, enumerate, zip and return contracts.',drills=[0,7,15],problems=[]),
    dict(title='Strings and lists',minutes=45,description='Slicing, comprehensions, append/pop, split/join; reason about copies.',drills=[1,2,12],problems=['Valid Palindrome']),
    dict(title='Dictionaries and sets',minutes=60,description='get, Counter, defaultdict; frequency and complement reasoning.',drills=[3,4,5,8],problems=['Two Sum','Group Anagrams']),
    dict(title='Sorting and containers',minutes=45,description='key tuples, deque, heapq and stack invariants.',drills=[6,9,10,11],problems=['Valid Parentheses','Merge Intervals']),
    dict(title='Patterns and boundaries',minutes=90,description='Two pointers, windows, prefix sums and binary search. Trace every update.',drills=[13,14],problems=['Longest Unique Substring','Product of Array Except Self','Subarray Sum Equals K','First and Last Position of Element']),
    dict(title='Independent IDE practice',minutes=90,description='Choose two variations and solve them in your IDE without opening the reference. Explain the contract and complexity.',drills=[],problems=['Product of Array Except Self','Merge Intervals'],route='problems'),
    dict(title='Review and explain',minutes=30,description='Revisit your weakest pattern, trace its state, then rewrite in your IDE and justify the complexity.',drills=[],problems=[],route='library'),
]
pitfalls=[
 ['sort / sorted','list.sort() mutates and returns None. sorted() returns a new list.','values = [3,1,2]\nordered = sorted(values)\nvalues.sort()'],
 ['Independent matrix rows','Repeated references share mutations. Construct each row separately.','matrix = [[0] * cols for _ in range(rows)]'],
 ['Index zero','Zero is false in a boolean condition. Use explicit sentinels.','if index != -1:\n    return index'],
 ['Division','/ produces a floating result. // floors, including negatives. −7 // 3 is −3; truncation toward zero gives −2.','mid = (left + right) // 2'],
 ['Slices are copies','List and string slices allocate new sequences. Account for their time and memory.','tail = nums[1:]'],
 ['Mutation during iteration','Do not add/delete keys from a dict/set while iterating it. Iterate a snapshot or collect changes first.','for key in list(mapping):\n    if should_remove(key):\n        del mapping[key]'],
 ['Mutable default arguments','A default list is created once, not on every call. Use None then create a list.','def collect(value, items=None):\n    if items is None:\n        items = []\n    items.append(value)\n    return items'],
 ['Short-circuit guards','Check bounds or emptiness before indexing or popping. and/or evaluate left to right.','if stack and stack[-1] == target:\n    stack.pop()'],
 ['Aliasing and tuple assignment','a=b=[] shares a list. Tuple assignment evaluates all right-hand values first.','a, b = [], []\nleft, right = right, left'],
 ['Hashability','Set elements and dict keys must be hashable. Use a tuple rather than a list for a coordinate.','seen.add((row, col))'],
 ['Counter and defaultdict','Counter counts items. defaultdict creates values for missing keys; reading a missing key can insert it.','counts = Counter(values)\ngroups = defaultdict(list)'],
 ['Recursion and input size','Deep DFS may hit Python recursion limits. Use an iterative stack for very deep chains.','stack = [start]\nwhile stack:\n    node = stack.pop()'],
 ['Complexity in Python','list membership is linear; set/dict membership is expected constant time. pop(0) shifts a list; deque.popleft does not.','seen = set(values)\nqueue = deque(values)'],
 ['Signature and return type','Match the supplied function name, parameters and return type. Do not print instead of returning. Check whether stdin/stdout is required.','def solve(values):\n    return sum(values)'],
]
Path('src/data/study-plan.json').write_text(json.dumps(dict(blocks=blocks,pitfalls=pitfalls,sqlMinutes=45,
    assessmentFacts=['Two programming tests, one coding question per test (from your Equip screenshot).','Python 3 is available.','Actual duration, questions and difficulty remain unknown.','The demo’s first-character task only confirms editor workflow.','SQL is useful for the role; its presence in this assessment is not confirmed.'],
    routine=['Read the contract and constraints before coding.','Write one ordinary case and one boundary case.','State a brute-force approach, then identify repeated work.','Choose an invariant or recurrence; estimate complexity.','Implement the exact signature and return type.','Test empty/singleton input, duplicates, zero, negatives and boundary positions when allowed.','In your IDE, inspect a failing input, explain the cause and rewrite the solution.']),ensure_ascii=False,indent=2))

