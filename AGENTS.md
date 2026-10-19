# Pattern Atlas

This repository is the finished app. Edit it in place. Do not rebuild it, re-scaffold it, or replace the stack.

Lovable reads this file on every message. `LOVABLE_PROMPT.md` is the product specification for content and teaching behaviour. `.lovable-agent/context.md` lists project facts.

## Favicon

Keep the existing icon.

- File: `public/favicon.svg`
- Markup in `index.html`: `<link rel="icon" type="image/svg+xml" href="/favicon.svg" />`
- Artwork: 64×64 lilac rounded square (`#7561cf`, corner radius 18) with a white eight-spoke mark

Do not replace, redraw, optimise, or convert that file. Do not add `favicon.ico`, `apple-touch-icon`, a generated site icon, an emoji icon, or an Open Graph image unless explicitly asked. Do not change the favicon link or the `theme-color` (`#f6f5f0`).

## Stack

- React 19 and Vite 8, JavaScript (`.jsx` / `.js`), not TypeScript.
- Styling is `src/styles.css` with the CSS variables already defined. Do not introduce Tailwind, CSS modules, shadcn/ui, or a component library.
- Hash routes in `src/lib/hooks.js`. Do not add React Router, TanStack Router, or TanStack Start.
- No authentication, backend, database, Supabase, Lovable Cloud, API keys, or server functions.
- The browser loads `/patterns.json`. `npm run dev` and `npm run build` copy `src/data/patterns.json` there via `scripts/prepare-content.mjs`.

## Do not add

Live code editors, Python or SQL execution, a Run button, mock assessments, mistake logs, accounts, or analytics. Reference code is copied into the learner’s own IDE.

## Content

Preserve the supplied data. Do not shorten it, substitute placeholders, or invent traces.

- `src/data/patterns.json`: 21 methods and 107 coding examples
- `src/data/python-drills.json`: 16 Python refresher examples
- `src/data/sql-lessons.json`: 25 SQL examples
- `src/data/study-plan.json`: study route and pitfalls
- `public/traces/`: 232 recorded input-case traces
- `src/lib/engine.js`: local problem mapper and recognition questions

Python files at the repo root regenerate and verify that content. They are not part of the website runtime. Change learner-facing content in the generators, then regenerate, rather than hand-editing JSON or traces.

## Routes

Default hash is `#assessment`.

| Hash | Screen |
| --- | --- |
| `#assessment` | Tonight’s plan |
| `#python` / `#python/:index` | Python refresh |
| `#problems` | Coding problem bank |
| `#library` | Pattern library |
| `#pattern/:id/:index` | Pattern detail |
| `#sql` / `#sql/:index` | SQL examples |
| `#finder` | Problem mapper |
| `#lab` | Visual playground |
| `#practice` | Recognition practice |
| `#saved` | Saved examples |
| `#resources` | Guides and resources |

## Persistence

- `localStorage` key `pattern-atlas-v1`: learned methods, saved examples, quiz best
- `localStorage` key `pattern-atlas-journey-v1`: study blocks and readiness checks
- Keep both keys. Tolerate missing, private, or corrupt storage. Progress is manual and stays on this browser.

## Visual system

Warm off-white workspace `#f6f5f0`, cards `#fffefa`, navy text `#25293a`, lilac `#7561cf` / `#eeebfa`, sage panels, thin `#e6e5df` borders, 10–14px radii. Manrope headings, DM Sans body, IBM Plex Mono code, with system fallbacks. Charcoal code panels. Desktop: fixed sidebar and a slim header. Mobile: compact header, horizontal nav, stacked panels, no page-level horizontal overflow. Tables and code scroll inside their own panels.

## Checks

`npm test` checks content, the mapper, and the study plan. `npm run test:examples` needs Python 3. After a content change, run `node scripts/prepare-content.mjs` before expecting the dev server to serve new data.

## Extra problems

`challenge_content.py` generates `src/data/challenges.json` (verified against brute-force oracles). These problems appear as normal rows in the Coding problems bank and open at `#challenge/:id`; keep them inside the bank, not a separate section. Expected values are stored as Python-literal text because JS loses precision on large integers.
