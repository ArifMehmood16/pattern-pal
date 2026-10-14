"""Additional independent practice examples; no assessment questions are predicted."""
def expand(patterns, E, P):
    by_id = {p['id']: p for p in patterns}
    def A(id, title, level, prompt, insight, time, space, code, check, blocks):
        E(by_id[id], title, level, prompt, insight, time, space, code, check)
        by_id[id]['examples'][-1]['teaching'] = blocks

    A('hash','Contains Duplicate','Easy','Return whether any integer occurs more than once.','Stop as soon as a value already exists in the seen set.','O(n) expected','O(n)', '''def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False''', 'contains_duplicate([1,2,3,1]) and not contains_duplicate([])', ['Create an empty set: it represents values strictly before the current index.','Before inserting x, check membership. A hit proves two distinct positions contain x.','If the scan finishes without a hit, return False. Empty input therefore returns False.'])
    A('hash','Valid Anagram','Easy','Return whether two strings contain the same characters with the same counts.','Compare character frequency maps after rejecting different lengths.','O(n + m)','O(alphabet size)', '''from collections import Counter

def is_anagram(s, t):
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)''', 'is_anagram("anagram","nagaram") and not is_anagram("rat","car")', ['Different lengths cannot have identical character multiplicities. Reject them first.','Counter constructs a mapping from each character to its frequency.','Equality compares keys and counts, so repeated letters are handled correctly.'])
    A('pointers','Valid Palindrome','Easy','Ignore non-alphanumeric characters and case. Determine whether the string is a palindrome.','Skip ignored characters at both ends, then compare the remaining pair.','O(n)','O(1)', '''def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True''', 'is_palindrome("A man, a plan, a canal: Panama") and not is_palindrome("race a car")', ['Initialise pointers at opposite ends. The region outside them has already matched.','Skip punctuation independently on each side, preserving bounds.','Compare case-normalised characters; on a match move both pointers. A mismatch returns immediately.'])
    A('pointers','Trapping Rain Water','Hard','Given nonnegative bar heights, return trapped water volume.','Resolve the side with the smaller established boundary maximum.','O(n)','O(1)', '''def trap_water(heights):
    left, right = 0, len(heights) - 1
    left_max = right_max = water = 0
    while left <= right:
        if left_max <= right_max:
            left_max = max(left_max, heights[left])
            water += left_max - heights[left]
            left += 1
        else:
            right_max = max(right_max, heights[right])
            water += right_max - heights[right]
            right -= 1
    return water''', 'trap_water([0,1,0,2,1,0,1,3,2,1,2,1])==6 and trap_water([])==0', ['Track the best wall seen from each side and the total water.','When left_max ≤ right_max, the left boundary determines the current left cell; symmetrically resolve right otherwise.','Update the chosen maximum before adding its difference from the current height, then advance only that side.'])
    A('window','Minimum Window Substring','Hard','Find the shortest substring of s containing every character of t, including multiplicities. Return empty if impossible.','Track how many required character occurrences are still missing.','O(n + m)','O(alphabet size)', '''from collections import Counter

def min_window(s, t):
    if not t:
        return ''
    need = Counter(t)
    missing = len(t)
    left = 0
    best_start, best_length = 0, len(s) + 1
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        while missing == 0:
            if right - left + 1 < best_length:
                best_start, best_length = left, right - left + 1
            old = s[left]
            need[old] += 1
            if need[old] > 0:
                missing += 1
            left += 1
    return '' if best_length > len(s) else s[best_start:best_start + best_length]''', 'min_window("ADOBECODEBANC","ABC")=="BANC" and min_window("a","aa")==""', ['Counter records required multiplicities. missing counts occurrences, not distinct characters.','Expansion reduces missing only when the new character was needed; counts below zero represent surplus.','While valid, record the candidate before removing the left character. Removal can make a required occurrence missing again.'])
    A('window','Longest Repeating Character Replacement','Medium','For uppercase English text, find the longest substring made uniform by replacing at most k characters.','A window needs length minus its most frequent character count replacements.','O(26n)','O(26)', '''def character_replacement(s, k):
    counts = {}
    left = best = 0
    for right, c in enumerate(s):
        counts[c] = counts.get(c, 0) + 1
        while right - left + 1 - max(counts.values()) > k:
            counts[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best''', 'character_replacement("AABABBA",1)==4 and character_replacement("",2)==0', ['Count each character inside the current window.','Recompute its maximum frequency exactly; with 26 possible letters this remains linear with a small factor.','Shrink while length − maximum frequency exceeds k, then update best using the valid window.'])
    A('prefix','Product of Array Except Self','Medium','Return the product of all other values at each index, without division.','Combine a prefix product with a suffix product. Zeros require no special case.','O(n)','O(1) auxiliary + output', '''def product_except_self(nums):
    answer = [1] * len(nums)
    prefix = 1
    for i, x in enumerate(nums):
        answer[i] = prefix
        prefix *= x
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer''', 'product_except_self([1,2,3,4])==[24,12,8,6] and product_except_self([0,2,0])==[0,0,0]', ['Initialise output to multiplicative identity 1.','Write the product strictly before i, then multiply the current value into prefix. Order matters.','Walk backwards: multiply by the product strictly after i, then update suffix. Both passes exclude nums[i].'])
    A('prefix','Continuous Subarray Sum','Medium','For nonnegative nums and k > 0, determine whether a subarray of length at least two has sum divisible by k.','Equal prefix remainders imply a divisible difference.','O(n) expected','O(min(n,k))', '''def continuous_subarray_sum(nums, k):
    first = {0: -1}
    total = 0
    for i, x in enumerate(nums):
        total = (total + x) % k
        if total in first:
            if i - first[total] >= 2:
                return True
        else:
            first[total] = i
    return False''', 'continuous_subarray_sum([23,2,4,6,7],6) and not continuous_subarray_sum([1],1)', ['Store remainder zero at virtual index −1 so ranges starting at index zero work.','Reduce each cumulative sum modulo k. Equal remainders mean the intermediate sum is a multiple of k.','Keep the earliest index for each remainder; it maximises potential length. Require a gap of at least two.'])
    A('sort','K Closest Points to Origin','Medium','Return k points closest to (0,0); ties may appear in any order.','Squared distances preserve ordering without square roots.','O(n log n)','O(n)', '''def k_closest(points, k):
    ordered = sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])
    return ordered[:k]''', 'k_closest([[1,3],[-2,2]],1)==[[-2,2]] and k_closest([],0)==[]', ['The key function computes x²+y², not the distance itself.','Sort copies the point list and orders it by that key.','Return the first k entries. A size-k heap is an alternative if sorting all points is too expensive.'])
    A('sort','Sort an Array (Merge Sort)','Medium','Sort integers with merge sort; return a new list.','Recursively sort each half, then merge their ordered fronts.','O(n log n)','O(n)', '''def merge_sort(nums):
    if len(nums) <= 1:
        return nums[:]
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]''', 'merge_sort([5,2,3,1])==[1,2,3,5] and merge_sort([])==[]', ['A length-zero or length-one array is already ordered; return a copy.','Recursively sort both halves. Recursion creates log n levels.','Merge by comparing the two fronts, then append the unconsumed tail. Each level processes O(n) values.'])
    A('intervals','Meeting Rooms','Easy','Determine whether one person can attend all half-open meetings [start,end).','After sorting, only neighboring meetings need to be compared.','O(n log n)','O(n)', '''def can_attend(intervals):
    meetings = sorted(intervals)
    for i in range(1, len(meetings)):
        if meetings[i][0] < meetings[i - 1][1]:
            return False
    return True''', 'not can_attend([[0,30],[5,10],[15,20]]) and can_attend([[1,2],[2,3]])', ['Sort by start time, copying the input.','Compare each start to the preceding end. Touching half-open intervals are allowed.','Any overlap proves failure; an empty or singleton schedule succeeds.'])
    A('intervals','Minimum Arrows to Burst Balloons','Medium','Closed intervals represent balloons. An arrow at x bursts all intervals containing x. Minimise arrows.','Fire at the earliest finishing interval’s end, covering every interval that reaches it.','O(n log n)','O(n)', '''def min_arrows(intervals):
    if not intervals:
        return 0
    ordered = sorted(intervals, key=lambda p: p[1])
    arrows, position = 1, ordered[0][1]
    for start, end in ordered[1:]:
        if start > position:
            arrows += 1
            position = end
    return arrows''', 'min_arrows([[10,16],[2,8],[1,6],[7,12]])==2 and min_arrows([])==0', ['Sort by interval end, the greedy decision boundary.','The first arrow goes at the earliest end. Any subsequent interval starting at or before it is already burst.','If start is strictly beyond the arrow, start a new group and shoot at this interval’s end. Closed endpoints require >, not ≥.'])
    A('binary','Find Minimum in Rotated Sorted Array','Medium','For a nonempty rotated sorted array of distinct values, return its minimum.','Comparing mid against the right endpoint identifies which side contains the rotation.','O(log n)','O(1)', '''def rotated_min(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]''', 'rotated_min([3,4,5,1,2])==1 and rotated_min([1])==1', ['Use inclusive boundaries on a nonempty input.','If mid is larger than the rightmost value, the minimum lies strictly after mid.','Otherwise keep mid as a candidate by setting right=mid. Finish at one index.'])
    A('binary','First and Last Position of Element','Medium','Return target’s first and last indices in a sorted array, or [-1,-1].','Find the boundary ≥ target and the boundary > target.','O(log n)','O(1)', '''def search_range(nums, target):
    def boundary(strict):
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] > target or (not strict and nums[mid] == target):
                right = mid
            else:
                left = mid + 1
        return left
    start, end = boundary(False), boundary(True)
    return [start, end - 1] if start < end else [-1, -1]''', 'search_range([5,7,7,8,8,10],8)==[3,4] and search_range([],0)==[-1,-1]', ['The helper searches a half-open interval and returns the first index satisfying its comparison.','strict=False gives lower bound; strict=True gives upper bound.','If the bounds coincide the target is absent. Otherwise upper bound minus one is the final matching index.'])
    A('fast','Linked List Cycle Entrance','Medium','Return the node where a linked-list cycle begins, or None. LeetCode supplies ListNode.','After collision, reset one pointer to head and move both one step.','O(n)','O(1)', '''def cycle_entrance(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            seeker = head
            while seeker is not slow:
                seeker, slow = seeker.next, slow.next
            return seeker
    return None''', 'cycle_entrance(cycle_list([3,2,0,-4],1)).val==2 and cycle_entrance(make_list([1,2])) is None', ['First detect a collision using one-step and two-step pointers.','A collision occurs inside the cycle. Reset seeker to head while slow stays at the collision.','Advance seeker and slow together. Their first meeting is the entrance; if no collision occurs, return None.'])
    A('fast','Find the Duplicate Number','Medium','n+1 integers each lie in [1,n], with exactly one duplicated value. Do not modify the input.','Treat each index as a node and nums[index] as its successor; the duplicate is the cycle entrance.','O(n)','O(1)', '''def find_duplicate(nums):
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    seeker = nums[0]
    while seeker != slow:
        seeker, slow = nums[seeker], nums[slow]
    return seeker''', 'find_duplicate([1,3,4,2,2])==2 and find_duplicate([3,1,3,4,2])==3', ['Use the value range as legal successor indices. This implicit graph has a cycle reachable from nums[0].','Floyd’s first phase finds a collision without a visited set.','Reset a seeker to the initial successor and advance both once; the entrance value is duplicated.'])
    A('linked','Reorder List','Medium','Reorder L0→L1→…→Ln as L0→Ln→L1→Ln−1…; mutate links. Returns head for practice.','Split at the middle, reverse the second half, then alternate nodes.','O(n)','O(1)', '''def reorder_list(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None
    previous = None
    while second:
        following = second.next
        second.next = previous
        previous, second = second, following
    first, second = head, previous
    while second:
        first_next, second_next = first.next, second.next
        first.next = second
        second.next = first_next
        first, second = first_next, second_next
    return head''', 'list_values(reorder_list(make_list([1,2,3,4,5])))==[1,5,2,4,3] and reorder_list(None) is None', ['Find the end of the first half and disconnect it to prevent accidental cycles.','Reverse the second half while preserving its next node before each rewrite.','For each interleave, save both next links before changing either link; then advance both lists using the saved nodes.'])
    A('linked','Add Two Numbers','Medium','Lists contain decimal digits in reverse order. Return their sum as a reverse-order digit list.','Carry propagates from one digit position to the next.','O(max(n,m))','O(max(n,m)) output', '''def add_two_numbers(a, b):
    dummy = tail = ListNode(0)
    carry = 0
    while a or b or carry:
        total = carry + (a.val if a else 0) + (b.val if b else 0)
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        a = a.next if a else None
        b = b.next if b else None
    return dummy.next''', 'list_values(add_two_numbers(make_list([2,4,3]),make_list([5,6,4])))==[7,0,8]', ['Start with a dummy output head and zero carry.','Process while either input or carry remains. Missing digits contribute zero.','divmod yields the next carry and digit simultaneously; append the digit and advance both input lists if present.'])
    A('stack','Min Stack','Medium','Support push, pop, top and get_min in constant time. pop/top/get_min require a nonempty stack.','Store each value alongside the minimum at that depth.','O(1) per operation','O(n)', '''class MinStack:
    def __init__(self):
        self.items = []
    def push(self, value):
        minimum = min(value, self.items[-1][1]) if self.items else value
        self.items.append((value, minimum))
    def pop(self):
        return self.items.pop()[0]
    def top(self):
        return self.items[-1][0]
    def get_min(self):
        return self.items[-1][1]''', 'check_min_stack(MinStack)', ['Each stored tuple contains the actual value and the minimum of the prefix ending there.','On push, combine the new value with the previous minimum.','On pop, the previous minimum is automatically restored because it is stored with the previous entry.'])
    A('stack','Evaluate Reverse Polish Notation','Medium','Evaluate valid postfix tokens with integer operands and +,−,*,/. Division truncates toward zero; divisor is nonzero.','Operators consume the two most recent values in their original operand order.','O(n)','O(n)', '''def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if token not in {'+', '-', '*', '/'}:
            stack.append(int(token))
            continue
        right, left = stack.pop(), stack.pop()
        if token == '+': result = left + right
        elif token == '-': result = left - right
        elif token == '*': result = left * right
        else:
            result = abs(left) // abs(right)
            if (left < 0) != (right < 0): result = -result
        stack.append(result)
    return stack[-1]''', 'eval_rpn(["2","1","+","3","*"])==9 and eval_rpn(["-7","3","/"])==-2', ['Numbers are pushed directly. Operators pop right first and left second; subtraction and division depend on this order.','Compute the operator result. For division, divide magnitudes using // and restore the sign to truncate toward zero.','Push the result so a later operator can consume it. A valid expression ends with exactly one value.'])
    A('deque','Moving Average From a Stream','Easy','For size > 0, report the average of the last size arriving values.','Maintain a FIFO queue and a running sum; expire at most one value per arrival.','O(1) per arrival','O(size)', '''from collections import deque

class MovingAverage:
    def __init__(self, size):
        self.size, self.values, self.total = size, deque(), 0
    def next(self, value):
        self.values.append(value)
        self.total += value
        if len(self.values) > self.size:
            self.total -= self.values.popleft()
        return self.total / len(self.values)''', 'check_moving_average(MovingAverage)', ['Store the maximum window size, queue, and running sum.','Add the new value to both queue and sum; if over capacity, remove the oldest value from both.','Divide by the current queue length, which is smaller than size during warm-up.'])
    A('deque','Longest Subarray Within Absolute Limit','Medium','Return the longest contiguous subarray with max−min ≤ limit, where limit ≥ 0.','Maintain increasing minima and decreasing maxima deques.','O(n)','O(n)', '''from collections import deque

def longest_with_limit(nums, limit):
    minima, maxima = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while minima and nums[minima[-1]] >= x: minima.pop()
        while maxima and nums[maxima[-1]] <= x: maxima.pop()
        minima.append(right)
        maxima.append(right)
        while nums[maxima[0]] - nums[minima[0]] > limit:
            if minima[0] == left: minima.popleft()
            if maxima[0] == left: maxima.popleft()
            left += 1
        best = max(best, right - left + 1)
    return best''', 'longest_with_limit([8,2,4,7],4)==2 and longest_with_limit([],4)==0', ['Discard dominated candidates from each deque before appending the new index.','The two fronts give current minimum and maximum. If their difference is too large, shrink left and expire front indices as necessary.','After shrinking, record the valid length. Every index is inserted and removed at most once per deque.'])
    A('heap','Top K Frequent Elements','Medium','Return k most frequent distinct integers; 0 ≤ k ≤ distinct count. Ties may appear in any order.','Count frequencies, then retrieve the largest counts with a heap-based selection.','O(n + u log k), u distinct values','O(u)', '''from collections import Counter
import heapq

def top_k_frequent(nums, k):
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)''', 'top_k_frequent([1,1,1,2,2,3],2)==[1,2] and top_k_frequent([],0)==[]', ['Counter reduces the input to unique values with counts.','nlargest selects keys according to their frequency.','Return the selected values; frequency counts determine rank, not numeric value.'])
    A('heap','Task Scheduler','Medium','Unit-time tasks can be reordered; identical labels need n idle slots between runs. Find minimum total slots.','The most frequent labels determine a lower bound that other tasks can fill.','O(task count)','O(distinct labels)', '''from collections import Counter

def least_interval(tasks, n):
    if not tasks: return 0
    counts = Counter(tasks)
    maximum = max(counts.values())
    tied = sum(value == maximum for value in counts.values())
    frame = (maximum - 1) * (n + 1) + tied
    return max(len(tasks), frame)''', 'least_interval(list("AAABBB"),2)==8 and least_interval([],2)==0', ['Count tasks and identify the maximum multiplicity and number of labels tied at that maximum.','The first maximum−1 blocks each need n+1 positions, with tied maximum labels forming the final partial block.','The answer cannot be below the total task count. This example uses counting mathematics; a heap simulation is an alternative.'])
    A('dfs','Invert Binary Tree','Easy','Swap left and right children recursively. LeetCode supplies TreeNode.','Every subtree is inverted independently after swapping its two child references.','O(n)','O(height)', '''def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = root.right, root.left
    invert_tree(root.left)
    invert_tree(root.right)
    return root''', 'invert_tree(TreeNode(1,TreeNode(2),TreeNode(3))).left.val==3 and invert_tree(None) is None', ['An empty subtree needs no work.','Swap both references simultaneously; Python evaluates the right-hand tuple before assigning either attribute.','Recursively invert the newly placed children and return the same root object.'])
    A('dfs','Lowest Common Ancestor','Medium','In a binary tree with unique node objects, find the LCA of two nodes known to exist.','If the two targets are found on opposite sides, the current root is their meeting point.','O(n)','O(height)', '''def lowest_common_ancestor(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right''', 'check_lca(lowest_common_ancestor)', ['Stop at an empty subtree or a target node. The returned node represents a target found or an LCA already established.','Search both subtrees and retain both results; do not skip a side.','Two nonempty results imply this root is the LCA. Otherwise propagate the only result upward.'])
    A('bfs','Word Ladder','Hard','Words use lowercase a–z. Change one letter per step using a word list; return the shortest sequence length or zero.','BFS layers count word transformations; remove a word when enqueuing.','O(26 × word length² × word count)','O(word count × word length)', '''from collections import deque

def ladder_length(begin, end, words):
    if begin == end: return 1
    remaining = set(words)
    if end not in remaining: return 0
    remaining.discard(begin)
    queue = deque([(begin, 1)])
    while queue:
        word, depth = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                candidate = word[:i] + c + word[i+1:]
                if candidate in remaining:
                    if candidate == end: return depth + 1
                    remaining.remove(candidate)
                    queue.append((candidate, depth + 1))
    return 0''', 'ladder_length("hit","cog",["hot","dot","dog","lot","log","cog"])==5', ['Reject a missing end word; put all permitted words in an unvisited set.','For each dequeued word, generate each single-letter replacement. Building strings costs O(word length).','Enqueue each valid word once and increase depth. First reaching end gives the shortest transformation sequence.'])
    A('bfs','01 Matrix','Medium','For a binary matrix containing at least one zero, return each cell’s Manhattan distance to the nearest zero.','Start a multi-source BFS from every zero at distance zero.','O(rows × cols)','O(rows × cols)', '''from collections import deque

def update_matrix(matrix):
    if not matrix or not matrix[0]: return []
    rows, cols = len(matrix), len(matrix[0])
    distance = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == 0:
                distance[r][c] = 0
                queue.append((r,c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if 0 <= nr < rows and 0 <= nc < cols and distance[nr][nc] == -1:
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr,nc))
    return distance''', 'update_matrix([[0,0,0],[0,1,0],[1,1,1]])==[[0,0,0],[0,1,0],[1,2,1]]', ['Create independent matrix rows; −1 means undiscovered. Seed every zero at distance zero.','Process the queue in distance order. An undiscovered neighbor receives parent distance +1 and is enqueued immediately.','Each cell is discovered once; return the entire distance matrix.'])
    A('backtrack','Word Search','Medium','Determine whether a nonempty word can be formed in a grid using adjacent cells without reusing a cell.','The visited set belongs to the current path and must be undone on return.','O(rows × cols × 4^word length) upper bound','O(word length)', '''def word_search(board, word):
    if not word: return True
    if not board or not board[0]: return False
    rows, cols, used = len(board), len(board[0]), set()
    def visit(r, c, i):
        if i == len(word): return True
        if not (0 <= r < rows and 0 <= c < cols): return False
        if (r,c) in used or board[r][c] != word[i]: return False
        used.add((r,c))
        found = any(visit(nr,nc,i+1) for nr,nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)])
        used.remove((r,c))
        return found
    return any(visit(r,c,0) for r in range(rows) for c in range(cols))''', 'word_search([list("ABCE"),list("SFCS"),list("ADEE")],"ABCCED") and not word_search([list("AA")],"AAA")', ['Reject out-of-bounds, reused, or mismatched cells before changing state.','Mark the matched cell, recursively try its four neighbors, and remove the mark even after a successful branch.','Start the search independently from each cell. Path-local visits allow the same cell to be considered in a different candidate path.'])
    A('backtrack','Generate Parentheses','Medium','Generate every well-formed sequence of n ≥ 0 pairs of parentheses.','Never allow more closes than opens in any partial prefix.','O(n × Catalan(n))','O(n) + output', '''def generate_parentheses(n):
    result, path = [], []
    def visit(opened, closed):
        if closed == n:
            result.append(''.join(path))
            return
        if opened < n:
            path.append('(')
            visit(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(')')
            visit(opened, closed + 1)
            path.pop()
    visit(0,0)
    return result''', 'generate_parentheses(2)==["(())","()()"] and generate_parentheses(0)==[""]', ['opened and closed counts define the recursive state; path holds the actual characters.','Add an opener only if opened<n. Add a closer only if closed<opened.','Each choice is undone after recursion. When closed=n, both counts must equal n, so store the completed string.'])
    A('greedy','Best Time to Buy and Sell Stock','Easy','Find maximum profit from one buy followed by one sell; return zero if no gain is possible.','Track the cheapest price seen strictly before or at the current day.','O(n)','O(1)', '''def max_profit(prices):
    cheapest, best = float('inf'), 0
    for price in prices:
        cheapest = min(cheapest, price)
        best = max(best, price - cheapest)
    return best''', 'max_profit([7,1,5,3,6,4])==5 and max_profit([7,6,4,3,1])==0', ['Initial best is zero so loss-making trades are never required.','Update the minimum purchase price available by this day.','Compare selling today against the best previous profit. A same-day buy/sell contributes zero and cannot hurt.'])
    A('greedy','Maximum Subarray (Kadane)','Medium','For a nonempty integer array, find the maximum sum of a nonempty contiguous subarray.','At each index, either extend the previous best ending here or start fresh.','O(n)','O(1)', '''def max_subarray(nums):
    ending = best = nums[0]
    for x in nums[1:]:
        ending = max(x, ending + x)
        best = max(best, ending)
    return best''', 'max_subarray([-2,1,-3,4,-1,2,1,-5,4])==6 and max_subarray([-3,-1,-2])==-1', ['Initialise from the first value, not zero: the selected subarray must be nonempty even for all-negative input.','ending is the maximum sum ending exactly at the current index.','best is the maximum of every ending seen. This is both a DP recurrence and a greedy discard of negative prior sums.'])
    A('dp','House Robber','Medium','Nonnegative house values; maximise loot without choosing adjacent houses.','Carry the best values for the previous one and two positions.','O(n)','O(1)', '''def house_robber(nums):
    two_back = one_back = 0
    for value in nums:
        current = max(one_back, two_back + value)
        two_back, one_back = one_back, current
    return one_back''', 'house_robber([2,7,9,3,1])==12 and house_robber([])==0', ['Before each house, one_back is the best previous prefix and two_back excludes its immediate neighbor.','Choose between skipping the current house and taking it with two_back.','Shift both states simultaneously using the old one_back. Return the final prefix optimum.'])
    A('dp','Longest Increasing Subsequence','Medium','Find the length of a strictly increasing subsequence; positions need not be contiguous.','dp[i] is the longest increasing subsequence ending exactly at i.','O(n²)','O(n)', '''def lis_length(nums):
    if not nums: return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)''', 'lis_length([10,9,2,5,3,7,101,18])==4 and lis_length([2,2,2])==1', ['Each element alone forms a length-one subsequence.','For each i, inspect every earlier j. Strict inequality excludes equal values.','A compatible j can extend its best sequence by one; take the best transition. The overall answer is max(dp), not necessarily dp[-1].'])
    A('dp','Unique Paths','Medium','Count paths across an m×n grid, moving only right/down; m,n ≥ 1.','A cell inherits paths from above plus paths from the left.','O(mn)','O(mn)', '''def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for r in range(1,m):
        for c in range(1,n):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[-1][-1]''', 'unique_paths(3,3)==6 and unique_paths(1,4)==1', ['The first row and column each have one path, because no alternative route exists there.','Create separate row objects to prevent shared-row mutations.','Fill interior cells in row order using already-computed above/left states. The bottom-right entry is the answer.'])
    A('dp','Edit Distance','Hard','Minimum insertions, deletions or replacements to turn a into b.','dp[i][j] is the distance between the first i and first j characters.','O(nm)','O(nm)', '''def edit_distance(a, b):
    dp = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)+1): dp[i][0] = i
    for j in range(len(b)+1): dp[0][j] = j
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[-1][-1]''', 'edit_distance("horse","ros")==3 and edit_distance("","abc")==3', ['The zero row and column encode converting from/to an empty string.','Equal final characters cost nothing extra; copy the diagonal.','Otherwise add one to the minimum of delete (above), insert (left), and replace (diagonal). The full trace includes each matrix update.'])
    A('graph','Clone Graph','Medium','Given an adjacency dictionary of an undirected graph, clone the component reachable from start. Return independent lists.','A visited mapping lets cycles reuse already-created copies.','O(V + E)','O(V + E)', '''from collections import deque

def clone_graph(graph, start):
    if start not in graph: return {}
    copies = {start: []}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in copies:
                copies[neighbor] = []
                queue.append(neighbor)
            copies[node].append(neighbor)
    return copies''', 'clone_graph({1:[2],2:[1,3],3:[2]},1)=={1:[2],2:[1,3],3:[2]}', ['This practice representation uses vertex labels and adjacency lists instead of LeetCode Node objects.','Create each cloned list once when its vertex is discovered, then process it via BFS.','Copy all neighbor labels into new lists. The output does not share the input adjacency-list objects.'])
    A('graph','Redundant Connection','Medium','Edges of a positive-label undirected tree plus one extra edge are given in order. Return the edge forming the cycle.','An edge between nodes already in one union-find component is redundant.','O(n α(n))','O(n)', '''def redundant_connection(edges):
    parent = list(range(len(edges)+1))
    size = [1] * len(parent)
    def find(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u,v in edges:
        a,b = find(u),find(v)
        if a == b: return [u,v]
        if size[a] < size[b]: a,b = b,a
        parent[b] = a
        size[a] += size[b]
    return []''', 'redundant_connection([[1,2],[1,3],[2,3]])==[2,3]', ['Initialise each vertex as its own component; find compresses paths.','For each edge compare roots. Equal roots prove an existing path, so the new edge closes a cycle.','Otherwise attach the smaller component beneath the larger and update its size.'])
    A('trie','Replace Words','Medium','Replace each sentence word by its shortest dictionary root, if present. Words are space separated.','Stop at the first terminal trie node while reading a word.','O(dictionary characters + sentence characters)','O(dictionary characters + output)', '''def replace_words(dictionary, sentence):
    root = {}
    for word in dictionary:
        node = root
        for c in word: node = node.setdefault(c,{})
        node[None] = True
    def replace(word):
        node = root
        for i,c in enumerate(word):
            if c not in node: return word
            node = node[c]
            if None in node: return word[:i+1]
        return word
    return ' '.join(replace(word) for word in sentence.split())''', 'replace_words(["cat","bat","rat"],"the cattle was rattled by the battery")=="the cat was rat by the bat"', ['Insert roots into a trie and mark terminal nodes with a unique key.','Read each word until a terminal root appears or the prefix path fails.','The first terminal is the shortest root. Join the replaced words with spaces.'])
    A('trie','Longest Common Prefix','Easy','Return the longest prefix shared by every string, or empty for an empty list.','Trim a candidate prefix until each successive word starts with it.','O(total characters) conservative bound','O(maximum word length)', '''def longest_common_prefix(words):
    if not words: return ''
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
    return prefix''', 'longest_common_prefix(["flower","flow","flight"])=="fl" and longest_common_prefix([])==""', ['Start with the first word as a candidate prefix.','For each next word, shorten the prefix from the right until it matches.','The candidate only shrinks, so previously processed words remain compatible. Slicing creates string copies.'])
    # Correct complexity for the deliberately simple repeated-prefix/slicing implementation.
    by_id['trie']['examples'][-1]['time'] = 'O(total characters + L²), L initial prefix length'
    A('bits','Reverse Bits','Easy','Reverse the bits of an unsigned 32-bit integer.','Consume the low bit and append it to the reversed result exactly 32 times.','O(32) = O(1)','O(1)', '''def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result''', 'reverse_bits(43261596)==964176192 and reverse_bits(0)==0', ['Initialise the output to zero.','Left shift opens the next output bit; OR the input’s current low bit into that position.','Right shift the input and repeat 32 times, including leading zeros required by the fixed width.'])
    A('bits','Pow(x, n)','Medium','Compute x raised to integer n; x must be nonzero if n is negative.','Exponentiation by squaring halves the remaining exponent each iteration.','O(log |n|)','O(1)', '''def power(x, n):
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n & 1: result *= x
        x *= x
        n //= 2
    return result''', 'power(2,10)==1024 and power(2,-2)==0.25', ['Negative exponents invert the base and make the exponent positive.','If the exponent’s current low bit is one, include the current power in result.','Square the base and halve the exponent. Each iteration accounts for one bit of the exponent.'])

    p = P('matrix','Matrices & simulation','Sequences','▧','Make coordinates, boundaries and mutation rules explicit.',
          'Use for traversing grids, rotating matrices, simulation, and in-place transformations.',
          'Already processed cells or layers match the target transformation; unprocessed cells remain available.',
          'Avoid shared rows. For simultaneous updates, preserve the old state or encode it separately.',
          ['matrix','spiral','rotate image','grid','simulation','game of life'],['dfs','bfs','pointers'])
    by_id['matrix'] = p
    A('matrix','Rotate Image','Medium','Rotate an n×n matrix 90 degrees clockwise in place; returns matrix for practice.','Transpose across the diagonal, then reverse every row.','O(n²)','O(1)', '''def rotate_image(matrix):
    n = len(matrix)
    for r in range(n):
        for c in range(r+1,n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]
    for row in matrix:
        row.reverse()
    return matrix''', 'rotate_image([[1,2],[3,4]])==[[3,1],[4,2]]', ['Swap only cells above the diagonal with their mirrored partners; each pair is processed once.','The transpose converts rows into columns.','Reversing each row after the transpose yields clockwise rotation. The input must be square.'])
    A('matrix','Spiral Matrix','Medium','Return a rectangular matrix’s values in clockwise spiral order.','Shrink top, bottom, left and right boundaries after each side.','O(rows × cols)','O(output)', '''def spiral_order(matrix):
    if not matrix or not matrix[0]: return []
    top, bottom, left, right = 0, len(matrix)-1, 0, len(matrix[0])-1
    result = []
    while top <= bottom and left <= right:
        for c in range(left,right+1): result.append(matrix[top][c])
        top += 1
        for r in range(top,bottom+1): result.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right,left-1,-1): result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom,top-1,-1): result.append(matrix[r][left])
            left += 1
    return result''', 'spiral_order([[1,2,3],[4,5,6],[7,8,9]])==[1,2,3,6,9,8,7,4,5]', ['Keep four inclusive boundaries around the unvisited rectangle.','Visit top then right, shrinking each boundary immediately.','Check remaining height and width before bottom and left, so a single row/column is not read twice.'])
    A('matrix','Set Matrix Zeroes','Medium','If a cell is zero, zero its entire row and column. This clear version uses extra sets.','Record original zero coordinates before mutating any cells.','O(rows × cols)','O(rows + cols)', '''def set_zeroes(matrix):
    rows, cols = set(), set()
    for r,row in enumerate(matrix):
        for c,value in enumerate(row):
            if value == 0:
                rows.add(r)
                cols.add(c)
    for r,row in enumerate(matrix):
        for c in range(len(row)):
            if r in rows or c in cols:
                matrix[r][c] = 0
    return matrix''', 'set_zeroes([[1,1,1],[1,0,1],[1,1,1]])==[[1,0,1],[0,0,0],[1,0,1]]', ['First scan the original matrix and remember affected row/column indices.','Do not zero during discovery: newly created zeros must not create new affected rows.','In a second pass, mutate cells in a recorded row or column. O(1)-extra-space marking is a possible advanced optimisation.'])
    A('matrix','Search a 2D Matrix','Medium','Rows are sorted and each row’s first value exceeds the previous row’s last. Find target.','The matrix is one globally sorted sequence when flattened.','O(log(rows × cols))','O(1)', '''def search_matrix(matrix, target):
    if not matrix or not matrix[0]: return False
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1
    while left <= right:
        mid = (left + right) // 2
        value = matrix[mid // cols][mid % cols]
        if value == target: return True
        if value < target: left = mid + 1
        else: right = mid - 1
    return False''', 'search_matrix([[1,3,5],[7,9,11]],9) and not search_matrix([],2)', ['Treat row-major indices as a sorted array without allocating it.','Map an index back to (row,column) using quotient and remainder by the column count.','Perform ordinary binary search. Merely sorting rows independently is not enough for this assumption.'])
    A('matrix','Game of Life','Medium','Compute one simultaneous update of a binary grid. Live cells survive with 2/3 live neighbors; dead cells revive with 3.','Use a separate next-state matrix so every neighbor count reads the original generation.','O(rows × cols)','O(rows × cols)', '''def game_of_life(board):
    if not board or not board[0]: return []
    rows, cols = len(board), len(board[0])
    following = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr,nc = r+dr,c+dc
                    if (dr or dc) and 0 <= nr < rows and 0 <= nc < cols:
                        neighbors += board[nr][nc]
            following[r][c] = int(neighbors == 3 or (board[r][c] == 1 and neighbors == 2))
    return following''', 'game_of_life([[0,1,0],[0,1,0],[0,1,0]])==[[0,0,0],[1,1,1],[0,0,0]]', ['Allocate independent next-state rows while retaining the original board.','For each cell count its eight in-bounds neighbors, excluding itself.','Write only into the next-state matrix. Reading and writing the same generation would violate simultaneous update semantics.'])
