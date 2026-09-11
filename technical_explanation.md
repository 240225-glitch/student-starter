# ACIS Club Compass — Final Technical Explanation

**Student:** 240225-glitch
**Assessment:** Week 4 Lesson 4 — Final Summative (80%)
**Project:** ACIS Club Matcher
**GitHub (public):** https://github.com/240225-glitch/student-starter

---

## 1. Final Product Summary

The ACIS Club Compass is a two-language web app that recommends the top 3 clubs for an ACIS student based on a short profile. It works as a single pipeline:

```
HTML form  →  app.js builds a typed profile object
           →  fetch POST /api/match (JSON)
           →  matcher.py scores 12 clubs
           →  JSON response (3 matches + reasons)
           →  app.js renders 3 result cards
```

**Why this works:** HTML structures the form, CSS makes it usable and accessible, JavaScript handles the browser side (input collection + output rendering), and Python executes the matching algorithm server-side. Each language does the job it is best at.

---

## 2. Live Demonstration — One Fictional Profile, Input to Results

**Demo profile — "Mina":**

| Field | Value |
|-------|-------|
| Name | Mina |
| Grade | 10 |
| Grade group | High School (auto-set when grade > 8) |
| House | Aqua |
| Best club day | Wednesday |
| I like to… | build and solve |
| Interests | technology, games, problem-solving |

**Step 1 — JavaScript builds the profile object** (`app.js`):
```javascript
const profile = {
  name: String(data.get("name")).trim(),      // "Mina"
  grade: Number(data.get("grade")),           // 10
  grade_group: String(data.get("gradeGroup")),// "High School"
  house: String(data.get("house")),           // "Aqua"
  day: String(data.get("day")),               // "Wednesday"
  style: String(data.get("style")),           // "build"
  interests: ["technology", "games", "problem-solving"]
};
```

**Step 2 — JavaScript sends it to Python** (`app.js`):
```javascript
const response = await fetch("/api/match", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(profile)
});
```

**Step 3 — Python scores every club** (`matcher.py`), e.g. for Code Creators:
```python
matched = ["technology", "games", "problem-solving"]  # all 3 in club list
score = 3 * 5                      # 15  (shared interests)
if "build" in club["styles"]:      # +3  (style match)
    score += 3
if "Wednesday" in club["days"]:    # +2  (day match)
    score += 2
# grade_group "High School" is in club["groups"]: +2
# Total = 22
```

**Step 4 — Python returns JSON:**
```json
{
  "profile": { "name": "Mina" },
  "checked_clubs": 12,
  "matches": [
    { "name": "Code Creators", "score": 22,
      "reasons": ["shared interests: technology, games, problem-solving",
                  "fits how you like to build",
                  "meets on your preferred day"] },
    { "name": "Robotics Lab", "score": 15, ... },
    { "name": "Eco Action Team", "score": 7, ... }
  ]
}
```

**Step 5 — JavaScript renders 3 result cards** (`app.js`, `buildCard` using `createElement` + `textContent`): each card shows the club name, score, description, and reasons.

**Verified live:** the above exact profile returns HTTP 200, 12 clubs checked, 3 matches (Code Creators 22, Robotics Lab 15, Eco Action Team 7).

---

## 3. Key Code Decisions

### 3.1 The scoring formula (algorithm core)
```
score = matched_interests × 5  +  style_match(3)  +  day_match(2)  +  grade_group_match(2)
```
- **Interests × 5** — interests are the strongest signal, so they dominate the score
- **Style +3** — how the student likes to learn matters, but secondary
- **Day +2** — scheduling fit helps but is weaker
- **Grade group +2** — age grouping is a tie-breaker-level signal

**Why points instead of boolean?** Points let multiple factors combine into a rankable score, so a student with 2 shared interests + style + day clearly beats one with 1 shared interest. This makes the algorithm explainable (each reason maps to a scored rule).

### 3.2 Why two languages?
- **JavaScript (browser):** owns the UI — reading the form, validating input, making the network request, and rendering results. No page reload; instant feedback.
- **Python (server):** owns the data + algorithm — `load_clubs()` reads the dataset, `score_club()` implements one rule, `top_matches()` sorts and selects. Keeping the algorithm server-side means the same scoring can be reused by other clients later, and the school's data stays consistent.

### 3.3 Modularity — one job per function
- **Python:** `load_clubs()` / `score_club()` / `top_matches()` — each does exactly one thing, so the scoring rule can be tested in isolation.
- **JavaScript:** `buildCard()` / `showResults()` — rendering is separated from data flow.

### 3.4 Safe rendering — `textContent`, never `innerHTML`
All user-controlled text (names, club descriptions, reasons) is rendered with `createElement()` + `.textContent`. This is the responsible-input decision: a name like `<script>alert(1)</script>` is displayed as plain text, never executed. Verified in testing.

### 3.5 Input handling — validation and types
- Fewer than 2 interests → blocked client-side with "Choose at least two interests."
- `String(...).trim()` normalizes whitespace; `Number(...)` types the grade.
- Grade group auto-updates from grade (7-8 → Middle School, 9-12 → High School), preventing contradictory input.
- No sensitive data (passwords, addresses) is ever collected or stored.

---

## 4. One Important Fix — before / after

**The most important fix: error handling when Python is unreachable.**

- **Symptom found in testing:** with the server off, clicking "Show my top 3 matches" did nothing — the fetch promise rejected and the page silently failed. A student got zero feedback.
- **Root cause:** `fetch()` had no `try/catch` and no `response.ok` check. If the network call failed or returned a 500, the code tried to parse and render error data.
- **Fix applied** (`app.js`):
```javascript
try {
  const response = await fetch("/api/match", { ... });
  if (!response.ok) {
    throw new Error(`Server error (${response.status})`);
  }
  const result = await response.json();
  showResults(result);
} catch (error) {
  message.textContent = "Sorry, the matcher is not reachable. Start it with: python matcher.py";
}
```
- **After:** the user sees a clear, actionable error message instead of a silent failure. This fix directly serves the "valid and invalid input both receive a clear response" requirement (Lesson 5) and the "clear error" accessibility goal.

**A second important fix (accessibility):** visible keyboard focus. Tabbing through the form with no `:focus` styling left keyboard users blind to their position. Added `:focus-visible { outline: 3px solid #2563eb; outline-offset: 2px; }` plus `<fieldset><legend>` for the interest group and focus move to results after submit.

---

## 5. Accessibility & Inclusive Design

| Check | Status |
|-------|--------|
| Every input has an associated `<label>` | PASS |
| Interest checkboxes grouped with `<fieldset>` + `<legend>` | PASS |
| Visible `:focus-visible` outline for keyboard navigation | PASS |
| Focus moves to results after submit (screen readers announce) | PASS |
| Contrast: `#172033` text on `#f6f7fb` background (> 7:1, WCAG AAA) | PASS |
| Responsive layout, usable at 375px width | PASS |
| Readable at 200% zoom | PASS |
| No `innerHTML` with user-controlled data (XSS-safe) | PASS |
| Multilingual-friendly: simple English labels, code comments in plain language | PASS |

---

## 6. Attribution & Documentation

- **Project structure:** ACIS curriculum starter package (Google Drive on slide 2 of the teacher slides).
- **All code:** written during lessons 1-16 by the student; no external libraries or frameworks used.
- **Python server:** built on the Python standard library `http.server` (no dependencies required).
- **Documentation included:** README.md, portfolio.md, test_report.md, technical_explanation.md.
- **Source control:** full commit history on GitHub main branch with descriptive messages.

---

## 7. CSTA Standards — Final Evidence

| Standard | Demonstrated by |
|----------|-----------------|
| **HS-ALG-PS-01** (data structures) | clubs.json uses consistent typed records; scoring uses list filtering + sorting |
| **HS-ALG-IM-09** (human-centered) | User-need brief, form labels/fieldsets, 10 algorithm tests, peer-feedback revisions |
| **HS-PRO-PD-12** (modular code) | load_clubs / score_club / top_matches; buildCard / showResults |
| **HS-PRO-VD-16** (structured data) | Typed profile object; consistent field names/types across form, app.js, and clubs.json |
| **HS-PRO-TR-20** (refine with evidence) | 10 algorithm tests; 5 bugs diagnosed and fixed with before/after evidence; feedback log |
| **HS-PRO-TR-19** (evaluate alignment) | Requirement table (10 items) all verified PASS; format checkouts per lesson |

---

## 8. Self-Assessment Against Rubric

| Criterion (points) | Evidence | Self score |
|--------------------|----------|-----------|
| **Final product quality/utility (45)** | Runs fully via `python matcher.py` → localhost:8000; form → match → 3 cards; error handling; 12 clubs; responsive | 42/45 |
| **CSTA knowledge/skills (20)** | Modular code, structured data, algorithm with reasons, refine-with-evidence | 19/20 |
| **Responsible/inclusive/attribution (15)** | TextContent XSS-safe, no sensitive data, accessibility audit, credits documented | 15/15 |
| **Communication + technical explanation/reflection (20)** | This document + README + portfolio; live demo trace; one key fix explained | 19/20 |

**Reflection — strongest design decision:** using server-side Python for scoring while the browser owns the form and rendering. It made the algorithm testable in isolation (pure functions, no UI needed) and let both languages stay small and readable — exactly the "one algorithm, two languages" goal, and the reason debugging was fast: I could POST a JSON profile and inspect exact scores without touching the form.

---

*Submitted for the final Club Compass summative assessment. Live demo uses the Mina profile above; results match this document exactly.*