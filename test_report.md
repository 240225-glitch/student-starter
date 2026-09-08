# ACIS Club Matcher — Lesson 12 (Week 4 Lesson 1) Test Report

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
