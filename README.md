# ACIS Club Compass

**How can an accessible algorithm match a student to clubs and explain the result?**

A four-week accessible web app built with HTML, CSS and JavaScript, supported by a Python scoring prototype and test evidence.

## What it does

A student fills in a short form (name, grade, house, preferred day, learning style, and interests). JavaScript sends the profile to a Python server, which scores all 12 clubs and returns the top 3 matches. Each result card explains why the club was recommended.

## How to run

1. Open a terminal in this folder
2. Run:
   ```
   python matcher.py
   ```
3. Open `http://localhost:8000` in Chrome
4. Fill in the form and click "Show my top 3 matches"

**Note:** Do NOT open `index.html` directly with `file://` — the Python server is needed for the `/api/match` endpoint.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Semantic HTML structure with form and results |
| `styles.css` | Responsive layout, accessible focus states, color palette |
| `app.js` | Reads form data, sends to Python, renders result cards |
| `matcher.py` | Python scoring algorithm + HTTP server |
| `clubs.json` | 12 fictional club records with structured data |
| `test_report.md` | Test evidence from Lessons 7, 12 and 14 |
| `portfolio.md` | Full evidence portfolio for the formative assessment |
| `technical_explanation.md` | Final summative technical explanation (code decisions, live demo, key fix) |

## Algorithm

Each club is scored against a student profile:
- **+5** for each shared interest
- **+3** if learning style matches
- **+2** if preferred day matches
- **+2** if grade group matches

The top 3 clubs by score are returned with human-readable reasons.

## Accessibility

- All form inputs have associated `<label>` elements
- Interest checkboxes grouped with `<fieldset><legend>`
- Visible `:focus-visible` outline for keyboard navigation
- Results rendered with `textContent` (no `innerHTML` — XSS safe)
- Focus moves to results after submit for screen reader announcement
- Responsive layout works at 375px width

## CSTA Standards

This project aligns with CSTA HS standards: HS-ALG-PS-01 (data structures), HS-ALG-IM-09 (human-centered design), HS-PRO-PD-12 (modular code), HS-PRO-VD-16 (structured data), HS-PRO-TR-20 (refine with evidence), HS-PRO-TR-19 (evaluate alignment).

## Credits

Built during HS Computer Science, ACIS, August-September 2026.
Project structure from ACIS curriculum starter package.
All code written during lessons 1-16.
