"""Generate the "Patterns Behind the Problem" challenge pack and verify it.

Expected outputs are computed by the optimal reference and cross-checked against an
independent brute-force oracle before anything is written. Run: python3 challenge_content.py
"""
import json
import itertools
import time
from pathlib import Path

ECHO_BRUTE = '''def solution(message: str) -> int:
    length = len(message)
    # Try every signature length from the longest legal one downwards.
    # A signature may use at most half the message, otherwise the two copies overlap.
    for signature_length in range(length // 2, 0, -1):
        opening = message[:signature_length]
        closing = message[length - signature_length:]
        if opening == closing:
            return signature_length
    return 0'''

ECHO_OPTIMAL = '''def solution(message: str) -> int:
    length = len(message)
    # longest_border[i] = length of the longest proper prefix of message[:i + 1]
    # that is also a suffix of message[:i + 1]  (the KMP "LPS" array).
    longest_border = [0] * length
    matched = 0
    for position in range(1, length):
        # On a mismatch, fall back to the next shorter border instead of restarting.
        while matched > 0 and message[position] != message[matched]:
            matched = longest_border[matched - 1]
        if message[position] == message[matched]:
            matched += 1
        longest_border[position] = matched

    if length == 0:
        return 0
    # The longest border of the whole message may overlap itself.
    # Every shorter border is reachable by following the fallback links.
    candidate = longest_border[length - 1]
    while candidate > length // 2:
        candidate = longest_border[candidate - 1]
    return candidate'''

MIRROR_BRUTE = '''def is_palindrome(number):
    digits = str(number)
    return digits == digits[::-1]


def solution(code: int) -> int:
    # Walk outwards one step at a time. Checking the smaller side first
    # makes ties resolve to the smaller palindrome automatically.
    distance = 1
    while True:
        lower = code - distance
        if lower >= 0 and is_palindrome(lower):
            return lower
        upper = code + distance
        if is_palindrome(upper):
            return upper
        distance += 1'''

MIRROR_OPTIMAL = '''def mirror(prefix_text, total_length):
    # Build a palindrome of total_length digits whose left half is prefix_text.
    if total_length % 2 == 0:
        right_half = prefix_text[::-1]
    else:
        right_half = prefix_text[:-1][::-1]
    return int(prefix_text + right_half)


def solution(code: int) -> int:
    digits = str(code)
    length = len(digits)
    candidates = set()

    # Digit-boundary candidates: 99...9 (one digit shorter) and 10...01 (one digit longer).
    candidates.add(10 ** (length - 1) - 1)
    candidates.add(10 ** length + 1)

    # The left half, including the middle digit when the length is odd.
    prefix = int(digits[:(length + 1) // 2])
    for nearby_prefix in (prefix - 1, prefix, prefix + 1):
        prefix_text = str(nearby_prefix)
        # Changing the prefix can add or remove a digit (e.g. 10 -> 9, 99 -> 100).
        # Those cases are already covered by the boundary candidates above.
        if len(prefix_text) == (length + 1) // 2 and nearby_prefix > 0:
            candidates.add(mirror(prefix_text, length))

    candidates.discard(code)

    best = None
    for candidate in candidates:
        if candidate < 0:
            continue
        if best is None:
            best = candidate
            continue
        candidate_gap = abs(candidate - code)
        best_gap = abs(best - code)
        # Closer wins; on a tie the smaller palindrome wins.
        if candidate_gap < best_gap or (candidate_gap == best_gap and candidate < best):
            best = candidate
    return best'''


def load(source):
    scope = {}
    exec(source, scope)
    return scope['solution']


echo_brute, echo_fast = load(ECHO_BRUTE), load(ECHO_OPTIMAL)
mirror_brute, mirror_fast = load(MIRROR_BRUTE), load(MIRROR_OPTIMAL)

# ---- Independent oracles (deliberately different code from the references) ----
def echo_oracle(message):
    return max([k for k in range(len(message) + 1) if 2 * k <= len(message) and message[:k] == message[len(message) - k:]])

def mirror_oracle(code):
    best = None
    for value in range(0, 2 * code + 12):
        if value != code and str(value) == str(value)[::-1]:
            key = (abs(value - code), value)
            if best is None or key < best:
                best = key
    return best[1]

# Exhaustive small-input checks.
for length in range(1, 11):
    for letters in itertools.product('ab', repeat=length):
        message = ''.join(letters)
        expected = echo_oracle(message)
        assert echo_fast(message) == expected == echo_brute(message), message
for length in range(1, 7):
    for letters in itertools.product('abc', repeat=length):
        message = ''.join(letters)
        assert echo_fast(message) == echo_oracle(message), message
for code in range(1, 20001):
    expected = mirror_oracle(code)
    assert mirror_fast(code) == expected == mirror_brute(code), code

# The examples in the brief, with 808 -> 818 (818 is 10 away, 797 is 11 away).
assert [echo_fast(m) for m in ['codebreakcode', 'playgroundplay', 'aaaaa', 'computer']] == [4, 4, 2, 0]
assert [mirror_fast(c) for c in [123, 808, 1000, 99, 121]] == [121, 818, 999, 101, 111]

# Performance: optimal versions on maximum inputs.
big_cases = {'"a" * 100000': 'a' * 100000, '"ab" * 50000': 'ab' * 50000,
             '"a" * 49999 + "b" + "a" * 50000': 'a' * 49999 + 'b' + 'a' * 50000,
             '("abcab" * 20000)': 'abcab' * 20000}
start = time.perf_counter()
for value in big_cases.values():
    echo_fast(value)
echo_seconds = time.perf_counter() - start
assert echo_seconds < 2, echo_seconds
start = time.perf_counter()
for code in [10 ** 18, 10 ** 18 - 1, 999999999999999999, 123456789987654321, 807045053224792883]:
    mirror_fast(code)
assert time.perf_counter() - start < 0.1

def case(label, call, value, visible=False, why=''):
    return dict(label=label, call=call, expected=value, visible=visible, why=why)

echo_cases = [
    case('Example 1', 'solution("codebreakcode")', 4, True, 'Opens and closes with "code".'),
    case('Example 2', 'solution("playgroundplay")', 4, True, 'Opens and closes with "play".'),
    case('Example 3', 'solution("aaaaa")', 2, True, 'Lengths 3 and 4 match but overlap.'),
    case('Example 4', 'solution("computer")', 0, True, 'No prefix matches a suffix.'),
]
for label, text, why in [
    ('Single character', 'z', 'One character cannot form two separate signatures.'),
    ('Two equal characters', 'aa', 'Each half is a signature of length 1.'),
    ('Alternating', 'abababab', '"abab" fits exactly in each half.'),
    ('Alternating, odd', 'ababababa', 'Border 7 overlaps; fallback gives 3.'),
    ('Overlapping border', 'abaabaaba', 'Border 6 overlaps; next border is 3.'),
    ('Several valid lengths', 'abcxabcyabcxabc', 'Borders 7 and 3; 7 fits in half.'),
    ('Case-sensitive', 'Abca', 'A and a are different characters.'),
    ('No overlap allowed, even', 'aaaaaa', 'Exactly half: 3.'),
    ('Near-periodic', 'aabaaabaa', 'Border 5 overlaps; next is 2.'),
]:
    echo_cases.append(case(label, f'solution({text!r})'.replace("'", '"'), echo_fast(text), False, why))
for call, value in big_cases.items():
    echo_cases.append(case('Maximum-length input', f'solution({call})', echo_fast(value), False, 'Brute force slows down here; KMP stays linear.'))

mirror_cases = [
    case('Example 1', 'solution(123)', 121, True, '121 is 2 away.'),
    case('Example 2', 'solution(808)', 818, True, '818 is 10 away, 797 is 11 away.'),
    case('Example 3', 'solution(1000)', 999, True, 'The answer has fewer digits.'),
    case('Example 4', 'solution(99)', 101, True, '99 itself is not allowed.'),
    case('Example 5', 'solution(121)', 111, True, '111 and 131 tie; the smaller wins.'),
]
for label, code, why in [
    ('Single digit', 1, '0 and 2 tie at distance 1; 0 is smaller.'),
    ('Single digit', 5, '4 and 6 tie; 4 wins.'),
    ('Ten', 10, '9 and 11 both 1 away; 9 wins.'),
    ('Power of ten', 100, '99 is 1 away.'),
    ('All nines', 999, '1001 is 2 away; 989 is 10 away.'),
    ('More digits', 9999, '10001 is 2 away.'),
    ('Fewer digits', 10001, '9999 is 2 away, 10101 is 100 away.'),
    ('Already palindrome, even', 1221, '1111 and 1331 tie; smaller wins.'),
    ('Middle change, odd', 12321, 'Change only the middle digit.'),
    ('Prefix carries', 1991, 'Prefix 19 -> 20 gives 2002.'),
    ('Prefix borrows', 2002, 'Prefix 20 -> 19 gives 1991.'),
    ('Eleven', 11, '9 is 2 away; 22 is 11 away.'),
    ('Very large', 807045053224792883, 'Only five candidates are ever needed.'),
    ('Very large palindrome', 123456789987654321, 'Must not return itself.'),
    ('Upper bound', 10 ** 18, '999...9 (18 nines) is 1 away.'),
]:
    mirror_cases.append(case(label, f'solution({code})', mirror_fast(code), False, why))

for item in echo_cases:
    assert eval(item['call'], {'solution': echo_fast}) == item['expected']
for item in mirror_cases:
    assert eval(item['call'], {'solution': mirror_fast}) == item['expected']

challenges = [
    dict(
        id='echo-protocol', number=1, title='The Echo Protocol', category='Strings / Pattern Matching',
        difficulty='Medium', time='O(n)', space='O(n)', pattern='KMP prefix function (LPS array)', patternId='strings',
        signature='def solution(message: str) -> int:',
        story=['You are building a communication protocol for a fleet of autonomous exploration robots.',
               'To confirm a transmission arrived whole, the protocol looks for the same sequence of characters at the very start and the very end of the message: an opening signature and a closing signature.',
               'The two signatures must sit in completely separate positions. They cannot share a single character. Find the longest signature possible.'],
        statement='Given a string message, return the largest integer k such that the first k characters equal the last k characters and the two sequences do not overlap (2k ≤ length). Return 0 if no non-empty signature exists.',
        examples=[dict(input='message = "codebreakcode"', output='4', why='Starts with "code" and ends with "code". They do not overlap.'),
                  dict(input='message = "playgroundplay"', output='4', why='The signatures are both "play".'),
                  dict(input='message = "aaaaa"', output='2', why='Longer matches exist (3 and 4) but they overlap. "aa" … "aa" is the longest separate pair.'),
                  dict(input='message = "computer"', output='0', why='No non-empty prefix matches a suffix.')],
        constraints=['1 ≤ message.length ≤ 100,000', 'Lowercase English letters in the hidden tests; matching is case-sensitive.', 'The two signatures must not overlap.'],
        hints=[dict(title='Understand the pattern', text='You are looking for a piece of text that is both a prefix and a suffix of the same string. Ignore the overlap rule for a moment: what is the longest such piece? Then ask what happens to the answer when that piece is too long.'),
               dict(title='Brute-force reasoning', text='Try every length k from len(message) // 2 down to 1 and compare message[:k] with message[-k:]. The first match is the answer. It is correct, but each comparison costs up to k characters, so a string like "aaaa…ab" makes it O(n²).'),
               dict(title='Optimisation', text='Build the KMP "longest prefix that is also a suffix" (LPS) array in one pass. Its last entry is the longest border of the whole message. If that border is longer than half the message, lps[border - 1] gives the next shorter border. Keep following those links until the border fits.')],
        reasoning=[dict(title='Explain it simply', text='"I need the longest chunk that the message both starts and ends with, as long as the two copies do not touch."'),
                   dict(title='First idea', text='Check every possible length from half the message downwards and compare the two slices directly. Stop at the first match.'),
                   dict(title='Why brute force is slow', text='Each check re-reads up to n/2 characters from scratch and throws away what it learned. For long, repetitive messages that is about n²/4 character comparisons, which is billions at n = 100,000.'),
                   dict(title='Spot the pattern', text='"Same text at the start and the end" is the definition of a border, and borders are exactly what the KMP prefix function computes. Whenever a problem talks about prefixes matching suffixes, repeated periods, or matching a pattern without restarting, think KMP.'),
                   dict(title='Say the optimisation out loud', text='"The LPS array tells me, for every position, how much of the start I have already matched. On a mismatch I fall back to a shorter match I already know is valid, so I never re-compare characters from scratch. The pointer only moves forward n times and falls back at most that many times, so the whole build is linear. Then the borders of the full string form a chain: lps of the end, then lps of that, and so on. I walk the chain until the border fits in half the message."'),
                   dict(title='Complexity', text='Time O(n): building the array is amortised linear and the fallback chain is at most n steps. Space O(n) for the LPS array.')],
        whyFast='KMP avoids restarting: when the next character does not extend the current match, the LPS array already knows the next-longest prefix that still matches, so the scan continues from there instead of going back to the start. Every border of the whole message appears in the fallback chain from its last entry, so the longest non-overlapping one is found by following links, never by re-comparing text.',
        brute=ECHO_BRUTE, optimal=ECHO_OPTIMAL, bruteComplexity='O(n²) time worst case, O(n) space for slices',
        tests=echo_cases),
    dict(
        id='mirror-vault', number=2, title='The Mirror Vault', category='Maths / Strings / Candidate generation',
        difficulty='Medium', time='O(d)', space='O(d)', pattern='Prefix mirroring with a small candidate set', patternId='greedy',
        signature='def solution(code: int) -> int:',
        story=['A high-security digital vault only accepts numeric access codes that read the same left to right and right to left.',
               'When a code has to be replaced, the vault picks the numerically closest mirrored code. For security the replacement must differ from the old code, even if the old code is already mirrored.',
               'If two replacements are equally close, the vault takes the smaller one. Write the replacement-code generator.'],
        statement='Given a positive integer code, return the non-negative integer palindrome (no leading zeros, except 0 itself) that is different from code and has the smallest absolute difference from it. If two palindromes are equally close, return the smaller.',
        examples=[dict(input='code = 123', output='121', why='121 is a palindrome only 2 away.'),
                  dict(input='code = 808', output='818', why='808 cannot be reused. 797 is 11 away and 818 is 10 away, so 818 wins.'),
                  dict(input='code = 1000', output='999', why='The closest palindrome has fewer digits.'),
                  dict(input='code = 99', output='101', why='99 is already a palindrome but cannot be returned.'),
                  dict(input='code = 121', output='111', why='111 and 131 are both 10 away; the smaller wins.')],
        constraints=['1 ≤ code ≤ 10^18', 'Return an int.', 'No leading zeros. 0 is a valid replacement.'],
        hints=[dict(title='Understand the pattern', text='A palindrome is completely decided by its left half. Look at how close 12921 is to 12345 compared with 99999. Which digits of a number matter most when you are trying to stay close to it?'),
               dict(title='Brute-force reasoning', text='Step outwards: check code - 1, code + 1, code - 2, code + 2 … and return the first palindrome. Checking the lower side first handles ties. It is correct, but near 10^18 the gap between palindromes can be around 10^9, far too many steps.'),
               dict(title='Optimisation', text='Take the left half (including the middle digit for odd lengths). Mirror it, and mirror it after adding or subtracting 1. Also add the two digit-boundary codes 99…9 (one digit shorter) and 10…01 (one digit longer). Drop the original code and pick the closest, smaller on ties.')],
        reasoning=[dict(title='Explain it simply', text='"Find the nearest number that reads the same both ways, but not the number itself, and prefer the smaller one on a tie."'),
                   dict(title='First idea', text='Walk outwards from the code one step at a time and test each number for being a palindrome.'),
                   dict(title='Why brute force is slow', text='The number of steps equals the distance to the answer, which can be about the square root of the code. For 18-digit codes that is up to a billion checks.'),
                   dict(title='Spot the pattern', text='When the answer must be "the nearest value with some structure" and the structure is fixed by a small part of the input (here, the left half), generate the few candidates that structure allows instead of searching. Keeping the left half as close as possible keeps the high-value digits unchanged.'),
                   dict(title='Say the optimisation out loud', text='"The left half decides everything, and the most significant digits matter most, so the answer\'s left half is the current one, one more, or one less. Mirroring those gives three candidates. The only time the length changes is around 99…9 and 10…01, so I add those two. Five candidates, remove the original, pick the closest, smaller on ties."'),
                   dict(title='Complexity', text='Time O(d) with d decimal digits: a constant number of candidates, each built and compared in O(d). Space O(d) for the strings.')],
        whyFast='Any palindrome with the same digit count is fixed by its left half, and changing that half by more than 1 moves the result further away than changing it by 1. So prefix − 1, prefix and prefix + 1 cover every same-length winner. The only other possibilities have a different number of digits, and the closest of those are always 99…9 just below and 10…01 just above, which is why the two boundary candidates are needed (1000 → 999, 99 → 101).',
        brute=MIRROR_BRUTE, optimal=MIRROR_OPTIMAL, bruteComplexity='O(√code · d) time in the worst case, O(d) space',
        tests=mirror_cases),
]

pack = dict(title='Patterns Behind the Problem',
            description='Two original stories, two classic techniques. Start from the obvious solution, then find the pattern that makes it fast.',
            challenges=challenges)
Path('src/data/challenges.json').write_text(json.dumps(pack, ensure_ascii=False, indent=2))
print(f'PASS: challenge pack verified against brute-force oracles ({len(echo_cases)} + {len(mirror_cases)} tests, maximum-length echo inputs in {echo_seconds:.2f}s).')
