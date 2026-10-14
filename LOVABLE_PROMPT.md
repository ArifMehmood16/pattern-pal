# Pattern Atlas — product specification

The app in this repository is already built. Edit that app. Do not recreate it, and do not replace `public/favicon.svg` or its link in `index.html`. Agent instructions are in `AGENTS.md`.

The product is a local-first React + Vite learning website called Pattern Atlas. It should help me understand algorithm patterns and become capable of solving unseen coding problems in Python. Preserve the supplied content and traces. This is a reference/explanation website for practising in my own IDE.

## Critical scope

Do not build live coding editors, Python/SQL execution, mock assessments, or mistake logs. I need complete reference code, detailed explanations, and a visual playground for EVERY example. SQL should be worked examples and queries, not a live database console.

Use these source assets:

- src/data/patterns.json: 21 methods and 107 coding examples.
- src/data/python-drills.json: 16 Python refresher examples.
- src/data/sql-lessons.json: 25 SQL examples.
- src/data/study-plan.json: focused study plan and pitfalls.
- public/traces/: 232 recorded input-case traces across all coding/refresher examples.
- src/lib/engine.js: explainable mapper and recognition questions.

The data is complete. Do not substitute placeholder text, shorter example counts or fabricated execution traces.

## Visual direction

Use a warm off-white workspace (#f6f5f0), near-white cards (#fffefa), navy text (#25293a), lilac accents (#7561cf / #eeebfa), pale sage panels, thin neutral borders, subtle shadows, rounded 10–14px cards and generous whitespace. Use Manrope headings, DM Sans body and IBM Plex Mono code, with fallbacks. Code panels have a charcoal background, coloured tokens and line numbers. Keep educational text readable and avoid tiny decorative typography.

Desktop: a fixed sidebar, slim breadcrumb header and spacious main area. Mobile: compact brand header, scrollable navigation and stacked teaching panels. Tables/code may scroll inside their own panels; the page must not overflow horizontally. Add semantic headings, labelled controls, visible focus states and keyboard-accessible example tabs.

## Navigation and screens

1. Tonight’s plan: the 400-minute core route, optional 45-minute SQL block, study checkboxes and future-readiness journey.
2. Python refresh: 16 complete worked examples, language definitions/pitfalls, inputs/outputs, code, explanations and playgrounds.
3. Coding problem bank: search all 107 examples, filter Tonight/Next/Stretch/All and difficulty, open the exact example.
4. Pattern library: 21 searchable families with definitions and links.
5. SQL examples: 25 worked queries, schemas and tables.
6. Problem mapper: deterministic suggestions with matching evidence and assumptions; no confidence percentages or external AI call.
7. Visual playground: choose ANY of the 123 coding/refresher examples and ANY supplied input case.
8. Recognition practice: 12 mixed questions with explanations; preserve allowed alternative approaches.
9. Saved examples and guides/resources.

Use hash routes or correctly configured client routes. The app must work without authentication, a backend, API keys or Supabase.

## Pattern teaching

The families include hashing, two pointers, sliding windows, prefix/difference arrays, sorting/sweeping, intervals, binary search, fast/slow pointers, linked-list rewiring, stacks, deques, heaps, DFS/tree recursion, BFS, backtracking, greedy, DP, graph algorithms, tries/string matching, bits/mathematics, and matrices/simulation.

For each family show:

- A precise definition, in plain language.
- When/why it applies and the clue to recognise it.
- A concrete small example with explained changes.
- The invariant or recurrence.
- Failure cases and assumptions.
- Every supplied worked example (5 per family, 7 for DP).
- Related methods with working links.

Patterns are composable. A family’s example may demonstrate a more efficient alternative, such as quickselect instead of a heap or combinatorics instead of obstacle-free grid DP. Explain that relationship explicitly rather than presenting every example as the same algorithm.

## Worked solution layout

For each example:

1. State the problem and input contract.
2. Show all supplied input/output examples. Outputs must be the solution’s real return values, not internal assertions or len()/sorted() test wrappers.
3. Show the WHOLE solution in one code block, with a copy action for my IDE.
4. Explain why it works and then explain each code block using line references.
5. Explain HOW time complexity is calculated: number of passes, loop bounds, amortised pushes/pops, shrinking search ranges, branching/output size or DP states.
6. Explain HOW space complexity is calculated: retained maps/sets/queues, recursion depth, copied slices, DP rows, input mutation and output storage.
7. Explain efficiency tradeoffs. Do not claim one implementation dominates every time/space/immutability constraint.
8. Include a visual playground with actual recorded execution for this exact code.
9. Finish with a transfer exercise: predict states, rebuild in the IDE, alter one constraint and decide whether the method still works.

Efficient source examples include O(n log n) LIS, one-row edit distance, O(min(n,m)) LCS storage, constant-space matrix zeroing and Game of Life, expected-linear quickselect with its worst-case warning, linear bucket frequency selection and a combinatorial Unique Paths count with big-integer cost notes. Preserve these implementations and their honest assumptions.

## Visual playground requirements

Keep the complete Python code and all variables INSIDE the playground workspace while the learner interacts. Use three reserved areas on desktop: a code inspector, a clear data visualisation stage, and a variable inspector. The panels may float visually with subtle shadows, but their docks must never cover the stage. Support dragging headers to swap docks, equivalent keyboard/arrow controls, and a Reset panels action. On compact layouts keep the inspectors below/beside the stage with independent scrolling rather than overlapping overlays.

Include a viewport-filling Focus playground mode with a labelled modal, trapped keyboard focus, Escape/Exit focus and restored focus afterwards. Highlight the actual current source line, wrap long lines, retain ALL code lines, and provide Copy code plus optional Follow line (scroll only the code pane). Render all local before/after values in the variable inspector and let clicking any variable choose the central visualisation. Show before/after data side by side and highlight changed cells. Controls include Previous/Next, a step slider, Play/Pause and speed selection. Manual stepping pauses playback; playback stops at the final event and can restart. Preserve progress when moving panels and entering/exiting focus.

The traces are captured BEFORE each executed source line. The next event in the SAME call supplies the after state. Calls have unique IDs and depths; do not compare unrelated recursive frames. Return events show the returned value. Built-in operations are atomic at source-line level.

For every example and every supplied input case provide:

- Previous/next controls and a seek slider.
- The current function, call ID, recursion depth and source line.
- A highlighted line in the whole code.
- A variable/object table with all before and after values.
- Indexed arrays, readable dictionaries/sets/node structures, and COMPLETE matrices with row/column indices.
- Highlight changed rows/cells. Show both sides of tuple assignments together.
- Full chronological event history, with no sampling or omitted source-line events.
- Final return value and the traced input expression.

Conceptual DP matrices must be labelled as explanatory matrices. Do not falsely present them as allocated by code that uses only one/two rows or a combinatorial count.

The global selector must contain all 107 coding examples AND all 16 Python examples. Detail pages embed the same playground. Empty/singleton/negative/duplicate input cases are selectable when they are legal under the example contract.

## SQL teaching

Display the exact problem contract, every sample input row, expected result table, whole query, logical stage explanations and supplied intermediate tables. Include filters, joins, anti-joins, self-joins, GROUP BY/HAVING, NULLs, scalar subqueries, CTEs, ranking/ties, LAG, conditional aggregation, running/rolling windows, dates, retention, UNION and streaks.

Provide SQLite and PostgreSQL reference versions, especially where date syntax differs. Include the sample schema/insert statements for my IDE. There is no Run button or query editor. State that SQLite outputs were verified; PostgreSQL references were not executed by this app.

Explain logical work and query-planning considerations. Avoid a universal complexity claim from SQL text alone: cardinalities, indexes, statistics, join algorithms and sort memory matter. Cover COUNT(*) versus COUNT(column), WHERE versus HAVING, LEFT JOIN predicates in ON versus WHERE, join fanout, NOT IN with NULL, ROW_NUMBER/RANK/DENSE_RANK, explicit window frames, integer division, safe parameters, indexes, EXPLAIN and transaction/constraint basics.

## Study journey and unseen questions

The context is an independent preparation period for an ActAI/BJAK coding assessment. User-provided facts: two coding tests, one question each; Python 3 available; actual questions/duration/difficulty unknown. The basic demo establishes only editor workflow. SQL is useful for the role but not confirmed in this assessment. Do not fabricate company questions, durations or predictions.

Tonight’s focused sequence: 40m fundamentals, 45m strings/lists, 60m dictionaries/sets, 45m sorting/containers, 90m patterns, 90m independent IDE practice, 30m review/explanation. Add breaks and sleep; optional SQL 45m. Link each block to relevant lessons.

Future progression: understand → trace → rebuild from blank in the IDE → vary a constraint → mix untagged problems → justify correctness/complexity → revisit weak methods. Include self-checks, not an unearned mastery score. Explain that a finite collection does not guarantee every unseen question; advanced structures, specialised DP and graph topics are later extensions.

## Persistence and implementation

Use native React components/state, not an iframe or imperative HTML wrapper. Keep data and UI separate. Preserve localStorage method/bookmark key pattern-atlas-v1 and journey key pattern-atlas-journey-v1. Store manual progress only. Handle unavailable/corrupt storage gracefully. Do not send problem descriptions externally. No personal recruiter/compensation data or credentials belong in the app.

## Acceptance checks

- All 21 definitions, 107 coding examples, 16 Python refreshers and 25 SQL examples are present.
- Every coding/refresher example has code, explanation, input/output, derived time/space and a working playground.
- All 232 traced input cases are accessible and synchronised with the displayed source.
- Complete code, variables and data stay together in every playground; panel movement never obscures the visualisation. Test focus entry/exit, input switching, playback, wrapping and desktop/mobile layouts.
- Rotate Image shows both swapped matrix cells changing in one after state.
- Edit Distance preserves old above/diagonal values while overwriting its DP row.
- Quickselect clearly states input mutation, expected O(n) and worst O(n²).
- Search/filter/deep links/tabs/copy/bookmarks/recognition questions work.
- No live editors, execution engines, mock screens or mistake logs.
- No unintended page-wide horizontal overflow on mobile.
- npm install, npm run dev and npm run build work; include a current README.
