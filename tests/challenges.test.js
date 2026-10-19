import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const pack = JSON.parse(readFileSync(new URL('../src/data/challenges.json', import.meta.url), 'utf8'));
const byId = id => pack.challenges.find(c => c.id === id);
const expected = (c, call) => c.tests.find(t => t.call === call)?.expected;

test('Mirror Vault: 808 returns 818, not 797', () => {
  assert.equal(expected(byId('mirror-vault'), 'solution(808)'), 818);
});
test('Mirror Vault: 121 ties between 111 and 131 and returns the smaller', () => {
  assert.equal(expected(byId('mirror-vault'), 'solution(121)'), 111);
});
test('Echo Protocol: "aaaaa" returns 2 because signatures may not overlap', () => {
  assert.equal(expected(byId('echo-protocol'), 'solution("aaaaa")'), 2);
});
test('each challenge has three hints, both solutions and hidden tests', () => {
  assert.equal(pack.challenges.length, 2);
  for (const c of pack.challenges) {
    assert.equal(c.hints.length, 3);
    assert(c.brute && c.optimal);
    assert(c.tests.some(t => !t.visible));
  }
});
