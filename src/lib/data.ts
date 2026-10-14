export type Pattern = {
  id: string;
  name: string;
  signals: string[];
  idea: string;
  complexity: string;
  template: string;
};

export const patterns: Pattern[] = [
  {
    id: "two-pointers",
    name: "Two Pointers",
    signals: ["Sorted array or string", "Find a pair / triplet with a target", "Reverse or compare from both ends", "In-place removal"],
    idea: "Use two indices moving toward each other (or same direction) to avoid nested loops.",
    complexity: "O(n) time, O(1) space",
    template: `def two_sum_sorted(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:
        s = nums[l] + nums[r]
        if s == target:
            return [l, r]
        if s < target:
            l += 1
        else:
            r -= 1
    return []`,
  },
  {
    id: "sliding-window",
    name: "Sliding Window",
    signals: ["Contiguous subarray / substring", "Longest / shortest / max sum of window", "'At most K' distinct items"],
    idea: "Grow the right edge, shrink the left edge when the window breaks a rule.",
    complexity: "O(n) time",
    template: `def longest_unique(s):
    seen = {}
    l = best = 0
    for r, ch in enumerate(s):
        if ch in seen and seen[ch] >= l:
            l = seen[ch] + 1
        seen[ch] = r
        best = max(best, r - l + 1)
    return best`,
  },
  {
    id: "hashing",
    name: "Hash Map / Counting",
    signals: ["Need O(1) lookup of seen values", "Frequencies, anagrams, duplicates", "Unsorted pair-sum"],
    idea: "Trade memory for speed: store what you've seen in a dict or set.",
    complexity: "O(n) time, O(n) space",
    template: `def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i`,
  },
  {
    id: "binary-search",
    name: "Binary Search",
    signals: ["Sorted input", "'Minimum value such that…' (search on answer)", "O(log n) required"],
    idea: "Halve the search space each step using a monotonic condition.",
    complexity: "O(log n) time",
    template: `def lower_bound(nums, target):
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo`,
  },
  {
    id: "stack",
    name: "Stack / Monotonic Stack",
    signals: ["Matching brackets", "Next greater / smaller element", "Undo / nested structure"],
    idea: "Push items; pop when the current item resolves earlier ones.",
    complexity: "O(n) time",
    template: `def next_greater(nums):
    res = [-1] * len(nums)
    stack = []  # indices
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            res[stack.pop()] = x
        stack.append(i)
    return res`,
  },
  {
    id: "bfs-dfs",
    name: "BFS / DFS (Graphs & Grids)",
    signals: ["Grid of cells / islands", "Shortest path in unweighted graph (BFS)", "Connected components, tree traversal"],
    idea: "Explore neighbors systematically; track visited nodes.",
    complexity: "O(V + E) time",
    template: `from collections import deque

def bfs(grid, sr, sc):
    R, C = len(grid), len(grid[0])
    q = deque([(sr, sc, 0)])
    seen = {(sr, sc)}
    while q:
        r, c, d = q.popleft()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen and grid[nr][nc] != '#':
                seen.add((nr, nc))
                q.append((nr, nc, d + 1))`,
  },
  {
    id: "heap",
    name: "Heap / Top K",
    signals: ["'K largest / smallest / most frequent'", "Merge K sorted lists", "Running median"],
    idea: "Keep a heap of size K so you never sort the whole input.",
    complexity: "O(n log k) time",
    template: `import heapq
from collections import Counter

def top_k_frequent(nums, k):
    return [x for x, _ in heapq.nlargest(k, Counter(nums).items(), key=lambda p: p[1])]`,
  },
  {
    id: "dp",
    name: "Dynamic Programming",
    signals: ["'Number of ways', 'min cost', 'max profit'", "Choices at each step with overlapping subproblems", "Brute force is exponential"],
    idea: "Define a state, a recurrence, and base cases; cache results.",
    complexity: "Usually O(n) – O(n²)",
    template: `from functools import cache

def climb_stairs(n):
    @cache
    def f(i):
        if i <= 1:
            return 1
        return f(i - 1) + f(i - 2)
    return f(n)`,
  },
  {
    id: "backtracking",
    name: "Backtracking",
    signals: ["Generate all subsets / permutations / combinations", "Constraint puzzles (N-Queens, Sudoku)", "Small n (≤ 20)"],
    idea: "Build a candidate step by step, undo the choice, try the next.",
    complexity: "Exponential",
    template: `def subsets(nums):
    res, path = [], []
    def bt(i):
        if i == len(nums):
            res.append(path[:])
            return
        path.append(nums[i]); bt(i + 1)
        path.pop(); bt(i + 1)
    bt(0)
    return res`,
  },
];

export type Problem = {
  id: string;
  title: string;
  difficulty: "Easy" | "Medium" | "Hard";
  source: string;
  statement: string;
  pattern: string;
  clues: string[];
  solution: string;
};

export const problems: Problem[] = [
  { id: "two-sum", title: "Two Sum", difficulty: "Easy", source: "LeetCode 1", pattern: "hashing",
    statement: "Given an unsorted array of integers and a target, return indices of the two numbers that add up to the target.",
    clues: ["Unsorted — sorting would lose indices", "Need fast lookup of 'target - x'"],
    solution: `def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i` },
  { id: "longest-substring", title: "Longest Substring Without Repeating Characters", difficulty: "Medium", source: "LeetCode 3", pattern: "sliding-window",
    statement: "Given a string s, find the length of the longest substring without repeating characters.",
    clues: ["'Substring' = contiguous", "'Longest' window satisfying a rule"],
    solution: `def lengthOfLongestSubstring(s):
    seen, l, best = {}, 0, 0
    for r, ch in enumerate(s):
        if seen.get(ch, -1) >= l:
            l = seen[ch] + 1
        seen[ch] = r
        best = max(best, r - l + 1)
    return best` },
  { id: "valid-parentheses", title: "Valid Parentheses", difficulty: "Easy", source: "LeetCode 20", pattern: "stack",
    statement: "Given a string of '()[]{}', determine if the brackets are balanced and correctly nested.",
    clues: ["Nested matching structure", "Most recent open must close first (LIFO)"],
    solution: `def isValid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []
    for ch in s:
        if ch in pairs:
            if not st or st.pop() != pairs[ch]:
                return False
        else:
            st.append(ch)
    return not st` },
  { id: "container-water", title: "Container With Most Water", difficulty: "Medium", source: "LeetCode 11", pattern: "two-pointers",
    statement: "Given heights of vertical lines, pick two that, with the x-axis, hold the most water.",
    clues: ["Pair of indices", "Area limited by shorter side — move that pointer inward"],
    solution: `def maxArea(h):
    l, r, best = 0, len(h) - 1, 0
    while l < r:
        best = max(best, (r - l) * min(h[l], h[r]))
        if h[l] < h[r]: l += 1
        else: r -= 1
    return best` },
  { id: "search-rotated", title: "Search in Rotated Sorted Array", difficulty: "Medium", source: "LeetCode 33", pattern: "binary-search",
    statement: "A sorted array was rotated at an unknown pivot. Find the index of target in O(log n).",
    clues: ["'Sorted' + 'O(log n)'", "One half is always sorted"],
    solution: `def search(nums, t):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        m = (lo + hi) // 2
        if nums[m] == t: return m
        if nums[lo] <= nums[m]:
            if nums[lo] <= t < nums[m]: hi = m - 1
            else: lo = m + 1
        else:
            if nums[m] < t <= nums[hi]: lo = m + 1
            else: hi = m - 1
    return -1` },
  { id: "num-islands", title: "Number of Islands", difficulty: "Medium", source: "LeetCode 200", pattern: "bfs-dfs",
    statement: "Given a 2D grid of '1' (land) and '0' (water), count the islands.",
    clues: ["Grid with neighbors", "Count connected components"],
    solution: `def numIslands(grid):
    R, C = len(grid), len(grid[0])
    def dfs(r, c):
        if not (0 <= r < R and 0 <= c < C) or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        dfs(r+1,c); dfs(r-1,c); dfs(r,c+1); dfs(r,c-1)
    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '1':
                dfs(r, c); count += 1
    return count` },
  { id: "kth-largest", title: "Kth Largest Element in an Array", difficulty: "Medium", source: "LeetCode 215", pattern: "heap",
    statement: "Find the kth largest element in an unsorted array.",
    clues: ["'Kth largest'", "Don't need full sort"],
    solution: `import heapq
def findKthLargest(nums, k):
    h = nums[:k]; heapq.heapify(h)
    for x in nums[k:]:
        if x > h[0]: heapq.heapreplace(h, x)
    return h[0]` },
  { id: "coin-change", title: "Coin Change", difficulty: "Medium", source: "LeetCode 322", pattern: "dp",
    statement: "Given coin denominations and an amount, return the fewest coins needed to make it, or -1.",
    clues: ["'Fewest' = optimization", "Same sub-amounts recur"],
    solution: `def coinChange(coins, amount):
    dp = [0] + [float('inf')] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1` },
  { id: "permutations", title: "Permutations", difficulty: "Medium", source: "LeetCode 46", pattern: "backtracking",
    statement: "Given distinct integers, return all possible permutations.",
    clues: ["'Return all'", "Small input, build choices step by step"],
    solution: `def permute(nums):
    res, path, used = [], [], [False] * len(nums)
    def bt():
        if len(path) == len(nums):
            res.append(path[:]); return
        for i, x in enumerate(nums):
            if used[i]: continue
            used[i] = True; path.append(x)
            bt()
            path.pop(); used[i] = False
    bt()
    return res` },
  { id: "sherlock-anagrams", title: "Sherlock and Anagrams", difficulty: "Medium", source: "HackerRank", pattern: "hashing",
    statement: "Count pairs of substrings of s that are anagrams of each other.",
    clues: ["Anagram = same character counts", "Group by a signature key"],
    solution: `from collections import Counter
def sherlockAndAnagrams(s):
    cnt = Counter()
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            cnt[''.join(sorted(s[i:j]))] += 1
    return sum(v * (v - 1) // 2 for v in cnt.values())` },
];

export const patternById = (id: string) => patterns.find((p) => p.id === id)!;
