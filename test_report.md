# ACIS Club Matcher — Test Report

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

---

## Lesson 12 (Week 4 Lesson 1) Test Report

**Date:** Tue 8 Sep 2026

## Feature freeze check
All five files are in the same folder (`student_starter`):
- `index.html`, `styles.css`, `app.js`, `matcher.py`, `clubs.json`

The app runs over **localhost**:
```
python matcher.py   # then open http://localhost:8000
```
All static files served correctly (`index.html`, `styles.css`, `app.js`, `clubs.json` -> 200; missing file -> 404).

## End-to-end test: form -> JS profile -> Python match -> 3 result cards
Three fictional profiles were sent to `POST /api/match`. Each returned **200** with **3 matches**:

| Profile | Grade | Style | Interests | Top match (score) |
|---------|-------|-------|-----------|-------------------|
| Ana | 8 (MS) | create | art, design, photography | Digital Art Studio (20) |
| Ben | 11 (HS) | compete | sports, fitness, teamwork | Football Club (22) |
| Ced | 10 (HS) | build | technology, engineering, problem-solving | Robotics Lab (22) |

Front-end rendering verified: 3 result cards show name, `N match points` and reasons; the results panel is shown.

## Two highest-priority gaps found and fixed

### Gap 1 — Front end was not connected to Python (chain broken)
- **Before:** `app.js` only did `console.log(profile)`; submitting the form never called Python and never displayed result cards, so the required "form -> JS -> Python -> 3 cards" flow did not work in the browser.
- **After:** Restored `fetch("/api/match")` and `showResults()` in `app.js`, so submitting the form sends the profile to Python and renders the top-3 result cards.

### Gap 2 — Cut/blank state missing and cards built with innerHTML
- **Before:** No empty / no-match handling, and result cards were (in the earlier version) rendered with `innerHTML`.
- **After:** Added a no-match fallback card ("No matches found."), and cards are built with `createElement` + `textContent` (no `innerHTML`) to keep the output safe and accessible.

## Evidence
- Back-end: 3 live `POST /api/match` responses (200, 3 matches each)
- Front-end: `node --check app.js` passes; DOM simulation produced exactly 3 cards and the no-match fallback.
