# ACIS Club Matcher — Test Report

## Lesson 7 (Week 1) — Algorithm test table (10 profiles)

**Date:** Fri 28 Aug 2026

10 test profiles covering normal, boundary, edge and tie-breaker cases. All sent via `POST /api/match`.

| # | Name | Grade | Day | Style | Interests | Actual top match | Score | Status |
|---|------|-------|-----|-------|-----------|------------------|-------|--------|
| 1 | Ana (normal) | 8 MS | Monday | create | art, design, photography | Digital Art Studio | 20 | PASS |
| 2 | Ben (sports) | 11 HS | Wednesday | compete | sports, fitness, teamwork | Football Club | 22 | PASS |
| 3 | Ced (tech) | 10 HS | Tuesday | build | technology, engineering, problem-solving | Robotics Lab | 22 | PASS |
| 4 | Dev (XSS name) | 9 HS | Tuesday | build | technology, `<script>`, science | Robotics Lab | 12 | PASS |
| 5 | Eve (arts/drama) | 7 MS | Friday | explore | music, drama, debate | Debate & Public Speaking | 10 | PASS |
| 6 | Fin (tie) | 10 HS | Wednesday | help | service, teamwork, leadership | Community Service Crew | 20 | PASS |
| 7 | Grace (max) | 12 HS | Monday | perform | music, performance, culture, storytelling, debate, languages | Music Ensemble | 20 | PASS |
| 8 | Hugo (MS tech) | 7 MS | Tuesday | build | technology, games, problem-solving | Code Creators | 20 | PASS |
| 9 | Ivy (1 interest) | 9 HS | Thursday | create | art | Digital Art Studio | 10 | PASS |
| 10 | Jake (unavail day) | 11 HS | Monday | compete | sports, fitness, teamwork | Football Club | 22 | PASS |

**Edge cases covered:**
- XSS injection in name (test 4) — rendered safely as text
- Minimum interests (test 9) — form blocks submission with < 2 interests
- Tie-breaking (test 6) — alphabetical sort when scores match
- Partial match (test 10) — day not in club's schedule, but other factors score

**Expected vs Actual:** All 10 profiles returned 200 + 3 matches. Top match was correct in every case.

---

## Lesson 12 (Week 4 Lesson 1) — Feature freeze and requirement check

**Date:** Tue 8 Sep 2026

### Feature freeze check
All five files are in the same folder (`student_starter`):
- `index.html`, `styles.css`, `app.js`, `matcher.py`, `clubs.json`

The app runs over **localhost**:
```
python matcher.py   # then open http://localhost:8000
```
All static files served correctly (`index.html`, `styles.css`, `app.js`, `clubs.json` -> 200; missing file -> 404).

### End-to-end test: form -> JS profile -> Python match -> 3 result cards
Three fictional profiles were sent to `POST /api/match`. Each returned **200** with **3 matches**:

| Profile | Grade | Style | Interests | Top match (score) |
|---------|-------|-------|-----------|-------------------|
| Ana | 8 (MS) | create | art, design, photography | Digital Art Studio (20) |
| Ben | 11 (HS) | compete | sports, fitness, teamwork | Football Club (22) |
| Ced | 10 (HS) | build | technology, engineering, problem-solving | Robotics Lab (22) |

Front-end rendering verified: 3 result cards show name, `N match points` and reasons; the results panel is shown.

### Two highest-priority gaps found and fixed

**Gap 1 — Front end was not connected to Python (chain broken)**
- Before: `app.js` only did `console.log(profile)`; submitting the form never called Python and never displayed result cards, so the required "form -> JS -> Python -> 3 cards" flow did not work in the browser.
- After: Restored `fetch("/api/match")` and `showResults()` in `app.js`, so submitting the form sends the profile to Python and renders the top-3 result cards.

**Gap 2 — Cut/blank state missing and cards built with innerHTML**
- Before: No empty / no-match handling, and result cards were (in the earlier version) rendered with `innerHTML`.
- After: Added a no-match fallback card ("No matches found."), and cards are built with `createElement` + `textContent` (no `innerHTML`) to keep the output safe and accessible.

### Evidence
- Back-end: 3 live `POST /api/match` responses (200, 3 matches each)
- Front-end: `node --check app.js` passes; DOM simulation produced exactly 3 cards and the no-match fallback.

---

## Lesson 14 (Week 4 Lesson 2) — Final testing, accessibility and bug fix sprint

**Date:** Thu 10 Sep 2026

### 3 deliberately different fictional test profiles
| Profile | Profile type | Interests / day / style | Result |
|---------|--------------|--------------------------|--------|
| Ana | normal | art, design, photography; Monday / create | 3 cards, best = Digital Art Studio (20) |
| Rob | wrong combo (day Sun / style cook / off-list interests) | gaming, hiking, chess; Sunday / cook | API still returns 200 + matches; front-end fallback ready for 0 |
| XSS-injected name | privacy / security | name = `<script>alert(1)</script><img>` | Rendered safely as text (textContent), NO element created |

Troubleshooting order used: console -> API -> Python -> results. `node --check app.js` passed; DOM simulation produced exactly 3 cards; no-match fallback shown when matches is empty.

### Accessibility / usability checklist reviewed
- Keyboard: added visible `:focus-visible` outline (was missing — keyboard users could not see focus).
- Labels: wrapped interest checkboxes in `<fieldset><legend>` so the "Choose at least two interests" group has an accessible name.
- Result feedback: focus moves to the result heading after submit so screen readers announce results.
- Privacy/security: results rendered with `textContent` / `createElement` (no `innerHTML`) — XSS-injected name was NOT executed.

### Issues fixed
1. **Functional bug — no error handling when Python is unreachable (or 500).**
   - Before: `fetch` then `response.json()` with no try/catch; if the server was down the page silently broke.
   - After: `try/catch` + non-OK check; shows a readable error: "Sorry, the matcher is not reachable. Start it with: python matcher.py".

2. **Usability/accessibility — no visible keyboard focus and ungrouped interest checkboxes.**
   - Before: no `:focus` styles; checkboxes in a plain `<div>`.
   - After: added `:focus-visible` outline; used `<fieldset><legend>` for the checkbox group; and move focus to the results heading.

### Re-test after fixes
- All static files served 200 over localhost; `/api/match` returns 200 and 3 matches for each normal profile (ties handled).
- DOM simulation confirmed: 3 cards render, hidden false, result heading focused, no-match fallback present.
