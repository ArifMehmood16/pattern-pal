"""Prefer efficient standard solutions; state mutation and time/space tradeoffs explicitly."""
def optimise(patterns):
    all_examples={e['title']:e for p in patterns for e in p['examples']}
    def change(title,code,time,space,insight,teaching,optimality):
        e=all_examples[title];e.update(code=code.strip(),time=time,space=space,insight=insight,teaching=teaching,optimality=optimality)
    change('K Closest Points to Origin','''import random

def k_closest(points, k):
    if k == 0: return []
    left, right = 0, len(points) - 1
    def distance(point):
        return point[0] * point[0] + point[1] * point[1]
    while left <= right:
        pivot = distance(points[random.randint(left, right)])
        low, i, high = left, left, right
        while i <= high:
            value = distance(points[i])
            if value < pivot:
                points[low], points[i] = points[i], points[low]
                low += 1
                i += 1
            elif value > pivot:
                points[i], points[high] = points[high], points[i]
                high -= 1
            else:
                i += 1
        if k - 1 < low: right = low - 1
        elif k - 1 > high: left = high + 1
        else: break
    return points[:k]''','O(n) expected; O(n²) worst case','O(1) auxiliary + O(k) output',
    'Partition by squared distance until the first k positions contain the closest points; their internal order need not be sorted.',
    ['The three regions contain distances below, equal to, and above the pivot.','A swap from the high side brings an unexamined point to i, so i must stay in place in that branch.','Continue only in the region containing position k−1. This solution reorders the input; a heap is an alternative when input preservation or guaranteed bounds matter.'],
    'Randomised quickselect gives expected linear selection and constant auxiliary storage, while sorting costs O(n log n). Worst-case time is quadratic; a size-k heap gives O(n log k) with O(k) space and preserves the input.')
    change('Kth Largest Element','''import random

def kth_largest(nums, k):
    target = len(nums) - k
    left, right = 0, len(nums) - 1
    while left <= right:
        pivot = nums[random.randint(left, right)]
        low, i, high = left, left, right
        while i <= high:
            if nums[i] < pivot:
                nums[low], nums[i] = nums[i], nums[low]
                low += 1
                i += 1
            elif nums[i] > pivot:
                nums[i], nums[high] = nums[high], nums[i]
                high -= 1
            else:
                i += 1
        if target < low: right = low - 1
        elif target > high: left = high + 1
        else: return pivot''','O(n) expected; O(n²) worst case','O(1) auxiliary',
    'The kth largest occupies zero-based sorted position n−k. Partition only the region containing that position.',
    ['Convert kth largest into a zero-based ascending position.','Three-way partition keeps duplicates together, avoiding repeated work on equal pivots.','Only one side can contain target; discard the other. This implementation mutates the input.'],
    'This improves expected time and auxiliary space over a size-k heap, with an explicit worst-case tradeoff. Use a heap for O(n log k) guaranteed selection time and an unchanged input.')
    change('Top K Frequent Elements','''from collections import Counter

def top_k_frequent(nums, k):
    if k == 0: return []
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, frequency in counts.items():
        buckets[frequency].append(value)
    result = []
    for frequency in range(len(nums), 0, -1):
        for value in buckets[frequency]:
            result.append(value)
            if len(result) == k: return result
    return result''','O(n)','O(n)',
    'A frequency lies between 1 and n, so direct-address buckets avoid comparison sorting.',
    ['Count occurrences, then place each distinct value in its frequency bucket.','Read buckets from highest frequency to lowest; append values until k have been collected.','Ties may appear in any order. Buckets trade O(n) storage for linear time.'],
    'Bucket selection is linear in the input size. A heap can use less auxiliary storage when n is much larger than the number of distinct values, at O(n + u log k) time.')
    change('Longest Increasing Subsequence','''from bisect import bisect_left

def lis_length(nums):
    tails = []
    for value in nums:
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    return len(tails)''','O(n log n)','O(n)',
    'tails[length−1] is the smallest possible ending value for an increasing subsequence of that length. tails is not necessarily an actual subsequence.',
    ['Binary search finds the first tail ≥ value, so equal values replace rather than extend a strictly increasing subsequence.','A new largest tail extends the maximum length. A replacement makes the same length easier to extend later.','Return tails length. Do not return tails itself as the reconstructed subsequence.'],
    'This improves the O(n²) pairwise DP recurrence to O(n log n). Reconstructing actual indices requires extra predecessor information.')
    change('Longest Common Prefix','''def longest_common_prefix(words):
    if not words: return ''
    first = words[0]
    for i, char in enumerate(first):
        for word in words[1:]:
            if i == len(word) or word[i] != char:
                return first[:i]
    return first''','O(total compared characters)','O(1) auxiliary + O(prefix length) output',
    'Compare one character column at a time and stop at the first mismatch or exhausted word.',
    ['The first word provides candidate characters.','Every other word must have that index and matching character; the bound check short-circuits before indexing.','Return the prefix ending before the failed column. There is only one final slice, rather than repeated shrinking copies.'],
    'Vertical scanning visits only relevant characters and avoids the repeated-prefix O(L²) copying of the simpler shrinking implementation.')
    # Avoid allocating words[1:] in every character-column iteration.
    e=all_examples['Longest Common Prefix'];e['code']=e['code'].replace('for word in words[1:]:','for j in range(1, len(words)):\n            word = words[j]')
    change('Maximum Subarray (Kadane)','''def max_subarray(nums):
    ending = best = nums[0]
    for i in range(1, len(nums)):
        value = nums[i]
        ending = max(value, ending + value)
        best = max(best, ending)
    return best''','O(n)','O(1)',
    'At each position, the best subarray ending here either starts here or extends the previous ending.',
    ['Initialise with nums[0] because the chosen subarray must be nonempty, including all-negative arrays.','ending chooses start versus extend; best then records the best ending seen anywhere.','Iterate by index instead of nums[1:] so the algorithm does not allocate a hidden slice.'],
    'A single pass is optimal for inspecting all arbitrary values, and only two running sums are stored.')
    change('Set Matrix Zeroes','''def set_zeroes(matrix):
    if not matrix or not matrix[0]: return matrix
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if first_row_zero:
        for c in range(cols): matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows): matrix[r][0] = 0
    return matrix''','O(rows × cols)','O(1) auxiliary',
    'Use the first row and column as marker storage, preserving their original zero status separately.',
    ['Remember whether the first row/column originally contained zeros before creating any markers.','Each interior zero marks its row in column 0 and its column in row 0.','Apply markers to interior cells first. Only then clear the first row/column using the saved flags.'],
    'Every cell must be inspected; this achieves linear-in-cells time while replacing extra row/column sets with constant auxiliary state.')
    all_examples['Set Matrix Zeroes']['prompt']='For a rectangular matrix, if an original cell is zero, zero its row and column. Mutate the matrix in place and return it for practice.'
    change('Game of Life','''def game_of_life(board):
    if not board or not board[0]: return []
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if (dr or dc) and 0 <= nr < rows and 0 <= nc < cols:
                        neighbors += board[nr][nc] & 1
            live_next = neighbors == 3 or ((board[r][c] & 1) == 1 and neighbors == 2)
            if live_next: board[r][c] |= 2
    for r in range(rows):
        for c in range(cols): board[r][c] >>= 1
    return board''','O(rows × cols)','O(1) auxiliary',
    'Keep the old generation in bit 0 and encode the next generation in bit 1, then commit all cells with a shift.',
    ['All neighbor reads use &1, so encoded next-state bits never contaminate the old-state calculation.','Setting bit 1 records the future state while preserving the old low bit. Encoded values 0/1/2/3 represent both generations.','After every future state is recorded, shift every cell once. This is a logically simultaneous update using constant extra storage.'],
    'Two cell passes with eight constant neighbor checks per cell give optimal O(rows×cols) inspection time and O(1) auxiliary space.')
    all_examples['Game of Life']['prompt']='Compute one simultaneous generation of a rectangular binary board. Mutate it in place; live cells survive with 2/3 neighbors and dead cells revive with 3. Return the board for practice.'
    change('Unique Paths','''def unique_paths(m, n):
    moves = m + n - 2
    chosen = min(m - 1, n - 1)
    ways = 1
    for i in range(1, chosen + 1):
        ways = ways * (moves - chosen + i) // i
    return ways''','O(min(m,n)) arithmetic operations','O(1) auxiliary integer variables',
    'Without obstacles, choose where the down moves occur among all moves: C(m+n−2,m−1). A DP matrix explains the same count but is unnecessary for this exact contract.',
    ['Every valid path has m−1 down moves and n−1 right moves; only their order differs.','Use the smaller choice count and build the binomial coefficient using exact integer multiplication/division.','The one-row/column case chooses zero moves and returns 1. For obstacles or path-dependent costs, use DP instead.'],
    'This count-only, obstacle-free problem admits a combinatorial shortcut beyond O(mn) DP. Python integer arithmetic grows with result size; the bound counts arithmetic operations, not constant-cost huge-integer bit operations.')
    change('Edit Distance','''def edit_distance(a, b):
    if len(a) < len(b): a, b = b, a
    dp = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        diagonal = dp[0]
        dp[0] = i
        for j, char_b in enumerate(b, 1):
            above = dp[j]
            if char_a == char_b:
                dp[j] = diagonal
            else:
                dp[j] = 1 + min(above, dp[j - 1], diagonal)
            diagonal = above
    return dp[-1]''','O(nm)','O(min(n,m))',
    'Keep one DP row. Save the old above cell before replacing it so the next column still has its previous diagonal.',
    ['Put the shorter string on columns and initialise the empty-a distances as 0..len(b).','Before an update, dp[j] is above, dp[j−1] is current-row left, and diagonal is previous-row diagonal.','Save above, write the new cell, then assign diagonal=above. This ordering preserves all three recurrence inputs.'],
    'The standard edit-distance recurrence evaluates nm states; retaining only one row reduces storage to the shorter string length. The visual playground shows each overwrite and its saved diagonal.')
    e=all_examples['Longest Common Subsequence'];e['code']=e['code'].replace('    previous =', '    if len(a) < len(b): a, b = b, a\n    previous =',1);e['space']='O(min(n,m))';e['optimality']='The standard recurrence evaluates nm character pairs. Two rows along the shorter string retain exactly the dependency frontier, instead of an entire matrix.'
    all_examples['Group Anagrams']['space']='O(26g + n) references; g groups'
    all_examples['Binary Tree Level Order']['space']='O(width) auxiliary + O(n) output'
    for title in ['K Closest Points to Origin','Kth Largest Element']:
        all_examples[title]['prompt'] += ' This efficient implementation may reorder its input list.'
