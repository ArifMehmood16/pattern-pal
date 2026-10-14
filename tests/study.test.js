import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const read=name=>JSON.parse(readFileSync(new URL(`../src/data/${name}`,import.meta.url),'utf8'));
test('the core study plan totals 400 minutes and labels unknown assessment details',()=>{
  const plan=read('study-plan.json');
  assert.equal(plan.blocks.reduce((n,b)=>n+b.minutes,0),400);
  assert(plan.assessmentFacts.some(x=>x.includes('remain unknown')));
  assert(plan.assessmentFacts.some(x=>x.includes('not confirmed')));
});
test('exercise banks and SQL dialect references are complete',()=>{
  assert.equal(read('python-drills.json').length,16);
  const sql=read('sql-lessons.json');assert.equal(sql.lessons.length,25);
  for(const lesson of sql.lessons){assert(lesson.code&&lesson.postgres&&lesson.expected&&lesson.inputs.length&&lesson.steps.length);}
});
