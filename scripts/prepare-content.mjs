import {copyFile} from 'node:fs/promises';
import {resolve} from 'node:path';
const root=resolve(import.meta.dirname,'..');
await copyFile(resolve(root,'src/data/patterns.json'),resolve(root,'public/patterns.json'));
await copyFile(resolve(root,'practice_fixtures.py'),resolve(root,'public/practice_fixtures.py'));
