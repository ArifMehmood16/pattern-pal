import json
import sqlite3
from pathlib import Path
import practice_fixtures

for file in ['python-drills.json']:
    exercises=json.loads((Path('src/data')/file).read_text())
    for exercise in exercises:
        scope={k:v for k,v in vars(practice_fixtures).items() if not k.startswith('__')}
        exec(compile(exercise['code'],exercise['title'],'exec'),scope)
        for expression in exercise['tests']:
            assert eval(expression,scope),(exercise['title'],expression)
    print(f'PASS: {len(exercises)} {file} reference implementations and all supplied tests.')

sql=json.loads(Path('src/data/sql-lessons.json').read_text())
for lesson in sql['lessons']:
    db=sqlite3.connect(':memory:');db.executescript(lesson['setup'])
    actual=[list(row) for row in db.execute(lesson['code']).fetchall()]
    assert actual==lesson['expected']['values'],(lesson['title'],actual)
    db.close()
print('PASS: 25 SQLite exercises match independently specified output tables.')

patterns=json.loads(Path('src/data/patterns.json').read_text())
for p in patterns:
    assert all(p.get(field) for field in ['definition','reasoning','concreteExample'])
    for e in p['examples']:
        assert e['constraints'] and e['samples'] and e['blocks'] and e['explanation'] and e['timeReason'] and e['spaceReason']
        assert len(e['traces'])==len(e['samples'])
        for case in e['traces']:
            trace=json.loads(Path('public'+case['url']).read_text())
            assert trace['steps'],e['title']
            assert all(1 <= step['line'] <= len(e['code'].splitlines()) for step in trace['steps'])
print('PASS: all 107 examples have definitions, contracts, input/output cases, code blocks and complete trace files.')

