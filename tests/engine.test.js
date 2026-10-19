import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import engine from '../src/lib/engine.js';

const patterns = JSON.parse(readFileSync(new URL('../src/data/patterns.json', import.meta.url), 'utf8'));
const match = (text, signals = []) => engine.match(text, signals, patterns);

test('all 21 methods have complete examples and valid related methods', () => {
  assert.equal(patterns.length, 21);
  assert.equal(new Set(patterns.map(p => p.id)).size, 21);
  assert.equal(patterns.reduce((n,p)=>n+p.examples.length,0),109);
  for (const p of patterns) {
    assert(p.examples.length>=5);
    for (const example of p.examples) {
      for (const field of ['title', 'prompt', 'insight', 'code', 'time', 'space', 'sampleInput', 'sampleOutput']) assert(example[field]);
    }
    for (const id of p.related) assert(patterns.some(p => p.id === id));
  }
});

test('maps unique substrings to sliding windows and character tracking', () => {
  const result = match('Find the longest substring without repeating characters');
  assert.equal(result.results[0].pattern.id, 'window');
  assert(result.results.some(r => r.pattern.id === 'hash'));
});

test('exact subarray sums with negatives favor prefixes and hashing over windows', () => {
  const result = match('Count subarrays whose sum equals k. Values may include negative numbers.');
  assert.equal(result.results[0].pattern.id, 'prefix');
  assert.equal(result.results[1].pattern.id, 'hash');
  assert(!result.results.some(r => r.pattern.id === 'window'));
  assert(result.cautions.some(c => c.includes('Negative values')));
});

test('unequal weighted paths and unweighted paths produce different suggestions', () => {
  const weighted = match('Find shortest paths in a weighted graph with nonnegative costs');
  assert.equal(weighted.results[0].pattern.id, 'graph');
  assert(weighted.results.some(r => r.pattern.id === 'heap'));
  assert(!weighted.cautions.some(c => c.startsWith('Negative edge')));
  assert.equal(match('Find shortest path in an unweighted graph').results[0].pattern.id, 'bfs');
  const negative = match('Find shortest path in a weighted graph with negative edge weights');
  assert(negative.cautions.some(c => c.includes('do not use Dijkstra')));
});

test('supports combinations, selected properties and no-match descriptions', () => {
  assert.equal(match('Return unique triplets in an unsorted array with sum zero').results[0].pattern.id, 'pointers');
  assert.equal(match('Courses have prerequisites; can all be completed?').results[0].pattern.id, 'graph');
  assert.equal(match('', ['topk']).results[0].pattern.id, 'heap');
  assert.equal(match('hello world').results.length, 0);
});

test('walkthrough results and invariants agree with independent brute force', () => {
  const brute = s => {
    let best = 0;
    for (let i = 0; i < s.length; i++) for (let j = i + 1; j <= s.length; j++) {
      const piece = s.slice(i, j);
      if (new Set(piece).size === piece.length) best = Math.max(best, piece.length);
    }
    return best;
  };
  const cases = ['', 'abcabcbb', 'pwwkew', 'bbbbb', 'dvdf'];
  function enumerate(prefix, depth) {
    cases.push(prefix);
    if (depth) for (const char of 'abc') enumerate(prefix + char, depth - 1);
  }
  enumerate('', 5);
  for (const input of cases) {
    const steps = engine.trace(input);
    assert.equal(steps.at(-1).best, brute(input));
    for (const step of steps.filter(s => s.line === 10)) assert(Object.values(step.counts).every(n => n <= 1));
  }
});
