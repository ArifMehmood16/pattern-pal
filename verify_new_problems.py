"""Hidden tests and brute-force oracles for Repeated Signal Signature and Nearest Symmetric Access Code."""
import itertools
import json
import random
import time
from pathlib import Path

patterns = json.loads(Path('src/data/patterns.json').read_text())
examples = {e['title']: e for p in patterns for e in p['examples']}


def load(title):
    scope = {}
    exec(examples[title]['code'], scope)
    return scope['solution']


# ---------- Repeated Signal Signature ----------
signature = load('Repeated Signal Signature')


def signature_brute(signal):
    for length in range(len(signal) // 2, 0, -1):
        if signal[:length] == signal[-length:]:
            return length
    return 0


hidden_signature = [
    ('planet', 0), ('z', 0), ('zz', 1), ('zzz', 1), ('zzzz', 2), ('zzzzzzz', 3),
    ('abcab', 2), ('abcabcab', 2), ('abababab', 4), ('ababa', 1), ('aabaaabaa', 2),
    ('kitekitekite', 4), ('mapletreemaple', 5), ('xyxyxyx', 3), ('abcdefgh', 0),
    ('abacaba', 3), ('aaaabaaaa', 4), ('qwertyqwerty', 6),
]
cases = 0
for signal, expected in hidden_signature:
    assert signature_brute(signal) == expected, signal
    assert signature(signal) == expected, signal
    cases += 1
for length in range(1, 11):
    for letters in itertools.product('ab', repeat=length):
        signal = ''.join(letters)
        assert signature(signal) == signature_brute(signal), signal
random.seed(7)
for _ in range(3000):
    signal = ''.join(random.choice('abc') for _ in range(random.randint(1, 40)))
    assert signature(signal) == signature_brute(signal), signal
# Maximum-length inputs (n = 100,000) must finish quickly.
large = [('a' * 100000, 50000), ('ab' * 50000, 50000), ('abc' * 33333 + 'a', 49999),
         ('a' * 99999 + 'b', 0), ('b' + 'a' * 99998 + 'b', 1)]
for signal, expected in large:
    started = time.perf_counter()
    assert signature(signal) == expected, len(signal)
    assert time.perf_counter() - started < 1.0
    cases += 1
print(f'PASS: Repeated Signal Signature — {cases} hidden cases, exhaustive length ≤ 10 and 3000 random cases match brute force.')

# ---------- Nearest Symmetric Access Code ----------
nearest = load('Nearest Symmetric Access Code')


def is_symmetric(value):
    text = str(value)
    return text == text[::-1]


def nearest_brute(code):
    distance = 1
    while True:
        if code - distance >= 0 and is_symmetric(code - distance):
            return code - distance
        if is_symmetric(code + distance):
            return code + distance
        distance += 1


hidden_nearest = [
    (1, 0), (5, 4), (9, 8), (10, 9), (11, 9), (99, 101), (100, 99), (101, 99), (121, 111),
    (808, 797), (1001, 999), (1234, 1221), (1991, 2002), (2002, 1991), (9009, 8998),
    (12932, 12921), (99999, 100001), (100000, 99999), (40404, 40304), (10 ** 9, 10 ** 9 - 1),
    (123456789012345678, 123456789987654321), (10 ** 18, 10 ** 18 - 1),
    (999999999999999999, 1000000000000000001), (807045053224792883, 807045053350540708),
]
cases = 0
for code, expected in hidden_nearest:
    if code < 10 ** 6:
        assert nearest_brute(code) == expected, code
    assert nearest(code) == expected, code
    cases += 1
for code in range(1, 20001):
    assert nearest(code) == nearest_brute(code), code
for _ in range(500):
    code = random.randint(1, 10 ** 7)
    assert nearest(code) == nearest_brute(code), code
print(f'PASS: Nearest Symmetric Access Code — {cases} hidden cases, every code 1..20000 and 500 random codes match brute force.')
