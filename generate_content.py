import json
import ast
from pathlib import Path

patterns = []
def P(id, name, group, icon, summary, use, invariant, pitfalls, signals, related):
    p = dict(id=id, name=name, group=group, icon=icon, summary=summary, use=use,
             invariant=invariant, pitfalls=pitfalls, signals=signals, related=related, examples=[])
    patterns.append(p)
    return p
def E(p, title, difficulty, prompt, insight, time, space, code, check):
    p['examples'].append(dict(title=title, difficulty=difficulty, prompt=prompt, insight=insight,
                             time=time, space=space, code=code.strip(), check=check))

p=P('hash','Hash maps & sets','Sequences','⌗','Remember what you have seen. Turn repeated searches into quick lookups.',
'Use for membership, frequencies, grouping, or matching a value with its complement.',
'The map describes exactly the elements processed so far.',
'Hashing gives expected constant-time lookup, not a universal worst-case guarantee. Store indices when the answer needs positions.',
['duplicates','frequency','frequencies','anagram','two sum','complement','lookup','distinct'],['window','prefix','sort'])
E(p,'Two Sum','Easy','Return indices of two distinct numbers that add to target. Assume one solution exists.','Look for the complement before storing the current index.','O(n)','O(n)', '''def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []''', 'two_sum([2,7,11,15],9)==[0,1] and two_sum([3,3],6)==[0,1]')
E(p,'Group Anagrams','Medium','Group lowercase English words with identical letter counts.','A tuple of 26 counts is a stable signature.','O(total characters + 26n)','O(total characters + 26n)', '''def group_anagrams(words):
    groups = {}
    for word in words:
        counts = [0] * 26
        for c in word:
            counts[ord(c) - ord('a')] += 1
        groups.setdefault(tuple(counts), []).append(word)
    return list(groups.values())''', 'sorted(sorted(g) for g in group_anagrams(["eat","tea","tan","ate","nat","bat"]))==[["ate","eat","tea"],["bat"],["nat","tan"]]')
E(p,'Longest Consecutive Sequence','Medium','Find the longest consecutive integer run in an unsorted array.','Only start a walk at a number without a predecessor.','O(n) expected','O(n)', '''def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:
            end = x
            while end in values:
                end += 1
            best = max(best, end - x)
    return best''', 'longest_consecutive([100,4,200,1,3,2])==4 and longest_consecutive([])==0')

p=P('pointers','Two pointers','Sequences','⇆','Move two boundaries with purpose, eliminating impossible choices.',
'Use on sorted sequences, opposite ends, or read/write positions in an array.',
'Every pointer move eliminates candidates that cannot improve or satisfy the answer.',
'Sorting changes original positions. You need a reason for which pointer moves; two variables alone do not make this pattern valid.',
['sorted array','pair','palindrome','three sum','3sum','two pointers','in-place','in place'],['sort','window','fast'])
E(p,'Pair in a Sorted Array','Easy','Return zero-based indices of a target pair in a sorted array.','A small sum needs a larger left value; a large sum needs a smaller right value.','O(n)','O(1)', '''def sorted_pair(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return []''', 'sorted_pair([2,7,11,15],9)==[0,1] and sorted_pair([],4)==[]')
E(p,'3Sum','Medium','Return unique triplets whose sum is zero.','Sort, fix one value, then solve a two-pointer pair search while skipping duplicates.','O(n²)','O(n) + output', '''def three_sum(nums):
    a = sorted(nums)
    result = []
    for i in range(len(a) - 2):
        if i > 0 and a[i] == a[i - 1]:
            continue
        left, right = i + 1, len(a) - 1
        while left < right:
            total = a[i] + a[left] + a[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([a[i], a[left], a[right]])
                left += 1
                right -= 1
                while left < right and a[left] == a[left - 1]:
                    left += 1
                while left < right and a[right] == a[right + 1]:
                    right -= 1
    return result''', 'three_sum([-1,0,1,2,-1,-4])==[[-1,-1,2],[-1,0,1]]')
E(p,'Container With Most Water','Medium','Given nonnegative heights, maximise water between two lines.','Move the shorter line: moving only the taller one cannot improve the current bottleneck.','O(n)','O(1)', '''def max_area(heights):
    left, right, best = 0, len(heights) - 1, 0
    while left < right:
        best = max(best, (right - left) * min(heights[left], heights[right]))
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    return best''', 'max_area([1,8,6,2,5,4,8,3,7])==49 and max_area([])==0')

p=P('window','Sliding window','Sequences','▣','Grow a contiguous region. Shrink it when a maintained condition breaks.',
'Use for fixed-length ranges or variable-length substrings with efficiently maintained validity.',
'After shrinking, the current window satisfies the required condition.',
'For sum-based windows, negative numbers can break monotonicity. Minimum-valid windows often record the answer inside the shrink loop.',
['substring','contiguous','subarray','window','at most','without repeating','consecutive ones'],['hash','prefix','deque'])
E(p,'Longest Unique Substring','Medium','Find the length of the longest substring without repeated characters.','A frequency map tells you when the new character breaks validity.','O(n)','O(min(n, alphabet size))', '''def longest_unique(s):
    counts = {}
    left = best = 0
    for right, c in enumerate(s):
        counts[c] = counts.get(c, 0) + 1
        while counts[c] > 1:
            old = s[left]
            counts[old] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best''', 'longest_unique("abcabcbb")==3 and longest_unique("")==0')
E(p,'Minimum Size Subarray Sum','Medium','For positive integers and a positive target, find the shortest subarray with sum at least target.','Positivity makes removing from the left decrease the sum.','O(n)','O(1)', '''def min_subarray_len(target, nums):
    left = total = 0
    best = len(nums) + 1
    for right, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best > len(nums) else best''', 'min_subarray_len(7,[2,3,1,2,4,3])==2 and min_subarray_len(8,[1,2])==0')
E(p,'Max Consecutive Ones III','Medium','In a binary array, find the longest run after flipping at most k zeros.','Maintain a window containing no more than k zeros.','O(n)','O(1)', '''def longest_ones(nums, k):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        zeros += x == 0
        while zeros > k:
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left + 1)
    return best''', 'longest_ones([1,1,1,0,0,0,1,1,1,1,0],2)==6 and longest_ones([0],0)==0')

p=P('prefix','Prefix sums & differences','Sequences','∑','Precompute cumulative information so ranges become subtraction.',
'Use for repeated range sums, exact subarray sums, and batched interval increments.',
'prefix[i] represents the sum of the first i values; a difference entry marks a change at a boundary.',
'Use a leading zero to avoid off-by-one errors. For exact subarray counts, store frequencies of prior sums, not just existence.',
['range sum','prefix','subarray sum','negative numbers','range update','cumulative','sum equals'],['hash','window','deque'])
E(p,'Immutable Range Sum','Easy','Answer inclusive range-sum queries on an unchanged array.','Subtract the prefix before the left boundary from the prefix after the right boundary.','O(n) build; O(1) query','O(n)', '''def range_sums(nums, queries):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return [prefix[right + 1] - prefix[left] for left, right in queries]''', 'range_sums([-2,0,3,-5,2,-1],[(0,2),(2,5),(0,5)])==[1,-1,-3]')
E(p,'Subarray Sum Equals K','Medium','Count contiguous subarrays summing to k, including arrays with negatives.','If current prefix is s, each earlier prefix s−k starts a valid subarray.','O(n) expected','O(n)', '''def subarray_sum(nums, k):
    frequencies = {0: 1}
    total = answer = 0
    for x in nums:
        total += x
        answer += frequencies.get(total - k, 0)
        frequencies[total] = frequencies.get(total, 0) + 1
    return answer''', 'subarray_sum([1,1,1],2)==2 and subarray_sum([1,-1,0],0)==3')
E(p,'Range Addition','Medium','Apply inclusive updates (left, right, delta) to a zero array of length n.','Mark where each update starts and where it stops; one prefix pass reconstructs the result.','O(n + updates)','O(n)', '''def range_addition(n, updates):
    diff = [0] * (n + 1)
    for left, right, delta in updates:
        diff[left] += delta
        diff[right + 1] -= delta
    result, running = [], 0
    for i in range(n):
        running += diff[i]
        result.append(running)
    return result''', 'range_addition(5,[(1,3,2),(2,4,3),(0,2,-2)])==[-2,0,3,5,3]')

p=P('sort','Sorting & sweep lines','Sequences','≋','Choose an order that makes the next decision simple.',
'Use when order exposes duplicates, scheduling conflicts, or events along a timeline.',
'Previously processed events are final; the current state describes the sweep position.',
'Define ties carefully. For half-open meetings, process an end before a start at the same time.',
['sort','unsorted','sweep','events','timeline','meeting rooms','chronological'],['pointers','intervals','greedy'])
E(p,'Meeting Rooms II','Medium','Find rooms needed for half-open meetings [start,end), with start < end.','A sweep counts active meetings. Ends come before starts at equal times.','O(n log n)','O(n)', '''def meeting_rooms(intervals):
    events = []
    for start, end in intervals:
        events.extend([(start, 1), (end, -1)])
    active = best = 0
    for _, delta in sorted(events):
        active += delta
        best = max(best, active)
    return best''', 'meeting_rooms([(0,30),(5,10),(15,20)])==2 and meeting_rooms([(0,1),(1,2)])==1')
E(p,'Merge Sorted Arrays','Easy','Return one sorted list from two sorted lists.','The smallest unconsumed value must be at one of the two fronts.','O(n + m)','O(n + m)', '''def merge_sorted(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result + a[i:] + b[j:]''', 'merge_sorted([1,3,5],[2,4,6])==[1,2,3,4,5,6] and merge_sorted([],[1])==[1]')
E(p,'Sort Colors','Medium','Sort values 0, 1, and 2 in place without a comparison sort.','Maintain partitions for zeros, ones, unknown values, and twos.','O(n)','O(1)', '''def sort_colors(nums):
    low = mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums''', 'sort_colors([2,0,2,1,1,0])==[0,0,1,1,2,2]')

p=P('intervals','Intervals','Sequences','↔','Treat ranges as objects: merge, intersect, or schedule them.',
'Use for overlapping ranges, inserting an interval, or intersecting sorted disjoint interval lists.',
'The output intervals are sorted and fully resolved except possibly the final interval.',
'Decide whether endpoints are inclusive. Touching closed intervals merge; half-open scheduling intervals may not conflict.',
['interval','overlap','merge intervals','schedule','ranges','intersection'],['sort','greedy','heap'])
E(p,'Merge Intervals','Medium','Merge overlapping closed intervals.','Sorting by start lets you compare only against the last merged interval.','O(n log n)','O(n)', '''def merge_intervals(intervals):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result''', 'merge_intervals([[1,3],[2,6],[8,10],[15,18]])==[[1,6],[8,10],[15,18]]')
E(p,'Insert Interval','Medium','Insert a closed interval into sorted, disjoint closed intervals.','Copy the left region, merge overlaps, then copy the right region.','O(n)','O(n)', '''def insert_interval(intervals, new):
    result, i = [], 0
    start, end = new
    while i < len(intervals) and intervals[i][1] < start:
        result.append(list(intervals[i])); i += 1
    while i < len(intervals) and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    return result + [[start, end]] + [list(x) for x in intervals[i:]]''', 'insert_interval([[1,3],[6,9]],[2,5])==[[1,5],[6,9]]')
E(p,'Interval Intersections','Medium','Intersect two lists of sorted, disjoint closed intervals.','After checking overlap, advance whichever interval ends first.','O(n + m)','O(output)', '''def interval_intersections(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        start = max(a[i][0], b[j][0])
        end = min(a[i][1], b[j][1])
        if start <= end:
            result.append([start, end])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result''', 'interval_intersections([[0,2],[5,10]],[[1,5],[8,12]])==[[1,2],[5,5],[8,10]]')

p=P('binary','Binary search','Search','⌁','Find the boundary where a monotonic answer changes.',
'Use for sorted lookup or a feasibility predicate that goes from false to true (or the reverse).',
'The desired boundary always remains inside the maintained search interval.',
'Write the predicate first. Binary search on an answer requires monotonicity, not merely a minimum or maximum in the wording.',
['sorted','binary search','monotonic','minimum capacity','minimum speed','rotated','feasible'],['greedy','prefix','pointers'])
E(p,'Lower Bound','Easy','Return the first index with value at least target, or len(nums).','Use a half-open interval [left,right) and shrink toward the first true position.','O(log n)','O(1)', '''def lower_bound(nums, target):
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] >= target:
            right = mid
        else:
            left = mid + 1
    return left''', 'lower_bound([1,2,2,4],2)==1 and lower_bound([],2)==0 and lower_bound([1],2)==1')
E(p,'Search Rotated Array','Medium','Search a rotated sorted array of distinct values. Return index or −1.','At least one half is sorted; use its endpoints to decide whether to keep it.','O(log n)','O(1)', '''def search_rotated(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        elif nums[mid] < target <= nums[right]:
            left = mid + 1
        else:
            right = mid - 1
    return -1''', 'search_rotated([4,5,6,7,0,1,2],0)==4 and search_rotated([],1)==-1')
E(p,'Koko Eating Bananas','Medium','Positive piles; h is at least the number of piles. Find the minimum integer eating speed.','Hours needed never increase when speed increases. Search the first feasible speed.','O(n log max(piles))','O(1)', '''def min_eating_speed(piles, h):
    left, right = 1, max(piles)
    while left < right:
        speed = (left + right) // 2
        hours = sum((pile + speed - 1) // speed for pile in piles)
        if hours <= h:
            right = speed
        else:
            left = speed + 1
    return left''', 'min_eating_speed([3,6,7,11],8)==4 and min_eating_speed([1],1)==1')

p=P('fast','Fast & slow pointers','Structures','⇉','Different speeds reveal cycles and midpoints without extra storage.',
'Use when repeatedly following one successor: linked lists or an implicit functional graph.',
'Inside a cycle, the relative distance between fast and slow changes by one per step.',
'Check fast and fast.next before advancing. To find the cycle entrance, reset one pointer after the first collision.',
['cycle','middle','midpoint','happy number','linked list cycle'],['linked','pointers','graph'])
E(p,'Linked List Cycle','Easy','Determine whether a linked list contains a cycle. LeetCode supplies ListNode.','A two-step pointer catches a one-step pointer inside a cycle.','O(n)','O(1)', '''def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False''', 'has_cycle(cycle_list([3,2,0,-4],1)) and not has_cycle(make_list([1,2]))')
E(p,'Middle of Linked List','Easy','Return the middle node; for even length, return the second middle.','When fast reaches the end, slow has taken half as many steps.','O(n)','O(1)', '''def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow''', 'middle_node(make_list([1,2,3,4])).val==3 and middle_node(None) is None')
E(p,'Happy Number','Easy','For positive n, repeatedly sum squared digits; decide whether the process reaches 1.','This deterministic process either reaches 1 or enters a cycle.','O(log n) for the initial reduction; then bounded state','O(1)', '''def is_happy(n):
    def advance(x):
        total = 0
        while x:
            x, digit = divmod(x, 10)
            total += digit * digit
        return total
    slow, fast = n, advance(n)
    while fast != 1 and slow != fast:
        slow = advance(slow)
        fast = advance(advance(fast))
    return fast == 1''', 'is_happy(19) and not is_happy(2) and is_happy(1)')

p=P('linked','Linked-list rewiring','Structures','⛓','Save the next link before changing the current one.',
'Use for reversal, merging ordered nodes, and deleting nodes by position.',
'Processed nodes form the correct partial list; remaining nodes are still reachable.',
'Do not lose the rest of the list when overwriting next. Dummy heads simplify changes at the first node.',
['linked list','reverse list','node','next pointer','remove nth','rewire'],['fast','pointers','heap'])
E(p,'Reverse Linked List','Easy','Reverse a singly linked list. LeetCode supplies ListNode.','Preserve the next node, reverse the edge, then advance.','O(n)','O(1)', '''def reverse_list(head):
    previous = None
    while head:
        following = head.next
        head.next = previous
        previous, head = head, following
    return previous''', 'list_values(reverse_list(make_list([1,2,3])))==[3,2,1] and reverse_list(None) is None')
E(p,'Merge Two Sorted Lists','Easy','Merge two sorted linked lists by reusing their nodes. LeetCode supplies ListNode.','Attach the smaller front node and move only that list forward.','O(n + m)','O(1)', '''def merge_lists(a, b):
    dummy = tail = ListNode(0)
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next''', 'list_values(merge_lists(make_list([1,2,4]),make_list([1,3,4])))==[1,1,2,3,4,4]')
E(p,'Remove Nth Node From End','Medium','Remove the nth node from the end, where 1 ≤ n ≤ list length. LeetCode supplies ListNode.','Keep an n-node gap so slow stops at the predecessor of the node to remove.','O(n)','O(1)', '''def remove_nth(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next''', 'list_values(remove_nth(make_list([1,2,3,4,5]),2))==[1,2,3,5] and remove_nth(make_list([1]),1) is None')

p=P('stack','Stacks & monotonic stacks','Structures','▤','Keep unresolved work in order until a new element resolves it.',
'Use for nesting, expression parsing, and next greater or smaller values.',
'A monotonic stack contains unresolved indices in increasing or decreasing value order.',
'Store indices when distances matter. Decide whether equal values should remain or be popped.',
['parentheses','brackets','next greater','next smaller','daily temperatures','nested','histogram'],['deque','pointers','greedy'])
E(p,'Valid Parentheses','Easy','Validate a string containing only (), [], and {}.','Every closer must match the most recent unclosed opener.','O(n)','O(n)', '''def valid_parentheses(s):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}
    for c in s:
        if c in matching:
            if not stack or stack.pop() != matching[c]:
                return False
        else:
            stack.append(c)
    return not stack''', 'valid_parentheses("([]{})") and not valid_parentheses("([)]") and valid_parentheses("")')
E(p,'Daily Temperatures','Medium','Return days until a strictly warmer temperature, or zero.','A warmer day resolves all cooler days at the top of the stack.','O(n)','O(n)', '''def daily_temperatures(temperatures):
    answer = [0] * len(temperatures)
    stack = []
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            previous = stack.pop()
            answer[previous] = i - previous
        stack.append(i)
    return answer''', 'daily_temperatures([73,74,75,71,69,72,76,73])==[1,1,4,2,1,1,0,0]')
E(p,'Largest Rectangle in Histogram','Hard','For nonnegative bar heights, find the largest rectangle area.','A shorter bar closes rectangles whose heights are no longer extendable.','O(n)','O(n)', '''def largest_rectangle(heights):
    stack, best = [], 0
    for i, height in enumerate(heights + [0]):
        start = i
        while stack and stack[-1][1] > height:
            index, old_height = stack.pop()
            best = max(best, old_height * (i - index))
            start = index
        stack.append((start, height))
    return best''', 'largest_rectangle([2,1,5,6,2,3])==10 and largest_rectangle([])==0')

p=P('deque','Queues & monotonic deques','Structures','☷','Keep only useful candidates, in the order they can expire.',
'Use for sliding extrema or maintaining a FIFO stream with efficient candidate removal.',
'Candidate indices are in arrival order and their values are monotonic.',
'Expire old indices before reading the answer. A deque differs from a heap: it can discard dominated candidates permanently.',
['sliding window maximum','window maximum','window minimum','shortest subarray','deque','fifo'],['window','stack','bfs'])
E(p,'Sliding Window Maximum','Hard','Find the maximum in each length-k window; 1 ≤ k ≤ n.','Smaller older values can never win against a larger newer value.','O(n)','O(k)', '''from collections import deque

def window_max(nums, k):
    candidates, answer = deque(), []
    for i, x in enumerate(nums):
        while candidates and candidates[0] <= i - k:
            candidates.popleft()
        while candidates and nums[candidates[-1]] <= x:
            candidates.pop()
        candidates.append(i)
        if i >= k - 1:
            answer.append(nums[candidates[0]])
    return answer''', 'window_max([1,3,-1,-3,5,3,6,7],3)==[3,3,5,5,6,7]')
E(p,'First Negative in Each Window','Medium','Return the first negative value in each length-k window, or zero; 1 ≤ k ≤ n.','Keep the positions of negatives in FIFO order.','O(n)','O(k)', '''from collections import deque

def first_negatives(nums, k):
    negatives, answer = deque(), []
    for i, x in enumerate(nums):
        while negatives and negatives[0] <= i - k:
            negatives.popleft()
        if x < 0:
            negatives.append(i)
        if i >= k - 1:
            answer.append(nums[negatives[0]] if negatives else 0)
    return answer''', 'first_negatives([12,-1,-7,8,-15,30,16,28],3)==[-1,-1,-7,-15,-15,0]')
E(p,'Shortest Subarray With Sum at Least K','Hard','Find the shortest nonempty subarray with sum ≥ k, allowing negative values.','Use increasing prefix sums. A smaller, later prefix dominates a larger, earlier one.','O(n)','O(n)', '''from collections import deque

def shortest_subarray(nums, k):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    candidates, best = deque(), len(nums) + 1
    for i, total in enumerate(prefix):
        while candidates and total - prefix[candidates[0]] >= k:
            best = min(best, i - candidates.popleft())
        while candidates and prefix[candidates[-1]] >= total:
            candidates.pop()
        candidates.append(i)
    return -1 if best > len(nums) else best''', 'shortest_subarray([2,-1,2],3)==3 and shortest_subarray([1],2)==-1')

p=P('heap','Heaps & priority queues','Structures','♧','Repeatedly retrieve the best candidate without sorting everything again.',
'Use for top K, streaming rankings, or merging many ordered streams.',
'The heap root is the smallest retained item (or largest with an inverted key).',
'Heap iteration is not sorted. Add a tie-breaker if payload objects cannot be compared.',
['top k','kth','k largest','priority','merge k','stream','smallest repeatedly'],['sort','graph','linked'])
E(p,'Kth Largest Element','Medium','Return the kth largest array value, counting duplicates; 1 ≤ k ≤ n.','A size-k min-heap retains the k largest values.','O(n log k)','O(k)', '''import heapq

def kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]''', 'kth_largest([3,2,1,5,6,4],2)==5 and kth_largest([2,2],2)==2')
E(p,'Merge K Sorted Streams','Medium','Merge k sorted arrays into one ordered array.','Only the next unconsumed item from each stream can be the global minimum.','O(N log k), N total items','O(k) + output', '''import heapq

def merge_streams(arrays):
    heap = [(a[0], i, 0) for i, a in enumerate(arrays) if a]
    heapq.heapify(heap)
    result = []
    while heap:
        value, source, position = heapq.heappop(heap)
        result.append(value)
        position += 1
        if position < len(arrays[source]):
            heapq.heappush(heap, (arrays[source][position], source, position))
    return result''', 'merge_streams([[1,4,5],[1,3,4],[2,6]])==[1,1,2,3,4,4,5,6] and merge_streams([[]])==[]')
E(p,'Last Stone Weight','Easy','Repeatedly smash the two heaviest positive stones. Return the remaining weight or zero.','Negated weights make Python’s min-heap act as a max-heap.','O(n log n)','O(n)', '''import heapq

def last_stone(stones):
    heap = [-x for x in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if first != second:
            heapq.heappush(heap, -(first - second))
    return -heap[0] if heap else 0''', 'last_stone([2,7,4,1,8,1])==1 and last_stone([2,2])==0')

p=P('dfs','DFS & tree recursion','Traversal','⑂','Explore one branch fully, then combine or return its result.',
'Use for tree properties, connected regions, reachability, and recursive structural computations.',
'Each call returns a precisely defined result for its subtree or reachable region.',
'Graphs need a visited set. Deep Python recursion can exceed the recursion limit; an iterative stack may be safer.',
['tree','subtree','depth','islands','connected component','traverse','reachability','dfs'],['bfs','backtrack','dp'])
E(p,'Maximum Tree Depth','Easy','Return the maximum depth of a binary tree. LeetCode supplies TreeNode.','A node’s depth is one plus the larger child depth.','O(n)','O(height)', '''def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))''', 'max_depth(TreeNode(1,TreeNode(2,TreeNode(3)),TreeNode(4)))==3 and max_depth(None)==0')
E(p,'Number of Islands','Medium','Count four-directional connected regions of "1" in a grid. This solution marks the grid in place.','Each new unvisited land cell starts exactly one flood fill.','O(rows × columns)','O(rows × columns)', '''def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols, answer = len(grid), len(grid[0]), 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '1':
                continue
            answer += 1
            grid[r][c] = '0'
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                        grid[nx][ny] = '0'
                        stack.append((nx, ny))
    return answer''', 'num_islands([list("110"),list("010"),list("001")])==2 and num_islands([])==0')
E(p,'Validate Binary Search Tree','Medium','Check strict BST ordering in a binary tree. LeetCode supplies TreeNode.','Carry bounds from all ancestors, not just the parent.','O(n)','O(height)', '''def valid_bst(root):
    def visit(node, low, high):
        if node is None:
            return True
        if not low < node.val < high:
            return False
        return visit(node.left, low, node.val) and visit(node.right, node.val, high)
    return visit(root, float('-inf'), float('inf'))''', 'valid_bst(TreeNode(2,TreeNode(1),TreeNode(3))) and not valid_bst(TreeNode(2,TreeNode(2)))')

p=P('bfs','Breadth-first search','Traversal','◎','Explore in layers. First arrival gives the shortest unweighted distance.',
'Use for minimum moves with equal-cost transitions, tree levels, and spreading processes.',
'Queue entries are processed in nondecreasing distance from the starting frontier.',
'Mark visited when enqueuing to avoid duplicates. Weighted edges require another algorithm unless all costs are equal.',
['unweighted','minimum moves','level order','nearest','rotting','breadth','equal cost','shortest path'],['dfs','graph','deque'])
E(p,'Binary Tree Level Order','Medium','Return node values grouped by depth. LeetCode supplies TreeNode.','Snapshot the queue length to process exactly one level.','O(n)','O(maximum width)', '''from collections import deque

def level_order(root):
    if root is None:
        return []
    queue, answer = deque([root]), []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        answer.append(level)
    return answer''', 'level_order(TreeNode(1,TreeNode(2),TreeNode(3)))==[[1],[2,3]] and level_order(None)==[]')
E(p,'Shortest Unweighted Path','Medium','Find the number of edges from start to goal in an adjacency-list graph, or −1.','Enqueue unseen neighbors with distance +1.','O(V + E)','O(V)', '''from collections import deque

def shortest_path(graph, start, goal):
    queue, seen = deque([(start, 0)]), {start}
    while queue:
        node, distance = queue.popleft()
        if node == goal:
            return distance
        for neighbor in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, distance + 1))
    return -1''', 'shortest_path({0:[1,2],1:[3],2:[3],3:[]},0,3)==2 and shortest_path({},0,1)==-1')
E(p,'Rotting Oranges','Medium','Grid values: 0 empty, 1 fresh, 2 rotten. Return minutes until all rot, or −1. Mutates the grid.','Start BFS from every rotten orange at once.','O(rows × columns)','O(rows × columns)', '''from collections import deque

def rotting_oranges(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    queue, fresh, minutes = deque(), 0, 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2: queue.append((r,c,0))
            if grid[r][c] == 1: fresh += 1
    while queue:
        r, c, minutes = queue.popleft()
        for nr, nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr,nc,minutes+1))
    return minutes if fresh == 0 else -1''', 'rotting_oranges([[2,1,1],[1,1,0],[0,1,1]])==4 and rotting_oranges([[1]])==-1 and rotting_oranges([])==0')

p=P('backtrack','Backtracking','Search','⋈','Choose, explore, undo. Search a tree of valid possibilities.',
'Use when the output asks for all combinations, permutations, arrangements, or constrained paths.',
'The current path is a valid partial candidate; recursive calls restore it before returning.',
'Copy paths when storing answers. Undo every state change. Distinguish reusing a value from reusing a position.',
['all combinations','permutations','subsets','generate','all possible','word search','arrangements'],['dfs','dp','bits'])
E(p,'Subsets','Medium','Return all subsets of distinct numbers.','Each position has two choices: include it or skip it.','O(n × 2ⁿ)','O(n) + output', '''def subsets(nums):
    result, path = [], []
    def visit(i):
        if i == len(nums):
            result.append(path.copy())
            return
        visit(i + 1)
        path.append(nums[i])
        visit(i + 1)
        path.pop()
    visit(0)
    return result''', 'len(subsets([1,2,3]))==8 and subsets([])==[[]]')
E(p,'Permutations','Medium','Return all permutations of distinct values.','Track used positions so each appears once in a candidate.','O(n × n!)','O(n) + output', '''def permutations(nums):
    result, path, used = [], [], set()
    def visit():
        if len(path) == len(nums):
            result.append(path.copy())
            return
        for i, x in enumerate(nums):
            if i not in used:
                used.add(i); path.append(x)
                visit()
                path.pop(); used.remove(i)
    visit()
    return result''', 'sorted(permutations([1,2]))==[[1,2],[2,1]] and permutations([])==[[]]')
E(p,'Combination Sum','Medium','Given distinct positive candidates, return combinations summing to target. Reuse is allowed.','Keep a start index to avoid permutations of the same combination; positivity enables pruning.','Exponential search + output','O(target / min(candidates)) + output', '''def combination_sum(candidates, target):
    values = sorted(candidates)
    result, path = [], []
    def visit(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for i in range(start, len(values)):
            if values[i] > remaining:
                break
            path.append(values[i])
            visit(i, remaining - values[i])
            path.pop()
    visit(0, target)
    return result''', 'combination_sum([2,3,6,7],7)==[[2,2,3],[7]] and combination_sum([2],1)==[]')

p=P('greedy','Greedy algorithms','Optimization','↗','Choose locally, but justify why that choice preserves an optimum.',
'Use when an exchange argument, dominance argument, or maintained reach proves the local decision safe.',
'The current choice can be extended to an optimal solution, or dominates discarded alternatives.',
'A plausible local rule is not a proof. Greedy fails for arbitrary coin systems and many scheduling variants.',
['jump game','maximum reach','non-overlapping','earliest finish','gas station','greedy'],['sort','intervals','dp'])
E(p,'Jump Game','Medium','Nonnegative jumps; determine whether the last index is reachable.','Track the furthest reachable index; encountering a gap proves failure.','O(n)','O(1)', '''def can_jump(nums):
    reach = 0
    for i, jump in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + jump)
    return True''', 'can_jump([2,3,1,1,4]) and not can_jump([3,2,1,0,4])')
E(p,'Non-overlapping Intervals','Medium','Find the minimum removals so half-open intervals do not overlap.','Keeping the earliest finish leaves the most room for future intervals.','O(n log n)','O(n)', '''def erase_overlap(intervals):
    end, kept = float('-inf'), 0
    for start, finish in sorted(intervals, key=lambda x: x[1]):
        if start >= end:
            kept += 1
            end = finish
    return len(intervals) - kept''', 'erase_overlap([[1,2],[2,3],[3,4],[1,3]])==1 and erase_overlap([])==0')
E(p,'Gas Station','Medium','Equal nonempty gas/cost arrays. Find a starting station to complete the circuit, or −1.','If a segment fails, none of its earlier starts can succeed; restart after it.','O(n)','O(1)', '''def gas_station(gas, cost):
    total = tank = start = 0
    for i, (fuel, expense) in enumerate(zip(gas, cost)):
        total += fuel - expense
        tank += fuel - expense
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1''', 'gas_station([1,2,3,4,5],[3,4,5,1,2])==3 and gas_station([2,3,4],[3,4,3])==-1')

p=P('dp','Dynamic programming','Optimization','▦','Name the state, define the recurrence, and reuse subproblem answers.',
'Use for repeated subproblems in counting or optimization where state captures all relevant history.',
'Each stored entry has one precise meaning and depends only on already computed states.',
'The state and transition are problem-specific. Loop order distinguishes 0/1 choices from unlimited reuse. Do not assume every maximum needs DP.',
['ways','number of ways','subsequence','knapsack','coin change','house robber','overlapping subproblems','optimal'],['backtrack','greedy','dfs'])
E(p,'Climbing Stairs','Easy','Count ways to climb n ≥ 0 steps using jumps of one or two.','Ways to reach i equals ways to reach i−1 plus ways to reach i−2.','O(n)','O(1)', '''def climb_stairs(n):
    previous, current = 1, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous''', 'climb_stairs(3)==3 and climb_stairs(0)==1 and climb_stairs(1)==1')
E(p,'Coin Change','Medium','Positive coin denominations; find the fewest coins making a nonnegative amount, or −1. Unlimited reuse.','dp[value] is the best count among possible final coins.','O(amount × coin count)','O(amount)', '''def coin_change(coins, amount):
    dp = [0] + [amount + 1] * amount
    for value in range(1, amount + 1):
        for coin in coins:
            if coin <= value:
                dp[value] = min(dp[value], dp[value - coin] + 1)
    return -1 if dp[amount] > amount else dp[amount]''', 'coin_change([1,2,5],11)==3 and coin_change([2],3)==-1 and coin_change([2],0)==0')
E(p,'Longest Common Subsequence','Medium','Find the longest subsequence shared by two strings. Characters need not be contiguous.','Matching characters extend a diagonal answer; otherwise discard one end and take the better choice.','O(nm)','O(m)', '''def longest_common_subsequence(a, b):
    previous = [0] * (len(b) + 1)
    for x in a:
        current = [0] * (len(b) + 1)
        for j, y in enumerate(b, 1):
            if x == y:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]''', 'longest_common_subsequence("abcde","ace")==3 and longest_common_subsequence("","a")==0')

p=P('graph','Graph algorithms','Traversal','⌘','Model relationships, then choose the algorithm for their structure and costs.',
'Use topological sort for dependencies, union-find for connectivity, and Dijkstra for nonnegative weighted paths.',
'Each algorithm has its own invariant: zero indegree is ready; representatives identify components; settled Dijkstra distances are optimal.',
'Dijkstra does not handle negative weights. Topological sorting requires a directed acyclic graph. Union-find does not directly support arbitrary deletions.',
['prerequisite','dependencies','weighted','network','union find','connectivity','course schedule','dijkstra','graph'],['bfs','dfs','heap'])
E(p,'Course Schedule','Medium','Given prerequisites (course, prerequisite), decide whether all n courses can be completed.','Remove zero-indegree vertices; a remaining directed cycle prevents completion.','O(V + E)','O(V + E)', '''from collections import deque

def can_finish(n, prerequisites):
    edges = [[] for _ in range(n)]
    indegree = [0] * n
    for course, prerequisite in prerequisites:
        edges[prerequisite].append(course)
        indegree[course] += 1
    queue = deque(i for i in range(n) if indegree[i] == 0)
    completed = 0
    while queue:
        node = queue.popleft()
        completed += 1
        for neighbor in edges[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0: queue.append(neighbor)
    return completed == n''', 'can_finish(2,[(1,0)]) and not can_finish(2,[(1,0),(0,1)])')
E(p,'Connected Components','Medium','Count components in an undirected graph with nodes 0..n−1.','Union representatives; each successful union decreases the component count by one.','O((V + E) α(V))','O(V)', '''def count_components(n, edges):
    parent, size = list(range(n)), [1] * n
    def find(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    components = n
    for a, b in edges:
        a, b = find(a), find(b)
        if a == b: continue
        if size[a] < size[b]: a, b = b, a
        parent[b] = a
        size[a] += size[b]
        components -= 1
    return components''', 'count_components(5,[(0,1),(1,2),(3,4)])==2 and count_components(0,[])==0')
E(p,'Dijkstra Shortest Distances','Medium','Return shortest distances from start in a weighted adjacency list. Every weight must be nonnegative.','Pop the lowest tentative distance, skipping stale entries.','O((V + E) log(V + E))','O(V + E)', '''import heapq

def dijkstra(graph, start):
    distance, heap = {start: 0}, [(0, start)]
    while heap:
        cost, node = heapq.heappop(heap)
        if cost != distance[node]: continue
        for neighbor, weight in graph.get(node, []):
            candidate = cost + weight
            if candidate < distance.get(neighbor, float('inf')):
                distance[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distance''', 'dijkstra({0:[(1,4),(2,1)],2:[(1,2)],1:[]},0)=={0:0,1:3,2:1}')

p=P('trie','Tries & string matching','Structures','Ψ','Share prefixes or reuse partial matches instead of restarting every search.',
'Use for dictionaries, prefix lookup, word segmentation, and repeated string matching.',
'A trie path represents a prefix. A matching algorithm retains the longest reusable matched prefix.',
'A trie can use substantial memory. A terminal marker distinguishes a whole word from a prefix.',
['prefix search','dictionary','autocomplete','trie','string matching','pattern matching','word break'],['hash','dp','dfs'])
E(p,'Implement a Trie','Medium','Support word insertion, exact search, and prefix search.','Nested dictionaries share common prefix paths; a unique marker records complete words.','O(word length) per operation','O(total inserted characters)', '''class Trie:
    def __init__(self):
        self.root = {}
        self.end = object()
    def insert(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node[self.end] = True
    def _walk(self, text):
        node = self.root
        for c in text:
            if c not in node: return None
            node = node[c]
        return node
    def search(self, word):
        node = self._walk(word)
        return node is not None and self.end in node
    def starts_with(self, prefix):
        return self._walk(prefix) is not None''', 'check_trie(Trie)')
E(p,'Find First Occurrence (KMP)','Medium','Return the first index of a pattern in text, or −1. Empty pattern returns zero.','The prefix table lets a failed match reuse a matching suffix.','O(n + m)','O(m)', '''def kmp_search(text, pattern):
    if not pattern: return 0
    lps, j = [0] * len(pattern), 0
    for i in range(1, len(pattern)):
        while j and pattern[i] != pattern[j]: j = lps[j - 1]
        if pattern[i] == pattern[j]: j += 1
        lps[i] = j
    j = 0
    for i, c in enumerate(text):
        while j and c != pattern[j]: j = lps[j - 1]
        if c == pattern[j]: j += 1
        if j == len(pattern): return i - j + 1
    return -1''', 'kmp_search("mississippi","issip")==4 and kmp_search("abc","d")==-1 and kmp_search("","")==0')
E(p,'Word Break With a Trie','Medium','Determine if a string can be segmented into words from a dictionary of nonempty strings.','A trie explores possible next words; DP remembers reachable boundaries.','O(dictionary characters + n²)','O(dictionary characters + n)', '''def word_break(s, words):
    root = {}
    for word in words:
        node = root
        for c in word: node = node.setdefault(c, {})
        node[None] = True
    reachable = [True] + [False] * len(s)
    for i in range(len(s)):
        if not reachable[i]: continue
        node = root
        for j in range(i, len(s)):
            if s[j] not in node: break
            node = node[s[j]]
            if None in node: reachable[j + 1] = True
    return reachable[-1]''', 'word_break("leetcode",["leet","code"]) and not word_break("catsandog",["cats","dog","sand","and","cat"])')

p=P('bits','Bits & mathematics','Foundations','⊕','Exploit algebra, integer structure, or compact representations of sets.',
'Use for XOR cancellation, bitmask states, divisibility, and number-theoretic properties.',
'Track the exact algebraic property: equal values cancel in XOR; Euclid preserves the gcd.',
'Check assumptions about repetition counts and integer sign. Fixed-width tricks need care with Python’s unbounded signed integers.',
['xor','bit','single number','power of two','divisible','gcd','bitmask','binary representation'],['backtrack','dp','hash'])
E(p,'Single Number','Easy','Every integer appears twice except one. Find that one.','XOR is associative; x XOR x = 0 and x XOR 0 = x.','O(n)','O(1)', '''def single_number(nums):
    answer = 0
    for x in nums:
        answer ^= x
    return answer''', 'single_number([4,1,2,1,2])==4 and single_number([-1,2,2])==-1')
E(p,'Counting Bits','Easy','For every integer from 0 to n ≥ 0, return its set-bit count.','Right shift removes the last bit; add that bit to the smaller number’s answer.','O(n)','O(n)', '''def counting_bits(n):
    counts = [0] * (n + 1)
    for i in range(1, n + 1):
        counts[i] = counts[i >> 1] + (i & 1)
    return counts''', 'counting_bits(5)==[0,1,1,2,1,2] and counting_bits(0)==[0]')
E(p,'Greatest Common Divisor','Easy','Compute the nonnegative gcd of two integers. gcd(0,0) is defined here as zero.','gcd(a,b) equals gcd(b,a mod b).','O(log min(|a|,|b|)) for nonzero inputs','O(1)', '''def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a''', 'gcd(48,18)==6 and gcd(-12,8)==4 and gcd(0,0)==0')

from extra_examples import expand
expand(patterns, E, P)
assert len(patterns) == 21 and sum(len(p['examples']) for p in patterns) == 109
from optimise_examples import optimise
optimise(patterns)
node_samples = {
    'Linked List Cycle': ('3 → 2 → 0 → -4, with the tail pointing to node 2', 'True'),
    'Middle of Linked List': ('1 → 2 → 3 → 4', 'Node with value 3'),
    'Reverse Linked List': ('1 → 2 → 3', '3 → 2 → 1'),
    'Merge Two Sorted Lists': ('1 → 2 → 4 and 1 → 3 → 4', '1 → 1 → 2 → 3 → 4 → 4'),
    'Remove Nth Node From End': ('1 → 2 → 3 → 4 → 5; n = 2', '1 → 2 → 3 → 5'),
    'Maximum Tree Depth': ('Root 1; left child 2 with left child 3; right child 4', '3'),
    'Validate Binary Search Tree': ('Root 2; left child 1; right child 3', 'True'),
    'Binary Tree Level Order': ('Root 1; left child 2; right child 3', '[[1], [2, 3]]'),
    'Implement a Trie': ('insert("apple"), then search("apple")', 'True'),
    'Min Stack': ('push(-2), push(0), push(-3); get_min(), pop(), top(), get_min()', '[-3, -3, 0, -2]'),
    'Moving Average From a Stream': ('size=3; next(1), next(10), next(3), next(5)', '[1.0, 5.5, 4.666666666666667, 6.0]'),
    'Lowest Common Ancestor': ('Root 1; left child 2 with children 4 and 5; right child 3. Targets: nodes 4 and 5.', 'Node 2'),
}
for p in patterns:
    for e in p['examples']:
        if e['title'] in node_samples:
            e['sampleInput'], e['sampleOutput'] = node_samples[e['title']]
            continue
        node = ast.parse(e['check'], mode='eval').body
        if isinstance(node, ast.BoolOp): node = node.values[0]
        if isinstance(node, ast.Compare):
            e['sampleInput'] = ast.unparse(node.left)
            e['sampleOutput'] = ast.unparse(node.comparators[0])
        else:
            e['sampleInput'] = ast.unparse(node)
            e['sampleOutput'] = 'True'
from enrich_content import enrich
enrich(patterns)
from pattern_teaching import teach
teach(patterns)
from complexity_teaching import explain_costs
explain_costs(patterns)
Path('src/data/patterns.json').write_text(json.dumps(patterns, ensure_ascii=False, indent=2))

print(f'Generated {len(patterns)} methods and {sum(len(p["examples"]) for p in patterns)} examples')
